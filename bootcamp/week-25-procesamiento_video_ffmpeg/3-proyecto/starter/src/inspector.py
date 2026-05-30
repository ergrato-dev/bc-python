"""Inspección de metadata de video con ffprobe."""

import json
import subprocess
from pathlib import Path


def ffprobe_json(path: Path) -> dict[str, object]:
    """Ejecuta ffprobe y retorna el JSON completo."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_format",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)  # type: ignore[return-value]


def get_video_info(path: Path) -> dict[str, object]:
    """
    Extrae campos clave del video.
    Retorna: path, duration_s, size_bytes, bitrate_bps,
             video_codec, width, height, fps,
             audio_codec, sample_rate, audio_channels.
    """
    # TODO: usar ffprobe_json(), extraer streams de video y audio
    # fps: parsear avg_frame_rate "num/den" → float
    raise NotImplementedError


def save_metadata(path: Path, info: dict[str, object], dest_dir: Path) -> Path:
    """Guarda la metadata como JSON en dest_dir/{stem}_meta.json."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / f"{path.stem}_meta.json"
    out.write_text(json.dumps(info, indent=2, ensure_ascii=False))
    return out
