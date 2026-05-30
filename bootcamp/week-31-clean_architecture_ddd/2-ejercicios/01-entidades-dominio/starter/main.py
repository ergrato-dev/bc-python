"""
Ejercicio 01: Entities de Dominio
==================================
Implementa las entidades Job y Asset con comportamiento de dominio.

Ejecutar: python main.py
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
        # TODO: igualdad basada en job_id (identidad de entity)
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.job_id)

    @classmethod
    def create(cls, asset_path: str, project: str) -> "Job":
        # TODO: crear job con UUID corto (8 caracteres) y status PENDING
        raise NotImplementedError

    def start(self) -> None:
        """Transiciona a RUNNING. Lanza ValueError si no está en PENDING."""
        # TODO: validar status == PENDING, luego asignar RUNNING
        raise NotImplementedError

    def complete(self) -> None:
        """Transiciona a DONE."""
        # TODO: asignar status = DONE
        raise NotImplementedError

    def fail(self, error: str) -> None:
        """Transiciona a FAILED y guarda el mensaje de error."""
        # TODO: asignar status = FAILED y error = error
        raise NotImplementedError


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
        # TODO: crear Asset con UUID corto
        raise NotImplementedError

    def set_transcoded(self, proxy: str, web: str, thumb: str) -> None:
        """Registra los outputs del transcode."""
        # TODO: asignar proxy_path, web_path, thumb_path
        raise NotImplementedError

    @property
    def is_transcoded(self) -> bool:
        # TODO: True si proxy_path no es None
        raise NotImplementedError


# ── Tests rápidos ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Test Job ===")
    job = Job.create("footage/clip.mp4", "canal9/spot")
    assert job.status == JobStatus.PENDING
    assert len(job.job_id) == 8
    print(f"Job creado: {job.job_id} — {job.status}")

    job.start()
    assert job.status == JobStatus.RUNNING
    print("start() OK")

    try:
        job.start()
        print("ERROR: debería haber lanzado ValueError")
    except ValueError:
        print("start() doble lanza ValueError — OK")

    job.complete()
    assert job.status == JobStatus.DONE
    print("complete() OK")

    job2 = Job.create("footage/otro.mp4", "canal9/spot")
    job2.start()
    job2.fail("S3 ConnectionError")
    assert job2.status == JobStatus.FAILED
    assert job2.error == "S3 ConnectionError"
    print("fail() OK")

    # Igualdad por identidad
    job3 = Job.create("footage/clip.mp4", "canal9/spot")
    assert job != job3  # distintos job_id
    job4 = Job(
        job_id=job.job_id,
        asset_path="otro.mp4",
        project="otro",
        status=JobStatus.PENDING,
    )
    assert job == job4  # mismo job_id → misma entidad
    print("__eq__ por identidad OK")

    print("\n=== Test Asset ===")
    asset = Asset.from_path("footage/clip.mp4", "canal9/spot")
    assert not asset.is_transcoded
    asset.set_transcoded("output/proxy.mp4", "output/web.mp4", "output/thumb.jpg")
    assert asset.is_transcoded
    print("Asset transcode OK")

    print("\nOK — Ejercicio 01 completado")
