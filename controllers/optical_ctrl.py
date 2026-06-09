# -*- coding: utf-8 -*-
"""
Controller for the Optical (Sentinel-2) page.

This milestone only proves the Earth Engine -> pandas path: clicking Run on the
Inputs tab fetches the vegetation-index time series and prints the resulting
DataFrame, including filter metadata, to the QGIS/Python console.
"""

import os
import tempfile

import pandas as pd

from qgis.PyQt.QtCore import QCoreApplication, QUrl
from qgis.core import QgsCoordinateTransform, QgsProject

from ..services.aoi_service import AOIService
from ..tools.aoi_draw_tool import start_draw_aoi
from ..view.optical_filter_dialog import DEFAULT_FILTER_SETTINGS
from ..view.optical_index_info import CUSTOM_INDEX_LABEL
from ..view.sar_plot import render_chart_html
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

        dates = self.dataframe["date"].dropna().astype(str).tolist()
        self.dialog.s2_available_dates = dates
        self.dialog.s2_result_date_combo.clear()
        self.dialog.s2_result_date_combo.addItems(dates)

        print(self.dataframe.to_string(index=False))  # TODO: remove (debug)

        self._render_timeseries()
        self.dialog.s2_set_tab(2)

    def apply_filter_settings(self, settings: dict):
        """Re-render the plot with new filter settings (called on dialog OK)."""
        self._filter_settings = dict(settings)
        if self.dataframe is not None and not self.dataframe.empty:
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

    def _filtered_dataframe(self) -> pd.DataFrame:
        """Apply the current threshold filters to the cached time series."""
        return self.dataframe[self._filter_mask(self.dataframe, self._filter_settings)]

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
