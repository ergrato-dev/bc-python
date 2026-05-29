# Idempotencia y Checksums

## Objetivos

- Entender por qué la idempotencia es crítica en pipelines de archivos
- Calcular checksums SHA-256 con hashlib
- Persistir un registro de archivos procesados en JSON
- Implementar lock files para evitar ejecuciones concurrentes

---

## 1. El problema del reprocesamiento

Un daemon que arranca después de un crash puede volver a procesar archivos ya organizados.
Sin un registro de procesados:
- Archivos duplicados en destino
- Operaciones innecesarias (cómputo, red)
- Datos corruptos si el proceso es destructivo

La solución: calcular un **checksum único** por archivo y guardarlo en un registro. Antes de procesar, verificar si el checksum ya está registrado.

---

## 2. Checksum SHA-256 con hashlib

```python
import hashlib
from pathlib import Path

def sha256(path: Path, chunk_size: int = 65536) -> str:
    # Calcula SHA-256 de un archivo en chunks (soporta archivos grandes)
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

# Uso
digest = sha256(Path("canal9_spot-verano_raw_20240315_v001.mp4"))
print(digest)  # "a3f4b2c1d0e9..."
```

Usar chunks evita cargar el archivo completo en RAM. `chunk_size=65536` (64 KB) es un buen balance velocidad/memoria.

---

## 3. Registro de procesados

```python
import json
from pathlib import Path

REGISTRY_FILE = Path(".processed.json")

def load_registry() -> dict[str, str]:
    # Lee {checksum: dest_path} desde disco
    if REGISTRY_FILE.exists():
        return json.loads(REGISTRY_FILE.read_text())
    return {}

def save_registry(registry: dict[str, str]) -> None:
    # Escribe el registro de forma atómica
    tmp = REGISTRY_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(registry, indent=2))
    tmp.rename(REGISTRY_FILE)

def is_processed(checksum: str, registry: dict[str, str]) -> bool:
    return checksum in registry

def mark_processed(checksum: str, dest: Path, registry: dict[str, str]) -> None:
    registry[checksum] = str(dest)
    save_registry(registry)
```

---

## 4. Pipeline idempotente completo

```python
from pathlib import Path

def process_file(src: Path, organizer: "FileOrganizer") -> None:
    registry = load_registry()
    digest = sha256(src)

    if is_processed(digest, registry):
        print(f"Ya procesado (skipping): {src.name}")
        return

    dest = organizer.organize(src)
    if dest:
        mark_processed(digest, dest, registry)
        print(f"Procesado: {src.name} → {dest}")
```

---

## 5. Lock file para ejecución única

Evita que dos instancias del daemon corran en paralelo y procesen los mismos archivos:

```python
import os
import sys
from pathlib import Path

LOCK_FILE = Path(".daemon.lock")

def acquire_lock() -> None:
    if LOCK_FILE.exists():
        pid = int(LOCK_FILE.read_text().strip())
        try:
            os.kill(pid, 0)   # señal 0: solo verifica si el proceso existe
            print(f"El daemon ya está corriendo (PID {pid}). Saliendo.")
            sys.exit(1)
        except ProcessLookupError:
            pass  # proceso muerto — borrar lock
    LOCK_FILE.write_text(str(os.getpid()))

def release_lock() -> None:
    LOCK_FILE.unlink(missing_ok=True)

# Uso
acquire_lock()
try:
    run_daemon()
finally:
    release_lock()
```

---

## 6. MD5 vs SHA-256

| Hash | Velocidad | Seguridad | Uso recomendado |
|------|-----------|-----------|-----------------|
| MD5 | Muy rápido | Vulnerable a colisiones | Checksums de integridad rápidos (non-security) |
| SHA-256 | Rápido | Sin colisiones conocidas | Deduplicación, firmas, almacenamiento |

Para detección de duplicados en producción audiovisual, **SHA-256** es la elección estándar.

---

## ✅ Resumen

| Problema | Solución |
|----------|----------|
| Reprocesamiento tras crash | Registro checksum en `.processed.json` |
| Archivo grande en RAM | `hashlib` con chunks de 64 KB |
| Escritura segura del registro | Escribe a `.tmp`, luego `rename()` |
| Dos daemons en paralelo | Lock file con PID |
