# Sincronización y Checksums

## 1. El Problema del Sync

Sincronizar una carpeta local con S3 implica determinar qué archivos:
- Son **nuevos** localmente → upload
- Fueron **modificados** localmente → re-upload
- Fueron **eliminados** localmente → delete en S3 (opcional)
- Existen **solo en S3** → download (sync bidireccional)

La estrategia ingenua (comparar por nombre) no detecta modificaciones. La estrategia correcta usa **checksums**.

---

## 2. SHA-256 Local vs ETag S3

```python
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()
```

**ETag de S3** para single-part upload = MD5 del archivo. Para comparar con SHA-256, necesitas mantener un registro propio.

```python
import boto3


def get_s3_etag(bucket: str, key: str) -> str | None:
    try:
        resp = boto3.client("s3").head_object(Bucket=bucket, Key=key)
        return resp["ETag"].strip('"')
    except boto3.client("s3").exceptions.ClientError:
        return None
```

---

## 3. Registro de Estado `.sync_state.json`

Para sync incremental eficiente, mantenemos un registro local que mapea cada archivo a su checksum y timestamp de última sincronización.

```python
import json
from pathlib import Path
from datetime import datetime


SyncState = dict[str, dict[str, str]]  # {local_path: {sha256, s3_key, synced_at}}


def load_state(state_path: Path) -> SyncState:
    if state_path.exists():
        return json.loads(state_path.read_text())
    return {}


def save_state(state: SyncState, state_path: Path) -> None:
    tmp = state_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(state_path)  # operación atómica


def needs_upload(path: Path, state: SyncState) -> bool:
    key = str(path)
    if key not in state:
        return True
    return sha256_file(path) != state[key]["sha256"]


def mark_synced(path: Path, s3_key: str, state: SyncState) -> None:
    state[str(path)] = {
        "sha256": sha256_file(path),
        "s3_key": s3_key,
        "synced_at": datetime.utcnow().isoformat(),
    }
```

---

## 4. Motor de Sincronización

```python
import boto3
from pathlib import Path


def sync_directory(
    local_dir: Path,
    bucket: str,
    s3_prefix: str,
    state_path: Path,
    extensions: set[str] | None = None,
) -> dict[str, int]:
    s3 = boto3.client("s3")
    state = load_state(state_path)
    stats = {"uploaded": 0, "skipped": 0, "errors": 0}

    for path in local_dir.rglob("*"):
        if not path.is_file():
            continue
        if extensions and path.suffix.lower() not in extensions:
            continue

        if not needs_upload(path, state):
            stats["skipped"] += 1
            continue

        relative = path.relative_to(local_dir)
        key = f"{s3_prefix}/{relative}".replace("\\", "/")

        try:
            s3.upload_file(str(path), bucket, key)
            mark_synced(path, key, state)
            stats["uploaded"] += 1
        except Exception as e:
            print(f"Error subiendo {path}: {e}")
            stats["errors"] += 1

    save_state(state, state_path)
    return stats
```

---

## 5. Sync Bidireccional

```python
def sync_bidirectional(
    local_dir: Path,
    bucket: str,
    prefix: str,
    state_path: Path,
) -> None:
    s3 = boto3.client("s3")
    state = load_state(state_path)

    # 1. Upload: local → S3
    for path in local_dir.rglob("*"):
        if path.is_file() and needs_upload(path, state):
            key = f"{prefix}/{path.relative_to(local_dir)}".replace("\\", "/")
            s3.upload_file(str(path), bucket, key)
            mark_synced(path, key, state)

    # 2. Download: S3 → local (archivos que no existen localmente)
    paginator = s3.get_paginator("list_objects_v2")
    remote_keys = set()
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            remote_keys.add(key)
            relative = key.removeprefix(f"{prefix}/")
            local_path = local_dir / relative
            if not local_path.exists():
                local_path.parent.mkdir(parents=True, exist_ok=True)
                s3.download_file(bucket, key, str(local_path))

    save_state(state, state_path)
```

---

## 6. Lock File para Evitar Ejecuciones Concurrentes

```python
import os


def acquire_lock(lock_path: Path) -> bool:
    if lock_path.exists():
        pid = int(lock_path.read_text().strip())
        try:
            os.kill(pid, 0)  # señal 0: solo verifica si el proceso existe
            return False  # proceso activo, no adquirir lock
        except ProcessLookupError:
            pass  # proceso muerto, limpiar lock
    lock_path.write_text(str(os.getpid()))
    return True


def release_lock(lock_path: Path) -> None:
    lock_path.unlink(missing_ok=True)
```

---

## Resumen

| Técnica | Por qué |
|---------|---------|
| SHA-256 local | Detecta modificaciones reales, no solo cambios de timestamp |
| ETag de S3 | Válido para comparar solo si el upload fue single-part |
| `.sync_state.json` | Evita recalcular checksums en cada ejecución |
| `tmp.replace(state)` | Escritura atómica del registro — no corrompe si hay crash |
| Lock file con PID | Previene dos instancias del sync corriendo en paralelo |
