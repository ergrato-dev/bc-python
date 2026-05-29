"""
Studio BC — Validators
TypeGuard functions for runtime type checking and narrowing.
"""

from __future__ import annotations

from datetime import date
from typing import TypeGuard

from src.models import Asset, Project


def is_video_asset(asset: Asset) -> TypeGuard[Asset]:
    """Return True if asset is a video asset."""
    # TODO: return True when asset.asset_type == "video"
    return False


def is_image_asset(asset: Asset) -> TypeGuard[Asset]:
    """Return True if asset is an image asset."""
    # TODO: return True when asset.asset_type == "image"
    return False


def is_uploadable(obj: object) -> TypeGuard[Asset]:
    """Return True if obj is an Asset with a non-empty file_path."""
    # TODO: check that obj has name, file_path, asset_type attributes
    # and that file_path is a non-empty string
    return False


def is_active_project(obj: object) -> TypeGuard[Project]:
    """Return True if obj is a Project whose end_date >= today."""
    # TODO: check obj is a Project instance and end_date >= date.today()
    return False
