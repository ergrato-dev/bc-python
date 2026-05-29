"""Tests para el clasificador de archivos."""

import pytest
from pathlib import Path
from src.classifier import classify, MediaType, build_dest_dir
import tempfile


@pytest.mark.parametrize("filename,expected", [
    ("spot.mp4", MediaType.VIDEO),
    ("audio.wav", MediaType.AUDIO),
    ("foto.jpg", MediaType.IMAGE),
    ("brief.pdf", MediaType.DOC),
    ("datos.csv", MediaType.OTHER),
    ("video.MP4", MediaType.VIDEO),  # case-insensitive
])
def test_classify(filename: str, expected: MediaType) -> None:
    assert classify(Path(filename)) == expected


def test_build_dest_dir_structure() -> None:
    with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
        path = Path(f.name)
        dest = build_dest_dir(Path("organized"), MediaType.VIDEO, path)
        # Debe ser organized/video/YYYY-MM
        assert dest.parts[0] == "organized"
        assert dest.parts[1] == "video"
        assert len(dest.parts[2]) == 7  # "YYYY-MM"
