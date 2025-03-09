# -*- coding: utf-8 -*-
"""Earth Engine and Dash related utility functions."""

import urllib.request
import json
import importlib

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import QSettings

print("Importing Earth Engine and Dash API utility functions...")


# --- Earth Engine API (Original Code - DO NOT MODIFY) ---
def get_installed_version_ee():
    """Return the installed Earth Engine API version, or None if not installed."""
    try:
        import ee

        return ee.__version__
    except ImportError:
        return None


def get_latest_version_ee():
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
        if QSettings().value("locale/userLocale", "en")[:2] == "pt":
            QMessageBox.information(
                None,
                "Informação",
                "A API do Google Earth Engine foi instalada ou atualizada. Por favor, reinicie o QGIS para que o plugin RAVI funcione corretamente.",
            )
        else:
            QMessageBox.information(
                None,
                "Information",
                "The Earth Engine API has been installed or upgraded. Please restart QGIS for the RAVI plugin to function correctly.",
            )
    except AttributeError:
        # Fallback for newer pip versions that do not expose pip.main
        try:
            from pip._internal.cli.main import main as pip_main

            pip_main(["install", "--upgrade", "earthengine-api"])
            print(
                "Earth Engine API installed/upgraded successfully (using pip._internal)."
            )
            QApplication.restoreOverrideCursor()
            if QSettings().value("locale/userLocale", "en")[:2] == "pt":
                QMessageBox.information(
                    None,
                    "Informação",
                    "A API do Google Earth Engine foi instalada ou atualizada. Por favor, reinicie o QGIS para que o plugin RAVI funcione corretamente.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Information",
                    "The Earth Engine API has been installed or upgraded. Please restart QGIS for the RAVI plugin to function correctly.",
                )
        except Exception as e:
            print("An error occurred during installation:", e)
    except Exception as e:
        print("An error occurred during installation:", e)


def initialize_ee(project_id):
    """Authenticates and initializes Earth Engine."""
    try:
        import ee

        ee.Authenticate()
        ee.Initialize(project=project_id)
        print("Earth Engine initialized successfully.")
        return True
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
        return False

# DASH WILL BE NECESSARY FOR A FUTURE Version of RAVI
# # --- Dash (Added Code) ---
# def get_installed_version_dash():
#     """Return the installed Dash version, or None if not installed."""
#     try:
#         import dash

#         return dash.__version__
#     except ImportError:
#         return None


# def get_latest_version_dash():
#     """Query PyPI for the latest Dash version."""
#     try:
#         url = "https://pypi.org/pypi/dash/json"
#         with urllib.request.urlopen(url) as response:
#             data = json.load(response)
#         return data["info"]["version"]
#     except Exception as e:
#         print("Error fetching latest Dash version from PyPI:", e)
#         return None


# def install_dash():
#     """Install or upgrade Dash to the latest version using pip's internal API."""
#     try:
#         # Attempt to use pip.main (for older pip versions)
#         import pip

#         print("Using pip version:", pip.__version__)
#         pip_args = ["install", "--upgrade", "dash"]
#         pip.main(pip_args)
#         print("Dash installed/upgraded successfully (using pip.main).")
#         QApplication.restoreOverrideCursor()
#         if QSettings().value("locale/userLocale", "en")[:2] == "pt":
#             QMessageBox.information(
#                 None,
#                 "Informação",
#                 "A biblioteca Dash foi instalada ou atualizada. Por favor, reinicie o QGIS para que o plugin RAVI funcione corretamente.",
#             )
#         else:
#             QMessageBox.information(
#                 None,
#                 "Information",
#                 "The Dash library has been installed or upgraded. Please restart QGIS for the RAVI plugin to function correctly.",
#             )
#     except AttributeError:
#         # Fallback for newer pip versions that do not expose pip.main
#         try:
#             from pip._internal.cli.main import main as pip_main

#             pip_main(["install", "--upgrade", "dash"])
#             print("Dash installed/upgraded successfully (using pip._internal).")
#             QApplication.restoreOverrideCursor()
#             if QSettings().value("locale/userLocale", "en")[:2] == "pt":
#                 QMessageBox.information(
#                     None,
#                     "Informação",
#                     "A biblioteca Dash foi instalada ou atualizada. Por favor, reinicie o QGIS para que o plugin RAVI funcione corretamente.",
#                 )
#             else:
#                 QMessageBox.information(
#                     None,
#                     "Information",
#                     "The Dash library has been installed or upgraded. Please restart QGIS for the RAVI plugin to function correctly.",
#                 )
#         except Exception as e:
#             print("An error occurred during Dash installation:", e)
#     except Exception as e:
#         print("An error occurred during Dash installation:", e)


# # --- Main Execution ---

# # Earth Engine API (Original Code - DO NOT MODIFY)
# installed_version_ee = get_installed_version_ee()
# latest_version_ee = get_latest_version_ee()

# if installed_version_ee:
#     print("Installed Earth Engine API version:", installed_version_ee)
# else:
#     print("Earth Engine API is not installed.")

# if latest_version_ee:
#     print("Latest Earth Engine API version available on PyPI:", latest_version_ee)
# else:
#     print("Could not determine the latest Earth Engine API version from PyPI.")

# # If there's no installation or the installed version differs from the latest, install/upgrade.
# if (installed_version_ee is None) or (
#     latest_version_ee is not None and installed_version_ee != latest_version_ee
# ):
#     print("Upgrading/Installing Earth Engine API to the latest version...")
#     install_earthengine_api()
#     # Invalidate caches so that the newly installed package is found.
#     importlib.invalidate_caches()
# else:
#     print("Latest version is already installed. Importing Earth Engine API...")

# # Dash (Added Code)
# installed_version_dash = get_installed_version_dash()
# latest_version_dash = get_latest_version_dash()

# if installed_version_dash:
#     print("Installed Dash version:", installed_version_dash)
# else:
#     print("Dash is not installed.")

# if latest_version_dash:
#     print("Latest Dash version available on PyPI:", latest_version_dash)
# else:
#     print("Could not determine the latest Dash version from PyPI.")

# # If there's no installation or the installed version differs from the latest, install/upgrade.
# if (installed_version_dash is None) or (
#     latest_version_dash is not None and installed_version_dash != latest_version_dash
# ):
#     print("Upgrading/Installing Dash to the latest version...")
#     install_dash()
#     # Invalidate caches so that the newly installed package is found.
#     importlib.invalidate_caches()
# else:
#     print("Latest Dash version is already installed.")

# # Import and print versions (if installed)
# try:
#     import ee

#     print("Final Earth Engine API version:", ee.__version__)
# except ImportError:
#     print("Earth Engine API could not be imported after installation.")

# try:
#     import dash

#     print("Final Dash version:", dash.__version__)
# except ImportError:
#     print("Dash could not be imported after installation.")
