"""AssetStreamer — procesamiento en streaming para archivos grandes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterator

from .config import AppConfig


class AssetStreamer:
    def __init__(self, config: AppConfig | None = None) -> None:
        self._cfg = config or AppConfig()

    def checksum(self, path: Path) -> str:
        """
        Calcula SHA-256 de un archivo sin cargarlo completo en memoria.

        TODO:
        - sha = hashlib.sha256()
        - Abrir path en "rb"
        - Leer en chunks de self._cfg.chunk_size con iter(lambda: f.read(...), b"")
        - sha.update(chunk) para cada chunk
        - retornar sha.hexdigest()

        Referencia: teoría 02 — checksum_sha256(), ejercicio 02
        """
        raise NotImplementedError

    def file_stats(self, path: Path) -> dict[str, object]:
        """
        Retorna {size_bytes, size_mb, checksum} sin cargar el archivo completo.

        TODO:
        - size_bytes = path.stat().st_size
        - size_mb = round(size_bytes / 1_048_576, 2)
        - checksum = self.checksum(path)
        - retornar los tres campos como dict
        """
        raise NotImplementedError

    def iter_lines(self, path: Path, encoding: str = "utf-8") -> Iterator[str]:
        """
        Generador que itera líneas de un archivo sin cargarlo completo.

        TODO:
        - Abrir con open(path, encoding=encoding)
        - Para cada línea: yield line.strip() si no está vacía
        """
        raise NotImplementedError

    def iter_json_records(self, path: Path) -> Iterator[dict[str, object]]:
        """
        Itera registros de un JSONL (JSON Lines) sin cargar el archivo.

        TODO:
        - Para cada línea en self.iter_lines(path):
            yield json.loads(line)

        Referencia: teoría 02 — iter_jsonl(), ejercicio 02
        """
        raise NotImplementedError
