# -*- coding: utf-8 -*-
"""Earth Engine related utility functions."""

import urllib.request
import json
import importlib

from PyQt5.QtWidgets import (
    QMessageBox,
    QApplication
)

print("Importing Earth Engine API utility functions...")
# Define utility functions for Earth Engine API installation and initialization.

def get_installed_version():
    """Return the installed Earth Engine API version, or None if not installed."""
    try:
        import ee

        return ee.__version__
    except ImportError:
        return None

def get_latest_version():
    """Query PyPI for the latest Earth Engine API version."""
    try:
        url = "https://pypi.org/pypi/earthengine-api/json"
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
        return data["info"]["version"]
    except Exception as e:
        print("Error fetching latest version from PyPI:", e)
        return None

def install_earthengine_api():
    """Install or upgrade the Earth Engine API to the latest version using pip's internal API."""
    try:
        # Attempt to use pip.main (for older pip versions)
        import pip

        print("Using pip version:", pip.__version__)
        pip_args = ["install", "--upgrade", "earthengine-api"]
        pip.main(pip_args)
        print("Earth Engine API installed/upgraded successfully (using pip.main).")
        QApplication.restoreOverrideCursor()
        QMessageBox.information(None, "Information", 
                                "The Earth Engine API has been installed or upgraded. Please restart QGIS for the RAVI plugin to function correctly.")
    except AttributeError:
        # Fallback for newer pip versions that do not expose pip.main
        try:
            from pip._internal.cli.main import main as pip_main

            pip_main(["install", "--upgrade", "earthengine-api"])
            print(
                "Earth Engine API installed/upgraded successfully (using pip._internal)."
            )
            QApplication.restoreOverrideCursor()
            QMessageBox.information(None, "Information", 
                                    "The Earth Engine API has been installed or upgraded. Please restart QGIS for the RAVI plugin to function correctly.")
        except Exception as e:
            print("An error occurred during installation:", e)
    except Exception as e:
        print("An error occurred during installation:", e)

def initialize_ee(project_id):
    """Authenticates and initializes Earth Engine."""
    try:
        ee.Authenticate()
        ee.Initialize(project=project_id)
        print("Earth Engine initialized successfully.")
        return True
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
        return False

# Determine installed and latest versions.
installed_version = get_installed_version()
latest_version = get_latest_version()

if installed_version:
    print("Installed Earth Engine API version:", installed_version)
else:
    print("Earth Engine API is not installed.")

if latest_version:
    print("Latest Earth Engine API version available on PyPI:", latest_version)
else:
    print("Could not determine the latest Earth Engine API version from PyPI.")

# If there's no installation or the installed version differs from the latest, install/upgrade.
if (installed_version is None) or (
    latest_version is not None and installed_version != latest_version
):
    print("Upgrading/Installing Earth Engine API to the latest version...")
    install_earthengine_api()
    # Invalidate caches so that the newly installed package is found.
    importlib.invalidate_caches()
else:
    print("Latest version is already installed. Importing Earth Engine API...")

# Import the Earth Engine API and print its version.
try:
    importlib.import_module("ee")
    import ee

    print("Final Earth Engine API version:", ee.__version__)
except ImportError:
    print("Earth Engine API could not be imported after installation.")
