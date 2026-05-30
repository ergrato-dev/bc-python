"""Perfiles de thumbnail para Studio BC."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ThumbProfile:
    name: str
    max_width: int
    max_height: int
    fmt: str      # "WEBP" | "TIFF" | "JPEG"
    quality: int
    fit: bool = False  # True = ImageOps.fit (crop), False = thumbnail (proporcional)


PROFILES: list[ThumbProfile] = [
    ThumbProfile("web",    1200, 800,  "WEBP", 85, fit=False),
    ThumbProfile("social", 1080, 1080, "WEBP", 85, fit=True),
    ThumbProfile("thumb",  300,  300,  "WEBP", 80, fit=True),
    ThumbProfile("print",  3000, 2000, "TIFF", 100, fit=False),
]
