# -*- coding: utf-8 -*-
"""File system related utility functions."""

import os
import platform
import subprocess
import shutil
import tempfile
import zipfile

def get_system_downloads_path():
    """Returns the default downloads path for the current operating system."""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    elif system == "Linux":
        return os.path.join(os.environ["HOME"], "Downloads")
    elif system == "Darwin":  # MacOS
        return os.path.join(os.environ["HOME"], "Downloads")
    else:
        return None

def open_file_explorer(path):
    """Opens the file explorer at the specified path."""
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", path])
    else:  # Linux and other Unix-like systems
        subprocess.call(["xdg-open", path])

def get_unique_filename(output_folder, base_file_name):
    """Generates a unique filename in the specified output folder."""
    name, extension = os.path.splitext(base_file_name)
    output_file = os.path.join(output_folder, base_file_name)
    counter = 1

    while os.path.exists(output_file):
        output_file = os.path.join(
            output_folder, f"{name}_{counter}{extension}"
        )
        counter += 1

    print(f"Unique filename: {output_file}")
    return output_file

def clear_earth_engine_config():
    """
    Completely clears Earth Engine authentication by deleting the entire
    Earth Engine configuration directory, including credentials and cached data.
    """
    system = platform.system()

    # Determine the Earth Engine configuration directory based on OS.
    if system == "Windows":
        config_dir = os.path.join(
            os.environ["USERPROFILE"], ".config", "earthengine"
        )
    elif system in ["Linux", "Darwin"]:  # Linux or MacOS (Darwin)
        config_dir = os.path.join(os.environ["HOME"], ".config", "earthengine")
    else:
        raise Exception(f"Unsupported operating system: {system}")

    # Check if the configuration directory exists and delete it.
    if os.path.exists(config_dir):
        try:
            shutil.rmtree(config_dir)
            return True
        except Exception as e:
            print(f"Error clearing Earth Engine configuration: {e}")
            return False
    else:
        print("No Earth Engine configuration found to clear.")
        return False
