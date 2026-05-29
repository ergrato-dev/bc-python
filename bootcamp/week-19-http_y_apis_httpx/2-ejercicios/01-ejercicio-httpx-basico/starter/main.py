"""
Ejercicio 01 — httpx Básico
============================
Practica los fundamentos de httpx: Client, params, headers, Response.

API de prueba: https://jsonplaceholder.typicode.com

Tareas:
  1. [get_posts]        Obtener los primeros 5 posts con params
  2. [get_post]         Obtener un post por ID y retornar su título
  3. [create_post]      Crear un post (POST con JSON body)
  4. [fetch_concurrent] Obtener 3 recursos en paralelo con asyncio.gather

Ejecutar: python main.py
"""
from __future__ import annotations

import asyncio
import httpx


BASE_URL = "https://jsonplaceholder.typicode.com"


# ── Tarea 1 ──────────────────────────────────────────────────────────────────

def get_posts(limit: int = 5) -> list[dict]:
    """Retorna los primeros `limit` posts usando query params."""
    # TODO: Usa httpx.Client con base_url=BASE_URL
    # TODO: Llama a GET /posts con params={"_limit": limit}
    # TODO: Llama a response.raise_for_status()
    # TODO: Retorna response.json()
    raise NotImplementedError


# ── Tarea 2 ──────────────────────────────────────────────────────────────────

def get_post(client: httpx.Client, post_id: int) -> str:
    """Retorna el título del post con id `post_id`."""
    # TODO: GET /posts/{post_id}
    # TODO: raise_for_status() — si el post no existe lanza HTTPStatusError
    # TODO: Retorna data["title"]
    raise NotImplementedError


# ── Tarea 3 ──────────────────────────────────────────────────────────────────

def create_post(title: str, body: str, user_id: int = 1) -> dict:
    """Crea un post y retorna el objeto creado (incluyendo el id asignado)."""
    # TODO: POST /posts con json={"title": ..., "body": ..., "userId": ...}
    # TODO: Verifica response.status_code == 201
    # TODO: Retorna response.json()
    raise NotImplementedError


# ── Tarea 4 ──────────────────────────────────────────────────────────────────

async def fetch_concurrent(paths: list[str]) -> list[dict]:
    """Obtiene múltiples recursos en paralelo usando AsyncClient + gather."""
    # TODO: Usa httpx.AsyncClient con base_url=BASE_URL
    # TODO: Crea una corutina por cada path usando client.get(path)
    # TODO: await asyncio.gather(*tasks)
    # TODO: Para cada response: raise_for_status() y retorna .json()
    raise NotImplementedError


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=== Tarea 1: get_posts ===")
    posts = get_posts(limit=3)
    for p in posts:
        print(f"  [{p['id']}] {p['title'][:50]}")

    print("\n=== Tarea 2: get_post con Client reutilizado ===")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        for post_id in [1, 5, 10]:
            title = get_post(client, post_id)
            print(f"  Post {post_id}: {title[:50]}")

    print("\n=== Tarea 3: create_post ===")
    new_post = create_post("Studio BC — new project", "Spot 30s para Canal 9")
    print(f"  Creado con id={new_post['id']}: {new_post['title']}")

    print("\n=== Tarea 4: fetch_concurrent ===")
    paths = ["/posts/1", "/users/1", "/todos/1"]
    results = asyncio.run(fetch_concurrent(paths))
    for path, data in zip(paths, results):
        label = data.get("title") or data.get("name") or data.get("username")
        print(f"  {path} → {label}")


if __name__ == "__main__":
    main()
