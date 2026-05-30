# Redis Queue (RQ)

## 1. ¿Qué es RQ?

RQ (Redis Queue) permite encolar funciones Python para ejecutarlas en **workers separados**, potencialmente en procesos o servidores distintos. Los jobs persisten en Redis, sobreviviendo al proceso principal.

```
[App] → enqueue(func, args) → [Redis] → [Worker] → result en Redis
```

Diferencia clave con `queue.Queue`: RQ persiste los jobs; si el worker muere, el job queda en Redis para reintentarse.

---

## 2. Setup

```bash
# Redis local
docker run -d -p 6379:6379 redis:alpine

# Instalar
pip install rq redis
```

---

## 3. Encolar Jobs

```python
# tasks.py — las funciones deben ser importables por el worker
from pathlib import Path
import time


def transcode_video(input_path: str, output_path: str, crf: int = 23) -> dict[str, object]:
    """Simula transcoding — en producción llamaría a ffmpeg."""
    time.sleep(2)
    return {
        "input": input_path,
        "output": output_path,
        "crf": crf,
        "status": "done",
    }


def generate_thumbnail(video_path: str, at_second: float = 5.0) -> str:
    time.sleep(0.5)
    thumb = video_path.replace(".mp4", f"_thumb_{at_second:.0f}s.jpg")
    return thumb
```

```python
# enqueue_jobs.py
from redis import Redis
from rq import Queue
from tasks import transcode_video, generate_thumbnail

redis_conn = Redis()
q = Queue(connection=redis_conn)

# Encolar job
job = q.enqueue(
    transcode_video,
    "footage/clip.mp4",
    "output/clip_web.mp4",
    crf=23,
    job_timeout=300,        # timeout en segundos
    result_ttl=3600,        # mantener resultado 1h
    failure_ttl=86400,      # mantener job fallido 24h
)

print(f"Job encolado: {job.id}")
print(f"Estado: {job.get_status()}")
```

---

## 4. Correr un Worker

```bash
# Terminal separada (o proceso/contenedor separado)
rq worker --with-scheduler
```

El worker importa la función, la ejecuta y guarda el resultado en Redis.

---

## 5. Consultar Estado y Resultado

```python
from redis import Redis
from rq import Queue
from rq.job import Job

redis_conn = Redis()

# Por ID
job = Job.fetch("job-id-aqui", connection=redis_conn)

print(job.get_status())    # queued | started | finished | failed
print(job.result)          # resultado si está finished
print(job.exc_info)        # traceback si está failed
print(job.enqueued_at)
print(job.started_at)
print(job.ended_at)

# Tiempo de ejecución
if job.started_at and job.ended_at:
    duration = (job.ended_at - job.started_at).total_seconds()
    print(f"Duración: {duration:.2f}s")
```

---

## 6. Colas con Prioridad

```python
redis_conn = Redis()

high_q = Queue("high", connection=redis_conn)
default_q = Queue("default", connection=redis_conn)
low_q = Queue("low", connection=redis_conn)

# Encolar en cola de alta prioridad
high_q.enqueue(transcode_video, "urgent.mp4", "output/urgent_web.mp4")
default_q.enqueue(generate_thumbnail, "clip.mp4")

# Worker que procesa en orden de prioridad
# rq worker high default low
```

---

## 7. Job Dependencies (Encadenamiento)

```python
redis_conn = Redis()
q = Queue(connection=redis_conn)

# Job 1: transcode
transcode_job = q.enqueue(transcode_video, "raw.mp4", "output/web.mp4")

# Job 2: thumbnail — solo corre cuando job 1 termine
thumb_job = q.enqueue(
    generate_thumbnail,
    "output/web.mp4",
    depends_on=transcode_job,
)

print(f"Transcode: {transcode_job.id}")
print(f"Thumbnail (depende del anterior): {thumb_job.id}")
```

---

## 8. Monitoreo con RQ Dashboard

```bash
pip install rq-dashboard
rq-dashboard
# http://localhost:9181
```

---

## Resumen

| Concepto | RQ |
|----------|----|
| Encolar | `q.enqueue(func, *args, **kwargs)` |
| Estado | `job.get_status()` → queued/started/finished/failed |
| Resultado | `job.result` (disponible si finished) |
| Error | `job.exc_info` (traceback si failed) |
| Prioridad | Múltiples colas: `Queue("high")`, `Queue("low")` |
| Dependencias | `depends_on=otro_job` |
| Worker CLI | `rq worker nombre-cola` |
