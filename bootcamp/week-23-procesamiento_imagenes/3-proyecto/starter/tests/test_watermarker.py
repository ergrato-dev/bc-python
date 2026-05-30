"""Tests para el módulo de watermarks."""

import pytest
from pathlib import Path
from PIL import Image

from src.watermarker import apply_text


def make_image(w: int = 800, h: int = 600) -> Image.Image:
    return Image.new("RGB", (w, h), color=(80, 120, 160))


def test_apply_text_returns_rgb() -> None:
    img = make_image()
    result = apply_text(img, text="© Test", opacity=80)
    assert result.mode == "RGB"


def test_apply_text_preserves_size() -> None:
    img = make_image(1000, 700)
    result = apply_text(img, text="Studio BC")
    assert result.size == (1000, 700)


def test_apply_text_different_from_original() -> None:
    img = make_image()
    result = apply_text(img, text="© Studio BC", opacity=200)
    # Con alta opacidad, los píxeles deben diferir del original
    import numpy as np
    arr_orig = list(img.getdata())
    arr_result = list(result.getdata())
    assert arr_orig != arr_result
