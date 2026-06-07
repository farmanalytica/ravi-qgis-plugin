# -*- coding: utf-8 -*-
import importlib
import os
import sys
import zipfile
import urllib.request

from qgis.PyQt.QtCore import QThread, pyqtSignal

EXTLIBS_URL = "https://github.com/farmanalytica/ravi-qgis-plugin/raw/main/extlibs.zip"
_PLUGIN_DIR = os.path.dirname(__file__)
EXTLIBS_PATH = os.path.join(_PLUGIN_DIR, "extlibs")
_SENTINEL = os.path.join(EXTLIBS_PATH, ".ready")

_downloader = None


def is_ready():
    return os.path.isfile(_SENTINEL)


def ensure_on_path():
    if EXTLIBS_PATH not in sys.path:
        sys.path.insert(0, EXTLIBS_PATH)
    importlib.invalidate_caches()


def get_downloader():
    return _downloader


def start_download():
    global _downloader
    if _downloader is not None and _downloader.isRunning():
        return _downloader
    _downloader = ExtlibsDownloader()
    _downloader.start()
    return _downloader


class ExtlibsDownloader(QThread):
    download_done = pyqtSignal(bool, str)

    def run(self):
        zip_path = os.path.join(_PLUGIN_DIR, "extlibs.zip")
        try:
            if not EXTLIBS_URL.startswith("https://"):
                raise ValueError(f"Unexpected URL scheme: {EXTLIBS_URL}")
            with urllib.request.urlopen(EXTLIBS_URL) as resp, open(zip_path, "wb") as f:  # nosec B310
                f.write(resp.read())
            with zipfile.ZipFile(zip_path, "r") as zf:
                names = zf.namelist()
                if names and names[0].startswith("extlibs/"):
                    zf.extractall(_PLUGIN_DIR)
                else:
                    os.makedirs(EXTLIBS_PATH, exist_ok=True)
                    zf.extractall(EXTLIBS_PATH)
            open(_SENTINEL, "w").close()
            ensure_on_path()
            self.download_done.emit(True, "")
        except Exception as e:
            self.download_done.emit(False, str(e))
        finally:
            if os.path.exists(zip_path):
                try:
                    os.remove(zip_path)
                except OSError:
                    pass
