# watchdog — Fundamentos

## Objetivos

- Entender el modelo Observer + Handler de watchdog
- Suscribirse a eventos del filesystem: created, modified, deleted, moved
- Filtrar eventos por extensión y directorio
- Iniciar y detener el Observer correctamente

---

## 1. Concepto central

watchdog ejecuta un hilo de fondo que llama al SO (inotify en Linux, FSEvents en macOS, ReadDirectoryChanges en Windows) para recibir notificaciones del filesystem. Cada evento se despacha a uno o más `EventHandler`.

```
Sistema Operativo
      │  inotify / FSEvents / kqueue
      ▼
  Observer (hilo daemon)
      │  despacha eventos
      ▼
  FileSystemEventHandler
      │  on_created / on_modified / on_deleted / on_moved
      ▼
  Tu código
```

---

## 2. Handler básico

```python
from watchdog.events import FileSystemEventHandler, FileSystemEvent

class StudioHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        print(f"Nuevo archivo: {event.src_path}")

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        print(f"Modificado: {event.src_path}")

    def on_deleted(self, event: FileSystemEvent) -> None:
        print(f"Eliminado: {event.src_path}")

    def on_moved(self, event: FileSystemEvent) -> None:
        print(f"Movido: {event.src_path} → {event.dest_path}")
```

---

## 3. Observer: iniciar y detener

```python
import time
from pathlib import Path
from watchdog.observers import Observer

handler = StudioHandler()
observer = Observer()
observer.schedule(handler, path=str(Path("drop")), recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()   # señal de parada

observer.join()       # esperar a que el hilo termine limpiamente
```

Puntos clave:
- `observer.start()` lanza el hilo daemon.
- `observer.stop()` + `observer.join()` garantizan salida limpia.
- Sin `join()`, el hilo puede cortarse a mitad de un despacho de evento.

---

## 4. Filtrar por extensión

watchdog también ofrece `PatternMatchingEventHandler` para filtrar en la fuente:

```python
from watchdog.events import PatternMatchingEventHandler

VIDEO_PATTERNS = ["*.mp4", "*.mov", "*.mxf", "*.prores"]

class VideoIngestHandler(PatternMatchingEventHandler):
    def __init__(self) -> None:
        super().__init__(
            patterns=VIDEO_PATTERNS,
            ignore_directories=True,
            case_sensitive=False,
        )

    def on_created(self, event: FileSystemEvent) -> None:
        print(f"Video recibido: {event.src_path}")
```

Alternativa manual (más flexible):

```python
from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mxf", ".prores"}

class GenericHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() in VIDEO_EXTENSIONS:
            self._process_video(path)

    def _process_video(self, path: Path) -> None:
        print(f"Procesando video: {path.name}")
```

---

## 5. Tipos de evento

| Clase de evento | Atributo clave | Cuándo |
|-----------------|----------------|--------|
| `FileCreatedEvent` | `src_path` | Archivo nuevo |
| `FileModifiedEvent` | `src_path` | Contenido o metadatos cambiados |
| `FileDeletedEvent` | `src_path` | Archivo eliminado |
| `FileMovedEvent` | `src_path`, `dest_path` | Renombrado / movido |
| `DirCreatedEvent` | `src_path` | Directorio nuevo |
| `DirDeletedEvent` | `src_path` | Directorio eliminado |

`event.is_directory` — `True` para eventos de directorio.

---

## 6. Problema de doble evento en Linux

En Linux con inotify, copiar un archivo al directorio observado genera:
1. `FileCreatedEvent` (archivo creado vacío o parcial)
2. `FileModifiedEvent` (contenido escrito)

Para esperar a que el archivo esté completo antes de procesarlo:

```python
import time
from pathlib import Path

def wait_for_file_stable(path: Path, interval: float = 0.5, retries: int = 10) -> bool:
    # Espera hasta que el tamaño del archivo no cambie
    prev_size = -1
    for _ in range(retries):
        size = path.stat().st_size
        if size == prev_size and size > 0:
            return True
        prev_size = size
        time.sleep(interval)
    return False
```

---

## ✅ Resumen

| Componente | Rol |
|------------|-----|
| `Observer` | Hilo daemon que escucha al SO |
| `FileSystemEventHandler` | Callbacks por tipo de evento |
| `PatternMatchingEventHandler` | Filtro por patrón en la fuente |
| `observer.schedule()` | Registra handler en una ruta |
| `observer.stop()` + `.join()` | Apagado limpio del hilo |
