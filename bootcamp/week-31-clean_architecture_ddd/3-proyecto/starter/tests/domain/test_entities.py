"""
Tests del dominio — sin mocks, sin boto3, sin httpx.
TODO: implementar los tests marcados con NotImplementedError.
"""
from __future__ import annotations
import pytest
from src.domain.entities import Job, JobStatus, Asset
from src.domain.value_objects import ProjectSlug, MediaType, S3Key


class TestJob:
    def test_create_returns_pending_job(self) -> None:
        # TODO: Job.create("clip.mp4", "canal9/spot")
        # assert result.status == JobStatus.PENDING
        # assert len(result.job_id) == 8
        raise NotImplementedError

    def test_start_transitions_to_running(self) -> None:
        # TODO: crear job, llamar start(), verificar RUNNING
        raise NotImplementedError

    def test_start_from_non_pending_raises(self) -> None:
        # TODO: crear job, llamar start() dos veces
        # verificar que la segunda lanza ValueError
        raise NotImplementedError

    def test_complete_transitions_to_done(self) -> None:
        # TODO: start() + complete(), verificar DONE
        raise NotImplementedError

    def test_fail_sets_status_and_error(self) -> None:
        # TODO: start() + fail("S3 error"), verificar FAILED y error
        raise NotImplementedError

    def test_equality_by_job_id(self) -> None:
        # TODO: dos jobs con mismo job_id son iguales
        # dos jobs con distinto job_id no son iguales
        raise NotImplementedError


class TestProjectSlug:
    def test_valid_slug(self) -> None:
        # TODO: ProjectSlug("canal9/spot") — no lanza
        raise NotImplementedError

    def test_invalid_slug_raises(self) -> None:
        # TODO: ProjectSlug("MAYUSCULAS/proyecto") lanza ValueError
        raise NotImplementedError

    def test_client_and_project_properties(self) -> None:
        # TODO: verificar .client y .project
        raise NotImplementedError


class TestMediaType:
    def test_from_extension_video(self) -> None:
        # TODO: MediaType.from_extension(".mp4").value == "video"
        raise NotImplementedError

    def test_from_extension_unknown(self) -> None:
        # TODO: MediaType.from_extension(".xyz").value == "other"
        raise NotImplementedError
