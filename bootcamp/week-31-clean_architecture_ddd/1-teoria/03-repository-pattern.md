# Repository Pattern

## 1. El Problema

Sin Repository Pattern:

```python
# Use case conoce boto3, SQLite y JSON al mismo tiempo
class ProcessAssetUseCase:
    def execute(self, path: str) -> None:
        import boto3  # infraestructura en application ← MAL
        s3 = boto3.client("s3")
        s3.upload_file(path, "bucket", "key")

        import json  # infraestructura en application ← MAL
        state = json.loads(Path(".state.json").read_text())
        state["jobs"].append({"path": path, "status": "done"})
```

Consecuencias: no se puede testear sin S3 real, no se puede cambiar de S3 a Drive sin tocar el use case.

---

## 2. Repository Interface (Port)

El **port** vive en `domain/` — es una interface Python pura sin dependencias externas.

```python
# domain/repositories.py
from __future__ import annotations
from typing import Protocol
from .entities import Job, Asset


class IJobRepository(Protocol):
    def save(self, job: Job) -> None: ...
    def find_by_id(self, job_id: str) -> Job | None: ...
    def find_all(self) -> list[Job]: ...
    def find_by_status(self, status: str) -> list[Job]: ...


class IAssetStore(Protocol):
    def upload(self, local_path: str, asset_id: str, media_type: str) -> str:
        """Devuelve la URL del asset subido."""
        ...
```

---

## 3. Adapter — InMemory (para tests)

```python
# infrastructure/memory_repository.py
from __future__ import annotations
from ..domain.entities import Job
from ..domain.repositories import IJobRepository


class InMemoryJobRepository:
    def __init__(self) -> None:
        self._store: dict[str, Job] = {}

    def save(self, job: Job) -> None:
        self._store[job.job_id] = job

    def find_by_id(self, job_id: str) -> Job | None:
        return self._store.get(job_id)

    def find_all(self) -> list[Job]:
        return list(self._store.values())

    def find_by_status(self, status: str) -> list[Job]:
        return [j for j in self._store.values() if str(j.status) == status]
```

---

## 4. Adapter — JSON (para producción)

```python
# infrastructure/json_repository.py
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

    def _save(self, data: dict[str, dict[str, object]]) -> None:
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        tmp.replace(self._path)

    def save(self, job: Job) -> None:
        data = self._load()
        data[job.job_id] = {
            "job_id": job.job_id,
            "asset_path": job.asset_path,
            "project": job.project,
            "status": str(job.status),
            "error": job.error,
            "created_at": job.created_at,
        }
        self._save(data)

    def find_by_id(self, job_id: str) -> Job | None:
        data = self._load()
        if job_id not in data:
            return None
        d = data[job_id]
        return Job(
            job_id=str(d["job_id"]),
            asset_path=str(d["asset_path"]),
            project=str(d["project"]),
            status=JobStatus(str(d["status"])),
            error=str(d["error"]) if d.get("error") else None,
            created_at=str(d.get("created_at", "")),
        )

    def find_all(self) -> list[Job]:
        return [self.find_by_id(jid) for jid in self._load() if self.find_by_id(jid)]  # type: ignore[misc]

    def find_by_status(self, status: str) -> list[Job]:
        return [j for j in self.find_all() if str(j.status) == status]
```

---

## 5. Application: Use Case que usa el Port

```python
# application/use_cases.py
from __future__ import annotations
from ..domain.entities import Job
from ..domain.repositories import IJobRepository, IAssetStore


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
            url = self._store.upload(asset_path, job.job_id, "video")
            job.complete()
        except Exception as e:
            job.fail(str(e))
        finally:
            self._jobs.save(job)

        return job
```

Tests con InMemoryJobRepository — sin ninguna dependencia externa:

```python
def test_process_asset_completes_job() -> None:
    repo = InMemoryJobRepository()
    store = FakeAssetStore()  # retorna URL ficticia

    use_case = ProcessAssetUseCase(repo, store)
    job = use_case.execute("/footage/clip.mp4", "canal9/spot")

    assert job.status == JobStatus.DONE
    saved = repo.find_by_id(job.job_id)
    assert saved is not None
    assert saved.status == JobStatus.DONE
```

---

## 6. Unit of Work (opcional avanzado)

El **Unit of Work** coordina múltiples repositorios en una sola transacción:

```python
class IUnitOfWork(Protocol):
    jobs: IJobRepository

    def __enter__(self) -> "IUnitOfWork": ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
```

Para este proyecto no es necesario — basta con repositorios individuales.

---

## Resumen

| Concepto | Rol |
|----------|-----|
| `IJobRepository` (Protocol) | Port — interface en domain |
| `InMemoryJobRepository` | Adapter — para tests |
| `JsonJobRepository` | Adapter — para producción |
| Use case recibe IJobRepository | Desacoplado del storage concreto |
| Test sin dependencias externas | Solo InMemory — instantáneo y sin setup |
