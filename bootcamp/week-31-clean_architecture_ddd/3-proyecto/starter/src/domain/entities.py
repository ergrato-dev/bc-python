"""Domain entities — Job y Asset."""
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
        return cls(job_id=str(uuid.uuid4())[:8], asset_path=asset_path, project=project)

    def start(self) -> None:
        """Transiciona a RUNNING. Lanza ValueError si no está en PENDING."""
        # TODO: validar status == PENDING, luego asignar RUNNING
        raise NotImplementedError

    def complete(self) -> None:
        """Transiciona a DONE."""
        # TODO: asignar DONE
        raise NotImplementedError

    def fail(self, error: str) -> None:
        """Transiciona a FAILED con mensaje de error."""
        # TODO: asignar FAILED y error
        raise NotImplementedError


@dataclass
class Asset:
    asset_id: str
    original_path: str
    project: str
    proxy_path: str | None = None
    web_path: str | None = None
    thumb_path: str | None = None
    s3_url: str | None = None

    @classmethod
    def from_path(cls, path: str, project: str) -> "Asset":
        return cls(asset_id=str(uuid.uuid4())[:8], original_path=path, project=project)

    def set_transcoded(self, proxy: str, web: str, thumb: str) -> None:
        """Registra los outputs del transcode."""
        # TODO: asignar proxy_path, web_path, thumb_path
        raise NotImplementedError

    def set_uploaded(self, s3_url: str) -> None:
        self.s3_url = s3_url

    @property
    def is_transcoded(self) -> bool:
        # TODO: True si proxy_path is not None
        raise NotImplementedError
