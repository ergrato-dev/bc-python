"""
Ejercicio 04: Notion API — Actualizar Base de Datos
====================================================
Crea un registro de entrega en Notion y lo actualiza con las URLs de video.

Requisitos:
    pip install httpx

Variables de entorno:
    NOTION_TOKEN=secret_...
    NOTION_DATABASE_ID=...  (ID de la DB "Proyectos" en tu workspace)

Ejecutar:
    python main.py
"""
from __future__ import annotations

import os
import httpx

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")
NOTION_VERSION = "2022-06-28"


def notion_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def create_delivery_record(project: str, client: str) -> str:
    """
    Crea una nueva página en la DB con estado "En proceso".
    Devuelve el page_id.
    """
    # TODO: POST /v1/pages con parent.database_id
    # TODO: propiedades: Proyecto (title), Cliente (rich_text), Estado (select), Fecha (date)
    raise NotImplementedError


def update_delivery_status(
    page_id: str,
    status: str,
    youtube_url: str = "",
    vimeo_url: str = "",
) -> None:
    """Actualiza el estado y las URLs de entrega en la página."""
    # TODO: PATCH /v1/pages/{page_id} con properties
    # TODO: Estado (select), YouTube URL (url), Vimeo URL (url)
    raise NotImplementedError


def append_delivery_note(page_id: str, note: str, video_urls: list[str]) -> None:
    """Agrega bloques de contenido: heading + párrafo + bookmarks."""
    # TODO: PATCH /v1/blocks/{page_id}/children con children
    # TODO: heading_2, paragraph, bookmark por cada URL
    raise NotImplementedError


if __name__ == "__main__":
    if not NOTION_TOKEN or not DATABASE_ID:
        print("Configurar NOTION_TOKEN y NOTION_DATABASE_ID")
        raise SystemExit(1)

    print("1. Creando registro de entrega...")
    page_id = create_delivery_record(
        project="canal9/spot-verano-2024",
        client="Canal 9",
    )
    print(f"   Página creada: {page_id}")

    print("2. Actualizando con URLs de video...")
    update_delivery_status(
        page_id,
        status="Entregado",
        youtube_url="https://youtu.be/dQw4w9WgXcQ",
        vimeo_url="https://vimeo.com/12345678",
    )
    print("   Estado: Entregado ✓")

    print("3. Agregando nota de entrega...")
    append_delivery_note(
        page_id,
        note="Entrega final aprobada por el cliente. Versión 3 final.",
        video_urls=["https://youtu.be/dQw4w9WgXcQ", "https://vimeo.com/12345678"],
    )
    print("   Nota agregada")

    print("OK — Ejercicio 04 completado")
