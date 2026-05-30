"""Orquestación del pipeline de post-producción."""

import logging
import shutil
from pathlib import Path

from .inspector import get_video_info, save_metadata
from .encoder import generate_proxy, generate_web, extract_thumbnail

logger = logging.getLogger(__name__)

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mxf", ".avi", ".mkv", ".prores"}


def process_video(src: Path, dest_dir: Path) -> dict[str, Path]:
    """
    Procesa un video completo:
    1. Extrae metadata → dest_dir/meta/
    2. Genera proxy → dest_dir/proxy/
    3. Genera web encode → dest_dir/web/
    4. Extrae thumbnail → dest_dir/thumbs/
    5. Mueve original a dest_dir/archive/

    Retorna dict con paths generados.
    """
    results: dict[str, Path] = {}

    # TODO:
    # 1. info = get_video_info(src)
    # 2. results["meta"] = save_metadata(src, info, dest_dir / "meta")
    # 3. results["proxy"] = generate_proxy(src, dest_dir / "proxy")
    # 4. results["web"] = generate_web(src, dest_dir / "web")
    # 5. results["thumb"] = extract_thumbnail(src, dest_dir / "thumbs")
    # 6. archive_dir = dest_dir / "archive"; archive_dir.mkdir(parents=True, exist_ok=True)
    #    results["archive"] = shutil.move(str(src), archive_dir / src.name)
    # 7. logger.info("Processed %s: %s", src.name, list(results.keys()))
    # 8. return results
    raise NotImplementedError
