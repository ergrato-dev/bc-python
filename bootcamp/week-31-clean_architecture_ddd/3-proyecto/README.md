# Proyecto Semana 31 — studio-refactored

## Objetivo

Refactorizar el módulo central del pipeline de Studio BC con Clean Architecture,
separando dominio, aplicación, infraestructura y presentación.

No es un rewrite completo — es una refactorización guiada de las capas más importantes.

---

## Lo que hay que refactorizar

Tomar el `studio-production-pipeline` de la semana 30 y reorganizarlo así:

```
Antes (semana 30)          →   Después (semana 31)
─────────────────────────────────────────────────────
pipeline.py (Job, StateStore)  domain/entities.py + infrastructure/json_repository.py
stages/ingest.py           →   domain/value_objects.py (MediaType)
stages/cloud.py            →   infrastructure/s3_adapter.py
stages/transcode.py        →   infrastructure/ffmpeg_transcoder.py
stages/distribute.py       →   infrastructure/slack_notifier.py
__main__.py                →   presentation/cli.py
```

---

## Estructura del Proyecto

```
starter/
├── pyproject.toml
├── src/
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities.py        # Job, Asset (TODO: comportamiento de dominio)
│   │   ├── value_objects.py   # ProjectSlug, MediaType, S3Key (TODO)
│   │   └── repositories.py    # IJobRepository, IAssetStore, ITranscoder (TODO: Protocols)
│   ├── application/
│   │   ├── __init__.py
│   │   └── use_cases.py       # ProcessAssetUseCase (TODO: lógica sin infraestructura)
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── memory_repository.py  # InMemoryJobRepository (COMPLETE)
│   │   ├── json_repository.py    # JsonJobRepository (TODO: load/save)
│   │   ├── s3_adapter.py         # S3AssetStore (TODO: upload)
│   │   └── containers.py         # DI Container (TODO: wiring)
│   └── presentation/
│       ├── __init__.py
│       └── cli.py                # CLI (COMPLETE — usa DI container)
└── tests/
    ├── __init__.py
    ├── domain/
    │   ├── __init__.py
    │   └── test_entities.py      # Tests del dominio (TODO)
    └── application/
        ├── __init__.py
        └── test_use_cases.py     # Tests de use cases (TODO)
```

---

## Comandos

```bash
pip install -e ".[dev]"

# Procesar un archivo
python -m src run footage/clip.mp4 --project canal9/spot

# Ver estado de jobs
python -m src status

# Tests (sin boto3, ffmpeg ni httpx)
pytest tests/domain/ tests/application/ -v

# Tests con infraestructura (requiere mocks)
pytest tests/ -v

# Type checking
mypy --strict src/
```

---

## Tareas del Estudiante

### `domain/entities.py`
- Completar `Job.start()`, `Job.complete()`, `Job.fail()` con reglas de dominio
- Completar `Asset.set_transcoded()` y `Asset.is_transcoded`

### `domain/value_objects.py`
- Completar `ProjectSlug.__post_init__()` con validación regex
- Completar `MediaType.from_extension()` con el mapa de extensiones
- Completar `S3Key.build()` con la estructura `{project}/{type}/{date}/{file}`

### `domain/repositories.py`
- Definir los 3 Protocols: `IJobRepository`, `IAssetStore`, `ITranscoder`

### `application/use_cases.py`
- Completar `ProcessAssetUseCase.execute()` usando solo interfaces del dominio

### `infrastructure/json_repository.py`
- Implementar `save()` y `find_by_id()` con escritura atómica a JSON

### `infrastructure/s3_adapter.py`
- Implementar `upload()` con boto3 + soporte `dry_run=True`

### `infrastructure/containers.py`
- Configurar Container con `dependency-injector`

### Tests
- `test_entities.py`: al menos 5 tests del dominio sin mocks
- `test_use_cases.py`: al menos 3 tests del use case con InMemory adapters

---

## Criterios de Aceptación

- [ ] `pytest tests/domain/ tests/application/ -v` pasa sin importar boto3, ffmpeg, httpx
- [ ] `mypy --strict src/` pasa sin errores
- [ ] `ProcessAssetUseCase` no importa nada de `infrastructure/`
- [ ] `domain/` no importa nada fuera de stdlib
