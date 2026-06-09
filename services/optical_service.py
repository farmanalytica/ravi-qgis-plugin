import ee

from typing import List, Dict, Any

from ..tools.indexes import INDEX_REGISTRY, calc_custom


class OpticalService:
    """
    Service class responsible for interacting with Google Earth Engine to build
    Sentinel-2 time series data, compute vegetation indices, and extract image metadata.
    """

    @staticmethod
    def get_time_series(
        aoi: ee.FeatureCollection,
        date_start: str,
        date_end: str,
        index_name: str,
        apply_scl: bool,
        invalid_scl_values: List[int],
    ) -> List[Dict[str, Any]]:

        collection = OpticalService._build_base_collection(aoi, date_start, date_end)
        collection = OpticalService._keep_one_image_per_date(collection, aoi)

        def process_image(image):
            processed_image = OpticalService._add_vegetation_index(image, index_name)
            if apply_scl:
                processed_image = OpticalService._apply_scl_mask(
                    processed_image, invalid_scl_values
                )

            processed_image = OpticalService._calculate_image_metadata(
                processed_image, image.select("SCL"), aoi, invalid_scl_values
            )
            return processed_image

        processed_collection = collection.map(process_image).sort("system:time_start")

        return OpticalService._extract_data_rows(processed_collection)

    @staticmethod
    def _build_base_collection(
        aoi: ee.FeatureCollection, date_start: str, date_end: str
    ) -> ee.ImageCollection:
        return (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(aoi)
            .filterDate(date_start, date_end)
        )

    @staticmethod
    def _keep_one_image_per_date(
        collection: ee.ImageCollection, aoi: ee.FeatureCollection
    ) -> ee.ImageCollection:
        """Keep a single image per acquisition date (always on).

        Criteria: highest AOI footprint coverage first, cloud cover as the
        tiebreaker. Both come from cheap geometry/metadata (no reduceRegion), so
        the expensive per-image statistics are computed for the kept images
        alone -- unlike the legacy approach, which derived stats before
        deduplicating. Footprint coverage uses image.geometry() (the full MGRS
        tile for Sentinel-2), so single-tile AOIs tie at full coverage and the
        cloud tiebreaker decides.
        """
        geometry = aoi.geometry()
        aoi_area = geometry.area()

        def tag(image):
            coverage = (
                image.geometry()
                .intersection(geometry, ee.ErrorMargin(1))
                .area()
                .divide(aoi_area)
            )
            cloud = ee.Number(image.get("CLOUDY_PIXEL_PERCENTAGE"))
            # Composite descending score: coverage dominates, low cloud breaks
            # ties (coverage in [0,1] scaled by 1000 outweighs cloud in [0,100]).
            score = coverage.multiply(1000).subtract(cloud.divide(100))
            return image.set(
                {
                    "date": ee.Date(image.get("system:time_start")).format(
                        "YYYY-MM-dd"
                    ),
                    "dedup_score": score,
                }
            )

        # distinct() returns a generic Collection; re-cast to ImageCollection so
        # downstream map() yields ee.Image elements (not ee.Feature).
        deduped = collection.map(tag).sort("dedup_score", False).distinct("date")
        return ee.ImageCollection(deduped)

    @staticmethod
    def _build_valid_scl_mask(
        image: ee.Image, invalid_scl_values: List[int]
    ) -> ee.Image:

        scl = image.select("SCL")
        mask = ee.Image(1)
        for value in invalid_scl_values:
            mask = mask.And(scl.neq(value))
        return mask.rename("valid_scl")

    @staticmethod
    def _apply_scl_mask(image: ee.Image, invalid_scl_values: List[int]) -> ee.Image:
        return image.updateMask(
            OpticalService._build_valid_scl_mask(image, invalid_scl_values)
        )

    @staticmethod
    def _add_vegetation_index(
        image: ee.Image, index_name: str, custom_expression: str = None
    ) -> ee.Image:
        key = "CUSTOM" if "custom" in index_name.lower() else index_name.upper()

        if key == "CUSTOM":
            index_band = calc_custom(image, custom_expression)
        elif key in INDEX_REGISTRY:
            index_band = INDEX_REGISTRY[key](image)

        return image.addBands(index_band)

    @staticmethod
    def _calculate_image_metadata(
        image: ee.Image,
        scl_band: ee.Image,
        aoi: ee.FeatureCollection,
        invalid_scl_values: List[int],
    ) -> ee.Image:

        geometry = aoi.geometry()

        # Geometry-based coverage (legacy): cheaper than a pixel count, but uses
        # image.geometry(), which for Sentinel-2 is the full nominal MGRS tile
        # square. AOIs inside a single tile therefore read ~100% even when the
        # swath only partially covers them; it only catches AOIs that extend
        # past a granule footprint (e.g. spanning multiple tiles).
        intersection_area = (
            image.geometry().intersection(geometry, ee.ErrorMargin(1)).area()
        )
        aoi_area = geometry.area()
        coverage_percentage = (
            ee.Number(intersection_area).divide(aoi_area).multiply(100)
        )

        total_pixels = (
            scl_band.unmask()
            .reduceRegion(
                reducer=ee.Reducer.count(), geometry=geometry, scale=10, maxPixels=1e9
            )
            .getNumber("SCL")
        )

        valid_mask = OpticalService._build_valid_scl_mask(
            image.addBands(scl_band, overwrite=True), invalid_scl_values
        )
        valid_pixels = (
            valid_mask.selfMask()
            .reduceRegion(
                reducer=ee.Reducer.count(), geometry=geometry, scale=10, maxPixels=1e9
            )
            .getNumber("valid_scl")
        )

        valid_pixel_percentage = ee.Algorithms.If(
            ee.Number(total_pixels).gt(0),
            ee.Number(valid_pixels).divide(total_pixels).multiply(100),
            0,
        )

        mean_dict = image.select("index").reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=10,
            maxPixels=1e9,
        )
        aoi_average = mean_dict.get("index")

        return image.set(
            {
                "date": ee.Date(image.get("system:time_start")).format("YYYY-MM-dd"),
                "AOI_average": aoi_average,
                "cloud_pct": image.get("CLOUDY_PIXEL_PERCENTAGE"),
                "valid_pixel_pct": valid_pixel_percentage,
                "coverage_pct": coverage_percentage,
                "image_id": image.get("system:index"),
            }
        )

    @staticmethod
    def _extract_data_rows(collection: ee.ImageCollection) -> List[Dict[str, Any]]:

        def extract_properties(image):
            return ee.Feature(
                None,
                {
                    "date": image.get("date"),
                    "AOI_average": image.get("AOI_average"),
                    "cloud_pct": image.get("cloud_pct"),
                    "valid_pixel_pct": image.get("valid_pixel_pct"),
                    "coverage_pct": image.get("coverage_pct"),
                    "image_id": image.get("image_id"),
                },
            )

        feature_collection = ee.FeatureCollection(collection.map(extract_properties))
        info = feature_collection.getInfo()

        rows = []
        for feature in info.get("features", []):
            property = feature.get("properties", {})
            if property.get("AOI_average") is not None:
                rows.append(property)

        return rows
