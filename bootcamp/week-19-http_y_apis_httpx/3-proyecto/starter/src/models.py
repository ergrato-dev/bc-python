"""Pydantic models para MusicLicensing BC y CloudRender BC."""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


# ── MusicLicensing BC ──────────────────────────────────────────────────────────

class Track(BaseModel):
    # TODO: track_id, title, artist, duration_secs, genre, license_type, price_usd
    pass


class TrackSearch(BaseModel):
    # TODO: results (list[Track]), total (int), page (int)
    pass


# ── CloudRender BC ─────────────────────────────────────────────────────────────

class RenderJob(BaseModel):
    # TODO: job_id, status, progress (0.0–100.0), output_url (optional), created_at (datetime)
    pass


class RenderJobCreated(BaseModel):
    # TODO: job_id, estimated_secs
    pass
