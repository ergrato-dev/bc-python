"""Tests para el generador de subtítulos."""

import pytest
from pathlib import Path

from src.subtitle_writer import (
    seconds_to_srt_time,
    seconds_to_vtt_time,
    generate_srt,
    generate_vtt,
)

SAMPLE_SEGMENTS = [
    {"start": 1.28,  "end": 4.72,  "text": "Bienvenidos a Studio BC."},
    {"start": 5.10,  "end": 8.34,  "text": "Hoy presentamos nuestro spot."},
    {"start": 65.50, "end": 68.00, "text": "Minuto siguiente."},
]


def test_srt_time_basic() -> None:
    assert seconds_to_srt_time(1.28) == "00:00:01,280"
    assert seconds_to_srt_time(65.5) == "00:01:05,500"
    assert seconds_to_srt_time(3600.0) == "01:00:00,000"


def test_vtt_time_uses_dot() -> None:
    assert seconds_to_vtt_time(1.28) == "00:00:01.280"
    assert "," not in seconds_to_vtt_time(5.1)


def test_generate_srt_structure(tmp_path: Path) -> None:
    out = tmp_path / "test.srt"
    generate_srt(SAMPLE_SEGMENTS, out)
    content = out.read_text(encoding="utf-8")

    assert "1\n" in content
    assert "00:00:01,280 --> 00:00:04,720" in content
    assert "Bienvenidos a Studio BC." in content
    assert "2\n" in content


def test_generate_vtt_header(tmp_path: Path) -> None:
    out = tmp_path / "test.vtt"
    generate_vtt(SAMPLE_SEGMENTS, out)
    content = out.read_text(encoding="utf-8")

    assert content.startswith("WEBVTT")
    assert "00:00:01.280 --> 00:00:04.720" in content
    assert "," not in content  # VTT usa punto, no coma


def test_generate_srt_multiple_segments(tmp_path: Path) -> None:
    out = tmp_path / "multi.srt"
    generate_srt(SAMPLE_SEGMENTS, out)
    content = out.read_text()
    assert "3\n" in content
    assert "00:01:05,500 --> 00:01:08,000" in content
