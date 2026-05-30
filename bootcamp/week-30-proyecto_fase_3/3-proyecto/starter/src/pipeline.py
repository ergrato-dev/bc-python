"""PipelineRunner — orquesta todas las etapas y persiste el estado."""
from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path

from .stages.base import Stage, StageResult

logger = logging.getLogger("studio.pipeline")


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class JobRecord:
    job_id: str
    input_path: str
    project: str = ""
    status: JobStatus = JobStatus.PENDING
    current_stage: str = ""
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: str | None = None
    finished_at: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "job_id": self.job_id,
            "input_path": self.input_path,
            "project": self.project,
            "status": str(self.status),
            "current_stage": self.current_stage,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }


class StateStore:
    def __init__(self, state_path: Path = Path(".pipeline_state.json")) -> None:
        self._path = state_path
        self._jobs: dict[str, JobRecord] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        raw: dict[str, object] = json.loads(self._path.read_text())
        for jid, d in raw.items():
            assert isinstance(d, dict)
            self._jobs[jid] = JobRecord(
                job_id=str(d["job_id"]),
                input_path=str(d["input_path"]),
                project=str(d.get("project", "")),
                status=JobStatus(str(d.get("status", "pending"))),
                current_stage=str(d.get("current_stage", "")),
                error=str(d["error"]) if d.get("error") else None,
                created_at=str(d.get("created_at", "")),
                started_at=str(d["started_at"]) if d.get("started_at") else None,
                finished_at=str(d["finished_at"]) if d.get("finished_at") else None,
            )

    def _save(self) -> None:
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(
            {jid: r.to_dict() for jid, r in self._jobs.items()},
            indent=2, ensure_ascii=False,
        ))
        tmp.replace(self._path)

    def create(self, job_id: str, input_path: str, project: str = "") -> JobRecord:
        r = JobRecord(job_id=job_id, input_path=input_path, project=project)
        self._jobs[job_id] = r
        self._save()
        return r

    def transition(self, job_id: str, status: JobStatus, **kwargs: object) -> JobRecord:
        r = self._jobs[job_id]
        r.status = status
        for k, v in kwargs.items():
            setattr(r, k, v)
        now = datetime.now(timezone.utc).isoformat()
        if status == JobStatus.RUNNING and not r.started_at:
            r.started_at = now
        if status in (JobStatus.DONE, JobStatus.FAILED):
            r.finished_at = now
        self._save()
        return r

    def list_all(self) -> list[JobRecord]:
        return list(self._jobs.values())

    def list_by_status(self, status: JobStatus) -> list[JobRecord]:
        return [r for r in self._jobs.values() if r.status == status]


class PipelineRunner:
    def __init__(self, stages: list[Stage], store: StateStore | None = None) -> None:
        self._stages = stages
        self._store = store or StateStore()

    def run(self, input_path: str, project: str = "") -> StageResult:
        job_id = str(uuid.uuid4())[:8]
        data: dict[str, object] = {"path": input_path, "project": project, "job_id": job_id}

        self._store.create(job_id, input_path, project)
        self._store.transition(job_id, JobStatus.RUNNING)

        for stage in self._stages:
            self._store.transition(job_id, JobStatus.RUNNING, current_stage=stage.name)
            logger.info("[%s] etapa=%s inicio", job_id, stage.name)
            t0 = time.perf_counter()
            result = stage.process(data)
            elapsed = time.perf_counter() - t0
            logger.info("[%s] etapa=%s ok=%s dur=%.2fs", job_id, stage.name, result.success, elapsed)

            if not result.success:
                self._store.transition(job_id, JobStatus.FAILED, error=result.error)
                logger.error("[%s] FALLO en %s: %s", job_id, stage.name, result.error)
                return result

            data = result.data

        self._store.transition(job_id, JobStatus.DONE)
        logger.info("[%s] DONE", job_id)
        return StageResult(success=True, data=data)
