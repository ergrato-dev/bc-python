# 🎯 Ejercicio 02: Pattern Matching en Studio BC

## 🎯 Objetivo

Usar `match/case` para hacer routing de comandos CLI, clasificar assets y manejar eventos del pipeline de producción.

---

## Paso 1: Routing de comandos con literales y OR

```python
def handle_command(command: str) -> str:
    match command:
        case "help" | "h" | "--help":
            return "Comandos: list, add, remove, status"
        case "list":
            return "Listando proyectos..."
        case "add":
            return "Agregando proyecto..."
        case _:
            return f"Comando desconocido: {command!r}"
```

**Abre `starter/main.py`** y descomenta la sección **PASO 1**.

---

## Paso 2: Guards con condiciones

```python
def classify_file(filename: str, size_mb: float) -> str:
    match filename:
        case name if name.endswith((".mp4", ".mov", ".avi")) and size_mb > 500:
            return f"video pesado: {name}"
        case name if name.endswith((".mp4", ".mov", ".avi")):
            return f"video liviano: {name}"
        case name if name.endswith((".jpg", ".png", ".webp")):
            return f"imagen: {name}"
        case _:
            return f"desconocido: {filename}"
```

**Descomenta la sección PASO 2.**

---

## Paso 3: Class patterns con dataclasses

```python
from dataclasses import dataclass

@dataclass
class VideoAsset:
    name: str
    duration_s: float
    codec: str

@dataclass
class ImageAsset:
    name: str
    width: int
    height: int

def describe(asset: VideoAsset | ImageAsset) -> str:
    match asset:
        case VideoAsset(name=n, duration_s=d) if d > 3600:
            return f"video largo: {n} ({d/3600:.1f}h)"
        case VideoAsset(name=n, codec="h265"):
            return f"video HEVC: {n}"
        case VideoAsset(name=n):
            return f"video: {n}"
        case ImageAsset(name=n, width=w, height=h):
            return f"imagen {w}×{h}: {n}"
```

**Descomenta la sección PASO 3.**

---

## Paso 4: Mapping patterns — eventos del pipeline

```python
def handle_pipeline_event(event: dict[str, object]) -> None:
    match event:
        case {"type": "upload_complete", "file": str(path), "size_mb": float(mb)}:
            print(f"upload OK: {path} ({mb:.1f} MB)")
        case {"type": "transcode_failed", "error": str(err)}:
            print(f"transcode error: {err}")
        case {"type": str(unknown)}:
            print(f"evento no manejado: {unknown}")
```

**Descomenta la sección PASO 4.**

---

## ✅ Resultado esperado

```
=== PASO 1: Routing de comandos ===
list → Listando proyectos...
help → Comandos: list, add, remove, status
xyz  → Comando desconocido: 'xyz'

=== PASO 2: Guards ===
video pesado: produccion_final.mp4
imagen: thumbnail.jpg
desconocido: notes.txt

=== PASO 3: Class patterns ===
video largo: documental.mp4 (2.1h)
video HEVC: campana_hevc.mp4
imagen 1920×1080: banner.png

=== PASO 4: Mapping patterns (pipeline events) ===
upload OK: /media/raw/video.mp4 (1024.0 MB)
transcode error: codec not supported
evento no manejado: health_check
```
