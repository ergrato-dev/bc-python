"""Tests de S3Uploader usando mocks de boto3."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.s3_uploader import (
    S3Uploader,
    load_state,
    save_state,
    sha256_file,
    _needs_upload,
)


@pytest.fixture
def tmp_file(tmp_path: Path) -> Path:
    f = tmp_path / "test.mp4"
    f.write_bytes(b"fake video content")
    return f


def test_sha256_file(tmp_file: Path) -> None:
    import hashlib
    expected = hashlib.sha256(b"fake video content").hexdigest()
    assert sha256_file(tmp_file) == expected


def test_load_state_missing(tmp_path: Path) -> None:
    state = load_state(tmp_path / "missing.json")
    assert state == {}


def test_save_and_load_state(tmp_path: Path) -> None:
    state_path = tmp_path / ".sync_state.json"
    state = {"file.mp4": {"sha256": "abc123", "s3_key": "test/file.mp4", "synced_at": "2026-01-01"}}
    save_state(state, state_path)
    loaded = load_state(state_path)
    assert loaded == state


def test_needs_upload_new_file(tmp_file: Path) -> None:
    assert _needs_upload(tmp_file, {}) is True


def test_needs_upload_unchanged(tmp_file: Path) -> None:
    checksum = sha256_file(tmp_file)
    state = {str(tmp_file): {"sha256": checksum}}
    assert _needs_upload(tmp_file, state) is False


def test_needs_upload_modified(tmp_file: Path) -> None:
    state = {str(tmp_file): {"sha256": "old_checksum"}}
    assert _needs_upload(tmp_file, state) is True


def test_sync_to_s3_skips_unchanged(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    f = output / "clip.mp4"
    f.write_bytes(b"video")

    state_path = tmp_path / ".sync_state.json"
    checksum = sha256_file(f)
    save_state({str(f): {"sha256": checksum, "s3_key": "proj/video/2026-01-01/clip.mp4"}}, state_path)

    with patch("boto3.client") as mock_client:
        uploader = S3Uploader.__new__(S3Uploader)
        uploader._bucket = "test-bucket"
        uploader._s3 = mock_client.return_value

        stats = uploader.sync_to_s3(output, "test-project", state_path, extensions={".mp4"})

    assert stats["skipped"] == 1
    assert stats["uploaded"] == 0


def test_sync_to_s3_uploads_new_file(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    (output / "new.mp4").write_bytes(b"new video")

    state_path = tmp_path / ".sync_state.json"

    with patch("boto3.client") as mock_client:
        mock_s3 = mock_client.return_value
        mock_s3.upload_file = MagicMock()

        uploader = S3Uploader.__new__(S3Uploader)
        uploader._bucket = "test-bucket"
        uploader._s3 = mock_s3

        stats = uploader.sync_to_s3(output, "canal9/spot", state_path, extensions={".mp4"})

    assert stats["uploaded"] == 1
    assert stats["skipped"] == 0
    mock_s3.upload_file.assert_called_once()
