"""
Ejercicio 04: Redis Queue — Encolar y Consultar Jobs — SOLUCIÓN
===============================================================

Requisitos:
    docker run -d -p 6379:6379 redis:alpine
    pip install rq redis

Ejecutar en terminal A (worker):
    rq worker studio --with-scheduler

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


# ── Conexión ──────────────────────────────────────────────────────────────────

redis_conn = Redis()
q = Queue("studio", connection=redis_conn)


# ── Funciones ─────────────────────────────────────────────────────────────────

def enqueue_transcode_job(input_path: str, crf: int = 23) -> str:
    job = q.enqueue(
        simulate_transcode,
        input_path,
        crf,
        job_timeout=60,
        result_ttl=300,
        failure_ttl=3600,
    )
    return job.id


def wait_for_job(job_id: str, timeout: float = 30.0) -> dict[str, object]:
    start = time.time()
    while time.time() - start < timeout:
        job = Job.fetch(job_id, connection=redis_conn)
        status_val = job.get_status()
        status_str = str(status_val) if status_val is not None else "unknown"
        if "finished" in status_str:
            return {"status": "finished", "result": job.result, "error": None}
        if "failed" in status_str:
            return {"status": "failed", "result": None, "error": str(job.exc_info)}
        time.sleep(0.5)
    return {"status": "timeout", "result": None, "error": "Job timed out"}


def enqueue_pipeline(video_path: str) -> tuple[str, str]:
    transcode_job = q.enqueue(
        simulate_transcode,
        video_path,
        job_timeout=60,
        result_ttl=300,
    )
    thumb_job = q.enqueue(
        simulate_thumbnail,
        video_path,
        depends_on=transcode_job,
        result_ttl=300,
    )
    return transcode_job.id, thumb_job.id


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
