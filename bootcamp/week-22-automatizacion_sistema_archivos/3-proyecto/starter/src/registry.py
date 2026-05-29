"""Registro de checksums para procesamiento idempotente."""

import hashlib
import json
from pathlib import Path

REGISTRY_FILE = Path(".processed.json")


def sha256(path: Path, chunk_size: int = 65536) -> str:
    # TODO: hashlib.sha256(), chunks con walrus operator
    raise NotImplementedError


def load_registry() -> dict[str, str]:
    # TODO: leer REGISTRY_FILE si existe, retornar {} si no
    raise NotImplementedError


def save_registry(registry: dict[str, str]) -> None:
    # TODO: escritura atómica — escribe a .tmp, luego rename
    raise NotImplementedError


def is_processed(checksum: str, registry: dict[str, str]) -> bool:
    return checksum in registry


def mark_processed(checksum: str, dest: Path, registry: dict[str, str]) -> None:
    registry[checksum] = str(dest)
    save_registry(registry)
