"""
Ejercicio 01: structlog — Logging Estructurado con Contexto
===========================================================
Configura structlog con JSON output y usa contextvars para agregar
job_id a todos los eventos de una ejecución.

Instalar: pip install structlog
Ejecutar: python main.py
"""
from __future__ import annotations

import time
import structlog


def configure_logging(json_output: bool = False) -> None:
    """
    Configura structlog con:
    - TimeStamper(fmt="iso")
    - add_log_level
    - JSONRenderer si json_output=True, ConsoleRenderer si no
    """
    # TODO: structlog.configure(processors=[...], ...)
    raise NotImplementedError


def process_stage(stage_name: str, duration_s: float = 0.1) -> None:
    """
    Loggea inicio y fin de una etapa.
    Usa structlog.get_logger() y agrega stage=stage_name al contexto.
    """
    # TODO: log = structlog.get_logger().bind(stage=stage_name)
    # TODO: log.info("stage_started")
    # TODO: time.sleep(duration_s)
    # TODO: log.info("stage_ok", duration_s=duration_s)
    raise NotImplementedError


def process_job(job_id: str, path: str) -> None:
    """
    Procesa un job de principio a fin.
    Usa contextvars para agregar job_id y path a todos los logs del job.
    """
    # TODO: structlog.contextvars.clear_contextvars()
    # TODO: structlog.contextvars.bind_contextvars(job_id=job_id, path=path)
    # TODO: log.info("job_started")
    # TODO: llamar process_stage para "ingest", "validate", "export"
    # TODO: log.info("job_done")
    raise NotImplementedError


if __name__ == "__main__":
    print("=== Modo desarrollo (ConsoleRenderer) ===")
    configure_logging(json_output=False)
    process_job("job-001", "footage/clip.mp4")

    print("\n=== Modo producción (JSON) ===")
    configure_logging(json_output=True)
    process_job("job-002", "footage/entrevista.mp4")

    print("\nOK — Ejercicio 01 completado")
