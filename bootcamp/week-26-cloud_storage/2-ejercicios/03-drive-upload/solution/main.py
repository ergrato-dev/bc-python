"""
Ejercicio 03: Google Drive API — Upload y Permisos — SOLUCIÓN
=============================================================

Requisitos:
    pip install google-api-python-client google-auth
    Colocar credentials.json (Service Account) en el directorio de trabajo.
"""
from __future__ import annotations

import mimetypes
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service(credentials_path: str = "credentials.json"):
    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def get_or_create_folder(service, name: str, parent_id: str | None = None) -> str:
    query = (
        f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    )
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    if files:
        return str(files[0]["id"])

    metadata: dict[str, object] = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    folder = service.files().create(body=metadata, fields="id").execute()
    return str(folder["id"])


def upload_file(
    service,
    local_path: Path,
    folder_id: str,
    description: str = "",
) -> dict[str, str]:
    mime_type, _ = mimetypes.guess_type(str(local_path))
    mime_type = mime_type or "application/octet-stream"

    metadata: dict[str, object] = {
        "name": local_path.name,
        "parents": [folder_id],
        "description": description,
    }
    media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)
    file = (
        service.files()
        .create(body=metadata, media_body=media, fields="id,name,webViewLink")
        .execute()
    )
    return {
        "id": str(file.get("id", "")),
        "name": str(file.get("name", "")),
        "webViewLink": str(file.get("webViewLink", "")),
    }


def share_with_reader(service, file_id: str, email: str) -> None:
    service.permissions().create(
        fileId=file_id,
        body={"type": "user", "role": "reader", "emailAddress": email},
        sendNotificationEmail=True,
    ).execute()


def share_with_link(service, file_id: str) -> str:
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
    ).execute()
    file = service.files().get(fileId=file_id, fields="webViewLink").execute()
    return str(file["webViewLink"])


# ── Ejercicio ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    service = get_drive_service()

    print("1. Creando estructura de carpetas...")
    studio_id = get_or_create_folder(service, "Studio BC Test")
    proyecto_id = get_or_create_folder(service, "spot-verano-2024", parent_id=studio_id)
    entrega_id = get_or_create_folder(service, "Entregables", parent_id=proyecto_id)
    print(f"   Carpeta entregables: {entrega_id}")

    print("2. Subiendo archivo de prueba...")
    test_file = Path("entregable_v1.mp4")
    test_file.write_bytes(b"fake video content for testing")

    result = upload_file(service, test_file, entrega_id, description="Entrega final spot verano")
    print(f"   Subido: {result['name']} → {result.get('webViewLink', 'N/A')[:60]}")

    print("3. Generando link público de solo lectura...")
    link = share_with_link(service, result["id"])
    print(f"   Link: {link[:70]}...")

    test_file.unlink(missing_ok=True)
    print("OK — Ejercicio 03 completado")
