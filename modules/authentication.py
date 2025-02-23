# ravi_plugin/modules/authentication.py
import os
import platform
import shutil
import re
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMessageBox, QApplication
import ee
from PyQt5.QtCore import Qt


def loadProjectId(dialog):
    """Loads the saved project ID from QSettings and sets it in the widget."""
    """Carrega o ID do projeto salvo de QSettings e o define no widget."""
    settings = QSettings()
    saved_project_id = settings.value("MyPlugin/projectID", "", type=str)
    dialog.project_QgsPasswordLineEdit.setText(saved_project_id)
    print("Loaded project ID:", saved_project_id)
    dialog.autenticacao.setEnabled(bool(dialog.project_QgsPasswordLineEdit.text()))


def autoSaveProjectId(dialog, new_text):
    """Automatically saves the project ID to QSettings whenever the text changes."""
    settings = QSettings()
    settings.setValue("MyPlugin/projectID", new_text)
    print("Project ID auto-saved:", new_text)
    dialog.autenticacao.setEnabled(bool(dialog.project_QgsPasswordLineEdit.text()))


def auth(dialog):
    """
    Authenticates Earth Engine and validates the default project. Warnings
    are displayed only if the default project is invalid.
    """
    """
    Autentica o Earth Engine e valida o projeto padrão. Avisos são
    exibidos apenas se o projeto padrão for inválido.
    """
    try:
        # Step 1: Authenticate and initialize Earth Engine / Passo 1:
        # Autentica e inicializa o Earth Engine
        print("Authenticating Earth Engine...")
        ee.Authenticate()
        project_id = re.sub(
            r"[^a-zA-Z0-9_-]", "", dialog.project_QgsPasswordLineEdit.text()
        )
        ee.Initialize(project=project_id)
        print("Authentication successful!")

        # Step 2: Test default project / Passo 2: Testa o projeto padrão
        print("Testing default project...")
        default_project_path = (
            f"projects/{project_id}/assets/"  # Replace with your default project's path if known
        )

        # Attempt to list assets in the default project / Tenta listar os
        # ativos no projeto padrão
        try:
            assets = ee.data.listAssets({"parent": default_project_path})
            print(f"Assets in default project: {assets}")

            if assets.get("assets") is not None:  # Valid project detected
                print("Default project is valid.")
                dialog.pop_aviso("Authentication successful!")
                dialog.autentication = True
                dialog.next_clicked()
            else:
                print(
                    "Default project is valid but contains no assets."
                )  # No warning needed for this case
        except ee.EEException as e:
            # Invalid project or access issue / Projeto inválido ou problema
            # de acesso
            print(f"Default project validation failed: {e}")
            dialog.pop_aviso_auth(
                f"Default project validation failed: {e}\nFollow the instructions to have a valid Google Cloud project."
            )
            auth_clear(dialog, True)

    except ee.EEException as e:
        # Handle Earth Engine-specific errors / Lida com erros
        # específicos do Earth Engine
        print(f"Earth Engine error: {e}")
        if "Earth Engine client library not initialized" in str(e):
            message = "Authentication failed. Please authenticate again."
            print(message)
            dialog.pop_aviso_auth(message)
        else:
            message = (
                f"An error occurred during authentication or initialization: {e}"
            )
            print(message)
            dialog.pop_aviso_auth(message)
            auth_clear(dialog, True)

    except Exception as e:
        # Handle unexpected errors / Lida com erros inesperados
        message = f"An unexpected error occurred: {e}"
        print(message)
        dialog.pop_aviso_auth(message)


def auth_clear(dialog, silent=False):
    """
    Completely clears Earth Engine authentication by deleting the entire
    Earth Engine configuration directory, including credentials and cached
    data.
    """
    """
    Limpa completamente a autenticação do Earth Engine, excluindo todo o
    diretório de configuração do Earth Engine, incluindo credenciais e
    dados em cache.
    """
    dialog.project_QgsPasswordLineEdit.clear()
    dialog.autenticacao.setEnabled(False)
    dialog.autentication = False

    system = platform.system()

    # Determine the Earth Engine configuration directory based on OS. /
    # Determina o diretório de configuração do Earth Engine com base no SO.
    if system == "Windows":
        config_dir = os.path.join(
            os.environ["USERPROFILE"], ".config", "earthengine"
        )
    elif system in ["Linux", "Darwin"]:  # Linux or MacOS (Darwin)
        config_dir = os.path.join(os.environ["HOME"], ".config", "earthengine")
    else:
        raise Exception(f"Unsupported operating system: {system}")

    # Check if the configuration directory exists and delete it. / Verifica
    # se o diretório de configuração existe e o exclui.
    if os.path.exists(config_dir):
        try:
            shutil.rmtree(config_dir)
            if not silent:
                message = "Earth Engine configuration cleared successfully (all files deleted)."
                print(message)
                dialog.pop_aviso_auth(message)
        except Exception as e:
            message = f"Error clearing Earth Engine configuration: {e}"
            print(message)
            dialog.pop_aviso_auth(message)
    else:
        message = "No Earth Engine configuration found to clear."
        print(message)
        dialog.pop_aviso_auth(message)