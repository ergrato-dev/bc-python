"""Tests para el inspector de metadata."""

import json
import subprocess
import pytest
from pathlib import Path

import ffmpeg

from src.inspector import ffprobe_json, get_video_info, save_metadata


@pytest.fixture
def sample_video(tmp_path: Path) -> Path:
    dest = tmp_path / "test.mp4"
    (
        ffmpeg
        .input("color=c=blue:size=1280x720:rate=25", f="lavfi", t=3)
        .output(str(dest), vcodec="libx264", crf=28, pix_fmt="yuv420p")
        .run(overwrite_output=True, quiet=True)
    )
    return dest


def test_ffprobe_returns_dict(sample_video: Path) -> None:
    data = ffprobe_json(sample_video)
    assert "streams" in data
    assert "format" in data


def test_get_video_info_basic(sample_video: Path) -> None:
    info = get_video_info(sample_video)
    assert info["video_codec"] == "h264"
    assert info["width"] == 1280
    assert info["height"] == 720
    assert info["fps"] == 25.0
    assert (info["duration_s"] or 0) >= 2.5


def test_save_metadata_creates_json(sample_video: Path, tmp_path: Path) -> None:
    info = get_video_info(sample_video)
    out = save_metadata(sample_video, info, tmp_path / "meta")
    assert out.exists()
    loaded = json.loads(out.read_text())
    assert loaded["video_codec"] == "h264"
