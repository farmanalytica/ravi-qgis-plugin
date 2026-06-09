# -*- coding: utf-8 -*-
"""
Landsat service layer (Super-Resolution page).

Wraps ``agrigee_lite`` Landsat 7/8/9 sources to deliver:

* **Super-resolution RGB** — HSV pan-sharpening merges the 15 m panchromatic
  band into RGB, taking Landsat from 30 m to an effective 15 m. The library
  only allows this on Top-of-Atmosphere (TOA) products, so super-res imagery is
  TOA reflectance, not surface reflectance.
* **Vegetation indices** and **multispectral RGB** — computed on the
  atmospherically-corrected Surface Reflectance (SR) product (30 m).

All Earth-Engine / ``agrigee_lite`` specifics live here, off the UI thread
(callers run these from QThread workers). The download path reuses the plugin's
established ``getDownloadURL`` + ``requests`` pattern (see ``OpticalService``)
rather than ``agrigee_lite.get`` (which shells out to aria2 and writes to a
private cache).
"""

import os
import tempfile
from datetime import datetime, timedelta

import ee
import requests

try:
    from osgeo import gdal
except ImportError:
    gdal = None


# Missions exposed by the page. Landsat 5 is excluded: it carries no
# panchromatic band, so pan-sharpening (the page's headline feature) is
# impossible. Imported lazily inside helpers because ``agrigee_lite`` only lands
# on sys.path after extlibs provisioning.
MISSIONS = ["Landsat 8", "Landsat 9", "Landsat 7"]

# Vegetation indices computable from the six Landsat SR bands
# (blue, green, red, nir, swir1, swir2). Display name -> agrigee_lite key.
# Red-edge indices (NDRE, MTCI, …) are intentionally absent: Landsat has no
# red-edge band. Keys must exist in agrigee_lite.vegetation_indices.
LANDSAT_INDEX_KEYS = {
    "NDVI": "ndvi",
    "GNDVI": "gndvi",
    "EVI": "evi",
    "EVI2": "evi2",
    "SAVI": "savi",
    "OSAVI": "osavi",
    "MSAVI": "msavi",
    "ARVI": "arvi",
    "NDWI": "ndwi",
    "MNDWI": "mndwi",
    "BSI": "bsi",
    "CIgreen": "ci_green",
    "CIred": "ci_red",
    "MCARI": "mcari",
}
LANDSAT_INDEX_ORDER = list(LANDSAT_INDEX_KEYS.keys())

# Multispectral RGB render modes over the SR bands. Friendly-band triples are
# resolved to numeral band names at download time. itemData carries the stable
# English key so the renderer survives a translated UI (same trick as optical).
MULTISPECTRAL_MODES = {
    "RGB: Real Color": ("red", "green", "blue"),
    "RGB: NIR-Red-Green": ("nir", "red", "green"),
    "RGB: SWIR1-NIR-Red": ("swir1", "nir", "red"),
    "RGB: SWIR2-NIR-Green": ("swir2", "nir", "green"),
}


def _mission_class(mission: str):
    """Return the agrigee_lite satellite class for a mission display name."""
    from agrigee_lite.sat.landsat import Landsat7, Landsat8, Landsat9

    return {
        "Landsat 7": Landsat7,
        "Landsat 8": Landsat8,
        "Landsat 9": Landsat9,
    }[mission]


