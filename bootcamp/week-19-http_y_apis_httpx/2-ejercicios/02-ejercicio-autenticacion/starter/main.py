"""
Ejercicio 02 — Autenticación con httpx.Auth
============================================
Implementa clases de autenticación personalizadas y un flujo OAuth2 simulado.

Tareas:
  1. [APIKeyAuth]            Implementar httpx.Auth que inyecta X-API-Key
  2. [BearerAuth]            Implementar httpx.Auth que inyecta Authorization: Bearer
  3. [verify_auth_headers]   Usar httpbin.org para verificar que los headers llegan
  4. [OAuth2ClientCredentials] Implementar refresh automático del token

Ejecutar: python main.py
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Generator

import httpx


HTTPBIN = "https://httpbin.org"


# ── Tarea 1 — API Key Auth ────────────────────────────────────────────────────

class APIKeyAuth(httpx.Auth):
    """Inyecta X-API-Key (o el header configurado) en cada request."""

    def __init__(self, api_key: str, header_name: str = "X-API-Key") -> None:
        # TODO: guardar api_key y header_name como atributos
        raise NotImplementedError

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        # TODO: añadir self.api_key al header self.header_name del request
        # TODO: yield request
        raise NotImplementedError


# ── Tarea 2 — Bearer Token Auth ───────────────────────────────────────────────

class BearerAuth(httpx.Auth):
    """Inyecta Authorization: Bearer <token> en cada request."""

    def __init__(self, token: str) -> None:
        # TODO: guardar token
        raise NotImplementedError

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        # TODO: request.headers["Authorization"] = f"Bearer {self.token}"
        # TODO: yield request
        raise NotImplementedError


# ── Tarea 3 — Verificar headers con httpbin ───────────────────────────────────

def verify_auth_headers() -> None:
    """
    Llama a GET https://httpbin.org/headers y verifica que el header de auth
    aparece en la respuesta. httpbin devuelve los headers recibidos como JSON.
    """
    print("--- API Key ---")
    # TODO: Usa httpx.Client(base_url=HTTPBIN, auth=APIKeyAuth("test-key-123"))
    # TODO: GET /headers — imprime el dict de headers que devuelve httpbin
    # TODO: Verifica que "X-Api-Key" (httpbin normaliza) está en la respuesta

    print("--- Bearer Token ---")
    # TODO: Usa httpx.Client(base_url=HTTPBIN, auth=BearerAuth("my-jwt-token"))
    # TODO: GET /headers — verifica que "Authorization" tiene "Bearer my-jwt-token"


# ── Tarea 4 — OAuth2 simulado (token en memoria) ──────────────────────────────

@dataclass
class FakeToken:
    access_token: str
    expires_at: float

    @property
    def is_expired(self) -> bool:
        return time.time() >= self.expires_at - 10   # 10s de margen


class FakeOAuth2Auth(httpx.Auth):
    """
    Simula OAuth2 client credentials:
    - El primer request "obtiene" un token (expires_in=60s)
    - Los siguientes reutilizan el token mientras no expire
    - Si el token está expirado, obtiene uno nuevo

    Como no hay servidor real, usa un token hardcoded con TTL real.
    """

    def __init__(self, client_id: str) -> None:
        self.client_id = client_id
        self._token: FakeToken | None = None

    def _issue_token(self) -> FakeToken:
        """Simula la obtención del token (en producción: POST /token)."""
        return FakeToken(
            access_token=f"fake-token-{self.client_id}-{int(time.time())}",
            expires_at=time.time() + 60.0,
        )

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        # TODO: Si self._token es None o está expirado, llama a self._issue_token()
        # TODO: Inyecta el token como Bearer en el header Authorization
        # TODO: yield request
        raise NotImplementedError


def verify_oauth2() -> None:
    """Verifica que FakeOAuth2Auth reutiliza el token entre requests."""
    print("--- OAuth2 (simulado) ---")
    auth = FakeOAuth2Auth("studio-bc")

    with httpx.Client(base_url=HTTPBIN, auth=auth) as client:
        r1 = client.get("/headers")
        r1.raise_for_status()
        token_1 = r1.json()["headers"].get("Authorization", "")

        r2 = client.get("/headers")
        r2.raise_for_status()
        token_2 = r2.json()["headers"].get("Authorization", "")

    # El token debe ser el mismo en ambas llamadas (no expired)
    assert token_1 == token_2, "El token debería reutilizarse"
    print(f"  Token reutilizado: {token_1[:40]}...")
    print("  OK — mismo token en ambas llamadas")


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    verify_auth_headers()
    verify_oauth2()


if __name__ == "__main__":
    main()
