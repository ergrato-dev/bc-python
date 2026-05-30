"""InMemoryJobRepository — adapter para tests (no persiste en disco)."""
from __future__ import annotations

from ..domain.entities import Job


class InMemoryJobRepository:
    def __init__(self) -> None:
        self._store: dict[str, Job] = {}

    def save(self, job: Job) -> None:
        self._store[job.job_id] = job

    def find_by_id(self, job_id: str) -> Job | None:
        return self._store.get(job_id)

    def find_all(self) -> list[Job]:
        return list(self._store.values())

    def find_by_status(self, status: str) -> list[Job]:
        return [j for j in self._store.values() if str(j.status) == status]
