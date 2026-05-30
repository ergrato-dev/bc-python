from __future__ import annotations
import os


class AIConfig:
    vision_model: str = os.getenv("VISION_MODEL", "gpt-4o")
    text_model: str = os.getenv("TEXT_MODEL", "gpt-4o-mini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    max_tags: int = int(os.getenv("MAX_TAGS", "12"))
    max_frames: int = int(os.getenv("MAX_FRAMES", "5"))
    min_chapter_s: float = float(os.getenv("MIN_CHAPTER_S", "60.0"))
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() == "true"
