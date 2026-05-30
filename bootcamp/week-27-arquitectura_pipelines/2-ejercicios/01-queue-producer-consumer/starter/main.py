"""
Ejercicio 01: Producer/Consumer con queue.Queue
===============================================
Implementa un pipeline básico donde el producer pone archivos en la cola
y dos workers los consumen en paralelo.

Ejecutar:
    python main.py
"""
from __future__ import annotations

import queue
import threading
import time
from pathlib import Path


def producer(
    q: "queue.Queue[dict[str, object] | None]",
    files: list[str],
    delay: float = 0.1,
) -> None:
    """Encola cada archivo como dict y envía sentinel None al terminar."""
    # TODO: q.put({"path": file, "ts": time.time()}) para cada archivo
    # TODO: q.put(None) como sentinel al final
    raise NotImplementedError


def consumer(
    q: "queue.Queue[dict[str, object] | None]",
    worker_id: int,
    results: list[str],
    lock: threading.Lock,
) -> None:
    """
    Procesa items hasta recibir el sentinel None.
    Guarda el nombre del archivo en results (con lock).
    Reencola el sentinel para que otros workers también puedan terminar.
    """
    # TODO: while True → q.get() → si None: q.put(None); break
    # TODO: procesar (simular con time.sleep(0.2)) y agregar a results con lock
    # TODO: q.task_done() después de procesar
    raise NotImplementedError


def run_pipeline(files: list[str], num_workers: int = 2) -> list[str]:
    """Corre el pipeline y devuelve la lista de archivos procesados."""
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
