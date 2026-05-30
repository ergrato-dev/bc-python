"""
Ejercicio 01: structlog — Logging Estructurado con Contexto — SOLUCIÓN
======================================================================
"""
from __future__ import annotations

import time
import structlog


def configure_logging(json_output: bool = False) -> None:
    processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


def process_stage(stage_name: str, duration_s: float = 0.1) -> None:
    log = structlog.get_logger().bind(stage=stage_name)
    log.info("stage_started")
    time.sleep(duration_s)
    log.info("stage_ok", duration_s=duration_s)


def process_job(job_id: str, path: str) -> None:
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(job_id=job_id, path=path)
    log = structlog.get_logger()

    log.info("job_started")
    for stage in ["ingest", "validate", "export"]:
        process_stage(stage, duration_s=0.05)
    log.info("job_done")


if __name__ == "__main__":
    print("=== Modo desarrollo (ConsoleRenderer) ===")
    configure_logging(json_output=False)
    process_job("job-001", "footage/clip.mp4")

    print("\n=== Modo producción (JSON) ===")
    configure_logging(json_output=True)
    process_job("job-002", "footage/entrevista.mp4")

    print("\nOK — Ejercicio 01 completado")
