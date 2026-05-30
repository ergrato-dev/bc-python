"""
Ejercicio 04: Redis Queue — Encolar y Consultar Jobs
====================================================
Encola jobs de transcoding simulado con RQ y consulta su estado/resultado.

Requisitos:
    docker run -d -p 6379:6379 redis:alpine
    pip install rq redis

Ejecutar en terminal A (worker):
    rq worker --with-scheduler

Ejecutar en terminal B (este script):
    python main.py
"""
from __future__ import annotations

import time
from redis import Redis
from rq import Queue
from rq.job import Job


# ── Tasks (importables por el worker) ─────────────────────────────────────────

def simulate_transcode(input_path: str, crf: int = 23) -> dict[str, object]:
    """Simula transcoding (tarda ~1 segundo)."""
    time.sleep(1)
    return {
        "input": input_path,
        "output": input_path.replace(".mp4", f"_web_crf{crf}.mp4"),
        "crf": crf,
        "status": "done",
    }


def simulate_thumbnail(video_path: str, at_second: float = 5.0) -> str:
    """Simula extracción de thumbnail."""
    time.sleep(0.5)
    return video_path.replace(".mp4", f"_thumb_{at_second:.0f}s.jpg")


# ── TODO 1 ─────────────────────────────────────────────────────────────────────
# Conectar a Redis y crear la cola "studio"
# redis_conn = ...
# q = Queue(...)

def enqueue_transcode_job(input_path: str, crf: int = 23) -> str:
    """Encola un job de transcoding y devuelve su ID."""
    # TODO: q.enqueue(simulate_transcode, input_path, crf, job_timeout=60, result_ttl=300)
    raise NotImplementedError


# ── TODO 2 ─────────────────────────────────────────────────────────────────────
def wait_for_job(job_id: str, timeout: float = 30.0) -> dict[str, object]:
    """
    Espera a que el job termine (polling cada 0.5s hasta timeout).
    Devuelve {"status": ..., "result": ..., "error": ...}.
    """
    # TODO: Job.fetch(job_id, connection=redis_conn)
    # TODO: loop: get_status() → si finished → return result; si failed → return error
    raise NotImplementedError


# ── TODO 3 ─────────────────────────────────────────────────────────────────────
def enqueue_pipeline(video_path: str) -> tuple[str, str]:
    """
    Encola transcode y thumbnail encadenados (thumbnail depende de transcode).
    Devuelve (transcode_job_id, thumb_job_id).
    """
    # TODO: transcode_job = q.enqueue(simulate_transcode, ...)
    # TODO: thumb_job = q.enqueue(simulate_thumbnail, ..., depends_on=transcode_job)
    raise NotImplementedError


if __name__ == "__main__":
    print("=== Test 1: Job único ===")
    jid = enqueue_transcode_job("footage/entrevista.mp4", crf=28)
    print(f"Job encolado: {jid}")
    result = wait_for_job(jid)
    print(f"Resultado: {result}")
    assert result.get("status") in ("finished", "done")

    print("\n=== Test 2: Pipeline encadenado ===")
    t_id, th_id = enqueue_pipeline("footage/spot_verano.mp4")
    print(f"Transcode: {t_id}")
    print(f"Thumbnail (depende del anterior): {th_id}")
    t_result = wait_for_job(t_id)
    th_result = wait_for_job(th_id)
    print(f"Transcode resultado: {t_result}")
    print(f"Thumbnail resultado: {th_result}")

    print("\nOK — Ejercicio 04 completado")
