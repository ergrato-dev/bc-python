# Organización Automática de Archivos

## Objetivos

- Definir reglas de clasificación basadas en extensión y metadata
- Construir la estructura de destino dinámicamente con pathlib
- Mover archivos con manejo de colisiones y errores
- Aplicar el principio de responsabilidad única al organizador

---

## 1. Clasificador por extensión

```python
from enum import StrEnum
from pathlib import Path

class MediaType(StrEnum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    DOC   = "doc"
    OTHER = "other"

EXTENSION_MAP: dict[str, MediaType] = {
    # Video
    ".mp4": MediaType.VIDEO,
    ".mov": MediaType.VIDEO,
    ".mxf": MediaType.VIDEO,
    ".prores": MediaType.VIDEO,
    ".avi": MediaType.VIDEO,
    # Audio
    ".wav": MediaType.AUDIO,
    ".aiff": MediaType.AUDIO,
    ".mp3": MediaType.AUDIO,
    ".flac": MediaType.AUDIO,
    # Imagen
    ".jpg": MediaType.IMAGE,
    ".jpeg": MediaType.IMAGE,
    ".png": MediaType.IMAGE,
    ".tiff": MediaType.IMAGE,
    ".psd": MediaType.IMAGE,
    # Documentos
    ".pdf": MediaType.DOC,
    ".docx": MediaType.DOC,
    ".xlsx": MediaType.DOC,
    ".txt": MediaType.DOC,
}

def classify(path: Path) -> MediaType:
    return EXTENSION_MAP.get(path.suffix.lower(), MediaType.OTHER)
```

---

## 2. Construir ruta de destino

El destino sigue la estructura: `organized/{tipo}/{YYYY-MM}/`

```python
from datetime import datetime
from pathlib import Path

def build_dest_dir(base: Path, media_type: MediaType, path: Path) -> Path:
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    month = mtime.strftime("%Y-%m")
    return base / media_type / month
```

---

## 3. Mover con seguridad

```python
import shutil
from pathlib import Path

def safe_move(src: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name

    if dest.exists():
        stem, suffix = src.stem, src.suffix
        counter = 1
        while dest.exists():
            dest = dest_dir / f"{stem}_{counter:03d}{suffix}"
            counter += 1

    shutil.move(str(src), dest)
    return dest
```

---

## 4. Organizador completo

```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self, dest_base: Path) -> None:
        self._dest = dest_base

    def organize(self, src: Path) -> Path | None:
        if not src.is_file():
            return None

        media_type = classify(src)
        dest_dir = build_dest_dir(self._dest, media_type, src)

        try:
            dest = safe_move(src, dest_dir)
            logger.info("Moved %s → %s", src.name, dest)
            return dest
        except OSError as e:
            logger.error("Failed to move %s: %s", src, e)
            return None

    def organize_folder(self, folder: Path) -> list[Path]:
        results = []
        for f in folder.rglob("*"):
            if f.is_file():
                dest = self.organize(f)
                if dest:
                    results.append(dest)
        return results
```

---

## 5. Integración con watchdog

```python
import time
from pathlib import Path
from watchdog.events import FileSystemEventHandler, FileSystemEvent

class IngestHandler(FileSystemEventHandler):
    def __init__(self, organizer: FileOrganizer) -> None:
        self._organizer = organizer

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        # Pequeña espera para que el archivo termine de escribirse
        time.sleep(0.3)
        if path.exists():
            self._organizer.organize(path)
```

---

## ✅ Resumen

| Concepto | Implementación |
|----------|----------------|
| Clasificación | `EXTENSION_MAP` dict + `MediaType` enum |
| Ruta de destino | `organized/{tipo}/{YYYY-MM}/` |
| Movimiento seguro | `shutil.move()` + counter de colisiones |
| Integración watcher | `on_created` llama a `FileOrganizer.organize()` |
