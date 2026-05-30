"""
Ejercicio 02: Vimeo API — Upload TUS y Álbumes — SOLUCIÓN
=========================================================
"""
from __future__ import annotations

import os
from pathlib import Path

import vimeo

VIMEO_TOKEN = os.getenv("VIMEO_TOKEN", "YOUR_ACCESS_TOKEN")
VIMEO_KEY = os.getenv("VIMEO_KEY", "YOUR_CLIENT_ID")
VIMEO_SECRET = os.getenv("VIMEO_SECRET", "YOUR_CLIENT_SECRET")


def get_vimeo_client() -> vimeo.VimeoClient:
    return vimeo.VimeoClient(token=VIMEO_TOKEN, key=VIMEO_KEY, secret=VIMEO_SECRET)


def upload_video(
    client: vimeo.VimeoClient,
    video_path: Path,
    title: str,
    description: str = "",
    privacy: str = "unlisted",
) -> str:
    uri: str = client.upload(
        str(video_path),
        data={
            "name": title,
            "description": description,
            "privacy": {
                "view": privacy,
                "embed": "private",
                "download": False,
            },
            "content_rating": ["safe"],
        },
    )
    return uri.split("/")[-1]


def get_or_create_album(client: vimeo.VimeoClient, name: str) -> str:
    resp = client.get("/users/me/albums", params={"per_page": 100})
    for album in resp.json().get("data", []):
        if album["name"] == name:
            return str(album["uri"].split("/")[-1])

    resp = client.post(
        "/users/me/albums",
        data={"name": name, "privacy": "unlisted"},
    )
    return str(resp.json()["uri"].split("/")[-1])


def add_to_album(client: vimeo.VimeoClient, album_id: str, video_id: str) -> None:
    client.put(f"/users/me/albums/{album_id}/videos/{video_id}")


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
