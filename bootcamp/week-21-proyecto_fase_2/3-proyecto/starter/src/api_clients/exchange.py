"""Cliente httpx async para tipos de cambio."""
from __future__ import annotations

import httpx
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from ..config import settings


def _is_retriable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {429, 500, 502, 503, 504}
    return isinstance(exc, (httpx.ConnectError, httpx.TimeoutException))


class ExchangeRates(BaseModel):
    base_code: str
    rates: dict[str, float]


class ExchangeClient:
    def __init__(self) -> None:
        self._timeout = httpx.Timeout(connect=3.0, read=10.0)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception(_is_retriable),
        reraise=True,
    )
    async def get_rates(self, base: str = "USD") -> ExchangeRates:
        """GET /latest/{base} → ExchangeRates validado con Pydantic."""
        # TODO: usar httpx.AsyncClient con self._timeout
        # TODO: response.raise_for_status()
        # TODO: return ExchangeRates.model_validate(response.json())
        raise NotImplementedError


exchange_client = ExchangeClient()