class LandsatService:
    """Earth-Engine logic for the Landsat super-resolution page."""

    # -- satellite builders ------------------------------------------------
    @staticmethod
    def _build_superres_sat(mission: str, use_cloud_mask: bool, tier: int):
        """TOA + pan-sharpening satellite (effective 15 m). ``use_sr`` must be
        False and ``pan`` must be selected or agrigee_lite raises ValueError."""
        return _mission_class(mission)(
            bands={"blue", "green", "red", "pan"},
            use_sr=False,
            use_pan_sharpening=True,
            tier=tier,
            use_cloud_mask=use_cloud_mask,
            border_pixels_to_erode=0,
        )

    @staticmethod
    def _build_sr_sat(mission: str, use_cloud_mask: bool, tier: int, indices=None):
        """Surface-reflectance satellite (30 m), optionally with one index."""
        return _mission_class(mission)(
            indices=indices,
            use_sr=True,
            tier=tier,
            use_cloud_mask=use_cloud_mask,
            border_pixels_to_erode=0,
        )

    # -- helpers -----------------------------------------------------------
    @staticmethod
    def _feature(aoi: ee.FeatureCollection, date_start: str, date_end: str) -> ee.Feature:
        """agrigee_lite expects a feature carrying ``s``/``e`` date strings and a
        dummy index ``0`` (used by its download/compute code paths)."""
        return ee.Feature(aoi.geometry(), {"s": date_start, "e": date_end, "0": 1})

    @staticmethod
    def _single_date_feature(aoi: ee.FeatureCollection, date: str) -> ee.Feature:
        next_date = (
            datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        return LandsatService._feature(aoi, date, next_date)

    @staticmethod
    def _numeral_band(sat, friendly: str) -> str:
        """Map a friendly band name (e.g. ``"red"``) to the numeral name
        agrigee_lite renames it to (e.g. ``"13_red"``). Robust to the library's
        ``sorted(bands)`` ordering."""
        for friendly_name, numeral_name in sat.selectedBands:
            if friendly_name == friendly:
                return numeral_name
        raise KeyError(f"Band '{friendly}' not selected on satellite.")

    @staticmethod
    def _numeral_index(sat, index_key: str) -> str:
        for _expr, name, numeral_name in sat.selectedIndices:
            if name == index_key:
                return numeral_name
        raise KeyError(f"Index '{index_key}' not selected on satellite.")

    @staticmethod
    def _region(aoi: ee.FeatureCollection, buffer_m: float):
        geometry = aoi.geometry()
        if buffer_m:
            geometry = geometry.buffer(buffer_m)
        return geometry

    # -- date discovery (Run) ---------------------------------------------
    @staticmethod
    def list_dated_missions(
        aoi: ee.FeatureCollection,
        date_start: str,
        date_end: str,
        use_cloud_mask: bool = True,
        tier: int = 1,
    ) -> list:
        """Available acquisition dates over the AOI/date-range across all
        missions (Landsat 7/8/9), as ``(date, mission)`` tuples sorted by date.

        ``ZZ_USER_TIME_DUMMY`` is the per-image date string agrigee_lite tags
        during its valid-pixel filtering step. Missions whose temporal range
        falls outside the request simply return no dates.
        """
        feature = LandsatService._feature(aoi, date_start, date_end)
        out = []
        for mission in MISSIONS:
            sat = LandsatService._build_sr_sat(mission, use_cloud_mask, tier)
            dates = sat.imageCollection(feature).aggregate_array(
                "ZZ_USER_TIME_DUMMY"
            ).getInfo()
            for date in set(dates or []):
                out.append((date, mission))
        out.sort(key=lambda pair: (pair[0], pair[1]))
        return out

    # -- index time series (agrigee_lite SITS) ----------------------------
    @staticmethod
    def get_index_timeseries(
        shapely_geom,
        date_start: str,
        date_end: str,
        mission: str,
        index_name: str,
        use_cloud_mask: bool = True,
        tier: int = 1,
        reducer: str = "median",
    ):
        """One mission's index time series as a DataFrame via agrigee_lite's
        ``download_single_sits`` (server-side ``computeFeatures``, no aria2).
        Columns include ``timestamp`` (datetime) and the index column (the
        agrigee key). Returns an empty DataFrame if the range misses the
        mission's lifespan.
        """
        import pandas as pd
        from agrigee_lite.get.sits import download_single_sits

        index_key = LANDSAT_INDEX_KEYS.get(index_name, "ndvi")
        sat = LandsatService._build_sr_sat(
            mission, use_cloud_mask, tier, indices={index_key}
        )

        # Clip the request to this mission's lifespan ∩ the requested range so a
        # range that only partly (or doesn't) cover a mission is handled cleanly
        # — non-intersecting missions are skipped, partial ones query only their
        # valid sub-window.
        sat_start, sat_end = sat.startDate[:10], sat.endDate[:10]
        clip_start = max(date_start, sat_start)
        clip_end = min(date_end, sat_end)
        if clip_end <= clip_start:
            return pd.DataFrame()
        try:
            df = download_single_sits(
                shapely_geom, clip_start, clip_end, sat, reducers={reducer}
            )
        except ValueError:
            # Requested period does not intersect this mission's range.
            return pd.DataFrame()
        if df is None or df.empty or index_key not in df.columns:
            return pd.DataFrame()
        return df

    @staticmethod
    def get_index_timeseries_df(
        shapely_geom,
        date_start: str,
        date_end: str,
        index_name: str,
        use_cloud_mask: bool = True,
        tier: int = 1,
        reducer: str = "median",
    ):
        """Combined index time series across all missions (L7/8/9) as a single
        DataFrame with columns ``dates``, ``AOI_average`` and ``mission``,
        sorted by date. Shaped for the plotly renderer reused from the optical
        page (``view/sar_plot.render_chart_html``)."""
        import pandas as pd

        index_key = LANDSAT_INDEX_KEYS.get(index_name, "ndvi")
        frames = []
        for mission in MISSIONS:
            try:
                df = LandsatService.get_index_timeseries(
                    shapely_geom,
                    date_start,
                    date_end,
                    mission,
                    index_name,
                    use_cloud_mask,
                    tier,
                    reducer,
                )
            except Exception as e:
                # One mission failing (range, quota…) must not drop the others.
                print(f"Landsat time-series ({mission}) skipped: {e}")
                continue
            if df.empty or index_key not in df.columns:
                continue
            sub = df[["timestamp", index_key]].dropna()
            if sub.empty:
                continue
            sub = sub.rename(columns={"timestamp": "dates", index_key: "AOI_average"})
            sub["dates"] = pd.to_datetime(sub["dates"]).dt.strftime("%Y-%m-%d")
            sub["mission"] = mission
            frames.append(sub)

        columns = ["dates", "AOI_average", "mission"]
        if not frames:
            return pd.DataFrame(columns=columns)

        out = pd.concat(frames, ignore_index=True)
        return out.sort_values("dates").reset_index(drop=True)

    # -- single-date image builders ---------------------------------------
    @staticmethod
    def get_superres_image_for_date(
        aoi, date, mission, use_cloud_mask=True, tier=1, buffer_m=0
    ):
        """Pan-sharpened real-colour RGB (15 m) for ``date``, clipped to the
        buffered AOI. Bands returned in R, G, B order so the renderer can always
        use (1, 2, 3)."""
        sat = LandsatService._build_superres_sat(mission, use_cloud_mask, tier)
        collection = sat.imageCollection(LandsatService._single_date_feature(aoi, date))
        image = ee.Image(collection.first())
        red = LandsatService._numeral_band(sat, "red")
        green = LandsatService._numeral_band(sat, "green")
        blue = LandsatService._numeral_band(sat, "blue")
        image = image.select([red, green, blue], ["red", "green", "blue"])
        region = LandsatService._region(aoi, buffer_m)
        return image.clip(region), region, sat.pixelSize

    @staticmethod
    def get_multispectral_image_for_date(
        aoi, date, mission, mode, use_cloud_mask=True, tier=1, buffer_m=0
    ):
        """Three SR bands (30 m) composited per ``mode``, in display order."""
        sat = LandsatService._build_sr_sat(mission, use_cloud_mask, tier)
        collection = sat.imageCollection(LandsatService._single_date_feature(aoi, date))
        image = ee.Image(collection.first())
        friendly = MULTISPECTRAL_MODES.get(mode, MULTISPECTRAL_MODES["RGB: Real Color"])
        numerals = [LandsatService._numeral_band(sat, b) for b in friendly]
        image = image.select(numerals, ["r", "g", "b"])
        region = LandsatService._region(aoi, buffer_m)
        return image.clip(region), region, sat.pixelSize

    @staticmethod
    def get_index_image_for_date(
        aoi, date, mission, index_name, use_cloud_mask=True, tier=1, buffer_m=0
    ):
        """Single-band vegetation index (30 m, SR) for ``date``."""
        index_key = LANDSAT_INDEX_KEYS.get(index_name, "ndvi")
        sat = LandsatService._build_sr_sat(
            mission, use_cloud_mask, tier, indices={index_key}
        )
        collection = sat.imageCollection(LandsatService._single_date_feature(aoi, date))
        image = ee.Image(collection.first())
        numeral = LandsatService._numeral_index(sat, index_key)
        image = image.select([numeral], ["index"])
        region = LandsatService._region(aoi, buffer_m)
        return image.clip(region), region, sat.pixelSize

    # -- download wrappers -------------------------------------------------
    @staticmethod
    def _download(image, region, scale, filename, output_folder, band_names=None) -> str:
        url = image.getDownloadURL(
            {
                "scale": scale,
                "region": region.bounds().getInfo(),
                "format": "GeoTIFF",
                "crs": "EPSG:4326",
            }
        )
        response = requests.get(url, timeout=300)
        if not response.ok:
            raise RuntimeError(
                f"Landsat download failed (HTTP {response.status_code}): "
                f"{response.reason}"
            )

        base_dir = (
            output_folder
            if (output_folder and os.path.isdir(output_folder))
            else tempfile.gettempdir()
        )
        output_path = LandsatService._unique_path(base_dir, filename)
        with open(output_path, "wb") as f:
            f.write(response.content)

        if band_names:
            LandsatService._set_band_names(output_path, band_names)
        return output_path

    @staticmethod
    def _slug(mission: str) -> str:
        return mission.replace(" ", "")

    @staticmethod
    def download_superres_for_date(
        aoi, date, mission, use_cloud_mask=True, tier=1, buffer_m=0, output_folder=None
    ) -> str:
        image, region, scale = LandsatService.get_superres_image_for_date(
            aoi, date, mission, use_cloud_mask, tier, buffer_m
        )
        return LandsatService._download(
            image,
            region,
            scale,
            f"{LandsatService._slug(mission)}_SuperRes_{date}.tiff",
            output_folder,
            band_names=["red", "green", "blue"],
        )

    @staticmethod
    def download_multispectral_for_date(
        aoi, date, mission, mode, use_cloud_mask=True, tier=1, buffer_m=0, output_folder=None
    ) -> str:
        image, region, scale = LandsatService.get_multispectral_image_for_date(
            aoi, date, mission, mode, use_cloud_mask, tier, buffer_m
        )
        return LandsatService._download(
            image,
            region,
            scale,
            f"{LandsatService._slug(mission)}_RGB_{date}.tiff",
            output_folder,
        )

    @staticmethod
    def download_index_for_date(
        aoi, date, mission, index_name, use_cloud_mask=True, tier=1, buffer_m=0, output_folder=None
    ) -> str:
        image, region, scale = LandsatService.get_index_image_for_date(
            aoi, date, mission, index_name, use_cloud_mask, tier, buffer_m
        )
        return LandsatService._download(
            image,
            region,
            scale,
            f"{LandsatService._slug(mission)}_{index_name}_{date}.tiff",
            output_folder,
        )

    # -- fs / metadata utilities ------------------------------------------
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
    def _set_band_names(file_path: str, band_names: list):
        if gdal is None:
            return
        try:
            dataset = gdal.Open(file_path, gdal.GA_Update)
            if dataset is None:
                return
            for i in range(1, min(dataset.RasterCount + 1, len(band_names) + 1)):
                band = dataset.GetRasterBand(i)
                if band is not None:
                    band.SetDescription(band_names[i - 1])
            dataset = None
        except Exception:
            pass
