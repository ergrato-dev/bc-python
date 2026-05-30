"""
Ejercicio 01: YouTube Data API v3 — Upload y Metadata — SOLUCIÓN
================================================================
"""
from __future__ import annotations

import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]
TOKEN_PATH = Path("youtube_token.json")
CLIENT_SECRETS = "client_secrets.json"


def get_youtube_service():
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

    return build("youtube", "v3", credentials=creds)


def upload_video(
    service,
    video_path: Path,
    title: str,
    description: str,
    tags: list[str],
    privacy_status: str = "unlisted",
) -> str:
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22",
            "defaultLanguage": "es",
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=10 * 1024 * 1024,
    )
    request = service.videos().insert(
        part="snippet,status", body=body, media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"  Upload YouTube: {pct}%")
    return str(response["id"])


def set_thumbnail(service, video_id: str, thumb_path: Path) -> None:
    media = MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
    service.thumbnails().set(videoId=video_id, media_body=media).execute()


def add_to_playlist(service, video_id: str, playlist_title: str) -> str:
    resp = service.playlists().list(part="snippet", mine=True, maxResults=50).execute()
    for pl in resp.get("items", []):
        if pl["snippet"]["title"] == playlist_title:
            playlist_id = pl["id"]
            break
    else:
        result = service.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": playlist_title},
                "status": {"privacyStatus": "unlisted"},
            },
        ).execute()
        playlist_id = result["id"]

    service.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()
    return str(playlist_id)


if __name__ == "__main__":
    service = get_youtube_service()

    test_video = Path("test_video.mp4")
    if not test_video.exists():
        print("Crea test_video.mp4 con ffmpeg: ffmpeg -f lavfi -i color=c=blue:size=1280x720:rate=1 -t 3 test_video.mp4")
        raise SystemExit(1)

    print("1. Subiendo video...")
    video_id = upload_video(
        service, test_video,
        title="[TEST] Studio BC — Ejercicio 28-01",
        description="Video de prueba para el bootcamp bc-python semana 28.",
        tags=["test", "studio-bc", "automatizacion"],
        privacy_status="private",
    )
    print(f"   Video ID: {video_id} — https://youtu.be/{video_id}")

    print("2. Configurando thumbnail...")
    thumb = Path("test_thumb.jpg")
    if thumb.exists():
        set_thumbnail(service, video_id, thumb)
        print("   Thumbnail OK")

    print("3. Agregando a playlist...")
    playlist_id = add_to_playlist(service, video_id, "Studio BC — Tests")
    print(f"   Playlist: {playlist_id}")

    print("OK — Ejercicio 01 completado")
