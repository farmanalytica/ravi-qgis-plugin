# -*- coding: utf-8 -*-
"""
GEE (Google Earth Engine) service layer.

All Earth Engine business logic lives here, keeping the UI layer free
of SDK-specific details.
"""

import os
import time

import ee
from qgis.PyQt.QtCore import QCoreApplication, QSettings


def _tr(text):
    return QCoreApplication.translate("RAVI", text)


class AuthCancelled(Exception):
    """Raised when the user aborts the OAuth flow before it completes."""


class AuthTimeout(Exception):
    """Raised when the browser sign-in is not completed within the deadline."""


class GEEService:
    """
    Service layer for Google Earth Engine operations.

    Handles authentication, initialization, and credential management
    for the Google Earth Engine API.
    """

    SETTINGS_PROJECT_ID_KEY = "MyPlugin/projectID"

    def __init__(self):
        self.is_authenticated = False

    def has_stored_credentials(self) -> bool:

        try:
            return os.path.exists(ee.oauth.get_credentials_path())
        except Exception:
            return False

    def check_silent_auth(self, project_id: str) -> bool:
        """Check authentication without ever launching the browser OAuth flow"""

        if not project_id or not self.has_stored_credentials():
            self.is_authenticated = False
            return False

        try:
            ee.Initialize(project=project_id)
            ee.data.listAssets({"parent": f"projects/{project_id}/assets/"})
            self.is_authenticated = True
            return True
        except Exception:
            self.is_authenticated = False
            return False

    def get_saved_project_id(self) -> str:
        return QSettings().value(self.SETTINGS_PROJECT_ID_KEY, "", type=str)

    def save_project_id(self, project_id) -> None:
        QSettings().setValue(self.SETTINGS_PROJECT_ID_KEY, project_id)

    def authenticate(
        self,
        project_id: str,
        timeout: float = 180,
        should_cancel=None,
        on_browser_open=None,
    ):

        should_cancel = should_cancel or (lambda: False)
        try:
            try:
                ee.Initialize(project=project_id)

            except ee.EEException:
                self._run_local_auth_flow(timeout, should_cancel, on_browser_open)
                ee.Initialize(project=project_id)

            default_project_path = f"projects/{project_id}/assets/"

            ee.data.listAssets({"parent": default_project_path})
            self.is_authenticated = True

        except (AuthCancelled, AuthTimeout):
            raise

        except ee.EEException as e:
            error_msg = str(e)

            if "Earth Engine client library not initialized" in error_msg:
                raise Exception("Authentication failed. Please authenticate again.")
            else:
                raise Exception(
                    f"An error occurred during authentication or initialization: {error_msg}"
                )

        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def _run_local_auth_flow(self, timeout, should_cancel, on_browser_open):
        """Run the GEE localhost OAuth flow with a bounded, cancellable wait"""
        from ee import oauth

        flow = oauth.Flow("localhost", oauth.SCOPES)
        local_server = flow.server.server
        try:
            oauth._open_new_browser(flow.auth_url)
            if on_browser_open:
                on_browser_open(flow.auth_url)

            local_server.timeout = 1.0
            request_handler = local_server.RequestHandlerClass
            deadline = time.monotonic() + timeout
            auth_code = None
            while not auth_code:
                if should_cancel():
                    raise AuthCancelled()
                if time.monotonic() > deadline:
                    raise AuthTimeout()
                local_server.handle_request()
                auth_code = getattr(request_handler, "code", None)
        finally:
            try:
                local_server.server_close()
            except Exception:
                pass

        oauth._obtain_and_write_token(
            auth_code, flow.code_verifier, flow.scopes, flow.server.url
        )

    def reset_authentication(self):

        credentials_path = ee.oauth.get_credentials_path()

        if not os.path.exists(credentials_path):
            raise FileNotFoundError(
                _tr("No Earth Engine configuration found to clear.")
            )

        os.remove(credentials_path)

        try:
            import importlib

            importlib.reload(ee.oauth)
            ee.Reset()
        except Exception:
            pass

        self.is_authenticated = False
        return _tr("Earth Engine configuration cleared successfully.")
