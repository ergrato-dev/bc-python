"""
Ejercicio 03 — Retry con tenacity
===================================
Practica el manejo de errores transitorios con reintentos inteligentes.

Usamos httpbin.org para simular errores:
  /status/500  → fuerza un 500 Internal Server Error
  /status/429  → fuerza un 429 Too Many Requests
  /status/200  → respuesta exitosa

Tareas:
  1. [call_with_retry]         Retry básico con stop + wait + retry_if_exception_type
  2. [is_transient_error]      Función que devuelve True solo para errores transitorios
  3. [call_smart_retry]        Retry solo en errores transitorios, falla en 4xx permanentes
  4. [async_retry]             Versión async de call_smart_retry
  5. [simulate_flaky_service]  Forzar N fallos y luego éxito usando un contador

Ejecutar: python main.py
"""
from __future__ import annotations

import asyncio
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_random_exponential,
    retry_if_exception_type,
    retry_if_exception,
    RetryCallState,
    before_sleep_log,
)
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

BASE_URL = "https://httpbin.org"
TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


# ── Tarea 1 — Retry básico ────────────────────────────────────────────────────

@retry(
    # TODO: stop=stop_after_attempt(3)
    # TODO: wait=wait_exponential(multiplier=1, min=1, max=8)
    # TODO: retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException))
    # TODO: reraise=True
)
def call_with_retry(client: httpx.Client, path: str) -> dict:
    """Reintenta solo en errores de red (no en 4xx/5xx del servidor)."""
    response = client.get(path, timeout=10.0)
    response.raise_for_status()
    return response.json()


# ── Tarea 2 — Función de clasificación ────────────────────────────────────────

def is_transient_error(exc: BaseException) -> bool:
    """
    Retorna True si el error es transitorio y vale la pena reintentar.

    Transitorio:
      - httpx.ConnectError, httpx.TimeoutException (errores de red)
      - httpx.HTTPStatusError con status_code en TRANSIENT_STATUS_CODES

    Permanente (retorna False):
      - httpx.HTTPStatusError con 4xx (400, 401, 403, 404, etc.) excepto 429
    """
    # TODO: implementar la lógica
    raise NotImplementedError


# ── Tarea 3 — Retry inteligente ───────────────────────────────────────────────

@retry(
    # TODO: stop=stop_after_attempt(4)
    # TODO: wait=wait_random_exponential(multiplier=1, max=20)
    # TODO: retry=retry_if_exception(is_transient_error)
    # TODO: reraise=True
    # TODO: before_sleep=before_sleep_log(logger, logging.WARNING)
)
def call_smart_retry(client: httpx.Client, path: str) -> dict:
    """
    Reintenta errores transitorios (5xx, 429, ConnectError, Timeout).
    Falla inmediatamente ante errores permanentes (4xx excepto 429).
    """
    response = client.get(path, timeout=10.0)
    response.raise_for_status()
    return response.json()


# ── Tarea 4 — Async retry ─────────────────────────────────────────────────────

@retry(
    # TODO: mismos parámetros que call_smart_retry
)
async def async_smart_retry(client: httpx.AsyncClient, path: str) -> dict:
    """Versión async de call_smart_retry."""
    # TODO: await client.get(path, timeout=10.0)
    # TODO: response.raise_for_status()
    # TODO: return response.json()
    raise NotImplementedError


# ── Tarea 5 — Simular servicio inestable ──────────────────────────────────────

class FlakyServer:
    """
    Simula un servidor que falla las primeras `fail_count` llamadas
    y luego responde correctamente.

    Uso con respuestas reales: monkeypatching del transport o
    wrapping de httpx.Client para contar llamadas.
    """

    def __init__(self, fail_count: int = 2) -> None:
        self.fail_count = fail_count
        self._calls = 0

    def call(self) -> str:
        """
        Simula una llamada HTTP:
        - Primeras `fail_count` llamadas: lanza httpx.ConnectError
        - Siguiente: retorna "success"
        """
        self._calls += 1
        # TODO: si self._calls <= self.fail_count:
        #           raise httpx.ConnectError("server down")
        # TODO: return "success"
        raise NotImplementedError

    @property
    def total_calls(self) -> int:
        return self._calls


def call_flaky_with_retry(server: FlakyServer) -> str:
    """Decora server.call() con retry y retorna el resultado exitoso."""
    # TODO: Envuelve server.call() en un @retry decorador o llama manualmente
    # Pista: puedes usar retry()(server.call) o definir una función interna
    raise NotImplementedError


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=== Tarea 1: retry básico (solo errores de red) ===")
    with httpx.Client(base_url=BASE_URL) as client:
        try:
            # /status/200 debe funcionar
            data = call_with_retry(client, "/status/200")
            print(f"  OK: /status/200")
        except Exception as e:
            print(f"  Error: {e}")

        try:
            # /status/500 NO se reintenta (solo reintenta ConnectError/Timeout)
            call_with_retry(client, "/status/500")
        except httpx.HTTPStatusError as e:
            print(f"  HTTPStatusError {e.response.status_code} (esperado — no reintenta 5xx)")

    print("\n=== Tarea 2: is_transient_error ===")
    # Test manual
    class FakeResponse:
        def __init__(self, code: int):
            self.status_code = code

    for code in [200, 400, 401, 404, 429, 500, 503]:
        fake_exc = httpx.HTTPStatusError("test", request=None, response=FakeResponse(code))  # type: ignore
        try:
            result = is_transient_error(fake_exc)
            print(f"  {code}: transitorio={result}")
        except NotImplementedError:
            print("  Tarea 2 no implementada aún")
            break

    print("\n=== Tarea 3: retry inteligente ===")
    with httpx.Client(base_url=BASE_URL) as client:
        try:
            # 404 es permanente — falla inmediatamente sin reintentar
            call_smart_retry(client, "/status/404")
        except httpx.HTTPStatusError as e:
            print(f"  404 falla inmediato (esperado): {e.response.status_code}")
        except NotImplementedError:
            print("  Tarea 3 no implementada aún")

    print("\n=== Tarea 4: async retry ===")
    async def run_async() -> None:
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            try:
                data = await async_smart_retry(client, "/status/200")
                print(f"  Async OK")
            except NotImplementedError:
                print("  Tarea 4 no implementada aún")
    asyncio.run(run_async())

    print("\n=== Tarea 5: flaky server ===")
    server = FlakyServer(fail_count=2)
    try:
        result = call_flaky_with_retry(server)
        print(f"  Resultado: {result} (llamadas totales: {server.total_calls})")
        assert server.total_calls == 3, f"Esperaba 3 llamadas, hubo {server.total_calls}"
        print("  OK — reintentó 2 veces y tuvo éxito en el 3er intento")
    except NotImplementedError:
        print("  Tarea 5 no implementada aún")


if __name__ == "__main__":
    main()
