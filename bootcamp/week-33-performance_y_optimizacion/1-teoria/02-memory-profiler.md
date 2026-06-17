# Memory Profiler y Streaming

## 1. El Problema: Archivos Grandes en Memoria

```python
# PROBLEMA: carga todo en memoria — falla con archivos >4K/8K
def process_manifest(path: Path) -> list[dict[str, object]]:
    data = path.read_text()        # 4 GB de JSON → 4 GB en RAM
    records = json.loads(data)     # + 4 GB para parsear → 8 GB total
    return [process(r) for r in records]
```

```python
# SOLUCIÓN: generador — solo una línea en memoria a la vez
def stream_manifest(path: Path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)
```

---

## 2. tracemalloc — Medir Memoria (stdlib)

```python
import tracemalloc
from pathlib import Path


def measure_memory(fn, *args):
    tracemalloc.start()
    result = fn(*args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Actual: {current / 1024:.1f} KB — Pico: {peak / 1024:.1f} KB")
    return result


# Comparar
measure_memory(load_full, Path("manifest.jsonl"))    # Pico: 4 096 000 KB
measure_memory(stream_count, Path("manifest.jsonl")) # Pico:        12 KB
```

### Snapshot detallado

```python
import tracemalloc

tracemalloc.start()
run_pipeline()
snapshot = tracemalloc.take_snapshot()

top = snapshot.statistics("lineno")[:10]
for stat in top:
    print(stat)

# salida:
# pipeline.py:45: size=1.2 GiB, count=8, average=153.6 MiB
```

---

## 3. memory_profiler — Line-by-Line

```bash
pip install memory-profiler
```

```python
from memory_profiler import profile


@profile
def process_manifest(path: Path) -> list[dict[str, object]]:
    data = path.read_bytes()       # ← cuánta RAM aquí
    text = data.decode("utf-8")    # ← y aquí
    records = json.loads(text)     # ← y aquí
    return records
```

```bash
python -m memory_profiler mi_script.py
```

Salida:

```
Line #    Mem usage    Increment  Occurrences   Line Contents
==============================================================
    12   45.2 MiB     45.2 MiB           1   def process_manifest(path):
    13  4141.2 MiB  4096.0 MiB           1       data = path.read_bytes()
    14  8236.2 MiB  4095.0 MiB           1       text = data.decode("utf-8")
    15  8236.3 MiB     0.1 MiB           1       records = json.loads(text)
```

---

## 4. Streaming I/O con Generadores

### 4.1 Leer chunks binarios

```python
def iter_chunks(path: Path, chunk_size: int = 4 * 1024 * 1024) -> Iterator[bytes]:
    """Lee el archivo en chunks de chunk_size bytes."""
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk
```

### 4.2 Calcular SHA-256 en streaming

```python
import hashlib

def checksum_sha256(path: Path, chunk_size: int = 4 * 1024 * 1024) -> str:
    sha = hashlib.sha256()
    for chunk in iter_chunks(path, chunk_size):
        sha.update(chunk)
    return sha.hexdigest()
```

### 4.3 Procesar JSONL (JSON Lines) en streaming

```python
import json
from pathlib import Path
from typing import Iterator


def iter_jsonl(path: Path, encoding: str = "utf-8") -> Iterator[dict[str, object]]:
    with open(path, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


# Contar sin cargar en memoria:
total = sum(1 for _ in iter_jsonl(Path("assets.jsonl")))

# Filtrar por categoría:
docs = [r for r in iter_jsonl(Path("assets.jsonl")) if r["category"] == "documental"]
```

---

## 5. Comparación: Carga Completa vs Streaming

```python
import tracemalloc, time
from pathlib import Path

path = Path("assets.jsonl")  # 1 GB


def load_full() -> int:
    data = path.read_text()
    return sum(1 for _ in data.splitlines() if _.strip())


def stream_count() -> int:
    return sum(1 for _ in iter_jsonl(path))


for fn in (load_full, stream_count):
    tracemalloc.start()
    t0 = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{fn.__name__}: {result} records | {elapsed:.2f}s | peak {peak/1e6:.1f} MB")
```

Resultado típico con un archivo de 1 GB:

```
load_full:    100000 records | 4.23s | peak 1024.8 MB
stream_count: 100000 records | 2.87s | peak    0.3 MB
```

---

## 6. Archivos Binarios Grandes — Video 4K/8K

Para archivos de video de varios GB, nunca cargarlos completos:

```python
def process_large_video(path: Path) -> dict[str, object]:
    # 1. Calcular checksum en streaming
    sha = checksum_sha256(path)

    # 2. Extraer metadata con ffprobe (sin cargar el video)
    import subprocess, json
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(path)],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(probe.stdout).get("streams", [])

    # 3. Extraer frames selectivos con ffmpeg (seek directo)
    # ffmpeg -ss {timestamp} -i {path} -vframes 1 frame.jpg
    # No decodifica todo el video

    return {"sha256": sha, "streams": streams}
```

---

## Resumen

| Herramienta | Cuándo usar |
|-------------|-------------|
| `tracemalloc` | Medir peak de memoria en pruebas (stdlib) |
| `memory_profiler` | Análisis línea a línea de uso de RAM |
| Generadores + `yield` | Archivos grandes sin límite de RAM |
| Lectura en chunks | Archivos binarios (video, audio) |
| `ffprobe` | Metadata de video sin decodificar |
