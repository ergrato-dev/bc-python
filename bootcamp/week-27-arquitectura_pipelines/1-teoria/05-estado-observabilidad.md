# Estado y Observabilidad

## 1. Máquina de Estados del Job

Un job de pipeline pasa por estados bien definidos. Las transiciones son unidireccionales (excepto `retrying → running`):

```
pending → running → done
                 → failed
                 → retrying → running
```

```python
from __future__ import annotations
from enum import StrEnum
from dataclasses import dataclass, field
from datetime import datetime, timezone


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class JobRecord:
    job_id: str
    input_path: str
    status: JobStatus = JobStatus.PENDING
    current_stage: str = ""
    attempt: int = 0
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: str | None = None
    finished_at: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "job_id": self.job_id,
            "input_path": self.input_path,
            "status": str(self.status),
            "current_stage": self.current_stage,
            "attempt": self.attempt,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }
```

---

## 2. Persistencia de Estado

```python
import json
from pathlib import Path


class StateStore:
    def __init__(self, state_path: Path = Path(".pipeline_state.json")) -> None:
        self._path = state_path
        self._jobs: dict[str, JobRecord] = {}
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            raw = json.loads(self._path.read_text())
            for job_id, data in raw.items():
                self._jobs[job_id] = JobRecord(
                    job_id=data["job_id"],
                    input_path=data["input_path"],
                    status=JobStatus(data["status"]),
                    current_stage=data.get("current_stage", ""),
                    attempt=data.get("attempt", 0),
                    error=data.get("error"),
                    created_at=data.get("created_at", ""),
                    started_at=data.get("started_at"),
                    finished_at=data.get("finished_at"),
                )

    def _save(self) -> None:
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(
            {jid: rec.to_dict() for jid, rec in self._jobs.items()},
            indent=2,
        ))
        tmp.replace(self._path)

    def create(self, job_id: str, input_path: str) -> JobRecord:
        record = JobRecord(job_id=job_id, input_path=input_path)
        self._jobs[job_id] = record
        self._save()
        return record

    def transition(self, job_id: str, new_status: JobStatus, **kwargs: object) -> JobRecord:
        record = self._jobs[job_id]
        record.status = new_status
        for k, v in kwargs.items():
            setattr(record, k, v)
        if new_status == JobStatus.RUNNING and not record.started_at:
            record.started_at = datetime.now(timezone.utc).isoformat()
        if new_status in (JobStatus.DONE, JobStatus.FAILED):
            record.finished_at = datetime.now(timezone.utc).isoformat()
        self._save()
        return record

    def get(self, job_id: str) -> JobRecord | None:
        return self._jobs.get(job_id)

    def list_by_status(self, status: JobStatus) -> list[JobRecord]:
        return [r for r in self._jobs.values() if r.status == status]
```

---

## 3. Logging por Etapa

```python
import logging
import sys
from pathlib import Path


def configure_pipeline_logging(log_file: Path | None = None) -> logging.Logger:
    fmt = "%(asctime)s [%(levelname)s] %(name)s — %(message)s"
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(level=logging.INFO, format=fmt, handlers=handlers)
    return logging.getLogger("studio.pipeline")


logger = configure_pipeline_logging(Path("pipeline.log"))
```

Cada etapa usa su propio logger con el nombre de la etapa:

```python
class TranscodeStage:
    name = "transcode"

    def __init__(self) -> None:
        self._log = logging.getLogger(f"studio.pipeline.{self.name}")

    def process(self, data: dict[str, object]) -> "StageResult":
        self._log.info("Iniciando transcode de %s", data.get("path"))
        # ... procesamiento ...
        self._log.info("Transcode OK — tamaño output: %d bytes", output_size)
        return StageResult(success=True, data={**data, "output_size": output_size})
```

---

## 4. Métricas de Throughput

```python
import time
from dataclasses import dataclass, field


@dataclass
class PipelineMetrics:
    start_time: float = field(default_factory=time.time)
    jobs_total: int = 0
    jobs_done: int = 0
    jobs_failed: int = 0
    stage_times: dict[str, list[float]] = field(default_factory=dict)

    def record_stage(self, stage_name: str, duration_s: float) -> None:
        self._times = self.stage_times.setdefault(stage_name, [])
        self._times.append(duration_s)

    @property
    def elapsed(self) -> float:
        return time.time() - self.start_time

    @property
    def throughput(self) -> float:
        return self.jobs_done / self.elapsed if self.elapsed > 0 else 0.0

    def report(self) -> dict[str, object]:
        stage_avg = {
            name: sum(times) / len(times)
            for name, times in self.stage_times.items()
        }
        return {
            "elapsed_s": round(self.elapsed, 2),
            "jobs_total": self.jobs_total,
            "jobs_done": self.jobs_done,
            "jobs_failed": self.jobs_failed,
            "throughput_per_s": round(self.throughput, 3),
            "stage_avg_s": stage_avg,
        }
```

---

## 5. Pipeline con Estado Integrado

```python
class ObservablePipeline:
    def __init__(self, stages: list, store: StateStore) -> None:
        self._stages = stages
        self._store = store
        self._metrics = PipelineMetrics()

    def run(self, job_id: str, data: dict[str, object]) -> "StageResult":
        self._store.transition(job_id, JobStatus.RUNNING)
        self._metrics.jobs_total += 1

        for stage in self._stages:
            self._store.transition(job_id, JobStatus.RUNNING, current_stage=stage.name)
            t0 = time.time()
            result = stage.process(data)
            self._metrics.record_stage(stage.name, time.time() - t0)

            if not result.success:
                self._store.transition(job_id, JobStatus.FAILED, error=result.error)
                self._metrics.jobs_failed += 1
                return result
            data = result.data

        self._store.transition(job_id, JobStatus.DONE)
        self._metrics.jobs_done += 1
        return StageResult(success=True, data=data)
```

---

## Resumen

| Concepto | Implementación |
|----------|----------------|
| `JobStatus` | `StrEnum` con pending/running/done/failed/retrying |
| `StateStore` | Persiste en JSON con escritura atómica |
| `transition()` | Cambia estado y actualiza timestamps automáticamente |
| Logging por etapa | `logging.getLogger(f"pipeline.{stage.name}")` |
| Throughput | `jobs_done / elapsed` — monitoreado en `PipelineMetrics` |
