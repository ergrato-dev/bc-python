# Structured Logging con structlog

## 1. El Problema del Logging Clásico

```python
# Logging clásico — difícil de parsear en producción
logging.info("Job abc123 en etapa transcode tardó 4.2s — OK")
logging.error("Job xyz789 falló en etapa export: S3 ConnectionError")
```

Estos mensajes son legibles para humanos pero difíciles de filtrar, agregar o enviar a Datadog/Loki/CloudWatch.

---

## 2. structlog — Logging Estructurado

```python
import structlog

log = structlog.get_logger()

# Cada campo es un par clave-valor
log.info("etapa_ok", job_id="abc123", stage="transcode", duration_s=4.2)
log.error("etapa_fallo", job_id="xyz789", stage="export", error="S3 ConnectionError")
```

Salida JSON (en producción):
```json
{"event": "etapa_ok", "job_id": "abc123", "stage": "transcode", "duration_s": 4.2, "level": "info", "timestamp": "2024-11-15T14:23:01Z"}
{"event": "etapa_fallo", "job_id": "xyz789", "stage": "export", "error": "S3 ConnectionError", "level": "error", "timestamp": "2024-11-15T14:23:05Z"}
```

---

## 3. Configuración

```python
import logging
import sys
import structlog


def configure_logging(json_output: bool = False) -> None:
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if json_output:
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
```

---

## 4. Contexto por Request con `bind()`

`bind()` agrega campos al logger que se incluyen en todos los eventos posteriores:

```python
import structlog

log = structlog.get_logger()


def process_job(job_id: str, path: str) -> None:
    bound_log = log.bind(job_id=job_id, path=path)

    bound_log.info("job_started")

    for stage_name in ["ingest", "validate", "transcode", "export"]:
        stage_log = bound_log.bind(stage=stage_name)
        stage_log.info("stage_started")
        # ... trabajo ...
        stage_log.info("stage_ok", duration_s=1.2)

    bound_log.info("job_done")
```

Salida:
```json
{"event": "job_started", "job_id": "abc123", "path": "clip.mp4"}
{"event": "stage_started", "job_id": "abc123", "path": "clip.mp4", "stage": "ingest"}
{"event": "stage_ok", "job_id": "abc123", "stage": "ingest", "duration_s": 1.2}
```

---

## 5. Context Variables (por Thread/Coroutine)

Para no pasar `bound_log` a cada función, usar `contextvars`:

```python
import structlog

structlog.contextvars.clear_contextvars()
structlog.contextvars.bind_contextvars(job_id="abc123", project="canal9/spot")

log = structlog.get_logger()
log.info("stage_ok", stage="transcode")
# → {"event": "stage_ok", "job_id": "abc123", "project": "canal9/spot", "stage": "transcode"}
```

`clear_contextvars()` al inicio de cada request/job evita que el contexto de uno contamine el siguiente.

---

## 6. Processors Personalizados

```python
from typing import Any


def add_studio_context(
    logger: Any, method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    event_dict["service"] = "studio-pipeline"
    event_dict["env"] = "production"
    return event_dict


def censor_secrets(
    logger: Any, method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    for key in ("token", "password", "secret", "api_key"):
        if key in event_dict:
            event_dict[key] = "***"
    return event_dict
```

Se agregan a la lista `processors` en `structlog.configure()`.

---

## Resumen

| Concepto | Uso |
|----------|-----|
| `log.info("event", key=value)` | Log estructurado con campos explícitos |
| `log.bind(**fields)` | Logger con contexto adicional para todos los siguientes logs |
| `contextvars.bind_contextvars()` | Contexto por thread/coroutine sin pasar el logger |
| `JSONRenderer()` | Salida JSON para producción (Datadog, Loki, CloudWatch) |
| `ConsoleRenderer()` | Salida colorizada para desarrollo |
| Processor | Función que transforma `event_dict` antes de renderizar |
