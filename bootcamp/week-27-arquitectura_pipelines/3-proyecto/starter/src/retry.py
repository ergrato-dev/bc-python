from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log

from .stages import Stage, StageResult

logger = logging.getLogger(__name__)


class RetryableStage:
    """Envuelve una etapa y reintenta su process() con backoff exponencial."""

    def __init__(self, inner: Stage, max_attempts: int = 3) -> None:
        self.name = f"retryable:{inner.name}"
        self._inner = inner
        self._max = max_attempts

    def process(self, data: dict[str, object]) -> StageResult:
        @retry(
            stop=stop_after_attempt(self._max),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            before_sleep=before_sleep_log(logger, logging.WARNING),
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
        return [json.loads(line) for line in self._path.read_text().splitlines() if line.strip()]

    def pop(self, job_id: str) -> dict[str, object] | None:
        items = self.list_failed()
        remaining = [item for item in items if item["job_id"] != job_id]
        self._path.write_text("\n".join(json.dumps(i) for i in remaining) + ("\n" if remaining else ""))
        for item in items:
            if item["job_id"] == job_id:
                return item["data"]  # type: ignore[return-value]
        return None
