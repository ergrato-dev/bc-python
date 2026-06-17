from __future__ import annotations
import os


class AppConfig:
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", str(4 * 1024 * 1024)))  # 4 MB
    dry_run: bool = os.getenv("DRY_RUN", "true").lower() == "true"
