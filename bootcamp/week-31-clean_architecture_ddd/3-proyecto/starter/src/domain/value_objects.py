"""Domain value objects — ProjectSlug, MediaType, S3Key."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectSlug:
    """'canal9/spot-verano' — inmutable, validado."""
    value: str

    def __post_init__(self) -> None:
        # TODO: validar con regex r"^[a-z0-9_-]+/[a-z0-9_-]+$"
        raise NotImplementedError

    @property
    def client(self) -> str:
        return self.value.split("/")[0]

    @property
    def project(self) -> str:
        return self.value.split("/")[1]

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class MediaType:
    value: str

    _VALID = frozenset({"video", "audio", "image", "document", "other"})
    _EXT_MAP: dict[str, str] = {
        ".mp4": "video", ".mov": "video", ".mxf": "video", ".avi": "video",
        ".mp3": "audio", ".wav": "audio", ".flac": "audio", ".aac": "audio",
        ".jpg": "image", ".jpeg": "image", ".png": "image", ".tif": "image",
        ".pdf": "document", ".docx": "document",
    }

    def __post_init__(self) -> None:
        if self.value not in self._VALID:
            raise ValueError(f"MediaType inválido: '{self.value}'")

    @classmethod
    def from_extension(cls, ext: str) -> "MediaType":
        # TODO: buscar en _EXT_MAP, devolver "other" si no existe
        raise NotImplementedError

    @classmethod
    def from_path(cls, path: Path) -> "MediaType":
        return cls.from_extension(path.suffix)

    @property
    def is_video(self) -> bool:
        return self.value == "video"


@dataclass(frozen=True)
class S3Key:
    value: str

    def __post_init__(self) -> None:
        if self.value.startswith("/"):
            raise ValueError(f"S3Key no puede empezar con '/': '{self.value}'")

    @classmethod
    def build(cls, project: ProjectSlug, media_type: MediaType, date: str, filename: str) -> "S3Key":
        # TODO: construir f"{project}/{media_type.value}/{date}/{filename}"
        raise NotImplementedError

    def __str__(self) -> str:
        return self.value
