"""Configuración centralizada desde variables de entorno."""
from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///studio.db"
    exchange_api_url: str = "https://open.er-api.com/v6/latest"
    exchange_api_key: str = ""
    log_level: str = "WARNING"


settings = Settings()
