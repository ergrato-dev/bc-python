# Batch Processing de Imágenes

## Objetivos

- Procesar lotes de imágenes con `ThreadPoolExecutor`
- Mostrar progreso en tiempo real con Rich
- Manejar errores por archivo sin interrumpir el lote
- Medir tiempos y optimizar throughput

---

## 1. Por qué ThreadPoolExecutor para imágenes

Procesar imágenes es **CPU-bound** (redimensionar, comprimir) pero también tiene partes **I/O-bound** (leer y escribir disco). `ThreadPoolExecutor` funciona bien en la práctica porque:
- El GIL se libera durante operaciones I/O del disco
- Pillow libera el GIL durante operaciones de compresión en C
- Para paralelismo CPU puro, usar `ProcessPoolExecutor`

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def process_one(src: Path, dest_dir: Path) -> Path:
    # Simula el trabajo: abrir, resize, guardar
    from PIL import Image
    with Image.open(src) as img:
        img.thumbnail((800, 600), Image.LANCZOS)
        dest = dest_dir / src.with_suffix(".webp").name
        img.convert("RGB").save(dest, "WEBP", quality=85)
    return dest

def batch_process(
    sources: list[Path],
    dest_dir: Path,
    max_workers: int = 4,
) -> tuple[list[Path], list[tuple[Path, Exception]]]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    results: list[Path] = []
    errors: list[tuple[Path, Exception]] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_src = {
            executor.submit(process_one, src, dest_dir): src
            for src in sources
        }
        for future in as_completed(future_to_src):
            src = future_to_src[future]
            try:
                dest = future.result()
                results.append(dest)
            except Exception as e:
                errors.append((src, e))

    return results, errors
```

---

## 2. Progress bar con Rich

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
)

def batch_with_progress(
    sources: list[Path],
    dest_dir: Path,
    max_workers: int = 4,
) -> tuple[list[Path], list[tuple[Path, Exception]]]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    results: list[Path] = []
    errors: list[tuple[Path, Exception]] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("Procesando imágenes...", total=len(sources))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_src = {
                executor.submit(process_one, src, dest_dir): src
                for src in sources
            }
            for future in as_completed(future_to_src):
                src = future_to_src[future]
                try:
                    dest = future.result()
                    results.append(dest)
                except Exception as e:
                    errors.append((src, e))
                    progress.console.print(f"[red]Error:[/] {src.name}: {e}")
                finally:
                    progress.advance(task)

    return results, errors
```

---

## 3. Manejar errores sin interrumpir el lote

Dos categorías de error en batch processing de imágenes:

```python
from PIL import UnidentifiedImageError

def process_one_safe(src: Path, dest_dir: Path) -> Path:
    from PIL import Image
    try:
        with Image.open(src) as img:
            img.verify()  # verifica cabecera sin cargar píxeles
    except (UnidentifiedImageError, OSError) as e:
        raise ValueError(f"No es una imagen válida: {src.name}") from e

    with Image.open(src) as img:
        img.thumbnail((800, 600), Image.LANCZOS)
        dest = dest_dir / src.with_suffix(".webp").name
        img.convert("RGB").save(dest, "WEBP", quality=85)
    return dest
```

Patrón: usar `img.verify()` en un bloque `with` separado — tras `verify()`, la imagen queda en estado inutilizable y hay que reabrirla.

---

## 4. Comparar velocidades: secuencial vs paralelo

```python
import time
from pathlib import Path

def benchmark(sources: list[Path], dest_dir: Path) -> None:
    # Secuencial
    t0 = time.perf_counter()
    for src in sources:
        process_one(src, dest_dir / "seq")
    seq_time = time.perf_counter() - t0

    # Paralelo (4 workers)
    t0 = time.perf_counter()
    batch_with_progress(sources, dest_dir / "par", max_workers=4)
    par_time = time.perf_counter() - t0

    print(f"Secuencial: {seq_time:.1f}s — Paralelo: {par_time:.1f}s — Speedup: {seq_time/par_time:.1f}x")
```

---

## 5. Optimización de memoria para imágenes grandes

Pillow carga la imagen completa en RAM. Para lotes de imágenes de alta resolución:

```python
import gc
from PIL import Image

def process_large_batch(sources: list[Path], dest_dir: Path) -> None:
    for src in sources:
        with Image.open(src) as img:
            # El context manager cierra y libera el archivo
            img.thumbnail((1200, 800), Image.LANCZOS)
            result = img.convert("RGB")
            dest = dest_dir / src.with_suffix(".webp").name
            result.save(dest, "WEBP", quality=85)
        # result fuera del with — se libera al siguiente ciclo de GC
        del result
        gc.collect()  # forzar liberación en lotes muy grandes
```

---

## ✅ Resumen

| Técnica | Uso |
|---------|-----|
| `ThreadPoolExecutor` | Paralelismo I/O + CPU Pillow |
| `as_completed()` | Actualizar progreso a medida que terminan |
| `Rich Progress` | Barra de progreso con tiempo y contador |
| `img.verify()` | Detectar imágenes corruptas antes de procesar |
| `with Image.open()` | Liberar archivos automáticamente |
| `gc.collect()` | Forzar liberación de RAM en lotes grandes |
