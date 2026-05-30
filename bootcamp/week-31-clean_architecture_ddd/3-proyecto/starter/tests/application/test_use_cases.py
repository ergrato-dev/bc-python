"""
Tests de use cases — solo InMemory adapters, sin boto3 ni ffmpeg.
TODO: implementar los tests marcados con NotImplementedError.
"""
from __future__ import annotations
import pytest
from src.domain.entities import Job, JobStatus
from src.infrastructure.memory_repository import InMemoryJobRepository
from src.application.use_cases import ProcessAssetUseCase, GetJobStatusUseCase


class FakeAssetStore:
    def __init__(self, url: str = "https://fake-s3/clip.mp4", fail: bool = False) -> None:
        self._url = url
        self._fail = fail
        self.calls: list[str] = []

    def upload(self, asset_path: str, asset_id: str, media_type: str) -> str:
        if self._fail:
            raise RuntimeError("Fake upload error")
        self.calls.append(asset_path)
        return self._url


class TestProcessAssetUseCase:
    def test_successful_execution_returns_done_job(self) -> None:
        # TODO: crear repo=InMemoryJobRepository(), store=FakeAssetStore()
        # TODO: use_case.execute("clip.mp4", "canal9/spot")
        # TODO: assert job.status == JobStatus.DONE
        raise NotImplementedError

    def test_failed_upload_returns_failed_job(self) -> None:
        # TODO: usar FakeAssetStore(fail=True)
        # TODO: assert job.status == JobStatus.FAILED
        # TODO: assert job.error is not None
        raise NotImplementedError

    def test_job_is_persisted_in_repository(self) -> None:
        # TODO: verificar que el job está en repo.find_by_id(job.job_id)
        # TODO: verificar que el job persistido tiene status DONE
        raise NotImplementedError


class TestGetJobStatusUseCase:
    def test_list_all_returns_all_jobs(self) -> None:
        # TODO: ejecutar 2 procesados
        # TODO: use_case.list_all() devuelve 2 jobs
        raise NotImplementedError

    def test_get_by_id_returns_correct_job(self) -> None:
        # TODO: ejecutar 1 job
        # TODO: use_case.execute(job.job_id) devuelve el job
        raise NotImplementedError
