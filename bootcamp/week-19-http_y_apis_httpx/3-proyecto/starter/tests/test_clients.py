"""Tests para MusicClient y RenderClient."""
from __future__ import annotations

import pytest
import httpx
from src.auth import APIKeyAuth, BearerAuth
from src.retry import is_transient_error
from src.models import Track, TrackSearch, RenderJob, RenderJobCreated


# ── Auth tests ────────────────────────────────────────────────────────────────

def test_api_key_auth_injects_header() -> None:
    """APIKeyAuth debe inyectar el header X-API-Key en cada request."""
    auth = APIKeyAuth("test-key-123")
    # TODO: crea una request dummy y verifica que el header se inyecta
    # Pista: list(auth.auth_flow(request)) ejecuta el generator
    pytest.skip("implementar")


def test_bearer_auth_injects_header() -> None:
    """BearerAuth debe inyectar Authorization: Bearer <token>."""
    auth = BearerAuth("my-token")
    pytest.skip("implementar")


# ── Retry classification ──────────────────────────────────────────────────────

class FakeResp:
    def __init__(self, code: int):
        self.status_code = code


@pytest.mark.parametrize("code,expected", [
    (200, False),
    (400, False),
    (401, False),
    (404, False),
    (429, True),
    (500, True),
    (503, True),
    (504, True),
])
def test_is_transient_error_http(code: int, expected: bool) -> None:
    exc = httpx.HTTPStatusError(
        "test", request=httpx.Request("GET", "http://test"), response=FakeResp(code)  # type: ignore
    )
    try:
        assert is_transient_error(exc) == expected
    except NotImplementedError:
        pytest.skip("is_transient_error no implementado")


def test_is_transient_connect_error() -> None:
    exc = httpx.ConnectError("down")
    try:
        assert is_transient_error(exc) is True
    except NotImplementedError:
        pytest.skip("is_transient_error no implementado")


# ── Model validation ──────────────────────────────────────────────────────────

def test_track_model() -> None:
    data = {
        "track_id": "t1",
        "title": "Cinematic Dawn",
        "artist": "Luna BC",
        "duration_secs": 60,
        "genre": "cinematic",
        "license_type": "royalty-free",
        "price_usd": 29.99,
    }
    try:
        track = Track.model_validate(data)
        assert track.track_id == "t1"
    except Exception as e:
        pytest.skip(f"Track model not implemented: {e}")


def test_render_job_model() -> None:
    data = {
        "job_id": "job-001",
        "status": "queued",
        "progress": 0.0,
        "output_url": None,
        "created_at": "2025-01-01T00:00:00Z",
    }
    try:
        job = RenderJob.model_validate(data)
        assert job.job_id == "job-001"
    except Exception as e:
        pytest.skip(f"RenderJob model not implemented: {e}")
