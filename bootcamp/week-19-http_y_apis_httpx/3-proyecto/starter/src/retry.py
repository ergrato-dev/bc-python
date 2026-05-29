"""Estrategia de retry centralizada para todos los clientes."""
from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception

TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


def is_transient_error(exc: BaseException) -> bool:
    """
    Retorna True para errores transitorios que vale la pena reintentar.
    - ConnectError, TimeoutException → siempre transitorio
    - HTTPStatusError con 429/5xx → transitorio
    - HTTPStatusError con 4xx (excepto 429) → permanente (False)
    """
    # TODO
    raise NotImplementedError


# Decorador pre-configurado para MusicLicensing BC
# stop=3 intentos, wait=random exponential max=20s
MUSIC_RETRY = retry(
    # TODO
)

# Decorador pre-configurado para CloudRender BC
# stop=4 intentos, wait=random exponential max=30s
RENDER_RETRY = retry(
    # TODO
)
