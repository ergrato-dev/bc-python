from __future__ import annotations

import mimetypes
from pathlib import Path


class DriveUploader:
    """Sube archivos a Google Drive usando Service Account."""

    def __init__(self, credentials_path: Path, root_folder: str = "Studio BC") -> None:
        self._root_folder = root_folder
        self._service = self._build_service(credentials_path)

    def _build_service(self, credentials_path: Path):  # type: ignore[return]
        """Crea el servicio autenticado de Drive v3."""
        # TODO: Credentials.from_service_account_file + build("drive", "v3", ...)
        raise NotImplementedError

    def get_or_create_folder(self, name: str, parent_id: str | None = None) -> str:
        """Devuelve el ID de la carpeta, creándola si no existe."""
        # TODO: files().list(q=...) → si no existe → files().create(mimeType=folder)
        raise NotImplementedError

    def upload_file(
        self,
        local_path: Path,
        folder_id: str,
        description: str = "",
    ) -> dict[str, str]:
        """Sube el archivo a la carpeta. Devuelve {id, name, webViewLink}."""
        # TODO: MediaFileUpload(resumable=True) + files().create(fields="id,name,webViewLink")
        raise NotImplementedError

    def share_with_reader(self, file_id: str, email: str) -> None:
        """Comparte el archivo con el email como lector."""
        # TODO: permissions().create(type="user", role="reader", emailAddress=email)
        raise NotImplementedError

    def ensure_project_structure(self, client: str, project: str) -> dict[str, str]:
        """
        Crea la estructura Studio BC/{client}/{project}/Entregables/ en Drive.
        Devuelve {root_id, client_id, project_id, delivery_id}.
        """
        root_id = self.get_or_create_folder(self._root_folder)
        client_id = self.get_or_create_folder(client, parent_id=root_id)
        project_id = self.get_or_create_folder(project, parent_id=client_id)
        delivery_id = self.get_or_create_folder("Entregables", parent_id=project_id)
        return {
            "root_id": root_id,
            "client_id": client_id,
            "project_id": project_id,
            "delivery_id": delivery_id,
        }
