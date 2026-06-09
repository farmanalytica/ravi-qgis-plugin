# -*- coding: utf-8 -*-
"""
Client-side filter popup for the Optical (Sentinel-2) Results tab.

Under the new architecture the Sentinel-2 collection is fetched once with the
filter metadata of every image attached. This dialog lets the user adjust the
cloud / coverage / valid-pixel filters and re-filter the cached series *without*
a new Earth Engine call: it owns no GEE logic, it only gathers settings and
emits ``filter_changed`` so a controller can re-render the plot.

Each control is paired with a short explanation. Per-date include/exclude lives
in the time-series controls on the Results tab, not here.
"""

from qgis.PyQt.QtCore import Qt, QCoreApplication, pyqtSignal
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from .styles import STYLE_BTN_PRIMARY, STYLE_BTN_SECONDARY, STYLE_CHECKBOX


def _tr(text):
    return QCoreApplication.translate("RAVI", text)


_DIALOG_STYLE = (
    "QDialog { background-color: #ffffff; color: #212121; }"
    "QLabel { background: transparent; border: none; }"
    + STYLE_CHECKBOX
)

_SLIDER_STYLE = """
QSlider::groove:horizontal { height: 4px; background: #d6d6d6; border-radius: 2px; }
QSlider::sub-page:horizontal { background: #1b6b39; border-radius: 2px; }
QSlider::add-page:horizontal { background: #d6d6d6; border-radius: 2px; }
QSlider::handle:horizontal {
    background: #1b6b39; width: 14px; height: 14px;
    margin: -6px 0; border-radius: 7px;
}
QSlider::handle:horizontal:hover { background: #15532d; }
"""

