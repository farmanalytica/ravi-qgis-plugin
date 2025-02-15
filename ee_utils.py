# ee_utils.py
import importlib
import urllib.request, json

def get_installed_version():
    """Return the installed Earth Engine API version or None."""
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
        print("Error fetching latest version:", e)
        return None

def install_earthengine_api():
    """Install or upgrade the Earth Engine API using pip."""
    try:
        import pip
        pip_args = ['install', '--upgrade', 'earthengine-api']
        pip.main(pip_args)
        print("Earth Engine API installed/upgraded successfully (using pip.main).")
    except AttributeError:
        try:
            from pip._internal.cli.main import main as pip_main
            pip_main(['install', '--upgrade', 'earthengine-api'])
            print("Earth Engine API installed/upgraded successfully (using pip._internal).")
        except Exception as e:
            print("An error occurred during installation:", e)
    except Exception as e:
        print("An error occurred during installation:", e)

def ensure_ee_import():
    """Ensure that the Earth Engine API can be imported; install it if needed."""
    try:
        importlib.import_module('ee')
        import ee
        print("Earth Engine API is already installed.")
        return ee
    except ImportError:
        print("Earth Engine API not found. Installing...")
        install_earthengine_api()
        try:
            importlib.import_module('ee')
            import ee
            print("Earth Engine API imported successfully.")
            return ee
        except ImportError:
            print("Earth Engine API could not be imported after installation.")
            return None