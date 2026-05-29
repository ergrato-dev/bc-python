"""Lógica de movimiento y organización de archivos."""

import logging
import shutil
from pathlib import Path

from .classifier import MediaType, classify, build_dest_dir
from .registry import sha256, load_registry, is_processed, mark_processed

logger = logging.getLogger(__name__)


def safe_move(src: Path, dest_dir: Path) -> Path:
    """Mueve src a dest_dir resolviendo colisiones de nombres."""
    # TODO:
    # 1. dest_dir.mkdir(parents=True, exist_ok=True)
    # 2. dest = dest_dir / src.name
    # 3. Resolver colisión: bucle while dest.exists() → agregar _{counter:03d}
    # 4. shutil.move(str(src), dest)
    # 5. retornar dest
    raise NotImplementedError


class FileOrganizer:
    def __init__(self, dest_base: Path) -> None:
        self._dest = dest_base

    def organize(self, src: Path) -> Path | None:
        """Clasifica y mueve src. Retorna destino o None si falla."""
        if not src.is_file():
            return None

        registry = load_registry()
        try:
            digest = sha256(src)
        except OSError as e:
            logger.error("Cannot read %s: %s", src, e)
            return None

        if is_processed(digest, registry):
            logger.debug("Skipping already processed: %s", src.name)
            return None

        media_type = classify(src)

        # TODO:
        # 1. dest_dir = build_dest_dir(self._dest, media_type, src)
        # 2. dest = safe_move(src, dest_dir)
        # 3. mark_processed(digest, dest, registry)
        # 4. logger.info("Organized %s → %s", src.name, dest)
        # 5. retornar dest
        raise NotImplementedError
