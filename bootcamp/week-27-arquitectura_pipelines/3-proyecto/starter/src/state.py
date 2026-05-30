from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path


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
    project: str = ""
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
            "project": self.project,
            "status": str(self.status),
            "current_stage": self.current_stage,
            "attempt": self.attempt,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }

    @classmethod
    def from_dict(cls, d: dict[str, object]) -> "JobRecord":
        return cls(
            job_id=str(d["job_id"]),
            input_path=str(d["input_path"]),
            project=str(d.get("project", "")),
            status=JobStatus(str(d.get("status", "pending"))),
            current_stage=str(d.get("current_stage", "")),
            attempt=int(str(d.get("attempt", 0))),
            error=str(d["error"]) if d.get("error") else None,
            created_at=str(d.get("created_at", "")),
            started_at=str(d["started_at"]) if d.get("started_at") else None,
            finished_at=str(d["finished_at"]) if d.get("finished_at") else None,
        )


class StateStore:
    def __init__(self, state_path: Path = Path(".pipeline_state.json")) -> None:
        self._path = state_path
        self._jobs: dict[str, JobRecord] = {}
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            raw: dict[str, object] = json.loads(self._path.read_text())
            for job_id, data in raw.items():
                self._jobs[job_id] = JobRecord.from_dict(data)  # type: ignore[arg-type]

    def _save(self) -> None:
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(
            {jid: rec.to_dict() for jid, rec in self._jobs.items()},
            indent=2, ensure_ascii=False,
        ))
        tmp.replace(self._path)

    def create(self, job_id: str, input_path: str, project: str = "") -> JobRecord:
        record = JobRecord(job_id=job_id, input_path=input_path, project=project)
        self._jobs[job_id] = record
        self._save()
        return record

    def transition(self, job_id: str, new_status: JobStatus, **kwargs: object) -> JobRecord:
        record = self._jobs[job_id]
        record.status = new_status
        for k, v in kwargs.items():
            setattr(record, k, v)
        now = datetime.now(timezone.utc).isoformat()
        if new_status == JobStatus.RUNNING and not record.started_at:
            record.started_at = now
        if new_status in (JobStatus.DONE, JobStatus.FAILED):
            record.finished_at = now
        self._save()
        return record

    def get(self, job_id: str) -> JobRecord | None:
        return self._jobs.get(job_id)

    def list_all(self) -> list[JobRecord]:
        return list(self._jobs.values())

    def list_by_status(self, status: JobStatus) -> list[JobRecord]:
        return [r for r in self._jobs.values() if r.status == status]
