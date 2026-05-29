# Rate Limiting

## Objetivos

- Entender cómo las APIs imponen límites de tasa
- Implementar un token bucket para limitar llamadas salientes
- Respetar el header `Retry-After` para backoff reactivo
- Medir ventanas deslizantes con timestamps

---

## 1. Por qué existe el rate limiting

Las APIs limitan peticiones para:
- Proteger infraestructura (evitar DDoS accidentales)
- Garantizar equidad entre clientes
- Forzar upgrades de plan

Cuando se supera el límite: **429 Too Many Requests**.

```
Headers comunes en la respuesta:
  X-RateLimit-Limit: 100          # límite total en la ventana
  X-RateLimit-Remaining: 0        # llamadas restantes
  X-RateLimit-Reset: 1716900060   # timestamp cuando se resetea
  Retry-After: 30                 # segundos hasta próximo intento
```

---

## 2. Token Bucket — limitar llamadas salientes

El token bucket acumula tokens a una tasa fija. Cada llamada consume un token. Si no hay tokens, espera.

```python
import time
import threading
from dataclasses import dataclass, field

@dataclass
class TokenBucket:
    """Token bucket para rate limiting en el cliente."""
    rate: float          # tokens por segundo
    capacity: float      # máximo de tokens acumulados
    _tokens: float = field(init=False)
    _last_refill: float = field(init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self) -> None:
        self._tokens = self.capacity
        self._last_refill = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        self._last_refill = now

    def acquire(self, tokens: float = 1.0) -> None:
        """Bloquea hasta que haya tokens disponibles."""
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                wait = (tokens - self._tokens) / self.rate
            time.sleep(wait)

# 10 llamadas/segundo, ráfaga máx de 20
bucket = TokenBucket(rate=10.0, capacity=20.0)

import httpx

def throttled_get(client: httpx.Client, path: str) -> dict:
    bucket.acquire()
    response = client.get(path, timeout=10.0)
    response.raise_for_status()
    return response.json()
```

---

## 3. Responder al header `Retry-After`

El servidor indica cuánto esperar. El cliente lo lee y espera exactamente eso:

```python
import time
import httpx

def call_with_retry_after(client: httpx.Client, path: str) -> dict:
    """Respeta el header Retry-After en respuestas 429."""
    while True:
        response = client.get(path, timeout=10.0)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "1")
            wait_secs = float(retry_after)
            print(f"Rate limited — esperando {wait_secs}s")
            time.sleep(wait_secs)
            continue

        response.raise_for_status()
        return response.json()
```

### Combinando tenacity + Retry-After

```python
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    retry_if_exception_type,
    RetryCallState,
)

def wait_for_retry_after(retry_state: RetryCallState) -> float:
    """Extrae el tiempo de espera del header Retry-After si está disponible."""
    exc = retry_state.outcome.exception()
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429:
        retry_after = exc.response.headers.get("Retry-After")
        if retry_after:
            return float(retry_after)
    return 2.0  # fallback

@retry(
    stop=stop_after_attempt(5),
    wait=wait_for_retry_after,
    retry=retry_if_exception_type(httpx.HTTPStatusError),
    reraise=True,
)
def fetch_respecting_limits(client: httpx.Client, path: str) -> dict:
    response = client.get(path, timeout=10.0)
    response.raise_for_status()
    return response.json()
```

---

## 4. Ventana deslizante (sliding window)

El token bucket controla la ráfaga. La ventana deslizante controla el total en una ventana de tiempo:

```python
import time
import collections
import threading
from dataclasses import dataclass, field

@dataclass
class SlidingWindowLimiter:
    """Máx `max_calls` llamadas en los últimos `window_secs` segundos."""
    max_calls: int
    window_secs: float
    _timestamps: collections.deque = field(
        default_factory=collections.deque, init=False
    )
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def acquire(self) -> None:
        while True:
            with self._lock:
                now = time.monotonic()
                # Eliminar timestamps fuera de la ventana
                cutoff = now - self.window_secs
                while self._timestamps and self._timestamps[0] < cutoff:
                    self._timestamps.popleft()

                if len(self._timestamps) < self.max_calls:
                    self._timestamps.append(now)
                    return

                # Esperar hasta que la llamada más antigua salga de la ventana
                wait = self._timestamps[0] + self.window_secs - now

            time.sleep(wait)

# 100 llamadas por minuto
limiter = SlidingWindowLimiter(max_calls=100, window_secs=60.0)
```

---

## 5. Async token bucket

Para código con `asyncio`:

```python
import asyncio
import time
from dataclasses import dataclass, field

@dataclass
class AsyncTokenBucket:
    rate: float
    capacity: float
    _tokens: float = field(init=False)
    _last_refill: float = field(init=False)

    def __post_init__(self) -> None:
        self._tokens = self.capacity
        self._last_refill = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        self._tokens = min(
            self.capacity,
            self._tokens + (now - self._last_refill) * self.rate,
        )
        self._last_refill = now

    async def acquire(self, tokens: float = 1.0) -> None:
        while True:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return
            wait = (tokens - self._tokens) / self.rate
            await asyncio.sleep(wait)

# Uso en async
async_bucket = AsyncTokenBucket(rate=5.0, capacity=10.0)

async def throttled_fetch(client: httpx.AsyncClient, path: str) -> dict:
    await async_bucket.acquire()
    response = await client.get(path, timeout=10.0)
    response.raise_for_status()
    return response.json()
```

---

## ✅ Resumen

| Técnica | Propósito | Implementación |
|---------|-----------|----------------|
| Token bucket | Limitar ráfagas salientes | `TokenBucket.acquire()` |
| Sliding window | Límite total en ventana temporal | `SlidingWindowLimiter.acquire()` |
| `Retry-After` | Respetar límite impuesto por el servidor | `response.headers.get("Retry-After")` |
| Tenacity + `Retry-After` | Backoff reactivo | `wait=wait_for_retry_after` |

---

## Recursos Adicionales

- [MDN — Retry-After header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After)
- [Token bucket — Wikipedia](https://en.wikipedia.org/wiki/Token_bucket)
