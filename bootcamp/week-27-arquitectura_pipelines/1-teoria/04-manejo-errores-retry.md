# Manejo de Errores y Retry

## 1. El Problema del Retry Manual

```python
# Forma ingenua — frágil y duplicada
for attempt in range(3):
    try:
        result = upload_to_s3(path)
        break
    except Exception:
        if attempt == 2:
            raise
        time.sleep(2 ** attempt)
```

`tenacity` reemplaza este patrón con decoradores declarativos.

---

## 2. `tenacity` — Retry Declarativo

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
)
def fetch_exchange_rate(currency: str) -> float:
    resp = httpx.get(f"https://api.example.com/rates/{currency}", timeout=5.0)
    resp.raise_for_status()
    return float(resp.json()["rate"])
```

- `stop_after_attempt(3)` — máximo 3 intentos
- `wait_exponential(multiplier=1, min=1, max=10)` — espera 1s, 2s, 4s (máx 10s)
- `retry_if_exception_type(...)` — solo reintenta para esas excepciones

---

## 3. Callbacks de Retry

```python
import logging
from tenacity import before_sleep_log, after_log

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO),
)
def upload_to_s3(path: str, bucket: str) -> None:
    ...
```

`before_sleep_log` loggea automáticamente cuántos intentos quedan y cuánto espera.

---

## 4. Retry en Etapas de Pipeline

```python
from __future__ import annotations
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class StageResult:
    success: bool
    data: dict[str, object]
    error: str | None = None


class RetryableStage:
    """Envuelve una etapa y reintenta su process() en caso de error."""

    def __init__(self, inner, max_attempts: int = 3) -> None:
        self.name = f"retryable:{inner.name}"
        self._inner = inner
        self._max = max_attempts

    def process(self, data: dict[str, object]) -> StageResult:
        @retry(
            stop=stop_after_attempt(self._max),
            wait=wait_exponential(multiplier=1, min=1, max=8),
            reraise=True,
        )
        def _attempt() -> StageResult:
            result = self._inner.process(data)
            if not result.success:
                raise RuntimeError(result.error or "stage failed")
            return result

        try:
            return _attempt()
        except Exception as e:
            return StageResult(success=False, data=data, error=str(e))
```

---

## 5. Dead-Letter Queue

Cuando un job falla de forma definitiva (se agotan los reintentos), se mueve a una **dead-letter queue** para inspección manual.

```python
import json
from pathlib import Path
from datetime import datetime, timezone


class DeadLetterQueue:
    def __init__(self, dlq_path: Path = Path(".dlq.jsonl")) -> None:
        self._path = dlq_path

    def push(self, job_id: str, data: dict[str, object], error: str) -> None:
        record = {
            "job_id": job_id,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "error": error,
            "data": data,
        }
        with self._path.open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def list_failed(self) -> list[dict[str, object]]:
        if not self._path.exists():
            return []
        return [json.loads(line) for line in self._path.read_text().splitlines()]

    def requeue(self, job_id: str) -> dict[str, object] | None:
        items = self.list_failed()
        for item in items:
            if item["job_id"] == job_id:
                return item["data"]  # type: ignore[return-value]
        return None
```

---

## 6. Skip-on-Error

Para pipelines donde un fallo no debe detener el batch completo:

```python
def run_batch_with_skip(
    pipeline,
    items: list[dict[str, object]],
    dlq: DeadLetterQueue,
) -> dict[str, int]:
    stats = {"ok": 0, "failed": 0, "skipped": 0}
    for item in items:
        result = pipeline.run(item)
        if result.success:
            stats["ok"] += 1
        else:
            dlq.push(
                job_id=str(item.get("path", "unknown")),
                data=item,
                error=result.error or "unknown error",
            )
            stats["failed"] += 1
    return stats
```

---

## Resumen

| Técnica | Cuándo |
|---------|--------|
| `@retry(stop_after_attempt(n))` | Operaciones que pueden fallar por red/timeouts |
| `wait_exponential` | Evitar sobrecargar el servicio externo |
| `retry_if_exception_type` | Solo reintentar errores recuperables |
| `RetryableStage` | Agregar retry a una etapa sin modificarla |
| Dead-Letter Queue | Inspeccionar y reencolar jobs fallidos manualmente |
| Skip-on-error | Procesar el batch completo aunque algunos fallen |
