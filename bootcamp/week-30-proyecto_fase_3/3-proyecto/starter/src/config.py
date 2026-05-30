from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # AWS
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "us-east-1"
    s3_bucket: str = "studio-bc-prod-assets"

    # Google Drive
    google_credentials_path: Path = Path("credentials.json")

    # Slack
    slack_webhook_url: str = ""

    # Pipeline
    project_slug: str = "studio-bc/default"
    drop_dir: Path = Path("drop")
    output_dir: Path = Path("output")
    state_file: Path = Path(".pipeline_state.json")
    watchdog_timeout_s: float = 30.0
    dry_run: bool = True

    def ensure_dirs(self) -> None:
        self.drop_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "proxy").mkdir(exist_ok=True)
        (self.output_dir / "thumbs").mkdir(exist_ok=True)
        (self.output_dir / "web").mkdir(exist_ok=True)
