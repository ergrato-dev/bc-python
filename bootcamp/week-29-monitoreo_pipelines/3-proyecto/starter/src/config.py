"""Settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    slack_webhook: str = field(default_factory=lambda: os.getenv("SLACK_WEBHOOK", ""))
    state_file: str = field(default_factory=lambda: os.getenv("STATE_FILE", ".sync_state.json"))
    redis_url: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    disk_min_free_gb: float = field(default_factory=lambda: float(os.getenv("DISK_MIN_FREE_GB", "5.0")))
    alert_cooldown_s: float = field(default_factory=lambda: float(os.getenv("ALERT_COOLDOWN_S", "60.0")))
    watchdog_timeout_s: float = field(default_factory=lambda: float(os.getenv("WATCHDOG_TIMEOUT_S", "30.0")))
    dashboard_refresh_s: float = field(default_factory=lambda: float(os.getenv("DASHBOARD_REFRESH_S", "1.0")))
    dry_run: bool = field(default_factory=lambda: os.getenv("DRY_RUN", "true").lower() == "true")


def load_settings() -> Settings:
    return Settings()
