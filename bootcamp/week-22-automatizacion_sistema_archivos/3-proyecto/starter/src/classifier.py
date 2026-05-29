"""Clasificación de archivos por tipo de media."""

from enum import StrEnum
from pathlib import Path

class MediaType(StrEnum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    DOC   = "doc"
    OTHER = "other"

EXTENSION_MAP: dict[str, MediaType] = {
    ".mp4": MediaType.VIDEO,
    ".mov": MediaType.VIDEO,
    ".mxf": MediaType.VIDEO,
    ".prores": MediaType.VIDEO,
    ".avi": MediaType.VIDEO,
    ".wav": MediaType.AUDIO,
    ".aiff": MediaType.AUDIO,
    ".mp3": MediaType.AUDIO,
    ".flac": MediaType.AUDIO,
    ".jpg": MediaType.IMAGE,
    ".jpeg": MediaType.IMAGE,
    ".png": MediaType.IMAGE,
    ".tiff": MediaType.IMAGE,
    ".psd": MediaType.IMAGE,
    ".pdf": MediaType.DOC,
    ".docx": MediaType.DOC,
    ".xlsx": MediaType.DOC,
    ".txt": MediaType.DOC,
}


def classify(path: Path) -> MediaType:
    # TODO: retornar EXTENSION_MAP.get(path.suffix.lower(), MediaType.OTHER)
    raise NotImplementedError


def build_dest_dir(base: Path, media_type: MediaType, path: Path) -> Path:
    """Retorna base/{media_type}/{YYYY-MM}/ usando el mtime del archivo."""
    # TODO: datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m")
    # retornar base / media_type / month
    raise NotImplementedError
