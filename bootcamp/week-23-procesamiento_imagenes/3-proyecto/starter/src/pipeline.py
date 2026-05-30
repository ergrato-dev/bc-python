"""Orquestación del pipeline completo."""

import logging
from pathlib import Path

from .profiles import PROFILES, ThumbProfile
from .thumbnailer import generate_thumb
from .watermarker import apply_logo, apply_text

logger = logging.getLogger(__name__)

WATERMARK_PROFILES = {"web", "social"}


def process_image(
    src: Path,
    dest_dir: Path,
    logo_path: Path | None = None,
    profiles: list[ThumbProfile] | None = None,
) -> list[Path]:
    """
    Para una imagen:
    1. Genera thumbnails para cada perfil
    2. Aplica watermark a los perfiles en WATERMARK_PROFILES (si logo_path dado)
    Retorna lista de paths generados.
    """
    if profiles is None:
        profiles = PROFILES

    generated: list[Path] = []

    for profile in profiles:
        try:
            dest = generate_thumb(src, dest_dir, profile)
            # TODO: si profile.name in WATERMARK_PROFILES y logo_path existe:
            #   abrir dest, apply_logo, apply_text, re-guardar dest
            generated.append(dest)
        except Exception as e:
            logger.error("Failed %s/%s: %s", profile.name, src.name, e)

    return generated
