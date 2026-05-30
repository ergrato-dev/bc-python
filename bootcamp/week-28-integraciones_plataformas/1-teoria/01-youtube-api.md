# YouTube Data API v3

## 1. Autenticación — OAuth2

YouTube requiere OAuth2 en nombre de un usuario real (no Service Account). El flujo es:

1. Redirigir al usuario a la URL de autorización de Google
2. El usuario aprueba → Google devuelve un `code`
3. Intercambiar el `code` por `access_token` + `refresh_token`
4. Usar `refresh_token` para renovar el `access_token` cuando expire

```python
# auth.py
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]
TOKEN_PATH = Path("youtube_token.json")
CLIENT_SECRETS = "client_secrets.json"  # descargado de Google Cloud Console


def get_credentials() -> Credentials:
    creds: Credentials | None = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_info(
            json.loads(TOKEN_PATH.read_text()), SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())

    return creds


def get_youtube_service():
    from googleapiclient.discovery import build
    return build("youtube", "v3", credentials=get_credentials())
```

---

## 2. Upload de Video (Resumable)

El upload resumable divide el archivo en chunks y puede retomar si se corta la conexión.

```python
from pathlib import Path
from googleapiclient.http import MediaFileUpload


def upload_video(
    service,
    video_path: Path,
    title: str,
    description: str,
    tags: list[str],
    category_id: str = "22",       # 22 = People & Blogs
    privacy_status: str = "unlisted",
) -> str:
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
            "defaultLanguage": "es",
        },
        "status": {
            "privacyStatus": privacy_status,  # "public" | "unlisted" | "private"
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=10 * 1024 * 1024,  # 10 MB por chunk
    )

    request = service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"Upload YouTube: {pct}%")

    video_id: str = response["id"]
    print(f"Video publicado: https://youtu.be/{video_id}")
    return video_id
```

---

## 3. Subir Thumbnail

```python
from googleapiclient.http import MediaFileUpload


def set_thumbnail(service, video_id: str, thumb_path: Path) -> None:
    media = MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
    service.thumbnails().set(videoId=video_id, media_body=media).execute()
    print(f"Thumbnail configurado para {video_id}")
```

Los thumbnails personalizados requieren que el canal esté verificado.

---

## 4. Listas de Reproducción

```python
def get_or_create_playlist(
    service,
    title: str,
    description: str = "",
    privacy_status: str = "unlisted",
) -> str:
    # Buscar playlist existente
    resp = service.playlists().list(part="snippet", mine=True, maxResults=50).execute()
    for pl in resp.get("items", []):
        if pl["snippet"]["title"] == title:
            return pl["id"]

    # Crear nueva
    result = service.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": privacy_status},
        },
    ).execute()
    return result["id"]


def add_to_playlist(service, playlist_id: str, video_id: str) -> None:
    service.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()
    print(f"Video {video_id} agregado a playlist {playlist_id}")
```

---

## 5. Actualizar Metadata de un Video Existente

```python
def update_video_metadata(
    service,
    video_id: str,
    title: str | None = None,
    description: str | None = None,
    privacy_status: str | None = None,
) -> None:
    current = service.videos().list(part="snippet,status", id=video_id).execute()
    item = current["items"][0]

    snippet = item["snippet"]
    status = item["status"]

    if title:
        snippet["title"] = title
    if description:
        snippet["description"] = description
    if privacy_status:
        status["privacyStatus"] = privacy_status

    service.videos().update(
        part="snippet,status",
        body={"id": video_id, "snippet": snippet, "status": status},
    ).execute()
```

---

## Resumen

| Operación | Método |
|-----------|--------|
| Upload resumable | `videos().insert(media_body=MediaFileUpload(..., resumable=True))` |
| Thumbnail | `thumbnails().set(videoId=..., media_body=...)` |
| Crear playlist | `playlists().insert(part="snippet,status", ...)` |
| Agregar a playlist | `playlistItems().insert(...)` |
| Actualizar metadata | `videos().update(part="snippet,status", ...)` |
| Privacy | `"public"` / `"unlisted"` / `"private"` |
