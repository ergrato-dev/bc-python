"""
Ejercicio 03: Retry con Backoff Exponencial (tenacity) — SOLUCIÓN
=================================================================
"""
from __future__ import annotations

import logging
import random
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class NetworkError(Exception):
    pass


class ValidationError(Exception):
    """Error de validación — NO se debería reintentar."""
    pass


_call_count = 0


def _unstable_api_call(fail_times: int = 2) -> dict[str, object]:
    global _call_count
    _call_count += 1
    if _call_count <= fail_times:
        raise NetworkError(f"Connection refused (intento {_call_count})")
    return {"status": "ok", "data": "respuesta exitosa"}


@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=0.1, max=2),
    retry=retry_if_exception_type(NetworkError),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def fetch_data() -> dict[str, object]:
    return _unstable_api_call(fail_times=2)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=0.1, max=5),
    retry=retry_if_exception_type(NetworkError),
    reraise=True,
)
def upload_with_retry(data: str) -> bool:
    if not data:
        raise ValidationError("data no puede estar vacío")
    if random.random() < 0.5:
        raise NetworkError("Upload timeout")
    return True


if __name__ == "__main__":
    global _call_count

    print("=== Test 1: fetch_data con retry ===")
    _call_count = 0
    result = fetch_data()
    assert result["status"] == "ok"
    print(f"OK: {result} (falló {_call_count - 1} veces antes de éxito)")

    print("\n=== Test 2: validar que ValidationError NO se reintenta ===")
    try:
        upload_with_retry("")
        print("ERROR: debería haber lanzado ValidationError")
    except ValidationError:
        print("OK: ValidationError lanzado sin retries")

    print("\n=== Test 3: NetworkError con retries ===")
    random.seed(42)
    try:
        upload_with_retry("payload")
        print("OK: upload exitoso")
    except Exception as e:
        print(f"Falló después de reintentos: {e}")

    print("\nOK — Ejercicio 03 completado")
