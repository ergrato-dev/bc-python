"""
Test de integración del pipeline completo — studio-production-pipeline.

TODO: Implementar los tests de integración.
Todos los servicios externos (ffmpeg, boto3, httpx) deben ser mockeados.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.pipeline import JobStatus, PipelineRunner, StateStore
from src.stages.cloud import CloudStage
from src.stages.distribute import DistributeStage
from src.stages.ingest import IngestStage
from src.stages.transcode import TranscodeStage
from src.stages.validate import ValidateStage


@pytest.fixture
def tmp_video(tmp_path: Path) -> Path:
    f = tmp_path / "spot_verano.mp4"
    f.write_bytes(b"fake mp4 — not empty")
    return f


@pytest.fixture
def state_path(tmp_path: Path) -> Path:
    return tmp_path / ".pipeline_state.json"


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    d = tmp_path / "output"
    (d / "proxy").mkdir(parents=True)
    (d / "thumbs").mkdir()
    (d / "web").mkdir()
    return d


# ── Test integración completa ─────────────────────────────────────────────────

class TestFullPipeline:
    def test_pipeline_succeeds_with_mocked_ffmpeg_and_s3(
        self,
        tmp_video: Path,
        state_path: Path,
        output_dir: Path,
    ) -> None:
        """
        Test de integración: pipeline completo con ffmpeg y S3 mockeados.

        TODO:
        1. Mockear ffmpeg.run() (o las funciones de TranscodeStage._generate_*)
           para que creen archivos vacíos en lugar de ejecutar ffmpeg real
        2. Crear el pipeline con DRY_RUN=True
        3. Llamar pipeline.run(str(tmp_video), "canal9/spot")
        4. Verificar:
           - result.success is True
           - result.data["distributed"] is True
           - El StateStore tiene el job con status DONE
           - state_path.exists() is True
        """
        raise NotImplementedError

    def test_pipeline_stops_at_first_failure(
        self,
        state_path: Path,
        output_dir: Path,
    ) -> None:
        """
        TODO: procesar un archivo que no existe (/no/existe.mp4)
        TODO: verificar que result.success is False
        TODO: verificar que el StateStore tiene el job con status FAILED
        TODO: verificar que las etapas posteriores a Ingest NO fueron llamadas
              (usando mocks con assert_not_called)
        """
        raise NotImplementedError

    def test_state_persists_across_runs(
        self,
        tmp_video: Path,
        state_path: Path,
        output_dir: Path,
    ) -> None:
        """
        TODO: ejecutar el pipeline dos veces con dos videos diferentes
        TODO: crear un nuevo StateStore apuntando al mismo state_path
        TODO: verificar que tiene exactamente 2 jobs registrados
        """
        raise NotImplementedError


# ── Test del StateStore ────────────────────────────────────────────────────────

class TestStateStore:
    def test_create_and_transition(self, state_path: Path) -> None:
        # TODO: store.create("job-1", "/footage/clip.mp4")
        # TODO: store.transition("job-1", JobStatus.RUNNING, current_stage="ingest")
        # TODO: assert store.get("job-1").status == JobStatus.RUNNING
        raise NotImplementedError

    def test_persistence_roundtrip(self, state_path: Path) -> None:
        # TODO: crear job y transicionar a DONE
        # TODO: crear nuevo StateStore desde mismo path
        # TODO: verificar que el job persiste con status DONE
        raise NotImplementedError

    def test_list_by_status(self, state_path: Path) -> None:
        # TODO: crear 3 jobs, marcar 1 como DONE, 1 como FAILED
        # TODO: assert len(store.list_by_status(JobStatus.DONE)) == 1
        # TODO: assert len(store.list_by_status(JobStatus.PENDING)) == 1
        raise NotImplementedError
