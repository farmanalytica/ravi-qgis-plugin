import os
import tempfile
from datetime import datetime, timedelta
from typing import List, Dict, Any

import ee
import requests

try:
    from osgeo import gdal
except ImportError:
    gdal = None

from ..tools.indexes import INDEX_REGISTRY, calc_custom


# Raw Sentinel-2 SR multispectral bands written by the batch download (no
# computed index bands). B10 is absent from the surface-reflectance product.
_MULTISPECTRAL_BANDS = [
    "B1", "B2", "B3", "B4", "B5", "B6",
    "B7", "B8", "B8A", "B9", "B11", "B12",
]


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

    # -- multispectral export (batch download) ----------------------------
    @staticmethod
    def _download_region(aoi: ee.FeatureCollection, buffer_m: float):
        """AOI geometry, optionally buffered (positive grows, negative crops)."""
        geometry = aoi.geometry()
        if buffer_m:
            geometry = geometry.buffer(buffer_m)
        return geometry

    @staticmethod
    def get_multispectral_image_for_date(
        aoi: ee.FeatureCollection, date: str, buffer_m: float = 0
    ):
        """Single Sentinel-2 SR multispectral image for ``date`` (one scene per
        date, same pick as the time series), clipped to the buffered AOI."""
        region = OpticalService._download_region(aoi, buffer_m)
        next_date = (
            datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")

        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(aoi)
            .filterDate(date, next_date)
        )
        collection = OpticalService._keep_one_image_per_date(collection, aoi)
        image = ee.Image(collection.first()).select(_MULTISPECTRAL_BANDS)
        return image.clip(region), region

    @staticmethod
    def download_multispectral_for_date(
        aoi: ee.FeatureCollection,
        date: str,
        buffer_m: float = 0,
        output_folder: str = None,
    ) -> str:
        """Download the multispectral scene for ``date`` as a GeoTIFF and return
        its path. Raises on a failed HTTP download."""
        image, region = OpticalService.get_multispectral_image_for_date(
            aoi, date, buffer_m
        )
        url = image.getDownloadURL(
            {
                "scale": 10,
                "region": region.bounds().getInfo(),
                "format": "GeoTIFF",
                "crs": "EPSG:4326",
            }
        )

        response = requests.get(url, timeout=300)
        if not response.ok:
            raise RuntimeError(
                f"Optical download failed (HTTP {response.status_code}): "
                f"{response.reason}"
            )

        base_dir = (
            output_folder
            if (output_folder and os.path.isdir(output_folder))
            else tempfile.gettempdir()
        )
        output_path = OpticalService._unique_path(base_dir, f"Sentinel2_{date}.tiff")
        with open(output_path, "wb") as f:
            f.write(response.content)

        OpticalService._set_band_names(output_path)
        return output_path

    @staticmethod
    def get_index_image_for_date(
        aoi: ee.FeatureCollection, date: str, index_name: str, buffer_m: float = 0
    ):
        """Single-band vegetation-index image for ``date`` (same scene pick as
        the time series), clipped to the buffered AOI."""
        region = OpticalService._download_region(aoi, buffer_m)
        next_date = (
            datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")

        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(aoi)
            .filterDate(date, next_date)
        )
        collection = OpticalService._keep_one_image_per_date(collection, aoi)
        image = OpticalService._add_vegetation_index(
            ee.Image(collection.first()), index_name
        )
        return image.select("index").clip(region), region

    @staticmethod
    def download_index_for_date(
        aoi: ee.FeatureCollection,
        date: str,
        index_name: str,
        buffer_m: float = 0,
        output_folder: str = None,
    ) -> str:
        """Download the single-band index scene for ``date`` as a GeoTIFF."""
        image, region = OpticalService.get_index_image_for_date(
            aoi, date, index_name, buffer_m
        )
        url = image.getDownloadURL(
            {
                "scale": 10,
                "region": region.bounds().getInfo(),
                "format": "GeoTIFF",
                "crs": "EPSG:4326",
            }
        )

        response = requests.get(url, timeout=300)
        if not response.ok:
            raise RuntimeError(
                f"Optical download failed (HTTP {response.status_code}): "
                f"{response.reason}"
            )

        base_dir = (
            output_folder
            if (output_folder and os.path.isdir(output_folder))
            else tempfile.gettempdir()
        )
        output_path = OpticalService._unique_path(
            base_dir, f"S2_{index_name}_{date}.tiff"
        )
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path

    @staticmethod
    def _unique_path(folder: str, filename: str) -> str:
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            return path
        stem, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(folder, f"{stem}_{i}{ext}")):
            i += 1
        return os.path.join(folder, f"{stem}_{i}{ext}")

    @staticmethod
    def _set_band_names(file_path: str):
        if gdal is None:
            return
        try:
            dataset = gdal.Open(file_path, gdal.GA_Update)
            if dataset is None:
                return
            for i in range(1, min(dataset.RasterCount + 1, len(_MULTISPECTRAL_BANDS) + 1)):
                band = dataset.GetRasterBand(i)
                if band is not None:
                    band.SetDescription(_MULTISPECTRAL_BANDS[i - 1])
            dataset = None
        except Exception:
            pass
