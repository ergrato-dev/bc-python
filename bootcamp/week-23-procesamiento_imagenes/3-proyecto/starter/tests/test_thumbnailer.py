"""Tests para el generador de thumbnails."""

import pytest
from pathlib import Path
from PIL import Image

from src.thumbnailer import generate_thumb
from src.profiles import ThumbProfile


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    img = Image.new("RGB", (3000, 2000), color=(100, 150, 200))
    p = tmp_path / "foto.jpg"
    img.save(p, quality=90)
    return p


def test_generate_thumb_web(sample_image: Path, tmp_path: Path) -> None:
    profile = ThumbProfile("web", 1200, 800, "WEBP", 85, fit=False)
    dest = generate_thumb(sample_image, tmp_path / "out", profile)

    assert dest.exists()
    with Image.open(dest) as img:
        w, h = img.size
        assert w <= 1200
        assert h <= 800
        assert w / h == pytest.approx(3000 / 2000, rel=0.05)  # proporciones preservadas


def test_generate_thumb_social_square(sample_image: Path, tmp_path: Path) -> None:
    profile = ThumbProfile("social", 1080, 1080, "WEBP", 85, fit=True)
    dest = generate_thumb(sample_image, tmp_path / "out", profile)

    assert dest.exists()
    with Image.open(dest) as img:
        assert img.size == (1080, 1080)


def test_generate_thumb_format_webp(sample_image: Path, tmp_path: Path) -> None:
    profile = ThumbProfile("thumb", 300, 300, "WEBP", 80, fit=True)
    dest = generate_thumb(sample_image, tmp_path / "out", profile)
    assert dest.suffix == ".webp"


def test_generate_thumb_creates_dir(sample_image: Path, tmp_path: Path) -> None:
    profile = ThumbProfile("web", 800, 600, "WEBP", 85)
    out_dir = tmp_path / "deep" / "nested" / "output"
    dest = generate_thumb(sample_image, out_dir, profile)
    assert dest.exists()
