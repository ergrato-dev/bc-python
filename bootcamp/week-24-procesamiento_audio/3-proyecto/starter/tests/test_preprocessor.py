"""Tests para el pre-procesador de audio."""

import pytest
from pathlib import Path
from pydub import AudioSegment

from src.preprocessor import normalize_audio


def make_quiet_audio(dbfs: float = -30.0) -> AudioSegment:
    import math, array as arr
    sample_rate = 44100
    n = sample_rate
    vol = 10 ** (dbfs / 20)
    samples = arr.array("h", [
        int(32767 * vol * math.sin(2 * math.pi * 440 * i / sample_rate))
        for i in range(n)
    ])
    return AudioSegment(data=samples.tobytes(), sample_width=2, frame_rate=sample_rate, channels=1)


def test_normalize_reaches_target() -> None:
    audio = make_quiet_audio(-30.0)
    normalized = normalize_audio(audio, target_dbfs=-14.0)
    assert abs(normalized.dBFS - (-14.0)) < 1.0


def test_normalize_preserves_duration() -> None:
    audio = make_quiet_audio(-25.0)
    normalized = normalize_audio(audio, target_dbfs=-14.0)
    assert len(normalized) == len(audio)


def test_normalize_custom_target() -> None:
    audio = make_quiet_audio(-30.0)
    normalized = normalize_audio(audio, target_dbfs=-20.0)
    assert abs(normalized.dBFS - (-20.0)) < 1.0
