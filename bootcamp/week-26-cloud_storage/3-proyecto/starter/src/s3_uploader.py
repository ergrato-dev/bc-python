from __future__ import annotations

import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


SyncState = dict[str, dict[str, str]]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_state(state_path: Path) -> SyncState:
    if state_path.exists():
        return json.loads(state_path.read_text())  # type: ignore[no-any-return]
    return {}


def save_state(state: SyncState, state_path: Path) -> None:
    tmp = state_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    tmp.replace(state_path)


def _needs_upload(path: Path, state: SyncState) -> bool:
    key = str(path)
    if key not in state:
        return True
    return sha256_file(path) != state[key].get("sha256", "")


def _build_s3_key(path: Path, local_dir: Path, project: str) -> str:
    date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    media_type = _classify_media_type(path)
    relative = path.relative_to(local_dir)
    return f"{project}/{media_type}/{date_prefix}/{relative}".replace("\\", "/")


def _classify_media_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".mp4", ".mov", ".mxf", ".avi", ".mkv", ".prores"}:
        return "video"
    if ext in {".mp3", ".wav", ".flac", ".aac", ".aiff"}:
        return "audio"
    if ext in {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".raw", ".arw"}:
        return "image"
    if ext in {".pdf", ".docx", ".xlsx", ".pptx", ".txt"}:
        return "doc"
    return "other"


class S3Uploader:
    def __init__(self, bucket: str, region: str = "us-east-1") -> None:
        self._bucket = bucket
        self._s3 = boto3.client("s3", region_name=region)

    def upload_file(self, local_path: Path, key: str, metadata: dict[str, str] | None = None) -> None:
        mime_type, _ = mimetypes.guess_type(str(local_path))
        extra: dict[str, object] = {
            "ContentType": mime_type or "application/octet-stream",
        }
        if metadata:
            extra["Metadata"] = metadata
        self._s3.upload_file(str(local_path), self._bucket, key, ExtraArgs=extra)

    def generate_download_url(self, key: str, expires_in: int = 3600) -> str:
        url: str = self._s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=expires_in,
        )
        return url

    def sync_to_s3(
        self,
        local_dir: Path,
        project: str,
        state_path: Path,
        extensions: set[str] | None = None,
        force: bool = False,
    ) -> dict[str, int]:
        state = load_state(state_path)
        stats: dict[str, int] = {"uploaded": 0, "skipped": 0, "errors": 0}

        for path in local_dir.rglob("*"):
            if not path.is_file():
                continue
            if extensions and path.suffix.lower() not in extensions:
                continue
            if not force and not _needs_upload(path, state):
                stats["skipped"] += 1
                continue

            key = _build_s3_key(path, local_dir, project)
            try:
                self.upload_file(path, key, metadata={"project": project})
                state[str(path)] = {
                    "sha256": sha256_file(path),
                    "s3_key": key,
                    "synced_at": datetime.now(timezone.utc).isoformat(),
                }
                stats["uploaded"] += 1
            except ClientError as e:
                print(f"Error subiendo {path.name}: {e}")
                stats["errors"] += 1

        save_state(state, state_path)
        return stats
