"""
Ejercicio 01: YouTube Data API v3 — Upload y Metadata
======================================================
Sube un video a YouTube, configura metadata y thumbnail.

Requisitos:
    pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
    Descargar client_secrets.json desde Google Cloud Console
    Habilitar YouTube Data API v3

Ejecutar:
    python main.py
"""
from __future__ import annotations

from pathlib import Path


def get_youtube_service():
    """Autentica con OAuth2 y devuelve el servicio de YouTube."""
    # TODO: InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    # TODO: guardar/cargar token de youtube_token.json
    # SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
    #           "https://www.googleapis.com/auth/youtube"]
    raise NotImplementedError


def upload_video(
    service,
    video_path: Path,
    title: str,
    description: str,
    tags: list[str],
    privacy_status: str = "unlisted",
) -> str:
    """Sube el video y devuelve el video_id."""
    # TODO: MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True, chunksize=10*1024*1024)
    # TODO: service.videos().insert(part="snippet,status", body={...}, media_body=media)
    # TODO: loop request.next_chunk() hasta response != None
    raise NotImplementedError


def set_thumbnail(service, video_id: str, thumb_path: Path) -> None:
    """Configura el thumbnail del video."""
    # TODO: service.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(...))
    raise NotImplementedError


def add_to_playlist(service, video_id: str, playlist_title: str) -> str:
    """Agrega el video a una playlist (creándola si no existe). Devuelve playlist_id."""
    # TODO: buscar playlist con ese título → crear si no existe
    # TODO: service.playlistItems().insert(...)
    raise NotImplementedError


if __name__ == "__main__":
    import tempfile
    service = get_youtube_service()

    # Video de prueba (1 segundo, 1 frame)
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
