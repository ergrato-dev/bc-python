"""SlowPipeline y OptimizedPipeline — orquestación del pipeline Studio BC."""
from __future__ import annotations

import time
import random
from pathlib import Path

from .cache import MetadataCache
from .config import AppConfig
from .streamer import AssetStreamer


def _simulate_ai_processing(asset_path: Path) -> dict[str, object]:
    """Simula llamadas AI costosas (Whisper + GPT). Latencia 0.1–0.3s."""
    time.sleep(random.uniform(0.1, 0.3))
    return {
        "title": f"Título generado para {asset_path.name}",
        "tags": ["studio-bc", "produccion-audiovisual", "video-profesional"],
        "category": "institucional",
        "transcription": "Bienvenidos a Studio BC. Somos un estudio de producción audiovisual.",
    }


class SlowPipeline:
    """Pipeline sin caching — llama al procesador AI en cada ejecución."""

    def process(self, asset_path: Path) -> dict[str, object]:
        return _simulate_ai_processing(asset_path)

    def process_batch(self, paths: list[Path]) -> list[dict[str, object]]:
        return [self.process(p) for p in paths]


class OptimizedPipeline:
    """Pipeline con caching Redis + streaming SHA-256 para la cache key."""

    def __init__(
        self,
        cache: MetadataCache | None = None,
        streamer: AssetStreamer | None = None,
        config: AppConfig | None = None,
    ) -> None:
        self._cfg = config or AppConfig()
        self._cache = cache or MetadataCache(self._cfg)
        self._streamer = streamer or AssetStreamer(self._cfg)

    def _cache_key(self, path: Path) -> str:
        if path.exists():
            checksum = self._streamer.checksum(path)
        else:
            checksum = path.name  # fallback para dry_run con archivos inexistentes
        return f"studio:meta:{checksum}"

    def process(self, asset_path: Path) -> dict[str, object]:
        key = self._cache_key(asset_path)
        cached = self._cache.get(key)
        if cached is not None:
            return {**cached, "_cache_hit": True}
        result = _simulate_ai_processing(asset_path)
        self._cache.set(key, result)
        return {**result, "_cache_hit": False}

    def process_batch(self, paths: list[Path]) -> list[dict[str, object]]:
        return [self.process(p) for p in paths]
