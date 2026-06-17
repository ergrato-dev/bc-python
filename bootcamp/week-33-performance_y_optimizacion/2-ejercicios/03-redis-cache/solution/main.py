"""
Ejercicio 03: Cache-aside con Redis — SOLUCIÓN
"""
from __future__ import annotations

import json
import os
import time
from typing import Any

MOCK_STORE: dict[str, str] = {}


def _simulate_ai_call(asset_key: str) -> dict[str, Any]:
    time.sleep(0.1)
    return {
        "title": f"Asset {asset_key} — Studio BC",
        "tags": ["produccion", "audiovisual", "studio-bc"],
        "category": "institucional",
        "transcription": "Bienvenidos a Studio BC...",
    }


def cache_get(key: str, dry_run: bool = True) -> dict[str, Any] | None:
    if dry_run:
        raw = MOCK_STORE.get(key)
        return json.loads(raw) if raw else None
    from redis import Redis
    r: Redis[bytes] = Redis()
    raw_bytes = r.get(key)
    return json.loads(raw_bytes) if raw_bytes is not None else None


def cache_set(key: str, value: dict[str, Any], ttl: int = 3600, dry_run: bool = True) -> None:
    if dry_run:
        MOCK_STORE[key] = json.dumps(value)
        return
    from redis import Redis
    r: Redis[bytes] = Redis()
    r.setex(key, ttl, json.dumps(value, ensure_ascii=False))


def cache_delete(key: str, dry_run: bool = True) -> None:
    if dry_run:
        MOCK_STORE.pop(key, None)
        return
    from redis import Redis
    r: Redis[bytes] = Redis()
    r.delete(key)


def get_metadata_cached(asset_key: str, dry_run: bool = True) -> tuple[dict[str, Any], bool]:
    cached = cache_get(asset_key, dry_run=dry_run)
    if cached is not None:
        return cached, True
    result = _simulate_ai_call(asset_key)
    cache_set(asset_key, result, dry_run=dry_run)
    return result, False


if __name__ == "__main__":
    dry_run = not os.getenv("REDIS_HOST")
    print(f"=== Cache-aside Pattern {'(dry-run)' if dry_run else '(Redis)'} ===\n")

    MOCK_STORE.clear()
    keys = ["spot_verano_001", "documental_patagonia_002", "entrevista_director_003"]

    print("Primera pasada (esperado: todos MISS):")
    for key in keys:
        t0 = time.perf_counter()
        meta, hit = get_metadata_cached(key, dry_run=dry_run)
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"  {'HIT' if hit else 'MISS'} [{elapsed:.0f}ms] {key}: {meta['title'][:40]}")

    print("\nSegunda pasada (esperado: todos HIT):")
    for key in keys:
        t0 = time.perf_counter()
        meta, hit = get_metadata_cached(key, dry_run=dry_run)
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"  {'HIT' if hit else 'MISS'} [{elapsed:.0f}ms] {key}: {meta['title'][:40]}")

    assert len(MOCK_STORE) == len(keys)
    print("\nOK — Ejercicio 03 completado")
