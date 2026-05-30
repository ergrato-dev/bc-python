"""
Ejercicio 03: Retry con Backoff Exponencial (tenacity)
======================================================
Implementa funciones con retry usando tenacity: backoff exponencial,
condición por tipo de excepción, y callback de logging.

Instalar: pip install tenacity
Ejecutar: python main.py
"""
from __future__ import annotations

import logging
import random
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class NetworkError(Exception):
    pass


class ValidationError(Exception):
    """Error de validación — NO se debería reintentar."""
    pass


# Simulador de API inestable
_call_count = 0

def _unstable_api_call(fail_times: int = 2) -> dict[str, object]:
    global _call_count
    _call_count += 1
    if _call_count <= fail_times:
        raise NetworkError(f"Connection refused (intento {_call_count})")
    return {"status": "ok", "data": "respuesta exitosa"}


# ── TODO 1 ─────────────────────────────────────────────────────────────────────
# Decorar fetch_data con @retry:
#   - max 4 intentos
#   - backoff exponencial: multiplier=1, min=0.1, max=2 (valores bajos para pruebas)
#   - solo reintentar NetworkError
#   - loggear antes de cada espera con before_sleep_log(logger, logging.WARNING)

def fetch_data() -> dict[str, object]:
    return _unstable_api_call(fail_times=2)


# ── TODO 2 ─────────────────────────────────────────────────────────────────────
# Implementar upload_with_retry:
#   - max 3 intentos
#   - backoff exponencial: multiplier=2, min=0.1, max=5
#   - reraise=True para que el error final se propague
#   - NO reintentar ValidationError (solo Exception genérica)

def upload_with_retry(data: str) -> bool:
    if not data:
        raise ValidationError("data no puede estar vacío")
    # Simular fallo 50% del tiempo
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
    from tenacity import RetryError
    try:
        upload_with_retry("")
        print("ERROR: debería haber lanzado ValidationError")
    except ValidationError:
        print("OK: ValidationError lanzado sin retries")

    print("\n=== Test 3: NetworkError con retries ===")
    random.seed(42)  # reproducible
    try:
        upload_with_retry("payload")
        print("OK: upload exitoso")
    except Exception as e:
        print(f"Falló después de reintentos: {e}")

    print("\nOK — Ejercicio 03 completado")
