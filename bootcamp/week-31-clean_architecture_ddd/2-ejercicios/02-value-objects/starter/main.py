"""
Ejercicio 02: Value Objects
===========================
Implementa ProjectSlug, MediaType y S3Key como Value Objects inmutables.

Ejecutar: python main.py
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectSlug:
    """
    Slug de proyecto en formato 'cliente/proyecto'.
    Solo acepta letras minúsculas, números, guiones y guiones bajos.

    Ejemplos válidos:   'canal9/spot-verano', 'bbc/documental_2024'
    Ejemplos inválidos: 'Canal9/spot', 'canal9', 'canal9/spot/extra'
    """
    value: str

    def __post_init__(self) -> None:
        # TODO: validar con regex r"^[a-z0-9_-]+/[a-z0-9_-]+$"
        # Si no coincide, lanzar ValueError con mensaje descriptivo
        raise NotImplementedError

    @property
    def client(self) -> str:
        # TODO: devolver la parte antes del "/"
        raise NotImplementedError

    @property
    def project(self) -> str:
        # TODO: devolver la parte después del "/"
        raise NotImplementedError

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class MediaType:
    """
    Tipo de media del archivo.
    Valores válidos: "video", "audio", "image", "document", "other"
    """
    value: str

    _VALID = frozenset({"video", "audio", "image", "document", "other"})
    _EXT_MAP: dict[str, str] = {
        ".mp4": "video", ".mov": "video", ".mxf": "video", ".avi": "video",
        ".mp3": "audio", ".wav": "audio", ".flac": "audio", ".aac": "audio",
        ".jpg": "image", ".jpeg": "image", ".png": "image", ".tif": "image",
        ".pdf": "document", ".docx": "document",
    }

    def __post_init__(self) -> None:
        # TODO: validar que value esté en _VALID
        raise NotImplementedError

    @classmethod
    def from_extension(cls, ext: str) -> "MediaType":
        # TODO: buscar ext.lower() en _EXT_MAP, devolver cls(resultado o "other")
        raise NotImplementedError

    @classmethod
    def from_path(cls, path: Path) -> "MediaType":
        return cls.from_extension(path.suffix)

    @property
    def is_video(self) -> bool:
        return self.value == "video"


@dataclass(frozen=True)
class S3Key:
    """
    Clave S3 con estructura: {project}/{media_type}/{date}/{filename}

    No puede contener espacios ni empezar con "/".
    """
    value: str

    def __post_init__(self) -> None:
        # TODO: validar que no empiece con "/" y no contenga espacios
        raise NotImplementedError

    @classmethod
    def build(
        cls,
        project: ProjectSlug,
        media_type: MediaType,
        date: str,
        filename: str,
    ) -> "S3Key":
        # TODO: construir f"{project}/{media_type.value}/{date}/{filename}"
        raise NotImplementedError

    def __str__(self) -> str:
        return self.value


# ── Tests ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== ProjectSlug ===")
    slug = ProjectSlug("canal9/spot-verano")
    assert slug.client == "canal9"
    assert slug.project == "spot-verano"
    assert str(slug) == "canal9/spot-verano"

    slug2 = ProjectSlug("canal9/spot-verano")
    assert slug == slug2  # Value Object — igualdad por valor
    print(f"slug={slug} client={slug.client} project={slug.project} OK")

    try:
        ProjectSlug("INVALIDO/MAYUSCULAS")
        print("ERROR: debería haber lanzado ValueError")
    except ValueError as e:
        print(f"ValueError esperado: {e}")

    try:
        ProjectSlug("sin-slash")
        print("ERROR: debería haber lanzado ValueError")
    except ValueError:
        print("sin-slash rechazado OK")

    print("\n=== MediaType ===")
    mt = MediaType.from_extension(".mp4")
    assert mt.value == "video"
    assert mt.is_video
    mt2 = MediaType.from_extension(".mp3")
    assert mt2.value == "audio"
    mt3 = MediaType.from_extension(".xyz")
    assert mt3.value == "other"
    print("MediaType.from_extension OK")

    try:
        MediaType("invalid_type")
        print("ERROR: debería haber lanzado ValueError")
    except ValueError:
        print("MediaType inválido rechazado OK")

    print("\n=== S3Key ===")
    key = S3Key.build(
        ProjectSlug("canal9/spot"),
        MediaType("video"),
        "2024-11-15",
        "spot_web.mp4",
    )
    assert str(key) == "canal9/spot/video/2024-11-15/spot_web.mp4"
    print(f"S3Key: {key} OK")

    try:
        S3Key("/empieza-con-slash/key.mp4")
        print("ERROR: debería haber lanzado ValueError")
    except ValueError:
        print("S3Key con slash inicial rechazado OK")

    print("\nOK — Ejercicio 02 completado")
