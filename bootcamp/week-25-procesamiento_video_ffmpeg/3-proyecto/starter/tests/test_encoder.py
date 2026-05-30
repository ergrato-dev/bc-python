"""Tests para el encoder (proxy, web, thumbnail)."""

import pytest
from pathlib import Path
import ffmpeg

from src.encoder import generate_proxy, extract_thumbnail
from src.inspector import get_video_info


@pytest.fixture
def sample_video(tmp_path: Path) -> Path:
    dest = tmp_path / "source.mp4"
    (
        ffmpeg
        .input("color=c=red:size=1920x1080:rate=25", f="lavfi", t=5)
        .output(str(dest), vcodec="libx264", crf=28, pix_fmt="yuv420p")
        .run(overwrite_output=True, quiet=True)
    )
    return dest


def test_proxy_is_25_percent(sample_video: Path, tmp_path: Path) -> None:
    proxy = generate_proxy(sample_video, tmp_path / "proxy", scale=0.25)
    assert proxy.exists()
    info = get_video_info(proxy)
    assert info["width"] == 480   # 1920 * 0.25
    assert info["height"] == 270  # 1080 * 0.25


def test_extract_thumbnail_creates_jpg(sample_video: Path, tmp_path: Path) -> None:
    thumb = extract_thumbnail(sample_video, tmp_path / "thumbs", at_second=2.0)
    assert thumb.exists()
    assert thumb.suffix == ".jpg"
    assert thumb.stat().st_size > 1000