class OpticalFilterDialog(QDialog):
    """Popup that adjusts the optical time-series filter client-side.

    ``filter_changed`` carries the full settings dict (see :meth:`get_settings`)
    and fires on every change so the plot can refresh live. ``dates`` is the
    list of available acquisition dates used by the per-date checklist; it may
    be empty before a series has been generated.
    """

    filter_changed = pyqtSignal(dict)

    def __init__(self, settings=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_tr("Adjust Filter"))
        self.setMinimumWidth(480)
        self.setMinimumHeight(460)
        self.resize(520, 560)
        self.setStyleSheet(_DIALOG_STYLE)

        self._initial = settings
        self._building = True

        self._build_ui()
        if settings:
            self.set_settings(settings)
        self._building = False

    # -- construction -----------------------------------------------------
    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(12, 12, 12, 12)
        main.setSpacing(10)

        intro = QLabel(
            _tr(
                "Adjust how the cached image series is filtered. Changes update "
                "the plot immediately — no new Earth Engine request is made."
            )
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #616161; font-size: 11px;")
        main.addWidget(intro)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { border: 1px solid #e0e0e0; border-radius: 4px; }"
        )
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        body = QVBoxLayout(content)
        body.setContentsMargins(12, 12, 12, 12)
        body.setSpacing(14)

        body.addWidget(self._build_cloud_section())
        body.addWidget(self._build_coverage_section())
        body.addStretch(1)

        scroll.setWidget(content)
        main.addWidget(scroll, 1)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        ok_btn = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_btn.setStyleSheet(STYLE_BTN_PRIMARY)
        ok_btn.setFixedHeight(32)
        ok_btn.setMinimumWidth(96)
        cancel_btn = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_btn.setStyleSheet(STYLE_BTN_SECONDARY)
        cancel_btn.setFixedHeight(32)
        cancel_btn.setMinimumWidth(96)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self._on_cancel)
        main.addWidget(button_box)

    def _section(self, title):
        frame = QFrame()
        frame.setStyleSheet(
            "QFrame { background: #fbfcfb; border: 1px solid #e4ebe6;"
            " border-radius: 8px; }"
            "QLabel { background: transparent; border: none; }"
        )
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(8)
        cap = QLabel(title)
        cap.setStyleSheet(
            "color: #9e9e9e; font-size: 11px; font-weight: bold; letter-spacing: 1px;"
        )
        lay.addWidget(cap)
        return frame, lay

    def _explain(self, text):
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setStyleSheet("color: #757575; font-size: 11px;")
        return lbl

    def _pct_slider(self, value):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(value)
        slider.setStyleSheet(_SLIDER_STYLE)
        return slider

    def _slider_row(self, slider, value_lbl):
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        row.addWidget(slider, 1)
        value_lbl.setMinimumWidth(42)
        value_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        value_lbl.setStyleSheet("color: #1b6b39; font-size: 11px; font-weight: bold;")
        row.addWidget(value_lbl)
        return row

    def _build_cloud_section(self):
        frame, lay = self._section(_tr("CLOUD COVER (SCENE)"))
        lay.addWidget(self._explain(_tr(
            "Drop scenes whose tile-level cloud cover (CLOUDY_PIXEL_PERCENTAGE, "
            "from the image metadata) exceeds this limit. Lower values keep only "
            "clearer scenes. The per-pixel and AOI-local filtering is driven by "
            "the SCL classes below."
        )))

        lay.addWidget(QLabel(_tr("Max scene cloud %")))
        self.cloud_scene_slider = self._pct_slider(100)
        self.cloud_scene_value = QLabel("100%")
        lay.addLayout(self._slider_row(self.cloud_scene_slider, self.cloud_scene_value))
        self.cloud_scene_slider.valueChanged.connect(
            lambda v: (self.cloud_scene_value.setText(f"{v}%"), self._emit())
        )
        return frame

    def _build_coverage_section(self):
        frame, lay = self._section(_tr("VALID PIXELS, COVERAGE & DUPLICATES"))
        lay.addWidget(self._explain(_tr(
            "Drop a date when valid (unmasked) pixels cover less than this share "
            "of the AOI. Valid pixels are defined by the SCL mask chosen on the "
            "Inputs tab; this slider only re-thresholds the cached counts."
        )))
        lay.addWidget(QLabel(_tr("Min valid pixels in AOI %")))
        self.valid_pixel_slider = self._pct_slider(0)
        self.valid_pixel_value = QLabel("0%")
        lay.addLayout(self._slider_row(self.valid_pixel_slider, self.valid_pixel_value))
        self.valid_pixel_slider.valueChanged.connect(
            lambda v: (self.valid_pixel_value.setText(f"{v}%"), self._emit())
        )

        lay.addWidget(self._explain(_tr(
            "Require each scene's footprint to cover at least this share of the "
            "AOI."
        )))
        lay.addWidget(QLabel(_tr("Min AOI coverage %")))
        self.coverage_slider = self._pct_slider(0)
        self.coverage_value = QLabel("0%")
        lay.addLayout(self._slider_row(self.coverage_slider, self.coverage_value))
        self.coverage_slider.valueChanged.connect(
            lambda v: (self.coverage_value.setText(f"{v}%"), self._emit())
        )
        return frame

    # -- behavior ---------------------------------------------------------
    def _emit(self):
        if self._building:
            return
        self.filter_changed.emit(self.get_settings())

    def _on_cancel(self):
        if self._initial is not None:
            self.filter_changed.emit(dict(self._initial))
        self.reject()

    # -- settings I/O -----------------------------------------------------
    def get_settings(self):
        """Return the current filter configuration as a plain dict."""
        return {
            "cloud_scene_max": self.cloud_scene_slider.value(),
            "valid_pixel_min": self.valid_pixel_slider.value(),
            "coverage_min": self.coverage_slider.value(),
        }

    def set_settings(self, settings):
        """Apply a previously captured settings dict to the widgets."""
        self._building = True
        self.cloud_scene_slider.setValue(settings.get("cloud_scene_max", 100))
        self.valid_pixel_slider.setValue(settings.get("valid_pixel_min", 0))
        self.coverage_slider.setValue(settings.get("coverage_min", 0))
        self._building = False
