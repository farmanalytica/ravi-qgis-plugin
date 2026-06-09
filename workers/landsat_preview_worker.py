# -*- coding: utf-8 -*-
"""
Background worker for single-date Landsat downloads (preview or export).

Downloads one scene for a date off the UI thread, in one of three kinds:
``"superres"`` (pan-sharpened 15 m RGB, TOA), ``"index"`` (single-band
vegetation index, 30 m SR) or ``"multispectral"`` (3-band RGB composite, 30 m
SR). The AOI is extracted on the main thread and passed in.
"""

from qgis.PyQt.QtCore import QThread, pyqtSignal

from ..services.landsat_service import LandsatService


class LandsatPreviewWorker(QThread):
    finished = pyqtSignal(str, str)   # output_path, kind
    failed = pyqtSignal(str)

    def __init__(
        self,
        kind,
        aoi,
        date,
        mission,
        index_name,
        mode,
        use_cloud_mask,
        tier,
        buffer_m,
        output_folder,
    ):
        super().__init__()
        self._kind = kind
        self._aoi = aoi
        self._date = date
        self._mission = mission
        self._index_name = index_name
        self._mode = mode
        self._use_cloud_mask = use_cloud_mask
        self._tier = tier
        self._buffer_m = buffer_m
        self._output_folder = output_folder

    def run(self):
        try:
            if self._kind == "superres":
                path = LandsatService.download_superres_for_date(
                    self._aoi,
                    self._date,
                    self._mission,
                    use_cloud_mask=self._use_cloud_mask,
                    tier=self._tier,
                    buffer_m=self._buffer_m,
                    output_folder=self._output_folder,
                )
            elif self._kind == "index":
                path = LandsatService.download_index_for_date(
                    self._aoi,
                    self._date,
                    self._mission,
                    self._index_name,
                    use_cloud_mask=self._use_cloud_mask,
                    tier=self._tier,
                    buffer_m=self._buffer_m,
                    output_folder=self._output_folder,
                )
            else:
                path = LandsatService.download_multispectral_for_date(
                    self._aoi,
                    self._date,
                    self._mission,
                    self._mode,
                    use_cloud_mask=self._use_cloud_mask,
                    tier=self._tier,
                    buffer_m=self._buffer_m,
                    output_folder=self._output_folder,
                )
            self.finished.emit(path, self._kind)
        except Exception as e:
            self.failed.emit(str(e))
