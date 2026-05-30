"""Tests de SyncEngine — lock file y orquestación."""
from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.config import BackupConfig
from src.sync_engine import SyncEngine, _acquire_lock, _release_lock


@pytest.fixture
def config(tmp_path: Path) -> BackupConfig:
    cfg = BackupConfig(
        s3_bucket="test-bucket",
        local_output_dir=tmp_path / "output",
        sync_state_path=tmp_path / ".sync_state.json",
        lock_file_path=tmp_path / ".backup.lock",
    )
    (tmp_path / "output").mkdir()
    return cfg


def test_acquire_lock_creates_file(config: BackupConfig) -> None:
    assert _acquire_lock(config.lock_file_path) is True
    assert config.lock_file_path.exists()
    pid = int(config.lock_file_path.read_text().strip())
    assert pid == os.getpid()
    _release_lock(config.lock_file_path)


def test_acquire_lock_fails_when_active(config: BackupConfig) -> None:
    config.lock_file_path.write_text(str(os.getpid()))
    result = _acquire_lock(config.lock_file_path)
    assert result is False
    config.lock_file_path.unlink()


def test_release_lock_removes_file(config: BackupConfig) -> None:
    config.lock_file_path.write_text("12345")
    _release_lock(config.lock_file_path)
    assert not config.lock_file_path.exists()


def test_incremental_backup_raises_when_locked(config: BackupConfig) -> None:
    config.lock_file_path.write_text(str(os.getpid()))
    engine = SyncEngine(config)
    with pytest.raises(RuntimeError, match="Lock activo"):
        engine.incremental_backup("canal9/spot")
    config.lock_file_path.unlink()


def test_get_status_empty(config: BackupConfig) -> None:
    engine = SyncEngine(config)
    status = engine.get_status()
    assert status["total_files"] == 0
    assert status["last_sync"] is None
