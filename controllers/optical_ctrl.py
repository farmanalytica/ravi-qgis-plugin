# -*- coding: utf-8 -*-
"""
Controller for the Optical (Sentinel-2) page.

This milestone only proves the Earth Engine -> pandas path: clicking Run on the
Inputs tab fetches the vegetation-index time series and prints the resulting
DataFrame, including filter metadata, to the QGIS/Python console.
"""

import os
import tempfile
from datetime import datetime

import pandas as pd

from qgis.PyQt.QtCore import QCoreApplication, QUrl
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtWidgets import QFileDialog, QProgressDialog
from qgis.core import (
    QgsContrastEnhancement,
    QgsCoordinateTransform,
    QgsMultiBandColorRenderer,
    QgsProject,
    QgsRasterLayer,
)

from ..managers.settings_manager import SettingsManager
from ..services.aoi_service import AOIService
from ..services.optical_service import OpticalService
from ..tools.aoi_draw_tool import start_draw_aoi
from ..view.optical_filter_dialog import DEFAULT_FILTER_SETTINGS
from ..view.optical_index_info import CUSTOM_INDEX_LABEL
from ..renderers.raster_renderer_utils import RasterRendererUtils
from ..view.sar_plot import render_chart_html
from ..workers.batch_download_worker import BatchDownloadWorker
from ..workers.optical_preview_worker import OpticalPreviewWorker
from ..workers.optical_worker import OpticalWorker


def _tr(text):
    return QCoreApplication.translate("RAVI", text)


