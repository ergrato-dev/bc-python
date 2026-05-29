"""Handler watchdog para ingest de archivos."""

import logging
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler, FileSystemEvent

from .organizer import FileOrganizer

logger = logging.getLogger(__name__)


class IngestHandler(FileSystemEventHandler):
    def __init__(self, organizer: FileOrganizer) -> None:
        self._organizer = organizer

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        path = Path(event.src_path)

        # TODO:
        # 1. Esperar 0.3s para que el archivo termine de escribirse
        # 2. Verificar que path.exists() (puede haber sido movido)
        # 3. Llamar self._organizer.organize(path)
        # 4. Capturar cualquier excepción con logger.error (no propagar)
        raise NotImplementedError
