"""Tests para el registro de checksums."""

import tempfile
from pathlib import Path

import pytest

from src.registry import sha256, load_registry, save_registry, is_processed, mark_processed


def test_sha256_consistency() -> None:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"studio bc content" * 1000)
        path = Path(f.name)

    digest1 = sha256(path)
    digest2 = sha256(path)
    assert digest1 == digest2
    assert len(digest1) == 64  # SHA-256 = 64 hex chars
    path.unlink()


def test_sha256_different_content() -> None:
    with tempfile.NamedTemporaryFile(delete=False) as f1:
        f1.write(b"content a")
        p1 = Path(f1.name)
    with tempfile.NamedTemporaryFile(delete=False) as f2:
        f2.write(b"content b")
        p2 = Path(f2.name)

    assert sha256(p1) != sha256(p2)
    p1.unlink(); p2.unlink()


def test_registry_roundtrip(tmp_path: Path) -> None:
    import os
    orig = os.getcwd()
    os.chdir(tmp_path)
    try:
        registry: dict[str, str] = {}
        mark_processed("abc123", Path("/organized/video/file.mp4"), registry)
        loaded = load_registry()
        assert "abc123" in loaded
        assert is_processed("abc123", loaded)
        assert not is_processed("xyz999", loaded)
    finally:
        os.chdir(orig)