_LOADING_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{height:100%;margin:0;font-family:Arial,sans-serif;background:#fff}
.box{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
text-align:center;color:#616161}.spinner{width:34px;height:34px;margin:0 auto 12px;
border:3px solid #e0e0e0;border-top-color:#1b6b39;border-radius:50%;
animation:spin .9s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
</style></head><body><div class="box"><div class="spinner"></div>
<div>Fetching Sentinel-2 time series...</div></div></body></html>"""


class OpticalCtrl:
    """Coordinate the Optical Inputs tab run action."""

    _CANVAS_SCALE_FACTOR = 1.5

    def __init__(self, dialog, interface=None, gee_service=None):
        self.dialog = dialog
        self.interface = interface
        self.gee_service = gee_service

        self.aoi = None
        self.dataframe = None
        self._current_index = "NDVI"
        self._optical_worker: OpticalWorker | None = None
        self._run_btn_text: str | None = None
        self._draw_tool = None
        self._plot_path: str | None = None
        self._filter_settings = dict(DEFAULT_FILTER_SETTINGS)
        self._active_dates: list | None = None
        self._date_filter_dialog = None
        self._batch_worker: BatchDownloadWorker | None = None
        self._batch_dialog: QProgressDialog | None = None
        self._preview_worker: OpticalPreviewWorker | None = None
        self._preview_btn_texts: tuple | None = None

        # The "Adjust filter" dialog shows a live image count (cheap) and only
        # re-renders the plot when the user clicks OK.
        self.dialog.optical_filter_count_fn = self.count_matching
        self.dialog.on_optical_filter_applied = self.apply_filter_settings
        self.dialog.s2_filter_settings = dict(DEFAULT_FILTER_SETTINGS)

    def _release_worker(self):
        worker, self._optical_worker = self._optical_worker, None
        if worker is not None:
            worker.deleteLater()

    def _show_auth_required_message(self):
        self.dialog.pop_message(
            _tr(
                "Authentication is required to download optical data. "
                "Please go to the Auth page and validate your Google Cloud project ID."
            ),
            "warning",
        )

    def handle_draw_aoi(self):
        """Toggle rectangular AOI drawing on the canvas."""

        if self.interface is None:
            return

        canvas = self.interface.mapCanvas()
        if self._draw_tool is not None and canvas.mapTool() is self._draw_tool:
            canvas.unsetMapTool(self._draw_tool)
            self._draw_tool = None
            return

        self._draw_tool = start_draw_aoi(
            self.interface, self.dialog.s2_layer_combo, self.dialog.s2_btn_draw_aoi
        )

    def handle_layer_changed(self, layer=None):
        """Zoom to the selected optical AOI layer."""

        if layer is None:
            layer = self.dialog.s2_layer_combo.currentLayer()

        if not layer or not layer.isValid() or self.interface is None:
            return

        canvas = self.interface.mapCanvas()
        transform = QgsCoordinateTransform(
            layer.crs(),
            canvas.mapSettings().destinationCrs(),
            QgsProject.instance(),
        )
        extent = transform.transformBoundingBox(layer.extent())
        extent.scale(self._CANVAS_SCALE_FACTOR)
        canvas.setExtent(extent)
        canvas.refresh()

    def handle_optical_run(self):
        """Fetch the optical time series and plot it on the results page."""

        if self._optical_worker is not None and self._optical_worker.isRunning():
            return

        if self.gee_service and not self.gee_service.is_authenticated:
            self._show_auth_required_message()
            return

        layer = self.dialog.s2_layer_combo.currentLayer()
        if not layer:
            self.dialog.pop_message(_tr("Select an AOI layer."), "warning")
            return

        start_qdate = self.dialog.s2_date_start.date()
        end_qdate = self.dialog.s2_date_end.date()
        if start_qdate >= end_qdate:
            self.dialog.pop_message(
                _tr("End date must be after start date."), "warning"
            )
            return

        index_name = self.dialog.s2_index_combo.currentData() or "NDVI"
        if index_name == CUSTOM_INDEX_LABEL:
            self.dialog.pop_message(
                _tr("Custom optical indices are not available in this milestone."),
                "warning",
            )
            return

        try:
            aoi, _bbox = AOIService.get_ee_feature_colection_from_layer(
                layer, use_selected_features=False
            )
        except Exception as e:
            self.dialog.pop_message(str(e), "warning")
            return

        self.aoi = aoi
        params = {
            "date_start": start_qdate.toString("yyyy-MM-dd"),
            "date_end": end_qdate.toString("yyyy-MM-dd"),
            "index_name": index_name,
            "apply_scl": self.dialog.s2_chk_apply_scl.isChecked(),
            "invalid_scl_values": self._selected_invalid_scl_values(),
        }

        self._current_index = index_name
        self._set_run_busy(True)
        self.dialog.s2_web_view.setHtml(_LOADING_HTML)
        self.dialog.s2_set_tab(2)

        self._optical_worker = OpticalWorker(aoi, params)
        self._optical_worker.finished.connect(self._on_optical_done)
        self._optical_worker.failed.connect(self._on_optical_failed)
        self._optical_worker.start()

    def _selected_invalid_scl_values(self) -> list[int]:
        checks = getattr(self.dialog, "s2_scl_checks", {})
        return [value for value, checkbox in checks.items() if checkbox.isChecked()]

    def _set_run_busy(self, busy: bool):
        btn = self.dialog.s2_btn_run
        if busy:
            self._run_btn_text = self._run_btn_text or btn.text()
            btn.setText(_tr("Running..."))
        else:
            btn.setText(self._run_btn_text or btn.text())
        btn.setEnabled(not busy)

    def _on_optical_done(self, data_rows, index_name):
        self._set_run_busy(False)
        self._release_worker()

        if not data_rows:
            self.dataframe = pd.DataFrame()
            self.dialog.s2_web_view.setHtml("")
            self.dialog.s2_set_tab(1)
            self.dialog.pop_message(
                _tr("No Sentinel-2 images found for this date range."), "warning"
            )
            return

        columns = [
            "date",
            "AOI_average",
            "cloud_pct",
            "valid_pixel_pct",
            "coverage_pct",
            "image_id",
        ]
        self.dataframe = pd.DataFrame(data_rows)
        self.dataframe = self.dataframe.reindex(columns=columns)
        self._current_index = index_name
        self._active_dates = None

        self._refresh_result_dates()
        self._render_timeseries()
        self.dialog.s2_set_tab(2)

    def apply_filter_settings(self, settings: dict):
        """Apply new threshold filters (called on Adjust-filter OK).

        Applying thresholds changes which dates qualify, so it overrides any
        manual date selection (Filter dates) and rebuilds the single-image date
        dropdown from the newly filtered set.
        """
        self._filter_settings = dict(settings)
        self._active_dates = None
        if self.dataframe is not None and not self.dataframe.empty:
            self._refresh_result_dates()
            self._render_timeseries()

    def count_matching(self, settings: dict) -> int:
        """Count cached images passing the given thresholds (live, no render)."""
        if self.dataframe is None or self.dataframe.empty:
            return 0
        return int(self._filter_mask(self.dataframe, settings).sum())

    @staticmethod
    def _filter_mask(df, s):
        return (
            (df["cloud_pct"] <= s["cloud_scene_max"])
            & (df["valid_pixel_pct"] >= s["valid_pixel_min"])
            & (df["coverage_pct"] >= s["coverage_min"])
        )

    def _threshold_dates(self) -> list:
        """Dates passing the current thresholds (ignores manual date selection)."""
        df = self.dataframe[self._filter_mask(self.dataframe, self._filter_settings)]
        return df["date"].dropna().astype(str).tolist()

    def _filtered_dataframe(self) -> pd.DataFrame:
        """Cached series after thresholds and the manual date selection."""
        df = self.dataframe[self._filter_mask(self.dataframe, self._filter_settings)]
        if self._active_dates is not None:
            df = df[df["date"].astype(str).isin(self._active_dates)]
        return df

    def _refresh_result_dates(self):
        """Repopulate the single-image date dropdown from the filtered series."""
        dates = self._filtered_dataframe()["date"].dropna().astype(str).tolist()
        self.dialog.s2_available_dates = dates
        combo = self.dialog.s2_result_date_combo
        previous = combo.currentText()
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(dates)
        if previous in dates:
            combo.setCurrentText(previous)
        combo.blockSignals(False)

    # -- Filter dates (manual per-date include/exclude) -------------------
    def handle_filter_dates(self):
        if self.dataframe is None or self.dataframe.empty:
            self.dialog.pop_message(_tr("Run the optical analysis first."), "warning")
            return

        if self._date_filter_dialog is not None:
            self._date_filter_dialog.raise_()
            self._date_filter_dialog.activateWindow()
            return

        from ..view.sar_date_filter_dialog import SARDateFilterDialog

        self._date_filter_dialog = SARDateFilterDialog(
            self._threshold_dates(), self._active_dates, parent=self.dialog
        )
        self._date_filter_dialog.filter_changed.connect(self._on_dates_changed)
        self._date_filter_dialog.finished.connect(self._on_date_filter_closed)
        self._date_filter_dialog.show()

    def _on_dates_changed(self, selected_dates):
        all_dates = self._threshold_dates()
        self._active_dates = (
            None if set(selected_dates) == set(all_dates) else list(selected_dates)
        )
        self._refresh_result_dates()
        self._render_timeseries()

    def _on_date_filter_closed(self):
        self._date_filter_dialog = None

    # -- export actions (time-series toolbar) -----------------------------
    def _has_results(self) -> bool:
        if self.dataframe is None or self.dataframe.empty:
            self.dialog.pop_message(_tr("Run the optical analysis first."), "warning")
            return False
        return True

    def _plot_dataframe(self):
        return (
            self._filtered_dataframe()
            .rename(columns={"date": "dates"})
            .dropna(subset=["dates", "AOI_average"])
        )

    def handle_open_browser(self):
        """Open the current (filtered) time series in the system browser."""
        if not self._has_results():
            return

        index_name = self._current_index
        html = render_chart_html(
            self._plot_dataframe(),
            hide_toolbar=False,
            title=_tr("%s Time Series") % index_name,
            ylabel=_tr("%s AOI average") % index_name,
        )
        with tempfile.NamedTemporaryFile(
            suffix=".html", delete=False, mode="w", encoding="utf-8"
        ) as f:
            f.write(html)
            path = f.name
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def handle_export_csv(self):
        """Export the current (filtered) time series as CSV."""
        if not self._has_results():
            return

        date_str = datetime.now().strftime("%Y%m%d")
        default_filename = f"optical_{self._current_index}_timeseries_{date_str}.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self.dialog,
            _tr("Export Optical Time Series as CSV"),
            default_filename,
            _tr("CSV Files (*.csv);;All Files (*)"),
        )
        if not file_path:
            return

        try:
            self._filtered_dataframe().to_csv(file_path, index=False)
            self.dialog.pop_message(
                _tr("CSV exported successfully to %s") % file_path, "info"
            )
        except Exception as e:
            self.dialog.pop_message(_tr("Failed to export CSV: %s") % str(e), "warning")

    def _buffer_meters(self) -> float:
        slider = getattr(self.dialog, "s2_buffer_slider", None)
        if slider is None:
            return 0
        value = slider.value()
        return 0 if -3 <= value <= 3 else value  # match the UI dead-zone

    def handle_batch_download(self):
        """Download the multispectral scene of every filtered date (raw S2
        bands, clipped to the AOI plus the buffer setting)."""
        if not self._has_results():
            return
        if self._batch_worker is not None and self._batch_worker.isRunning():
            return

        dates = self._filtered_dataframe()["date"].dropna().astype(str).tolist()
        if not dates:
            self.dialog.pop_message(_tr("No dates selected to download."), "warning")
            return

        aoi = self.aoi
        buffer_m = self._buffer_meters()
        folder = SettingsManager.load_download_folder()

        self._batch_dialog = QProgressDialog(
            _tr("Preparing batch download..."),
            _tr("Cancel"),
            0,
            len(dates),
            self.dialog,
        )
        self._batch_dialog.setWindowTitle(_tr("Batch Download Progress"))
        self._batch_dialog.setModal(True)
        self._batch_dialog.show()

        def _download_one(date):
            return OpticalService.download_multispectral_for_date(
                aoi, date, buffer_m=buffer_m, output_folder=folder
            )

        self._batch_worker = BatchDownloadWorker(dates, _download_one)
        self._batch_worker.progress.connect(self._on_batch_progress)
        self._batch_worker.finished.connect(self._on_batch_done)
        self._batch_worker.cancelled.connect(self._on_batch_cancelled)
        self._batch_worker.failed.connect(self._on_batch_failed)
        self._batch_dialog.canceled.connect(self._batch_worker.request_cancel)
        self._batch_worker.start()

    def _on_batch_progress(self, current: int, total: int, date_str: str):
        if self._batch_dialog is None:
            return
        self._batch_dialog.setMaximum(total)
        self._batch_dialog.setValue(current)
        self._batch_dialog.setLabelText(
            _tr("Downloading %d of %d: %s") % (current, total, date_str)
        )

    def _on_batch_done(self, successful: int, total: int, paths: list):
        self._close_batch_dialog()
        self._load_downloaded_images(paths)
        failed = total - successful
        msg = _tr("Batch download complete: %d/%d successful") % (successful, total)
        if failed > 0:
            msg += _tr(" (%d failed)") % failed
        self.dialog.pop_message(msg, "warning" if failed > 0 else "info")
        self._batch_worker = None

    def _on_batch_cancelled(self, successful: int, total: int, paths: list):
        self._close_batch_dialog()
        self._load_downloaded_images(paths)
        self.dialog.pop_message(
            _tr("Batch download cancelled. %d/%d downloaded.") % (successful, total),
            "info",
        )
        self._batch_worker = None

    def _on_batch_failed(self, message: str):
        self._close_batch_dialog()
        self.dialog.pop_message(_tr("Batch download failed: %s") % message, "warning")
        self._batch_worker = None

    def _close_batch_dialog(self):
        if self._batch_dialog is not None:
            self._batch_dialog.close()
            self._batch_dialog = None

    # Band positions within the _MULTISPECTRAL_BANDS stack (1-based):
    # B1=1 B2=2 B3=3 B4=4 B5=5 B6=6 B7=7 B8=8 B8A=9 B9=10 B11=11 B12=12.
    _RGB_MODE_BANDS = {
        "RGB: Real Color": (4, 3, 2),       # B4 B3 B2
        "RGB: Red-NIR-Green": (4, 8, 3),    # B4 B8 B3
        "RGB: NIR-Red-Green": (8, 4, 3),    # B8 B4 B3
        "RGB: SWIR2-NIR-Green": (12, 8, 3),  # B12 B8 B3
        "RGB: SWIR1-NIR-SWIR2": (11, 8, 12),  # B11 B8 B12
    }

    def _load_downloaded_images(self, paths: list):
        for path in paths:
            try:
                name = os.path.splitext(os.path.basename(path))[0]
                self._add_rgb_raster(path, name)
            except Exception:
                continue

    def _add_rgb_raster(self, path: str, name: str, bands=(4, 3, 2)):
        """Load a multispectral GeoTIFF as an RGB composite (default true colour
        B4/B3/B2) with a 2–98% cumulative-cut stretch per band."""
        layer = QgsRasterLayer(path, name)
        if not layer.isValid():
            return

        provider = layer.dataProvider()
        red, green, blue = bands
        renderer = QgsMultiBandColorRenderer(provider, red, green, blue)

        extent = layer.extent()
        for band, set_enhancement in (
            (red, renderer.setRedContrastEnhancement),
            (green, renderer.setGreenContrastEnhancement),
            (blue, renderer.setBlueContrastEnhancement),
        ):
            val_min, val_max = provider.cumulativeCut(band, 0.02, 0.98, extent, 250000)
            ce = QgsContrastEnhancement(provider.dataType(band))
            ce.setContrastEnhancementAlgorithm(
                QgsContrastEnhancement.StretchToMinimumMaximum
            )
            ce.setMinimumValue(val_min)
            ce.setMaximumValue(val_max)
            set_enhancement(ce)

        layer.setRenderer(renderer)
        RasterRendererUtils.add_layer_to_project(layer, at_top=True)
        layer.triggerRepaint()

    # -- single-date image (preview / download) ---------------------------
    def handle_rgb_preview(self):
        self._run_single("rgb", to_folder=False)

    def handle_rgb_download(self):
        self._run_single("rgb", to_folder=True)

    def handle_vi_preview(self):
        self._run_single("index", to_folder=False)

    def handle_vi_download(self):
        self._run_single("index", to_folder=True)

    def _run_single(self, kind: str, to_folder: bool):
        if not self._has_results():
            return
        if self._preview_worker is not None and self._preview_worker.isRunning():
            return

        date = self.dialog.s2_result_date_combo.currentText()
        if not date:
            self.dialog.pop_message(_tr("Select a date first."), "warning")
            return

        index_name = self.dialog.s2_vi_index_combo.currentData() or "NDVI"
        if kind == "index" and index_name == CUSTOM_INDEX_LABEL:
            self.dialog.pop_message(
                _tr("Custom optical indices are not available in this milestone."),
                "warning",
            )
            return

        folder = (
            SettingsManager.load_download_folder()
            if to_folder
            else tempfile.gettempdir()
        )

        self._set_single_busy(kind, True)
        self._preview_worker = OpticalPreviewWorker(
            kind, self.aoi, date, index_name, self._buffer_meters(), folder
        )
        self._preview_worker.finished.connect(
            lambda path, k: self._on_single_done(path, k, to_folder)
        )
        self._preview_worker.failed.connect(self._on_single_failed)
        self._preview_worker.start()

    def _single_buttons(self, kind: str):
        if kind == "index":
            return (self.dialog.s2_btn_vi_preview, self.dialog.s2_btn_vi_download)
        return (self.dialog.s2_btn_rgb_preview, self.dialog.s2_btn_rgb_download)

    def _set_single_busy(self, kind: str, busy: bool):
        btns = self._single_buttons(kind)
        if busy:
            self._preview_btn_texts = tuple(b.text() for b in btns)
            for b in btns:
                b.setText(_tr("Loading..."))
        elif self._preview_btn_texts:
            for b, txt in zip(btns, self._preview_btn_texts):
                b.setText(txt)
        for b in btns:
            b.setEnabled(not busy)

    def _on_single_done(self, path: str, kind: str, to_folder: bool):
        self._set_single_busy(kind, False)
        worker, self._preview_worker = self._preview_worker, None
        if worker is not None:
            worker.deleteLater()

        date = self.dialog.s2_result_date_combo.currentText()
        if kind == "index":
            index_name = self.dialog.s2_vi_index_combo.currentData() or "NDVI"
            ramp = self.dialog.s2_vi_ramp_combo.currentText()
            RasterRendererUtils.load_pseudocolor_raster(
                path, f"S2 {index_name} {date}", 1, ramp
            )
        else:
            mode = self.dialog.s2_rgb_render_combo.currentData()
            bands = self._RGB_MODE_BANDS.get(mode, (4, 3, 2))
            self._add_rgb_raster(path, f"S2 RGB {date}", bands)

        if self.interface is not None:
            action = _tr("downloaded and loaded") if to_folder else _tr("loaded")
            self.interface.messageBar().pushMessage(
                "RAVI", _tr("Optical image %s into QGIS.") % action
            )

    def _on_single_failed(self, message: str):
        worker, self._preview_worker = self._preview_worker, None
        if worker is not None:
            worker.deleteLater()
        # Both pairs may show "Loading..."; restore whichever is disabled.
        for kind in ("rgb", "index"):
            self._set_single_busy(kind, False)
        self.dialog.pop_message(message, "warning")

    def _render_timeseries(self):
        """Plot the AOI-average time series into the optical results web view."""
        index_name = self._current_index
        plot_df = self._filtered_dataframe().rename(columns={"date": "dates"})
        plot_df = plot_df.dropna(subset=["dates", "AOI_average"])

        html = render_chart_html(
            plot_df,
            title=_tr("%s Time Series") % index_name,
            ylabel=_tr("%s AOI average") % index_name,
        )

        fd, path = tempfile.mkstemp(suffix=".html", prefix="ravi_optical_")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        self.dialog.s2_web_view.load(QUrl.fromLocalFile(path))

        if self._plot_path and os.path.exists(self._plot_path):
            try:
                os.remove(self._plot_path)
            except OSError:
                pass
        self._plot_path = path

    def _on_optical_failed(self, message):
        self._set_run_busy(False)
        self._release_worker()
        self.dialog.s2_web_view.setHtml("")
        self.dialog.s2_set_tab(1)
        self.dialog.pop_message(message, "warning")
