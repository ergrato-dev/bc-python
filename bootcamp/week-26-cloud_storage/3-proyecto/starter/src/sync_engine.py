from __future__ import annotations

import os
from pathlib import Path

from .config import BackupConfig
from .s3_uploader import S3Uploader


VIDEO_EXTENSIONS = {".mp4", ".mov", ".mxf", ".avi", ".mkv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".raw", ".arw"}
ALL_MEDIA = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | IMAGE_EXTENSIONS


def _acquire_lock(lock_path: Path) -> bool:
    if lock_path.exists():
        try:
            pid = int(lock_path.read_text().strip())
            os.kill(pid, 0)
            return False
        except (ProcessLookupError, ValueError):
            pass
    lock_path.write_text(str(os.getpid()))
    return True


def _release_lock(lock_path: Path) -> None:
    lock_path.unlink(missing_ok=True)


class SyncEngine:
    def __init__(self, config: BackupConfig) -> None:
        self._config = config
        self._s3 = S3Uploader(config.s3_bucket, config.aws_default_region)

    def incremental_backup(self, project: str, force: bool = False) -> dict[str, int]:
        cfg = self._config
        if not _acquire_lock(cfg.lock_file_path):
            raise RuntimeError("Otro backup está en ejecución. Lock activo.")

        try:
            stats = self._s3.sync_to_s3(
                local_dir=cfg.local_output_dir,
                project=project,
                state_path=cfg.sync_state_path,
                extensions=ALL_MEDIA,
                force=force,
            )
        finally:
            _release_lock(cfg.lock_file_path)

        return stats

    def get_status(self) -> dict[str, object]:
        from .s3_uploader import load_state
        state = load_state(self._config.sync_state_path)
        total = len(state)
        if not state:
            return {"total_files": 0, "last_sync": None}

        last_sync = max(v.get("synced_at", "") for v in state.values())
        return {
            "total_files": total,
            "last_sync": last_sync,
            "state_path": str(self._config.sync_state_path),
        }
