# -*- coding: utf-8 -*-
"""
Authentication page for the RAVI dialog.

Builds the first workflow page: Google Earth Engine project configuration
and authentication controls. Signal connections are wired externally by
``ravi.py``.
"""

import os

from qgis.PyQt.QtCore import Qt, QCoreApplication
from qgis.PyQt.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qgis.gui import QgsPasswordLineEdit

from .styles import STYLE_BTN_PRIMARY, STYLE_BTN_SECONDARY


def _tr(text):
    return QCoreApplication.translate("RAVI", text)


def setup_auth_page(dialog, page):
    """
    Populate the authentication page.

    The layout is a two-column row centred vertically on the page:

    - **Left column** (220 px fixed): plugin icon + caption, title label,
      plain-text description, and an info box explaining GEE prerequisites.
    - **Right card** (260 px fixed, white rounded card): a ``project_id_input``
      field for the Google Cloud project ID, a ``btn_authenticate`` primary
      action button, and a ``btn_reset_auth`` discrete reset link.
    All interactive widgets are exposed on ``dialog`` so ``ravi.py`` can wire
    signal connections without importing this module's internals.
    """
    page.setStyleSheet("background-color: #f5f5f5;")

    outer = QVBoxLayout(page)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)
    outer.addStretch(2)

    row = QHBoxLayout()
    row.setContentsMargins(28, 0, 28, 0)
    row.setSpacing(34)

    left = QWidget()
    left.setFixedWidth(230)
    left.setStyleSheet("background: transparent;")
    left_lay = QVBoxLayout(left)
    left_lay.setContentsMargins(0, 0, 0, 0)
    left_lay.setSpacing(8)

    left_lay.addStretch(1)

    title_lbl = QLabel(_tr("GEE Authentication"))
    title_lbl.setStyleSheet("color: #1a1a1a; font-size: 18px; font-weight: bold;")
    left_lay.addWidget(title_lbl)

    desc_lbl = QLabel(
        _tr(
            "RAVI uses <b>Google Earth Engine</b> for processing. "
            "To continue, you will need authorized access."
        )
    )
    desc_lbl.setWordWrap(True)
    desc_lbl.setTextFormat(Qt.TextFormat.RichText)
    desc_lbl.setStyleSheet("color: #616161; font-size: 13px;")
    left_lay.addWidget(desc_lbl)

    info_frame = QFrame()
    info_frame.setStyleSheet("""
        QFrame {
            background-color: #e8f5e9;
            border-left: 3px solid #43a047;
            border-radius: 4px;
        }
        QLabel { background: transparent; border: none; }
    """)
    info_lay = QHBoxLayout(info_frame)
    info_lay.setContentsMargins(12, 10, 12, 10)
    info_lay.setSpacing(8)

    info_icon = QLabel("ⓘ")
    info_icon.setFixedWidth(18)
    info_icon.setAlignment(Qt.AlignmentFlag.AlignTop)
    info_icon.setStyleSheet("color: #2e7d32; font-size: 14px; font-weight: bold;")
    info_lay.addWidget(info_icon)

    info_text = QLabel(
        _tr(
            "Requires an active GEE account and a Google Cloud Console project "
            "with the API enabled."
        )
    )
    info_text.setWordWrap(True)
    info_text.setStyleSheet("color: #1b5e20; font-size: 12px;")
    info_lay.addWidget(info_text, 1)

    left_lay.addWidget(info_frame)
    left_lay.addStretch(1)
    row.addStretch(1)
    row.addWidget(left)

    card = QFrame()
    card.setFixedWidth(258)
    card.setFixedHeight(250)
    card.setStyleSheet("""
        QFrame {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
        }
        QLabel { background: transparent; border: none; }
    """)
    card_lay = QVBoxLayout(card)
    card_lay.setContentsMargins(20, 18, 20, 14)
    card_lay.setSpacing(7)

    dialog.auth_status_badge = QPushButton(_tr("Checking sign-in status…"))
    dialog.auth_status_badge.setCursor(Qt.CursorShape.PointingHandCursor)
    dialog.auth_status_badge.setToolTip(
        _tr("Click to re-check your Earth Engine sign-in status")
    )
    dialog.auth_status_badge.setFixedHeight(22)
    dialog.auth_status_badge.setStyleSheet(
        """
        QPushButton {
            background-color: transparent;
            color: #757575;
            border: none;
            font-size: 11px;
            font-weight: bold;
            padding: 0 10px;
            text-align: center;
        }
        """
    )
    card_lay.addWidget(dialog.auth_status_badge)
    card_lay.addSpacing(4)

    pid_lbl = QLabel(_tr("PROJECT ID (GOOGLE CLOUD)"))
    pid_lbl.setStyleSheet(
        "color: #9e9e9e; font-size: 11px; letter-spacing: 1px; font-weight: bold;"
    )
    card_lay.addWidget(pid_lbl)
    card_lay.addSpacing(18)

    dialog.project_id_input = QgsPasswordLineEdit()
    dialog.project_id_input.setEchoMode(QLineEdit.EchoMode.Normal)
    dialog.project_id_input.setPlaceholderText(_tr("e.g. my-geospatial-project-42"))
    dialog.project_id_input.setFixedHeight(28)
    dialog.project_id_input.setStyleSheet("""
        QLineEdit {
            background-color: transparent;
            color: #212121;
            border: none;
            border-bottom: 1.5px solid #d0d0d0;
            border-radius: 0;
            padding: 2px 0 6px 0;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-bottom: 2px solid #1b6b39;
        }
    """)
    card_lay.addWidget(dialog.project_id_input)

    card_lay.addSpacing(3)

    dialog.btn_authenticate = QPushButton(_tr("🔑   Validate ID"))
    dialog.btn_authenticate.setFixedHeight(34)
    dialog.btn_authenticate.setStyleSheet(STYLE_BTN_PRIMARY)
    card_lay.addWidget(dialog.btn_authenticate)

    card_lay.addSpacing(2)

    dialog.btn_reset_auth = QPushButton(_tr("Reset authentication"))
    dialog.btn_reset_auth.setFixedHeight(20)
    dialog.btn_reset_auth.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: #bdbdbd;
            border: none;
            font-size: 10px;
        }
        QPushButton:hover { color: #c62828; }
    """)
    card_lay.addWidget(dialog.btn_reset_auth, 0, Qt.AlignmentFlag.AlignHCenter)
    card_lay.addStretch(1)

    row.addWidget(card)
    row.addStretch(1)
    outer.addLayout(row)

    outer.addSpacing(6)
    dialog.auth_status_lbl = QLabel("")
    dialog.auth_status_lbl.setWordWrap(True)
    dialog.auth_status_lbl.setTextFormat(Qt.TextFormat.RichText)
    dialog.auth_status_lbl.setOpenExternalLinks(True)
    dialog.auth_status_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    dialog.auth_status_lbl.setStyleSheet("color: #616161; font-size: 11px;")
    dialog.auth_status_lbl.hide()
    outer.addWidget(dialog.auth_status_lbl)

    dialog.btn_go_to_aoi = QPushButton(page)
    dialog.btn_go_to_aoi.hide()
    dialog.btn_go_to_aoi.clicked.connect(dialog.show_dem_page)

    outer.addStretch(2)

    folder_frame = QFrame()
    folder_frame.setFixedWidth(560)
    folder_frame.setStyleSheet("""
        QFrame {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        QLabel { background: transparent; border: none; }
    """)
    folder_lay = QHBoxLayout(folder_frame)
    folder_lay.setContentsMargins(14, 8, 10, 8)
    folder_lay.setSpacing(8)

    folder_lbl = QLabel(_tr("Download folder"))
    folder_lbl.setStyleSheet("color: #616161; font-size: 11px; font-weight: bold;")
    folder_lay.addWidget(folder_lbl)

    dialog.folder_input = QLineEdit()
    dialog.folder_input.setReadOnly(True)
    dialog.folder_input.setPlaceholderText(_tr("System temp (default)"))
    dialog.folder_input.setFixedHeight(28)
    dialog.folder_input.setStyleSheet("""
        QLineEdit {
            background-color: #f5f5f5;
            color: #424242;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 12px;
        }
    """)
    folder_lay.addWidget(dialog.folder_input, 1)

    dialog.btn_clear_folder = QPushButton("✕")
    dialog.btn_clear_folder.setFixedSize(28, 28)
    dialog.btn_clear_folder.setToolTip(_tr("Clear download folder"))
    dialog.btn_clear_folder.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: #bdbdbd;
            border: none;
            border-radius: 4px;
            font-size: 13px;
        }
        QPushButton:hover:enabled {
            color: #c62828;
            background-color: #fdecea;
        }
        QPushButton:disabled { color: #eeeeee; }
    """)
    folder_lay.addWidget(dialog.btn_clear_folder)

    dialog.btn_browse_folder = QPushButton(_tr("Browse"))
    dialog.btn_browse_folder.setFixedHeight(28)
    dialog.btn_browse_folder.setStyleSheet(STYLE_BTN_SECONDARY)
    folder_lay.addWidget(dialog.btn_browse_folder)

    def _sync_clear_enabled(text):
        dialog.btn_clear_folder.setEnabled(bool(text))

    dialog.folder_input.textChanged.connect(_sync_clear_enabled)
    _sync_clear_enabled(dialog.folder_input.text())

    folder_outer_row = QHBoxLayout()
    folder_outer_row.setContentsMargins(0, 0, 0, 0)
    folder_outer_row.addStretch(1)
    folder_outer_row.addWidget(folder_frame)
    folder_outer_row.addStretch(1)
    outer.addLayout(folder_outer_row)

    outer.addSpacing(16)
