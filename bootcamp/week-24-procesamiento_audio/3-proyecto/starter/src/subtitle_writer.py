"""Generación de archivos SRT y WebVTT."""

from pathlib import Path
from typing import Any


def seconds_to_srt_time(seconds: float) -> str:
    # TODO: HH:MM:SS,mmm
    raise NotImplementedError


def seconds_to_vtt_time(seconds: float) -> str:
    # TODO: HH:MM:SS.mmm (punto, no coma)
    raise NotImplementedError


def generate_srt(segments: list[dict[str, Any]], output: Path) -> Path:
    # TODO: generar bloques numerados con timestamps SRT
    raise NotImplementedError


def generate_vtt(segments: list[dict[str, Any]], output: Path) -> Path:
    # TODO: generar WEBVTT header + bloques con timestamps VTT
    raise NotImplementedError
