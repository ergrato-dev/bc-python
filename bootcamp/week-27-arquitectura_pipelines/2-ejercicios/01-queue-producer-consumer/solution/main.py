"""
Ejercicio 01: Producer/Consumer con queue.Queue — SOLUCIÓN
==========================================================
"""
from __future__ import annotations

import queue
import threading
import time


def producer(
    q: "queue.Queue[dict[str, object] | None]",
    files: list[str],
    delay: float = 0.1,
) -> None:
    for file in files:
        print(f"[producer] encolando {file}")
        q.put({"path": file, "ts": time.time()})
        time.sleep(delay)
    q.put(None)  # sentinel: señal de fin


def consumer(
    q: "queue.Queue[dict[str, object] | None]",
    worker_id: int,
    results: list[str],
    lock: threading.Lock,
) -> None:
    while True:
        item = q.get()
        if item is None:
            q.put(None)  # reencolar sentinel para otros workers
            break
        path = str(item["path"])
        print(f"[worker-{worker_id}] procesando {path}")
        time.sleep(0.2)  # simular trabajo
        with lock:
            results.append(path)
        q.task_done()


def run_pipeline(files: list[str], num_workers: int = 2) -> list[str]:
    q: queue.Queue[dict[str, object] | None] = queue.Queue(maxsize=5)
    results: list[str] = []
    lock = threading.Lock()

    prod = threading.Thread(target=producer, args=(q, files))
    workers = [
        threading.Thread(target=consumer, args=(q, i, results, lock))
        for i in range(num_workers)
    ]

    prod.start()
    for w in workers:
        w.start()

    prod.join()
    for w in workers:
        w.join()

    return results


if __name__ == "__main__":
    files = [f"clip_{i:02d}.mp4" for i in range(8)]
    print(f"Procesando {len(files)} archivos con 2 workers...")
    t0 = time.time()
    processed = run_pipeline(files, num_workers=2)
    elapsed = time.time() - t0

    print(f"Procesados: {len(processed)} archivos en {elapsed:.2f}s")
    assert len(processed) == len(files), f"Esperaba {len(files)}, obtuve {len(processed)}"
    print("OK — Ejercicio 01 completado")
