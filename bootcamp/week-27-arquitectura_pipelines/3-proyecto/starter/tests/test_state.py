"""Tests de StateStore y transiciones de JobStatus."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.state import JobRecord, JobStatus, StateStore


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    return StateStore(tmp_path / ".test_state.json")


def test_create_job(store: StateStore) -> None:
    job = store.create("job-001", "/footage/clip.mp4", project="canal9/spot")
    assert job.status == JobStatus.PENDING
    assert job.job_id == "job-001"
    assert job.project == "canal9/spot"


def test_transition_to_running(store: StateStore) -> None:
    store.create("job-001", "/footage/clip.mp4")
    job = store.transition("job-001", JobStatus.RUNNING, current_stage="ingest")
    assert job.status == JobStatus.RUNNING
    assert job.current_stage == "ingest"
    assert job.started_at is not None


def test_transition_to_done(store: StateStore) -> None:
    store.create("job-001", "/footage/clip.mp4")
    store.transition("job-001", JobStatus.RUNNING)
    job = store.transition("job-001", JobStatus.DONE)
    assert job.status == JobStatus.DONE
    assert job.finished_at is not None


def test_transition_to_failed(store: StateStore) -> None:
    store.create("job-001", "/footage/clip.mp4")
    store.transition("job-001", JobStatus.RUNNING)
    job = store.transition("job-001", JobStatus.FAILED, error="Transcode error")
    assert job.status == JobStatus.FAILED
    assert job.error == "Transcode error"
    assert job.finished_at is not None


def test_persistence_roundtrip(tmp_path: Path) -> None:
    state_path = tmp_path / ".state.json"
    s1 = StateStore(state_path)
    s1.create("job-abc", "/path/file.mp4", project="test")
    s1.transition("job-abc", JobStatus.DONE)

    s2 = StateStore(state_path)
    job = s2.get("job-abc")
    assert job is not None
    assert job.status == JobStatus.DONE
    assert job.finished_at is not None


def test_list_by_status(store: StateStore) -> None:
    store.create("j1", "a.mp4")
    store.create("j2", "b.mp4")
    store.create("j3", "c.mp4")
    store.transition("j1", JobStatus.DONE)
    store.transition("j2", JobStatus.FAILED, error="oops")

    pending = store.list_by_status(JobStatus.PENDING)
    done = store.list_by_status(JobStatus.DONE)
    failed = store.list_by_status(JobStatus.FAILED)

    assert len(pending) == 1
    assert len(done) == 1
    assert len(failed) == 1
