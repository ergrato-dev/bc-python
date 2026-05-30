"""
Ejercicio 03: Repository Pattern — SOLUCIÓN
============================================
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Protocol


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Job:
    job_id: str
    asset_path: str
    project: str
    status: JobStatus = JobStatus.PENDING
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Job): return NotImplemented
        return self.job_id == other.job_id

    def __hash__(self) -> int: return hash(self.job_id)

    @classmethod
    def create(cls, asset_path: str, project: str) -> "Job":
        return cls(job_id=str(uuid.uuid4())[:8], asset_path=asset_path, project=project)

    def start(self) -> None:
        if self.status != JobStatus.PENDING:
            raise ValueError(f"No se puede iniciar desde '{self.status}'")
        self.status = JobStatus.RUNNING

    def complete(self) -> None: self.status = JobStatus.DONE
    def fail(self, error: str) -> None:
        self.status = JobStatus.FAILED
        self.error = error


class IJobRepository(Protocol):
    def save(self, job: Job) -> None: ...
    def find_by_id(self, job_id: str) -> Job | None: ...
    def find_all(self) -> list[Job]: ...
    def find_by_status(self, status: str) -> list[Job]: ...


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


class FakeAssetStore:
    def __init__(self, url: str = "https://fake-s3/clip.mp4") -> None:
        self._url = url
        self.upload_calls: list[str] = []

    def upload(self, asset_path: str, asset_id: str, media_type: str) -> str:
        self.upload_calls.append(asset_path)
        return self._url


class ProcessAssetUseCase:
    def __init__(self, job_repo: IJobRepository, asset_store: FakeAssetStore) -> None:
        self._jobs = job_repo
        self._store = asset_store

    def execute(self, asset_path: str, project: str) -> Job:
        job = Job.create(asset_path=asset_path, project=project)
        self._jobs.save(job)
        job.start()
        self._jobs.save(job)
        try:
            self._store.upload(asset_path, job.job_id, "video")
            job.complete()
        except Exception as e:
            job.fail(str(e))
        finally:
            self._jobs.save(job)
        return job


if __name__ == "__main__":
    repo = InMemoryJobRepository()
    job1 = Job.create("clip1.mp4", "canal9/spot")
    job2 = Job.create("clip2.mp4", "canal9/spot")
    repo.save(job1)
    repo.save(job2)

    assert len(repo.find_all()) == 2
    assert repo.find_by_id(job1.job_id) is not None
    assert repo.find_by_id("no-existe") is None

    job1.start()
    repo.save(job1)
    assert len(repo.find_by_status("pending")) == 1
    assert len(repo.find_by_status("running")) == 1

    repo2 = InMemoryJobRepository()
    store = FakeAssetStore(url="https://s3/result.mp4")
    result = ProcessAssetUseCase(repo2, store).execute("footage/spot.mp4", "canal9/spot")
    assert result.status == JobStatus.DONE
    assert repo2.find_by_id(result.job_id) is not None

    print("OK — Ejercicio 03 completado")
