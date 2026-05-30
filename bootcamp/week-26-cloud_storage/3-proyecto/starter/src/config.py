from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackupConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "us-east-1"
    s3_bucket: str = "studio-bc-prod-assets"

    google_credentials_path: Path = Path("credentials.json")
    drive_root_folder: str = "Studio BC"

    local_output_dir: Path = Path("output")
    sync_state_path: Path = Path(".sync_state.json")
    lock_file_path: Path = Path(".backup.lock")


config = BackupConfig()
