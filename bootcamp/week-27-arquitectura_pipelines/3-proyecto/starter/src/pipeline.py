from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path

from .stages import Stage, StageResult
from .state import JobStatus, StateStore

logger = logging.getLogger("studio.pipeline")


class Pipeline:
    def __init__(self, stages: list[Stage], store: StateStore | None = None) -> None:
        self._stages = stages
        self._store = store or StateStore()

    def run(self, input_path: str, project: str = "") -> StageResult:
        job_id = str(uuid.uuid4())[:8]
        data: dict[str, object] = {"path": input_path, "project": project, "job_id": job_id}

        self._store.create(job_id, input_path, project)
        self._store.transition(job_id, JobStatus.RUNNING)

        for stage in self._stages:
            self._store.transition(job_id, JobStatus.RUNNING, current_stage=stage.name)
            logger.info("[%s] etapa=%s inicio", job_id, stage.name)
            t0 = time.time()
            result = stage.process(data)
            elapsed = time.time() - t0
            logger.info("[%s] etapa=%s ok=%s dur=%.2fs", job_id, stage.name, result.success, elapsed)

            if not result.success:
                self._store.transition(job_id, JobStatus.FAILED, error=result.error)
                logger.error("[%s] FALLO en %s: %s", job_id, stage.name, result.error)
                return result

            data = result.data

        self._store.transition(job_id, JobStatus.DONE)
        logger.info("[%s] DONE", job_id)
        return StageResult(success=True, data=data)

    def run_batch(
        self,
        paths: list[str],
        project: str = "",
        skip_on_error: bool = True,
    ) -> dict[str, int]:
        stats = {"ok": 0, "failed": 0}
        for path in paths:
            result = self.run(path, project)
            if result.success:
                stats["ok"] += 1
            else:
                stats["failed"] += 1
                if not skip_on_error:
                    break
        return stats
