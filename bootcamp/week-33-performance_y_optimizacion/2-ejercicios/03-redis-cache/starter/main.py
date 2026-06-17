"""
Ejercicio 03: Cache-aside con Redis
=====================================
Implementa el patrón cache-aside para metadata de Studio BC.
En dry-run, usa un dict en memoria como mock de Redis.

Requisitos: pip install redis
            docker run -d -p 6379:6379 redis:7-alpine  (opcional)

Ejecutar: python main.py
"""
from __future__ import annotations

import json
import os
import time
from typing import Any

# ── Mock en memoria (sustituto de Redis para tests/dry-run) ───────────────────

MOCK_STORE: dict[str, str] = {}


def _simulate_ai_call(asset_key: str) -> dict[str, Any]:
    """Simula una llamada costosa a la API (Whisper + GPT)."""
    time.sleep(0.1)  # 100ms de latencia simulada
    return {
        "title": f"Asset {asset_key} — Studio BC",
        "tags": ["produccion", "audiovisual", "studio-bc"],
        "category": "institucional",
        "transcription": "Bienvenidos a Studio BC...",
    }


# ── Funciones a implementar ───────────────────────────────────────────────────

def cache_get(key: str, dry_run: bool = True) -> dict[str, Any] | None:
    """
    Lee del cache.

    TODO (dry_run=True):
    - raw = MOCK_STORE.get(key)
    - Si raw: retornar json.loads(raw)
    - Si no: retornar None

    TODO (dry_run=False):
    - from redis import Redis; r = Redis()
    - raw = r.get(key) → bytes o None
    - Si raw: retornar json.loads(raw)
    - Si no: retornar None
    """
    if dry_run:
        raw = MOCK_STORE.get(key)
        return json.loads(raw) if raw else None
    raise NotImplementedError


def cache_set(key: str, value: dict[str, Any], ttl: int = 3600, dry_run: bool = True) -> None:
    """
    Guarda en el cache con TTL.

    TODO (dry_run=True):
    - MOCK_STORE[key] = json.dumps(value)

    TODO (dry_run=False):
    - r.setex(key, ttl, json.dumps(value, ensure_ascii=False))
    """
    if dry_run:
        MOCK_STORE[key] = json.dumps(value)
        return
    raise NotImplementedError


def cache_delete(key: str, dry_run: bool = True) -> None:
    """
    Borra del cache.

    TODO (dry_run=True): MOCK_STORE.pop(key, None)
    TODO (dry_run=False): r.delete(key)
    """
    if dry_run:
        MOCK_STORE.pop(key, None)
        return
    raise NotImplementedError


def get_metadata_cached(asset_key: str, dry_run: bool = True) -> tuple[dict[str, Any], bool]:
    """
    Implementa el patrón cache-aside completo.
    Retorna (metadata, cache_hit).

    TODO:
    1. Intentar cache_get(asset_key, dry_run)
    2. Si hit: retornar (result, True)
    3. Si miss: llamar _simulate_ai_call(asset_key)
    4. cache_set(asset_key, result, dry_run=dry_run)
    5. retornar (result, False)
    """
    raise NotImplementedError


if __name__ == "__main__":
    dry_run = not os.getenv("REDIS_HOST")

    print(f"=== Cache-aside Pattern {'(dry-run)' if dry_run else '(Redis)'} ===\n")

    MOCK_STORE.clear()

    keys = ["spot_verano_001", "documental_patagonia_002", "entrevista_director_003"]

    # Primera pasada: todos serán MISS
    print("Primera pasada (esperado: todos MISS):")
    for key in keys:
        t0 = time.perf_counter()
        meta, hit = get_metadata_cached(key, dry_run=dry_run)
        elapsed = (time.perf_counter() - t0) * 1000
        status = "HIT" if hit else "MISS"
        print(f"  {status} [{elapsed:.0f}ms] {key}: {meta['title'][:40]}")

    print("\nSegunda pasada (esperado: todos HIT):")
    for key in keys:
        t0 = time.perf_counter()
        meta, hit = get_metadata_cached(key, dry_run=dry_run)
        elapsed = (time.perf_counter() - t0) * 1000
        status = "HIT" if hit else "MISS"
        print(f"  {status} [{elapsed:.0f}ms] {key}: {meta['title'][:40]}")

    # Verificar que los HIT son más rápidos
    assert len(MOCK_STORE) == len(keys) or not dry_run
    print("\nOK — Ejercicio 03 completado")
