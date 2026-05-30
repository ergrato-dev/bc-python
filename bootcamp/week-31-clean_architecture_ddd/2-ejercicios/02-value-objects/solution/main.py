"""
Ejercicio 02: Value Objects — SOLUCIÓN
======================================
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectSlug:
    value: str

    def __post_init__(self) -> None:
        if not re.match(r"^[a-z0-9_-]+/[a-z0-9_-]+$", self.value):
            raise ValueError(
                f"ProjectSlug inválido: '{self.value}'. "
                "Formato: 'cliente/proyecto' (minúsculas, guiones, números)"
            )

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
            raise ValueError(f"MediaType inválido: '{self.value}'. Válidos: {self._VALID}")

    @classmethod
    def from_extension(cls, ext: str) -> "MediaType":
        return cls(cls._EXT_MAP.get(ext.lower(), "other"))

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
        if " " in self.value:
            raise ValueError(f"S3Key no puede contener espacios: '{self.value}'")

    @classmethod
    def build(cls, project: ProjectSlug, media_type: MediaType, date: str, filename: str) -> "S3Key":
        return cls(f"{project}/{media_type.value}/{date}/{filename}")

    def __str__(self) -> str:
        return self.value


if __name__ == "__main__":
    slug = ProjectSlug("canal9/spot-verano")
    assert slug.client == "canal9"
    assert slug.project == "spot-verano"

    slug2 = ProjectSlug("canal9/spot-verano")
    assert slug == slug2

    try:
        ProjectSlug("INVALIDO/MAYUSCULAS")
    except ValueError as e:
        print(f"ValueError esperado: {e}")

    mt = MediaType.from_extension(".mp4")
    assert mt.value == "video" and mt.is_video
    assert MediaType.from_extension(".xyz").value == "other"

    key = S3Key.build(ProjectSlug("canal9/spot"), MediaType("video"), "2024-11-15", "spot_web.mp4")
    assert str(key) == "canal9/spot/video/2024-11-15/spot_web.mp4"

    print("OK — Ejercicio 02 completado")
