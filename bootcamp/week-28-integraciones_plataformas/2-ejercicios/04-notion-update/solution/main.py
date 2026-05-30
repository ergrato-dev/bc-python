"""
Ejercicio 04: Notion API — Actualizar Base de Datos — SOLUCIÓN
==============================================================
"""
from __future__ import annotations

import datetime
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
    body: dict[str, object] = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Proyecto": {
                "title": [{"text": {"content": project}}]
            },
            "Cliente": {
                "rich_text": [{"text": {"content": client}}]
            },
            "Estado": {
                "select": {"name": "En proceso"}
            },
            "Fecha": {
                "date": {"start": datetime.date.today().isoformat()}
            },
        },
    }
    resp = httpx.post(
        "https://api.notion.com/v1/pages",
        headers=notion_headers(),
        json=body,
    )
    resp.raise_for_status()
    return str(resp.json()["id"])


def update_delivery_status(
    page_id: str,
    status: str,
    youtube_url: str = "",
    vimeo_url: str = "",
) -> None:
    properties: dict[str, object] = {
        "Estado": {"select": {"name": status}},
    }
    if youtube_url:
        properties["YouTube URL"] = {"url": youtube_url}
    if vimeo_url:
        properties["Vimeo URL"] = {"url": vimeo_url}

    resp = httpx.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=notion_headers(),
        json={"properties": properties},
    )
    resp.raise_for_status()


def append_delivery_note(page_id: str, note: str, video_urls: list[str]) -> None:
    children: list[dict[str, object]] = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Entrega"}}]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": note}}]
            },
        },
    ]
    for url in video_urls:
        children.append({
            "object": "block",
            "type": "bookmark",
            "bookmark": {"url": url},
        })

    resp = httpx.patch(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=notion_headers(),
        json={"children": children},
    )
    resp.raise_for_status()


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
