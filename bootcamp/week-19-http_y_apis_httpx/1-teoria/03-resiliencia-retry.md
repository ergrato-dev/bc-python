# Resiliencia y Retry

## Objetivos

- Usar `tenacity` para retry con backoff exponencial y jitter
- Configurar condiciones de stop y wait personalizadas
- Combinar retry con timeouts de httpx
- Implementar un circuit breaker básico

---

## 1. Por qué las redes fallan

Las APIs externas fallan por razones transitorias:
- Timeout de red (pico de carga, route flap)
- 503 Service Unavailable (servidor reiniciando)
- 429 Too Many Requests (rate limit)
- 500 Internal Server Error (error transitorio)

Un cliente robusto **reintenta automáticamente** errores transitorios y **falla rápido** ante errores permanentes (401, 404, 400).

---

## 2. `tenacity` — retry declarativo

```python
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def fetch_catalog(client: httpx.Client) -> list[dict]:
    response = client.get("/catalog", timeout=10.0)
    response.raise_for_status()
    return response.json()
```

### Intentos y tiempos de espera

```
Intento 1 → falla → espera 1s (1 * 2^0)
Intento 2 → falla → espera 2s (1 * 2^1)
Intento 3 → falla → espera 4s (1 * 2^2)
Intento 4 → falla → STOP (stop_after_attempt=4)
```

---

## 3. Backoff exponencial + jitter

Sin jitter, múltiples clientes reintentan al mismo tiempo (thundering herd):

```python
from tenacity import wait_exponential_jitter, wait_random_exponential

# wait_random_exponential añade jitter automáticamente
@retry(
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=1, max=30),
    # Tiempos: ~1s, ~2s, ~4s, ~8s (con variación aleatoria ±50%)
)
def fetch_with_jitter(client: httpx.Client) -> dict:
    ...
```

---

## 4. Reintentar solo errores transitorios

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}

def is_transient_error(exc: BaseException) -> bool:
    """Reintentar solo errores de red y 5xx/429. No 4xx permanentes."""
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in TRANSIENT_STATUS_CODES
    return isinstance(exc, (httpx.ConnectError, httpx.TimeoutException))

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    retry=retry_if_exception(is_transient_error),
    reraise=True,
)
def call_api(client: httpx.Client, path: str) -> dict:
    response = client.get(path, timeout=10.0)
    response.raise_for_status()   # lanza HTTPStatusError para 4xx/5xx
    return response.json()
```

---

## 5. Async con tenacity

```python
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception(is_transient_error),
    reraise=True,
)
async def fetch_async(client: httpx.AsyncClient, path: str) -> dict:
    response = await client.get(path, timeout=10.0)
    response.raise_for_status()
    return response.json()

async def main() -> None:
    async with httpx.AsyncClient(base_url="https://api.studio.bc") as client:
        data = await fetch_async(client, "/projects")
        print(data)
```

---

## 6. Timeouts de httpx como primera defensa

El retry es la segunda línea. Los timeouts son la primera:

```python
import httpx

# Timeout granular — la mayoría de los problemas son de lectura
timeout = httpx.Timeout(
    connect=3.0,   # falla rápido si el servidor no responde
    read=15.0,     # APIs lentas pueden tardar en generar la respuesta
    write=5.0,
    pool=2.0,
)

with httpx.Client(
    base_url="https://api.studio.bc",
    timeout=timeout,
) as client:
    # Si read > 15s → ReadTimeout → tenacity reintenta
    response = client.get("/heavy-report")
```

---

## 7. Circuit breaker básico

Después de N fallos consecutivos, el circuit breaker abre el circuito y falla rápido durante un período de cooldown sin intentar más llamadas:

```python
import time
from dataclasses import dataclass, field

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    cooldown_secs: float = 60.0
    _failures: int = 0
    _opened_at: float = 0.0

    @property
    def is_open(self) -> bool:
        if self._failures >= self.failure_threshold:
            if time.time() - self._opened_at < self.cooldown_secs:
                return True
            self._failures = 0   # cooldown expiró → half-open
        return False

    def record_success(self) -> None:
        self._failures = 0

    def record_failure(self) -> None:
        self._failures += 1
        if self._failures >= self.failure_threshold:
            self._opened_at = time.time()

# Integración con el cliente
_cb = CircuitBreaker()

def call_with_circuit_breaker(client: httpx.Client, path: str) -> dict:
    if _cb.is_open:
        raise RuntimeError("Circuit breaker open — skipping request")
    try:
        response = client.get(path, timeout=10.0)
        response.raise_for_status()
        _cb.record_success()
        return response.json()
    except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError) as e:
        _cb.record_failure()
        raise
```

> En producción usa la biblioteca `circuitbreaker` o el equivalente en tu framework de observabilidad.

---

## ✅ Resumen

| Herramienta | Propósito |
|------------|-----------|
| `@retry(stop=stop_after_attempt(N))` | Reintentar hasta N veces |
| `wait_random_exponential(max=30)` | Backoff con jitter — evita thundering herd |
| `retry_if_exception(fn)` | Reintentar solo si la excepción es transitoria |
| `httpx.Timeout(connect=, read=)` | Primera defensa — falla rápido |
| Circuit breaker | No intentar si el servicio está caído |

---

## Recursos Adicionales

- [tenacity docs](https://tenacity.readthedocs.io/)
- [httpx — Timeouts](https://www.python-httpx.org/advanced/timeouts/)
