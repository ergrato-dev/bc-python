# Google Drive API

## 1. Autenticación — Service Account

Un **Service Account** es una cuenta de servicio (no humano) con su propio JSON de credenciales. Es la forma recomendada para scripts automatizados.

### Pasos de configuración

1. Ir a [Google Cloud Console](https://console.cloud.google.com/) → IAM & Admin → Service Accounts
2. Crear Service Account → Generar key JSON → Descargar `credentials.json`
3. Habilitar Google Drive API en el proyecto
4. Compartir la carpeta Drive con el email del Service Account (`xxx@proyecto.iam.gserviceaccount.com`)

### Inicializar el cliente

```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_drive_service(credentials_path: str = "credentials.json"):
    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)
```

---

## 2. Carpetas — Crear y Navegar

```python
def get_or_create_folder(service, name: str, parent_id: str | None = None) -> str:
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    if files:
        return files[0]["id"]

    metadata: dict[str, object] = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]
```

`get_or_create_folder` es idempotente: si la carpeta ya existe la reutiliza.

---

## 3. Subir Archivos

```python
from pathlib import Path
import mimetypes

def upload_file(
    service,
    local_path: Path,
    folder_id: str,
    description: str = "",
) -> str:
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
        .create(body=metadata, media_body=media, fields="id, name, webViewLink")
        .execute()
    )
    return file["id"]
```

`resumable=True` activa el upload en chunks — esencial para videos grandes.

---

## 4. Descargar Archivos

```python
import io
from googleapiclient.http import MediaIoBaseDownload

def download_file(service, file_id: str, dest: Path) -> None:
    request = service.files().get_media(fileId=file_id)
    dest.parent.mkdir(parents=True, exist_ok=True)

    with dest.open("wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
```

---

## 5. Listar y Buscar Archivos

```python
def list_folder(service, folder_id: str) -> list[dict[str, str]]:
    query = f"'{folder_id}' in parents and trashed=false"
    results = (
        service.files()
        .list(q=query, fields="files(id, name, mimeType, size, modifiedTime)")
        .execute()
    )
    return results.get("files", [])


def find_file(service, name: str, folder_id: str) -> str | None:
    query = f"name='{name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None
```

---

## 6. Permisos — Compartir con el Cliente

```python
def share_with_reader(service, file_id: str, email: str) -> None:
    permission = {
        "type": "user",
        "role": "reader",
        "emailAddress": email,
    }
    service.permissions().create(
        fileId=file_id,
        body=permission,
        sendNotificationEmail=True,
    ).execute()


def share_with_link(service, file_id: str) -> str:
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
    ).execute()
    file = service.files().get(fileId=file_id, fields="webViewLink").execute()
    return file["webViewLink"]
```

---

## 7. Manejo de Errores

```python
from googleapiclient.errors import HttpError

def safe_upload(service, local_path: Path, folder_id: str) -> str | None:
    try:
        return upload_file(service, local_path, folder_id)
    except HttpError as e:
        print(f"Drive error [{e.status_code}]: {e.reason}")
        return None
```

---

## Resumen

| Operación | Método |
|-----------|--------|
| Crear/reusar carpeta | `files().list(q=...)` + `files().create()` |
| Subir archivo | `files().create(media_body=MediaFileUpload(..., resumable=True))` |
| Descargar | `MediaIoBaseDownload` + `next_chunk()` |
| Compartir por email | `permissions().create(type="user", role="reader")` |
| Compartir con link | `permissions().create(type="anyone", role="reader")` |
