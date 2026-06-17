"""MetadataCache — cache-aside con Redis para metadata de Studio BC."""
from __future__ import annotations

import json
from typing import Any

from .config import AppConfig

MOCK_CACHE: dict[str, str] = {}


class MetadataCache:
    def __init__(self, config: AppConfig | None = None) -> None:
        self._cfg = config or AppConfig()
        if not self._cfg.dry_run:
            from redis import Redis
            self._redis: "Redis[bytes]" = Redis(
                host=self._cfg.redis_host,
                port=self._cfg.redis_port,
                db=self._cfg.redis_db,
            )

    def get(self, key: str) -> dict[str, Any] | None:
        """
        Patrón cache-aside — lectura.
        Retorna el dict si hay hit, None si hay miss.

        TODO (dry_run=True):
        - raw = MOCK_CACHE.get(key)
        - Si raw: retornar json.loads(raw)
        - Si no: retornar None

        TODO (dry_run=False):
        - raw = self._redis.get(key)  → bytes | None
        - Si raw: retornar json.loads(raw)
        - Si no: retornar None

        Referencia: teoría 03 — patrón cache-aside, ejercicio 03
        """
        if self._cfg.dry_run:
            raw = MOCK_CACHE.get(key)
            return json.loads(raw) if raw else None
        raise NotImplementedError

    def set(self, key: str, value: dict[str, Any], ttl: int | None = None) -> None:
        """
        Guarda en cache con TTL (usa cfg.cache_ttl si no se especifica).

        TODO (dry_run=True):
        - MOCK_CACHE[key] = json.dumps(value, ensure_ascii=False)

        TODO (dry_run=False):
        - self._redis.setex(key, ttl or self._cfg.cache_ttl, json.dumps(value, ensure_ascii=False))

        Referencia: teoría 03 — setex, TTL
        """
        if self._cfg.dry_run:
            MOCK_CACHE[key] = json.dumps(value, ensure_ascii=False)
            return
        raise NotImplementedError

    def delete(self, key: str) -> None:
        """
        Invalida una entrada del cache.

        TODO (dry_run=True): MOCK_CACHE.pop(key, None)
        TODO (dry_run=False): self._redis.delete(key)
        """
        if self._cfg.dry_run:
            MOCK_CACHE.pop(key, None)
            return
        raise NotImplementedError

    def stats(self) -> dict[str, Any]:
        """
        Retorna métricas del cache.

        TODO (dry_run=True):
        - retornar {"keys": len(MOCK_CACHE), "backend": "mock"}

        TODO (dry_run=False):
        - info = self._redis.info()
        - retornar {"keys": self._redis.dbsize(), "backend": "redis",
                    "used_memory_human": info["used_memory_human"],
                    "keyspace_hits": info["keyspace_hits"],
                    "keyspace_misses": info["keyspace_misses"]}
        """
        if self._cfg.dry_run:
            return {"keys": len(MOCK_CACHE), "backend": "mock"}
        raise NotImplementedError
