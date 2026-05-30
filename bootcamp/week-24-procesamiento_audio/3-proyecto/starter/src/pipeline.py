"""Orquestación del pipeline completo."""

import logging
from pathlib import Path
from typing import Any

from .preprocessor import preprocess
from .transcriber import load_model, transcribe
from .subtitle_writer import generate_srt, generate_vtt

logger = logging.getLogger(__name__)

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a"}


def process_audio(
    src: Path,
    dest_dir: Path,
    model: Any = None,
    language: str = "es",
) -> tuple[Path, Path]:
    """
    Procesa un archivo de audio:
    1. Normaliza y guarda en dest_dir/normalized/
    2. Transcribe con Whisper (o stub)
    3. Genera SRT y VTT en dest_dir/subtitles/

    Retorna (srt_path, vtt_path).
    """
    sub_dir = dest_dir / "subtitles"
    sub_dir.mkdir(parents=True, exist_ok=True)

    # TODO:
    # 1. preprocess(src, dest_dir)
    # 2. segments = transcribe(src, model=model, language=language)
    # 3. srt = generate_srt(segments, sub_dir / src.with_suffix(".srt").name)
    # 4. vtt = generate_vtt(segments, sub_dir / src.with_suffix(".vtt").name)
    # 5. logger.info("Processed %s → %s, %s", src.name, srt.name, vtt.name)
    # 6. return srt, vtt
    raise NotImplementedError
