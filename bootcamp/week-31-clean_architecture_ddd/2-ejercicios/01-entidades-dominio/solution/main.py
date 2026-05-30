"""
Ejercicio 01: Entities de Dominio — SOLUCIÓN
============================================
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


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
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Job):
            return NotImplemented
        return self.job_id == other.job_id

    def __hash__(self) -> int:
        return hash(self.job_id)

    @classmethod
    def create(cls, asset_path: str, project: str) -> "Job":
        return cls(
            job_id=str(uuid.uuid4())[:8],
            asset_path=asset_path,
            project=project,
        )

    def start(self) -> None:
        if self.status != JobStatus.PENDING:
            raise ValueError(
                f"No se puede iniciar un job en estado '{self.status}'. "
                "Solo se puede iniciar desde 'pending'."
            )
        self.status = JobStatus.RUNNING

    def complete(self) -> None:
        self.status = JobStatus.DONE

    def fail(self, error: str) -> None:
        self.status = JobStatus.FAILED
        self.error = error


@dataclass
class Asset:
    asset_id: str
    original_path: str
    project: str
    proxy_path: str | None = None
    web_path: str | None = None
    thumb_path: str | None = None

    @classmethod
    def from_path(cls, path: str, project: str) -> "Asset":
        return cls(asset_id=str(uuid.uuid4())[:8], original_path=path, project=project)

    def set_transcoded(self, proxy: str, web: str, thumb: str) -> None:
        self.proxy_path = proxy
        self.web_path = web
        self.thumb_path = thumb

    @property
    def is_transcoded(self) -> bool:
        return self.proxy_path is not None


if __name__ == "__main__":
    print("=== Test Job ===")
    job = Job.create("footage/clip.mp4", "canal9/spot")
    assert job.status == JobStatus.PENDING
    assert len(job.job_id) == 8

    job.start()
    assert job.status == JobStatus.RUNNING

    try:
        job.start()
    except ValueError:
        print("start() doble lanza ValueError — OK")

    job.complete()
    assert job.status == JobStatus.DONE

    job2 = Job.create("footage/otro.mp4", "canal9/spot")
    job2.start()
    job2.fail("S3 ConnectionError")
    assert job2.status == JobStatus.FAILED

    job3 = Job.create("footage/clip.mp4", "canal9/spot")
    assert job != job3
    job4 = Job(job_id=job.job_id, asset_path="otro.mp4", project="otro")
    assert job == job4

    print("\n=== Test Asset ===")
    asset = Asset.from_path("footage/clip.mp4", "canal9/spot")
    assert not asset.is_transcoded
    asset.set_transcoded("output/proxy.mp4", "output/web.mp4", "output/thumb.jpg")
    assert asset.is_transcoded

    print("\nOK — Ejercicio 01 completado")
