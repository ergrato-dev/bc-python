"""Generación de thumbnails en múltiples resoluciones."""

import logging
from pathlib import Path

from PIL import Image, ImageOps

from .profiles import ThumbProfile, PROFILES

logger = logging.getLogger(__name__)


def generate_thumb(src: Path, dest_dir: Path, profile: ThumbProfile) -> Path:
    """
    Genera un thumbnail de src según profile.
    Retorna el path del archivo generado.
    """
    out_dir = dest_dir / profile.name
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".tiff" if profile.fmt == "TIFF" else ".webp"
    dest = out_dir / src.with_suffix(suffix).name

    # TODO:
    # 1. Abrir imagen con Image.open(src)
    # 2. Corregir orientación: ImageOps.exif_transpose(img)
    # 3. Convertir a RGB si el modo es RGBA o P
    # 4. Si profile.fit: usar ImageOps.fit(img, (profile.max_width, profile.max_height), Image.LANCZOS)
    #    Si no: usar img.thumbnail((profile.max_width, profile.max_height), Image.LANCZOS)
    # 5. Guardar: img.save(dest, profile.fmt, quality=profile.quality)
    # 6. logger.info("Generated %s/%s", profile.name, dest.name)
    # 7. Retornar dest
    raise NotImplementedError


def batch_generate(
    sources: list[Path],
    dest_dir: Path,
    profiles: list[ThumbProfile] | None = None,
    max_workers: int = 4,
) -> tuple[list[Path], list[tuple[Path, Exception]]]:
    """
    Genera todos los perfiles para cada imagen en parallel.
    Retorna (resultados_ok, errores).
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    if profiles is None:
        profiles = PROFILES

    tasks = [(src, profile) for src in sources for profile in profiles]
    results: list[Path] = []
    errors: list[tuple[Path, Exception]] = []

    # TODO: ThreadPoolExecutor + as_completed, capturar excepciones por tarea
    raise NotImplementedError
