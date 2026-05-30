"""JsonJobRepository — adapter de producción que persiste en .pipeline_state.json."""
from __future__ import annotations

import json
from pathlib import Path

from ..domain.entities import Job, JobStatus


class JsonJobRepository:
    def __init__(self, state_path: Path = Path(".pipeline_state.json")) -> None:
        self._path = state_path

    def _load(self) -> dict[str, dict[str, object]]:
        if not self._path.exists():
            return {}
        return json.loads(self._path.read_text())  # type: ignore[no-any-return]

    def _save_raw(self, data: dict[str, dict[str, object]]) -> None:
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        tmp.replace(self._path)

    def save(self, job: Job) -> None:
        """
        TODO: cargar el estado actual con _load(), actualizar con el job serializado
        y guardar con _save_raw().

        Serializar job como:
        {
            "job_id": job.job_id,
            "asset_path": job.asset_path,
            "project": job.project,
            "status": str(job.status),
            "error": job.error,
            "created_at": job.created_at,
        }
        """
        raise NotImplementedError

    def find_by_id(self, job_id: str) -> Job | None:
        """
        TODO: cargar datos, buscar job_id, reconstruir Job con JobStatus().
        Devolver None si no existe.
        """
        raise NotImplementedError

    def find_all(self) -> list[Job]:
        return [j for j in (self.find_by_id(jid) for jid in self._load()) if j]

    def find_by_status(self, status: str) -> list[Job]:
        return [j for j in self.find_all() if str(j.status) == status]
