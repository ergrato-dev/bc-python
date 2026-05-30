"""
Ejercicio 02: Vimeo API — Upload TUS y Álbumes
===============================================
Sube un video a Vimeo con el protocolo TUS y lo agrega a un álbum.

Requisitos:
    pip install PyVimeo

Ejecutar:
    python main.py
"""
from __future__ import annotations

from pathlib import Path


VIMEO_TOKEN = "YOUR_ACCESS_TOKEN"
VIMEO_KEY = "YOUR_CLIENT_ID"
VIMEO_SECRET = "YOUR_CLIENT_SECRET"


def get_vimeo_client():
    """Crea y devuelve el cliente Vimeo autenticado."""
    # TODO: import vimeo; return vimeo.VimeoClient(token=..., key=..., secret=...)
    raise NotImplementedError


def upload_video(
    client,
    video_path: Path,
    title: str,
    description: str = "",
    privacy: str = "unlisted",
) -> str:
    """Sube el video y devuelve el video_id (sin el /videos/ prefix)."""
    # TODO: uri = client.upload(str(video_path), data={...})
    # TODO: devolver uri.split("/")[-1]
    raise NotImplementedError


def get_or_create_album(client, name: str) -> str:
    """Devuelve el album_id, creándolo si no existe."""
    # TODO: client.get("/users/me/albums") → buscar por name
    # TODO: si no existe: client.post("/users/me/albums", data={"name": name, "privacy": "unlisted"})
    raise NotImplementedError


def add_to_album(client, album_id: str, video_id: str) -> None:
    """Agrega el video al álbum."""
    # TODO: client.put(f"/users/me/albums/{album_id}/videos/{video_id}")
    raise NotImplementedError


if __name__ == "__main__":
    client = get_vimeo_client()

    test_video = Path("test_video.mp4")
    if not test_video.exists():
        print("Crea test_video.mp4 con ffmpeg antes de ejecutar")
        raise SystemExit(1)

    print("1. Subiendo video a Vimeo...")
    video_id = upload_video(client, test_video, "Studio BC — Test 28-02", privacy="unlisted")
    print(f"   Video: https://vimeo.com/{video_id}")

    print("2. Creando/buscando álbum...")
    album_id = get_or_create_album(client, "Studio BC Tests")
    print(f"   Album ID: {album_id}")

    print("3. Agregando a álbum...")
    add_to_album(client, album_id, video_id)
    print("   OK")

    print("OK — Ejercicio 02 completado")
