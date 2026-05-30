# Proyecto Semana 27 — studio-pipeline

## Objetivo

Construir un framework de pipeline propio para Studio BC que encadena etapas
`Ingest → Validate → Process → Export` con:

- Contrato de etapa via `Stage` Protocol
- Estado persistido por job en `.pipeline_state.json`
- Retry automático con backoff exponencial en etapas configurables
- Dead-letter queue para jobs definitivamente fallidos
- CLI con comandos `run`, `status` y `requeue`

---

## Estructura

```
starter/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── stages.py          # Stage Protocol, StageResult, etapas concretas
│   ├── pipeline.py        # Pipeline: run(), run_batch()
│   ├── state.py           # JobStatus, JobRecord, StateStore
│   ├── retry.py           # RetryableStage, DeadLetterQueue
│   └── __main__.py        # Typer CLI: run, status, requeue
└── tests/
    ├── __init__.py
    ├── test_pipeline.py
    └── test_state.py
```

---

## Comandos CLI

```bash
# Procesar un archivo
python -m src run --path footage/clip.mp4 --project canal9/spot

# Ver estado de todos los jobs
python -m src status

# Reencolar un job fallido
python -m src requeue --job-id abc123
```

---

## Criterios de Aprobación

- [ ] Pipeline encadena Ingest → Validate → Process → Export
- [ ] Estado persiste en `.pipeline_state.json` con transiciones correctas
- [ ] Retry automático (max 3) en etapas marcadas como retryable
- [ ] `mypy --strict` sin errores
