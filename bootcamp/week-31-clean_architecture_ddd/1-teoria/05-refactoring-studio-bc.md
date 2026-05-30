# Refactoring Studio BC con Clean Architecture

## 1. El Sistema Antes (Semana 30)

El pipeline de la semana 30 tiene una estructura plana:

```
src/
├── config.py         ← mezcla configuración y dominio
├── pipeline.py       ← orquesta + persiste estado
├── stages/
│   ├── ingest.py     ← lógica de negocio mezclada con pathlib
│   ├── transcode.py  ← lógica + ffmpeg
│   ├── cloud.py      ← lógica + boto3
│   └── distribute.py ← lógica + httpx
```

**Problemas:**
- Para testear `transcode.py` hay que tener ffmpeg instalado
- Para testear `cloud.py` hay que tener credenciales S3 o mockear boto3 en cada test
- No hay lugar claro para "las reglas de negocio" separadas de "cómo se implementan"

---

## 2. El Sistema Después (Clean Architecture)

```
src/
├── domain/
│   ├── entities.py      ← Job, Asset — lógica de negocio pura
│   ├── value_objects.py ← ProjectSlug, MediaType, S3Key
│   └── repositories.py  ← IJobRepository, IAssetStore (Protocols)
│
├── application/
│   ├── use_cases.py     ← ProcessAssetUseCase, GetStatusUseCase
│   └── services.py      ← PipelineService (orquesta use cases)
│
├── infrastructure/
│   ├── json_repository.py   ← JsonJobRepository
│   ├── s3_adapter.py        ← S3AssetStore
│   ├── ffmpeg_transcoder.py ← FfmpegTranscoder
│   ├── slack_notifier.py    ← SlackNotifier
│   └── containers.py        ← DI Container
│
└── presentation/
    └── cli.py               ← Typer CLI sin lógica de negocio
```

---

## 3. Mapeo: Antes → Después

| Antes (semana 30) | Después (semana 31) | Capa |
|------------------|---------------------|------|
| `pipeline.py` + `StateStore` | `Job.start()`, `Job.complete()` | domain |
| `JobRecord`, `JobStatus` | `Job` entity | domain |
| `stages/ingest.py` | `Asset.from_path()` | domain |
| `stages/validate.py` | `ValidateAssetUseCase` | application |
| `stages/transcode.py` | `ITranscoder` port + `FfmpegTranscoder` | infrastructure |
| `stages/cloud.py` | `IAssetStore` port + `S3AssetStore` | infrastructure |
| `stages/distribute.py` | `INotifier` port + `SlackNotifier` | infrastructure |
| `__main__.py` | `cli.py` (presentation) | presentation |

---

## 4. Estrategia de Refactoring

Aplicar el patrón **Strangler Fig**: reescribir capa a capa sin romper lo que funciona.

```
Paso 1: Extraer domain (entities, value objects)
        → Tests del dominio en verde sin mocks
Paso 2: Definir ports (IJobRepository, IAssetStore, ITranscoder)
        → Tests de application con InMemory adapters
Paso 3: Mover infraestructura a adaptadores concretos
        → Tests de infraestructura (mocks de boto3, ffmpeg)
Paso 4: Configurar DI container
        → Presentation llama al container
```

---

## 5. Tests por Capa

```python
# tests/domain/test_job.py — sin imports externos
def test_job_start_transitions_to_running() -> None:
    job = Job.create("clip.mp4", "canal9/spot")
    job.start()
    assert job.status == JobStatus.RUNNING

def test_job_cannot_start_twice() -> None:
    job = Job.create("clip.mp4", "canal9/spot")
    job.start()
    with pytest.raises(ValueError):
        job.start()


# tests/application/test_use_cases.py — InMemory adapters
def test_process_asset_saves_job_as_done() -> None:
    repo = InMemoryJobRepository()
    store = FakeAssetStore(url="https://s3/clip.mp4")

    use_case = ProcessAssetUseCase(repo, store)
    job = use_case.execute("clip.mp4", "canal9/spot")

    assert job.status == JobStatus.DONE
    assert repo.find_by_id(job.job_id) is not None


# tests/infrastructure/test_s3_adapter.py — mock boto3
def test_s3_upload_calls_boto3(tmp_path: Path) -> None:
    f = tmp_path / "clip.mp4"
    f.write_bytes(b"video")

    with patch("boto3.client") as mock:
        mock.return_value.upload_file = MagicMock()
        store = S3AssetStore("bucket", "us-east-1", dry_run=False)
        url = store.upload(str(f), "job-001", "video")

    assert "bucket" in url
    mock.return_value.upload_file.assert_called_once()
```

La clave: `tests/domain/` no importa boto3, ffmpeg ni httpx — nunca.

---

## 6. Ejemplo: ProcessAssetUseCase

```python
# application/use_cases.py
from __future__ import annotations
from ..domain.entities import Job, Asset
from ..domain.value_objects import ProjectSlug
from ..domain.repositories import IJobRepository, IAssetStore, ITranscoder


class ProcessAssetUseCase:
    def __init__(
        self,
        job_repo: IJobRepository,
        asset_store: IAssetStore,
        transcoder: ITranscoder,
    ) -> None:
        self._jobs = job_repo
        self._store = asset_store
        self._transcoder = transcoder

    def execute(self, asset_path: str, project_slug: str) -> Job:
        project = ProjectSlug(project_slug)
        job = Job.create(asset_path=asset_path, project=str(project))
        self._jobs.save(job)

        job.start()
        self._jobs.save(job)

        try:
            # Transcoding (solo si es video)
            if "video" in asset_path:  # simplificado — usar MediaType en producción
                outputs = self._transcoder.transcode(asset_path)
            else:
                outputs = {"original": asset_path}

            # Upload
            url = self._store.upload(asset_path, job.job_id, "video")
            job.complete()
        except Exception as e:
            job.fail(str(e))
        finally:
            self._jobs.save(job)

        return job
```

---

## Resumen del Proceso

```
1. domain/     — Entities + VOs + Ports    (sin deps externas)
2. application/ — Use Cases               (solo domain)
3. infrastructure/ — Adapters             (domain + libs externas)
4. presentation/ — CLI                    (DI Container)
```

La arquitectura es correcta cuando `pytest tests/domain/ tests/application/` pasa en < 100ms sin boto3, ffmpeg ni httpx instalados.
