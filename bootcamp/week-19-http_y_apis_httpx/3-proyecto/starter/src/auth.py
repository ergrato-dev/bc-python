"""Clases de autenticación httpx.Auth para los proveedores de Studio BC."""
from __future__ import annotations

from typing import Generator
import httpx


class APIKeyAuth(httpx.Auth):
    """Inyecta X-API-Key (u otro header) en cada request."""

    def __init__(self, api_key: str, header_name: str = "X-API-Key") -> None:
        # TODO
        raise NotImplementedError

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        # TODO
        raise NotImplementedError


class BearerAuth(httpx.Auth):
    """Inyecta Authorization: Bearer <token> en cada request."""

    def __init__(self, token: str) -> None:
        # TODO
        raise NotImplementedError

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        # TODO
        raise NotImplementedError
