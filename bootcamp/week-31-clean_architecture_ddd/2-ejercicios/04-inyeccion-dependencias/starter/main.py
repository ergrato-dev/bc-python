"""
Ejercicio 04: Dependency Injection con dependency-injector
===========================================================
Configura un Container que inyecta repositorios y use cases.
Incluye override del container para tests.

Instalar: pip install dependency-injector
Ejecutar: python main.py
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Protocol
from pathlib import Path


# ── Domain (copiado del ejercicio 03) ─────────────────────────────────────────

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


# ── Adapters ─────────────────────────────────────────────────────────────────

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


# ── Application ───────────────────────────────────────────────────────────────

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


# ── DI Container ──────────────────────────────────────────────────────────────

# TODO 1: Importar dependency_injector (containers, providers)
# from dependency_injector import containers, providers

class Container:
    """
    TODO 2: Definir un Container (DeclarativeContainer) con:
        - config: providers.Configuration()
        - job_repository: providers.Singleton(InMemoryJobRepository)
        - asset_store: providers.Singleton(FakeAssetStore, base_url=config.base_url)
        - process_use_case: providers.Factory(
              ProcessAssetUseCase,
              job_repo=job_repository,
              asset_store=asset_store,
          )
    """
    pass  # Reemplazar con la implementación real


# ── Simulación ───────────────────────────────────────────────────────────────

def run_with_di() -> None:
    """
    TODO 3: Crear el Container, configurar config con from_dict(),
    obtener process_use_case() y ejecutar con "footage/spot.mp4" y "canal9/spot".
    Verificar que result.status == JobStatus.DONE.
    """
    raise NotImplementedError


def run_with_di_override() -> None:
    """
    TODO 4: Override del container para tests:
    Crear un Container, usar container.job_repository.override(providers.Singleton(InMemoryJobRepository))
    para reemplazar el adapter por uno alternativo.
    Verificar que el use case usa el override.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("=== DI Container básico ===")
    run_with_di()
    print("OK: Container configuró e inyectó dependencias")

    print("\n=== DI Container con override ===")
    run_with_di_override()
    print("OK: Override aplicado correctamente")

    print("\nOK — Ejercicio 04 completado")
