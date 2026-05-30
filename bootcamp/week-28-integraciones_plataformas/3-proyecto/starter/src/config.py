from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class DistributorConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    youtube_client_secrets: Path = Path("client_secrets.json")
    youtube_token_path: Path = Path("youtube_token.json")
    youtube_playlist: str = "Studio BC — Entregas"

    vimeo_token: str = ""
    vimeo_key: str = ""
    vimeo_secret: str = ""
    vimeo_album: str = "Studio BC"

    slack_bot_token: str = ""
    slack_channel: str = "#distribuciones"

    discord_webhook_url: str = ""

    notion_token: str = ""
    notion_database_id: str = ""


config = DistributorConfig()
