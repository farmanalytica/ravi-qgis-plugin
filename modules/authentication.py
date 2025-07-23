# ravi_plugin/modules/authentication.py
import os
import platform
import shutil
import re
from qgis.PyQt.QtCore import QSettings, Qt
from qgis.PyQt.QtWidgets import QMessageBox, QApplication
import ee


def loadProjectId(self):
    """Loads the saved project ID from QSettings and sets it in the widget."""
    """Carrega o ID do projeto salvo de QSettings e o define no widget."""
    settings = QSettings()
    saved_project_id = settings.value("MyPlugin/projectID", "", type=str)
    self.project_QgsPasswordLineEdit.setText(saved_project_id)
    print("Loaded project ID:", saved_project_id)
    self.autenticacao.setEnabled(bool(self.project_QgsPasswordLineEdit.text()))


def autoSaveProjectId(self, new_text):
    """Automatically saves the project ID to QSettings whenever the text changes."""
    settings = QSettings()
    settings.setValue("MyPlugin/projectID", new_text)
    print("Project ID auto-saved:", new_text)
    self.autenticacao.setEnabled(bool(self.project_QgsPasswordLineEdit.text()))


def auth(self):
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
            r"[^a-zA-Z0-9_-]", "", self.project_QgsPasswordLineEdit.text()
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
                if self.language == "pt":
                    self.pop_warning("Autenticação bem-sucedida!")
                else:  
                    self.pop_warning("Authentication successful!")
                self.autentication = True
                self.next_clicked()
            else:
                print(
                    "Default project is valid but contains no assets."
                )  # No warning needed for this case
        except ee.EEException as e:
            # Invalid project or access issue / Projeto inválido ou problema
            # de acesso
            print(f"Default project validation failed: {e}")
            self.pop_warning(
                f"Default project validation failed: {e}\nFollow the instructions to have a valid Google Cloud project."
            )
            auth_clear(self, True)

    except ee.EEException as e:
        # Handle Earth Engine-specific errors / Lida com erros
        # específicos do Earth Engine
        print(f"Earth Engine error: {e}")
        if "Earth Engine client library not initialized" in str(e):
            message = "Authentication failed. Please authenticate again."
            print(message)
            self.pop_warning(message)
        else:
            message = (
                f"An error occurred during authentication or initialization: {e}"
            )
            print(message)
            self.pop_warning(message)
            auth_clear(self, True)

    except Exception as e:
        # Handle unexpected errors / Lida com erros inesperados
        message = f"An unexpected error occurred: {e}"
        print(message)
        self.pop_warning(message)


def auth_clear(self, silent=False):
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
    self.project_QgsPasswordLineEdit.clear()
    self.autenticacao.setEnabled(False)
    self.autentication = False

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
                self.pop_warning(message)
        except Exception as e:
            message = f"Error clearing Earth Engine configuration: {e}"
            print(message)
            self.pop_warning(message)
    else:
        message = "No Earth Engine configuration found to clear."
        print(message)
        self.pop_warning(message)