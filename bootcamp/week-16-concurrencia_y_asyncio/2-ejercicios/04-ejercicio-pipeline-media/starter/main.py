"""
Ejercicio 04 — Pipeline de Media con Semáforos
Studio BC: pipeline de descarga, transcodificación y subida con control de concurrencia.
"""

import asyncio
import random
import time
from dataclasses import dataclass, field
from typing import Literal

MAX_CONCURRENT = 3

type JobStatus = Literal["pending", "downloading", "transcoding", "uploading", "done", "failed"]


# ─────────────────────────────────────────────
# PASO 1 — Dataclass de estado
# ─────────────────────────────────────────────

# TODO: completa el dataclass AssetJob con:
# - name: str
# - url: str
# - status: JobStatus = "pending"
# - error: str | None = None
# - retries: int = 0
# Añade un método mark_failed(self, reason: str) -> None que:
# - establece status = "failed"
# - guarda reason en error

@dataclass
class AssetJob:
    name: str
    url: str
    # TODO: añadir status, error, retries con valores por defecto
    # status: JobStatus = ...
    # error: str | None = ...
    # retries: int = ...

    # def mark_failed(self, reason: str) -> None:
    #     ...


# ─────────────────────────────────────────────
# PASO 2 — Etapas del pipeline
# ─────────────────────────────────────────────

# TODO: implementa las 3 etapas. Cada una debe:
# - actualizar job.status al nombre de la etapa
# - simular trabajo con await asyncio.sleep(...)
# - lanzar RuntimeError(f"{job.name}: etapa falló") con ~20% de probabilidad
#   usando: if random.random() < 0.2: raise RuntimeError(...)

# async def download_stage(job: AssetJob) -> None:
#     job.status = "downloading"
#     await asyncio.sleep(1.5)
#     if random.random() < 0.2:
#         raise RuntimeError(f"{job.name}: download failed")

# async def transcode_stage(job: AssetJob) -> None:
#     ...

# async def upload_stage(job: AssetJob) -> None:
#     ...


# ─────────────────────────────────────────────
# PASO 3 — Semáforo de concurrencia
# ─────────────────────────────────────────────

# TODO: implementa process_job(sem, job) que:
# 1. Adquiere el semáforo con `async with sem:`
# 2. Ejecuta download_stage → transcode_stage → upload_stage en secuencia
# 3. Si cualquier etapa lanza una excepción, llama job.mark_failed(str(e))
# 4. Si todo sale bien, establece job.status = "done"
# Imprime: f"[{job.name}] {job.status}" en cada cambio de estado

# async def process_job(sem: asyncio.Semaphore, job: AssetJob) -> None:
#     async with sem:
#         try:
#             ...
#         except Exception as e:
#             ...


# ─────────────────────────────────────────────
# PASO 4 — Retry con backoff
# ─────────────────────────────────────────────

# TODO: implementa process_job_with_retry(sem, job, max_retries=2) que:
# 1. Llama a process_job(sem, job)
# 2. Si el job queda en "failed" y job.retries < max_retries:
#    - incrementa job.retries
#    - resetea job.status = "pending" y job.error = None
#    - espera base_delay * (2 ** job.retries) segundos (backoff exponencial)
#    - reintenta
# 3. Imprime cuando reintenta: f"  ↺ {job.name} retry {job.retries}/{max_retries}"

# async def process_job_with_retry(
#     sem: asyncio.Semaphore,
#     job: AssetJob,
#     max_retries: int = 2,
#     base_delay: float = 1.0,
# ) -> None:
#     for attempt in range(max_retries + 1):
#         ...


# ─────────────────────────────────────────────
# Pipeline principal
# ─────────────────────────────────────────────

async def run_pipeline(jobs: list[AssetJob]) -> None:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    start = time.perf_counter()

    # TODO: reemplaza la línea de abajo con process_job_with_retry cuando esté listo
    # await asyncio.gather(*[process_job_with_retry(sem, job) for job in jobs])

    # Versión de prueba sin retry (descomenta cuando tengas process_job):
    # await asyncio.gather(*[process_job(sem, job) for job in jobs])

    elapsed = time.perf_counter() - start

    done = sum(1 for j in jobs if j.status == "done")
    failed = sum(1 for j in jobs if j.status == "failed")
    retried = sum(1 for j in jobs if j.retries > 0)

    print(f"\n── Resumen ──")
    print(f"  ✅ done: {done}")
    print(f"  ❌ failed: {failed}")
    print(f"  ↺ retried: {retried}")
    print(f"  ⏱ tiempo total: {elapsed:.2f}s")


if __name__ == "__main__":
    jobs = [
        AssetJob(f"clip_{i:02d}.mp4", f"https://cdn.studio.bc/clip_{i}.mp4")
        for i in range(9)
    ]
    asyncio.run(run_pipeline(jobs))
