"""
Ejercicio 02 — watchdog: Monitor de Directorio

Contexto: Necesitamos un monitor que registre todos los eventos
en la carpeta `drop/` del estudio y los imprima en consola con timestamp.

Instrucciones:
1. Completá `StudioMonitorHandler` — imprime cada evento con su tipo y path
2. Completá `run_monitor()` — inicia el Observer y maneja KeyboardInterrupt
3. La función `on_created` debe filtrar directorios (ignorar DirCreatedEvent)
4. Incluir timestamp en cada mensaje: `[HH:MM:SS] TIPO path`

Ejecutar: python main.py
Probar: crear/modificar/borrar archivos en drop/ mientras corre
"""

import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileSystemEvent,
)


class StudioMonitorHandler(FileSystemEventHandler):
    def _log(self, event_type: str, path: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        # TODO: imprimir f"[{ts}] {event_type:<10} {path}"
        raise NotImplementedError

    def on_created(self, event: FileSystemEvent) -> None:
        # TODO: ignorar directorios, llamar _log("CREATED", event.src_path)
        raise NotImplementedError

    def on_modified(self, event: FileSystemEvent) -> None:
        # TODO: ignorar directorios, llamar _log("MODIFIED", event.src_path)
        raise NotImplementedError

    def on_deleted(self, event: FileSystemEvent) -> None:
        # TODO: llamar _log("DELETED", event.src_path)
        raise NotImplementedError

    def on_moved(self, event: FileSystemEvent) -> None:
        # TODO: llamar _log con "MOVED" y mostrar src → dest
        raise NotImplementedError


def run_monitor(watch_path: Path) -> None:
    """Inicia el Observer y bloquea hasta KeyboardInterrupt."""
    watch_path.mkdir(parents=True, exist_ok=True)
    handler = StudioMonitorHandler()
    observer = Observer()

    # TODO: observer.schedule(handler, path=str(watch_path), recursive=True)
    # TODO: observer.start()
    # TODO: bucle while True + time.sleep(1)
    # TODO: capturar KeyboardInterrupt → observer.stop()
    # TODO: observer.join()
    raise NotImplementedError


if __name__ == "__main__":
    drop_dir = Path("drop")
    print(f"Monitoreando {drop_dir.resolve()} — Ctrl+C para detener")
    run_monitor(drop_dir)
