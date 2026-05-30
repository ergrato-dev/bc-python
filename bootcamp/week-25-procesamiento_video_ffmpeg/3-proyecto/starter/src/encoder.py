"""Operaciones de encoding: proxy, web, thumbnail."""

from pathlib import Path
import ffmpeg


def generate_proxy(src: Path, dest_dir: Path, scale: float = 0.25) -> Path:
    """Genera proxy al scale% de resolución. H.264 veryfast."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{src.stem}_proxy.mp4"
    # TODO: filter("scale", f"iw*{scale}", -2), libx264, crf=23, veryfast
    raise NotImplementedError


def generate_web(src: Path, dest_dir: Path, max_height: int = 1080) -> Path:
    """
    Genera web encode H.264 CRF 23, máximo max_height px de alto.
    Si el video ya es menor, no lo agranda.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{src.stem}_web.mp4"
    # TODO:
    # scale: si ih > max_height → scale -2:max_height, si no → "iw:ih" (sin cambio)
    # Usar filter("scale", -2, f"min(ih,{max_height})")
    # libx264, crf=23, preset=slow, aac 128k, movflags=+faststart
    raise NotImplementedError


def extract_thumbnail(src: Path, dest_dir: Path, at_second: float = 5.0) -> Path:
    """Extrae 1 frame como JPG."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{src.stem}_thumb.jpg"
    # TODO: input(src, ss=at_second), output(dest, vframes=1)
    raise NotImplementedError
