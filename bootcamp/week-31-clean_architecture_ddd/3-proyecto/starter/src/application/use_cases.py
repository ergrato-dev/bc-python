"""Application use cases — orquestan el dominio sin conocer infraestructura."""
from __future__ import annotations

from ..domain.entities import Job
from ..domain.repositories import IJobRepository, IAssetStore


class ProcessAssetUseCase:
    """
    Orquesta el procesamiento de un asset:
    1. Crear job en dominio
    2. Iniciar job
    3. Subir asset al store
    4. Completar o fallar el job
    5. Persistir estado

    IMPORTANTE: Este use case NO importa boto3, httpx, ffmpeg ni ningún
    adaptador concreto. Solo trabaja con los Protocols del dominio.
    """

    def __init__(self, job_repo: IJobRepository, asset_store: IAssetStore) -> None:
        self._jobs = job_repo
        self._store = asset_store

    def execute(self, asset_path: str, project: str) -> Job:
        """
        TODO:
        1. Job.create(asset_path, project)
        2. self._jobs.save(job)
        3. job.start() — puede lanzar ValueError si no está en PENDING
        4. self._jobs.save(job)
        5. Intentar self._store.upload(asset_path, job.job_id, "video")
        6. Si éxito: job.complete()
           Si excepción: job.fail(str(e))
        7. self._jobs.save(job) en finally
        8. Retornar job

        Referencia: ejercicio 03 — ProcessAssetUseCase.execute()
        """
        raise NotImplementedError


class GetJobStatusUseCase:
    def __init__(self, job_repo: IJobRepository) -> None:
        self._jobs = job_repo

    def execute(self, job_id: str) -> Job | None:
        return self._jobs.find_by_id(job_id)

    def list_all(self) -> list[Job]:
        return self._jobs.find_all()
