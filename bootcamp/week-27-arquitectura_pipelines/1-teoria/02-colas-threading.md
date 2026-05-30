# Colas y Threading

## 1. `queue.Queue` — Thread-Safe FIFO

`queue.Queue` de la stdlib es thread-safe: múltiples threads pueden hacer `put()` y `get()` sin race conditions.

```python
import queue
import threading
import time


def producer(q: queue.Queue[dict[str, object]], items: list[str]) -> None:
    for item in items:
        print(f"[producer] encolando {item}")
        q.put({"path": item, "ts": time.time()})
        time.sleep(0.1)
    q.put(None)  # sentinel: señal de fin


def consumer(q: queue.Queue[dict[str, object]], worker_id: int) -> None:
    while True:
        item = q.get()
        if item is None:
            q.put(None)  # reencolar el sentinel para otros workers
            break
        print(f"[worker-{worker_id}] procesando {item['path']}")
        time.sleep(0.3)  # simular trabajo
        q.task_done()


def run_pipeline(files: list[str], num_workers: int = 2) -> None:
    q: queue.Queue[dict[str, object]] = queue.Queue(maxsize=10)

    prod = threading.Thread(target=producer, args=(q, files))
    workers = [
        threading.Thread(target=consumer, args=(q, i))
        for i in range(num_workers)
    ]

    prod.start()
    for w in workers:
        w.start()

    prod.join()
    for w in workers:
        w.join()

    print("Pipeline completado")
```

### Variantes de Queue

| Clase | Orden | Uso |
|-------|-------|-----|
| `queue.Queue` | FIFO | Pipeline clásico |
| `queue.LifoQueue` | LIFO (pila) | DFS, undo stacks |
| `queue.PriorityQueue` | Por prioridad | Tareas urgentes primero |

---

## 2. `maxsize` y Backpressure

```python
q: queue.Queue[dict[str, object]] = queue.Queue(maxsize=5)

# put() bloquea si la cola está llena
q.put(item)  # bloquea hasta que haya espacio

# put_nowait() lanza queue.Full si está llena
try:
    q.put_nowait(item)
except queue.Full:
    print("Cola llena — descartar o esperar")
```

`maxsize > 0` activa **backpressure**: el producer se frena si los consumers no pueden seguir el ritmo.

---

## 3. `asyncio.Queue` — Para Coroutines

Cuando el pipeline usa `async/await`, `queue.Queue` no funciona — bloquea el event loop. Se usa `asyncio.Queue`:

```python
import asyncio


async def producer(q: asyncio.Queue[str], items: list[str]) -> None:
    for item in items:
        await q.put(item)
        await asyncio.sleep(0.05)
    await q.put("")  # sentinel


async def consumer(q: asyncio.Queue[str], worker_id: int) -> None:
    while True:
        item = await q.get()
        if not item:
            await q.put("")  # reencolar sentinel
            break
        print(f"[async-worker-{worker_id}] procesando {item}")
        await asyncio.sleep(0.1)
        q.task_done()


async def main() -> None:
    files = ["clip1.mp4", "clip2.mp4", "clip3.mp4"]
    q: asyncio.Queue[str] = asyncio.Queue(maxsize=5)

    await asyncio.gather(
        producer(q, files),
        consumer(q, 0),
        consumer(q, 1),
    )

asyncio.run(main())
```

---

## 4. Pipeline con `concurrent.futures`

Para pipelines donde cada etapa es CPU-bound, `ProcessPoolExecutor` permite verdadero paralelismo:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def process_file(path: str) -> dict[str, object]:
    # Simular procesamiento (IO-bound → ThreadPool está bien)
    import time; time.sleep(0.5)
    return {"path": path, "size": Path(path).stat().st_size if Path(path).exists() else 0}


def batch_process(files: list[str], max_workers: int = 4) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(process_file, f): f for f in files}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error en {futures[future]}: {e}")
    return results
```

---

## 5. Cuándo usar cada herramienta

| Herramienta | Cuándo |
|-------------|--------|
| `queue.Queue` | Pipeline síncrono con múltiples threads, IO-bound |
| `asyncio.Queue` | Pipeline async con `await` (httpx, aiofiles) |
| `ThreadPoolExecutor` | Batch de tareas IO-bound con control de concurrencia |
| `ProcessPoolExecutor` | Tareas CPU-bound (encoding, procesamiento de imágenes) |
| RQ / Celery | Trabajos en background que sobreviven al proceso principal |

---

## Resumen

| Concepto | Clave |
|----------|-------|
| `q.task_done()` | Señal al `q.join()` de que un item fue procesado |
| Sentinel `None` / `""` | Señal de fin de stream para consumers |
| `maxsize` | Limita memoria y aplica backpressure al producer |
| `asyncio.Queue` | No bloquea el event loop — obligatorio en contextos async |
