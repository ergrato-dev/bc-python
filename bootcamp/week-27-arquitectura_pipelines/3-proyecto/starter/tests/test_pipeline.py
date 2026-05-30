"""Tests del Pipeline y sus etapas."""
from __future__ import annotations

import tempfile
import os
from pathlib import Path

import pytest

from src.stages import IngestStage, ValidateStage, ProcessStage, ExportStage, StageResult
from src.pipeline import Pipeline
from src.state import StateStore, JobStatus


@pytest.fixture
def tmp_mp4(tmp_path: Path) -> Path:
    f = tmp_path / "clip.mp4"
    f.write_bytes(b"fake video content — not empty")
    return f


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    return StateStore(tmp_path / ".pipeline_state.json")


def test_ingest_stage_success(tmp_mp4: Path) -> None:
    result = IngestStage().process({"path": str(tmp_mp4)})
    assert result.success
    assert result.data["size_bytes"] == tmp_mp4.stat().st_size
    assert result.data["suffix"] == ".mp4"


def test_ingest_stage_missing_file() -> None:
    result = IngestStage().process({"path": "/no/existe.mp4"})
    assert not result.success
    assert "no encontrado" in (result.error or "").lower()


def test_validate_stage_allowed(tmp_mp4: Path) -> None:
    data = {"path": str(tmp_mp4), "suffix": ".mp4", "size_bytes": 100}
    result = ValidateStage().process(data)
    assert result.success
    assert result.data["validated"] is True


def test_validate_stage_rejected() -> None:
    result = ValidateStage().process({"path": "file.exe", "suffix": ".exe", "size_bytes": 100})
    assert not result.success
    assert "extensión" in (result.error or "").lower()


def test_full_pipeline_success(tmp_mp4: Path, store: StateStore) -> None:
    pipeline = Pipeline(
        [IngestStage(), ValidateStage(), ProcessStage(), ExportStage()],
        store=store,
    )
    result = pipeline.run(str(tmp_mp4), project="canal9/spot")
    assert result.success
    assert result.data.get("exported") is True


def test_pipeline_stops_on_failure(store: StateStore) -> None:
    pipeline = Pipeline(
        [IngestStage(), ValidateStage(), ProcessStage(), ExportStage()],
        store=store,
    )
    result = pipeline.run("/no/existe.mp4", project="test")
    assert not result.success

    jobs = store.list_by_status(JobStatus.FAILED)
    assert len(jobs) == 1
    assert "no encontrado" in (jobs[0].error or "").lower()


def test_pipeline_state_transitions(tmp_mp4: Path, store: StateStore) -> None:
    pipeline = Pipeline(
        [IngestStage(), ValidateStage(), ProcessStage(), ExportStage()],
        store=store,
    )
    pipeline.run(str(tmp_mp4))

    done_jobs = store.list_by_status(JobStatus.DONE)
    assert len(done_jobs) == 1
    job = done_jobs[0]
    assert job.started_at is not None
    assert job.finished_at is not None


def test_batch_run_skip_on_error(tmp_mp4: Path, store: StateStore) -> None:
    pipeline = Pipeline(
        [IngestStage(), ValidateStage(), ProcessStage(), ExportStage()],
        store=store,
    )
    paths = [str(tmp_mp4), "/no/existe.mp4", str(tmp_mp4)]
    stats = pipeline.run_batch(paths, skip_on_error=True)
    assert stats["ok"] == 2
    assert stats["failed"] == 1
