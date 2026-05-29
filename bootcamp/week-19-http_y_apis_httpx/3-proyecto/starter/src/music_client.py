"""Cliente para MusicLicensing BC."""
from __future__ import annotations

import httpx
from .auth import APIKeyAuth
from .models import Track, TrackSearch
from .retry import MUSIC_RETRY

DEFAULT_TIMEOUT = httpx.Timeout(connect=3.0, read=15.0, write=5.0, pool=2.0)


class MusicClient:
    """Cliente de MusicLicensing BC con auth por API Key, timeouts y retry."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.musiclicensing.bc",
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            auth=APIKeyAuth(api_key),
            timeout=DEFAULT_TIMEOUT,
            headers={"User-Agent": "studio-bc-client/1.0"},
        )

    def __enter__(self) -> "MusicClient":
        return self

    def __exit__(self, *args: object) -> None:
        self._client.close()

    @MUSIC_RETRY
    def search_tracks(self, genre: str, max_duration: int = 120) -> TrackSearch:
        """
        Busca pistas por género y duración máxima.
        GET /tracks?genre=<genre>&max_duration=<max_duration>
        Retorna TrackSearch validado con Pydantic.
        """
        # TODO: GET /tracks con params
        # TODO: response.raise_for_status()
        # TODO: return TrackSearch.model_validate(response.json())
        raise NotImplementedError

    @MUSIC_RETRY
    def get_track(self, track_id: str) -> Track:
        """
        Obtiene una pista por ID.
        GET /tracks/<track_id>
        Retorna Track validado con Pydantic.
        """
        # TODO
        raise NotImplementedError
