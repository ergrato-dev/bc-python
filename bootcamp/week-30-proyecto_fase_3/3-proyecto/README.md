# Proyecto Fase 3 — studio-production-pipeline

## Descripción

Sistema completo de pipeline de producción para Studio BC. Monitorea la carpeta `drop/`,
procesa cada video que aparece, lo sube a la nube y notifica al equipo.

## Flujo completo

```
1. Watcher detecta nuevo archivo en drop/
2. IngestStage    — lee el archivo, extrae metadata básica
3. ValidateStage  — verifica extensión, tamaño y que no esté duplicado
4. TranscodeStage — genera proxy + thumbnail + web encode con ffmpeg
5. CloudStage     — sube a S3 con estructura {project}/{type}/{date}/
6. DistributeStage — notifica a Slack con URLs
7. StateStore     — persiste estado en .pipeline_state.json
8. Monitor        — dashboard Rich en tiempo real
```

## Estructura

```
starter/
├── pyproject.toml
├── .env.example
├── src/
│   ├── __init__.py
│   ├── config.py              # PipelineConfig desde .env (COMPLETE)
│   ├── watcher.py             # Watchdog daemon (TODO: on_created)
│   ├── pipeline.py            # PipelineRunner (COMPLETE)
│   ├── monitor.py             # Rich Live dashboard (TODO: build_layout)
│   ├── __main__.py            # CLI: watch | run | status (COMPLETE)
│   └── stages/
│       ├── __init__.py
│       ├── base.py            # Stage Protocol + StageResult (COMPLETE)
│       ├── ingest.py          # IngestStage (COMPLETE)
│       ├── validate.py        # ValidateStage (COMPLETE)
│       ├── transcode.py       # TranscodeStage (TODO: ffmpeg)
│       ├── cloud.py           # CloudStage (TODO: S3 upload)
│       └── distribute.py      # DistributeStage (TODO: Slack)
└── tests/
    ├── __init__.py
    ├── test_stages.py         # Unit tests por etapa (TODO)
    └── test_pipeline.py       # Integration test (TODO)
```

## Comandos

```bash
# Instalar
pip install -e ".[dev]"

# Arrancar daemon
python -m src watch

# Procesar manualmente
python -m src run --path video.mp4 --project canal9/spot-verano

# Estado de jobs
python -m src status

# Dashboard
python -m src dashboard

# Tests
pytest tests/ -v --tb=short
mypy --strict src/
```

## Configuración (.env)

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET=studio-bc-prod-assets
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
PROJECT_SLUG=canal9/spot-verano
DROP_DIR=drop
OUTPUT_DIR=output
STATE_FILE=.pipeline_state.json
DRY_RUN=true
```

## Tareas del Estudiante

### `TranscodeStage.process()` — `stages/transcode.py`
Con `ffmpeg-python`:
- Proxy: 25 % de la resolución original, H.264 veryfast
- Thumbnail: captura en el segundo 5, JPG
- Web encode: H.264 CRF 23, máximo 1080p, `+faststart`

### `CloudStage.process()` — `stages/cloud.py`
Con `boto3`:
- Subir a S3 con clave `{project}/{type}/{date}/{filename}`
- En `dry_run=True`: solo imprimir la clave, no llamar AWS

### `DistributeStage.process()` — `stages/distribute.py`
Con `httpx`:
- Enviar mensaje a Slack webhook con la S3 URL del contexto
- En `dry_run=True`: solo imprimir, no llamar la API

### `FileEventHandler.on_created()` — `watcher.py`
- Filtrar por extensiones de video válidas
- Esperar a que el archivo termine de copiarse
- Encolar la ruta en `self._queue`

### `MonitorDashboard.build_layout()` — `monitor.py`
- Layout Rich con tabla de jobs y panel de estado global

### Tests
- `test_stages.py`: unit tests de cada etapa con mocks de ffmpeg, boto3, httpx
- `test_pipeline.py`: test de integración del flujo completo

## Criterios de Aceptación

- [ ] `pytest tests/ -v` pasa con cobertura ≥ 80 %
- [ ] `mypy --strict src/` pasa sin errores
- [ ] Demo: copiar `.mp4` a `drop/` → pipeline lo procesa automáticamente
- [ ] `.pipeline_state.json` contiene el job con `status: done`
