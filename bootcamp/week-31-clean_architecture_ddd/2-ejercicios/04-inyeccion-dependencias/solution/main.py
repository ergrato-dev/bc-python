"""
Ejercicio 04: Dependency Injection — SOLUCIÓN
=============================================
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Protocol

from dependency_injector import containers, providers


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


class IAssetStore(Protocol):
    def upload(self, asset_path: str, asset_id: str, media_type: str) -> str: ...


class InMemoryJobRepository:
    def __init__(self) -> None:
        self._store: dict[str, Job] = {}
    def save(self, job: Job) -> None: self._store[job.job_id] = job
    def find_by_id(self, job_id: str) -> Job | None: return self._store.get(job_id)
    def find_all(self) -> list[Job]: return list(self._store.values())


class FakeAssetStore:
    def __init__(self, base_url: str = "https://fake-s3") -> None:
        self._base = base_url
        self.calls: list[str] = []
    def upload(self, asset_path: str, asset_id: str, media_type: str) -> str:
        self.calls.append(asset_path)
        return f"{self._base}/{asset_id}.mp4"


class ProcessAssetUseCase:
    def __init__(self, job_repo: IJobRepository, asset_store: IAssetStore) -> None:
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


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    job_repository = providers.Singleton(InMemoryJobRepository)

    asset_store = providers.Singleton(
        FakeAssetStore,
        base_url=config.base_url,
    )

    process_use_case = providers.Factory(
        ProcessAssetUseCase,
        job_repo=job_repository,
        asset_store=asset_store,
    )


def run_with_di() -> None:
    container = Container()
    container.config.from_dict({"base_url": "https://fake-s3.example.com"})

    use_case = container.process_use_case()
    result = use_case.execute("footage/spot.mp4", "canal9/spot")
    assert result.status == JobStatus.DONE
    print(f"  Job {result.job_id} → {result.status}")


def run_with_di_override() -> None:
    container = Container()
    container.config.from_dict({"base_url": "https://override-store.example.com"})

    alt_store = FakeAssetStore(base_url="https://override-store.example.com")
    container.asset_store.override(providers.Object(alt_store))

    use_case = container.process_use_case()
    result = use_case.execute("footage/otro.mp4", "bbc/doc")
    assert result.status == JobStatus.DONE
    assert "override-store" in alt_store.calls[0] or alt_store.calls == ["footage/otro.mp4"]
    print(f"  Job {result.job_id} → {result.status} (store overrideado)")


if __name__ == "__main__":
    print("=== DI Container básico ===")
    run_with_di()
    print("OK")

    print("\n=== DI Container con override ===")
    run_with_di_override()
    print("OK")

    print("\nOK — Ejercicio 04 completado")
