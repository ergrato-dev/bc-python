"""Servicio de tipos de cambio — convierte async a sync para CLI."""
from __future__ import annotations

import asyncio
import httpx
from ..api_clients.exchange import exchange_client
from ..exceptions import ExternalServiceError


class ExchangeService:
    def get_ars_rate(self) -> float:
        """Obtiene ARS/USD de forma sincrónica."""
        try:
            return asyncio.run(self._fetch_ars())
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            raise ExternalServiceError(f"No se pudo contactar el servicio de cambio: {e}") from e
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(f"Error {e.response.status_code} del servicio") from e
        except NotImplementedError:
            # ExchangeClient no implementado aún — retornar tasa stub
            return 1050.0

    async def _fetch_ars(self) -> float:
        rates = await exchange_client.get_rates("USD")
        return rates.rates.get("ARS", 1.0)

    def convert(self, amount_usd: float) -> float:
        return amount_usd * self.get_ars_rate()


exchange_service = ExchangeService()
