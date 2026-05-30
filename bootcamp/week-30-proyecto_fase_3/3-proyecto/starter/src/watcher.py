"""
Watchdog daemon — monitorea drop/ y encola archivos nuevos para el pipeline.

Referencia: semana 22 — sistema de archivos con watchdog
"""
from __future__ import annotations

import queue
import time
from pathlib import Path

from watchdog.events import FileCreatedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .stages.ingest import VIDEO_EXTENSIONS, AUDIO_EXTENSIONS, IMAGE_EXTENSIONS

WATCHED_EXTENSIONS = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | IMAGE_EXTENSIONS


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, q: "queue.Queue[str]") -> None:
        super().__init__()
        self._queue = q

    def on_created(self, event: FileCreatedEvent) -> None:  # type: ignore[override]
        """
        Maneja la creación de un archivo en drop/.

        TODO:
        1. Ignorar directorios: if event.is_directory: return
        2. Filtrar por extensión: si no está en WATCHED_EXTENSIONS, return
        3. Esperar a que el archivo termine de copiarse:
               while True:
                   size_before = path.stat().st_size
                   time.sleep(0.5)
                   if path.stat().st_size == size_before: break
           (si el archivo desaparece, ignorar)
        4. Encolar: self._queue.put(str(path))

        Referencia: semana 22 — FileSystemEventHandler.on_created()
        """
        raise NotImplementedError


def start_watcher(drop_dir: Path, q: "queue.Queue[str]") -> Observer:
    """Inicia el Observer de watchdog en drop_dir y devuelve el Observer activo."""
    handler = FileEventHandler(q)
    observer = Observer()
    observer.schedule(handler, str(drop_dir), recursive=False)
    observer.start()
    return observer
