"""
Ejercicio 04: Sincronización Incremental con Checksums — SOLUCIÓN
=================================================================
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import boto3


BUCKET = "studio-bc-dev-sandbox"
STATE_FILE = Path(".sync_state.json")

SyncState = dict[str, dict[str, str]]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_state(state_path: Path = STATE_FILE) -> SyncState:
    if state_path.exists():
        return json.loads(state_path.read_text())  # type: ignore[no-any-return]
    return {}


def save_state(state: SyncState, state_path: Path = STATE_FILE) -> None:
    tmp = state_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    tmp.replace(state_path)


def needs_upload(path: Path, state: SyncState) -> bool:
    key = str(path)
    if key not in state:
        return True
    return sha256_file(path) != state[key].get("sha256", "")


def sync_to_s3(
    local_dir: Path,
    bucket: str,
    prefix: str,
    extensions: set[str] | None = None,
) -> dict[str, int]:
    s3 = boto3.client("s3")
    state = load_state()
    stats: dict[str, int] = {"uploaded": 0, "skipped": 0, "errors": 0}

    for path in local_dir.rglob("*"):
        if not path.is_file():
            continue
        if extensions and path.suffix.lower() not in extensions:
            continue

        if not needs_upload(path, state):
            stats["skipped"] += 1
            continue

        relative = path.relative_to(local_dir)
        key = f"{prefix}/{relative}".replace("\\", "/")

        try:
            s3.upload_file(str(path), bucket, key)
            state[str(path)] = {
                "sha256": sha256_file(path),
                "s3_key": key,
                "synced_at": datetime.now(timezone.utc).isoformat(),
            }
            stats["uploaded"] += 1
        except Exception as e:
            print(f"Error subiendo {path}: {e}")
            stats["errors"] += 1

    save_state(state)
    return stats


# ── Ejercicio ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    output_dir = Path("output_test")
    (output_dir / "renders").mkdir(parents=True, exist_ok=True)
    (output_dir / "exports").mkdir(parents=True, exist_ok=True)

    (output_dir / "renders" / "spot_v1.mp4").write_bytes(b"fake video v1")
    (output_dir / "renders" / "spot_v2.mp4").write_bytes(b"fake video v2")
    (output_dir / "exports" / "web_720p.mp4").write_bytes(b"fake web export")

    print("=== Primera ejecución (todo es nuevo) ===")
    stats = sync_to_s3(output_dir, BUCKET, "sync-test", extensions={".mp4", ".mov"})
    print(f"Subidos: {stats['uploaded']} | Saltados: {stats['skipped']} | Errores: {stats['errors']}")

    print("\n=== Segunda ejecución (sin cambios) ===")
    stats2 = sync_to_s3(output_dir, BUCKET, "sync-test", extensions={".mp4", ".mov"})
    print(f"Subidos: {stats2['uploaded']} | Saltados: {stats2['skipped']} | Errores: {stats2['errors']}")
    assert stats2["uploaded"] == 0, "No debería subir nada si no cambió nada"
    assert stats2["skipped"] == 3

    print("\n=== Modificar un archivo y re-sincronizar ===")
    (output_dir / "renders" / "spot_v1.mp4").write_bytes(b"fake video v1 UPDATED")
    stats3 = sync_to_s3(output_dir, BUCKET, "sync-test", extensions={".mp4", ".mov"})
    print(f"Subidos: {stats3['uploaded']} | Saltados: {stats3['skipped']} | Errores: {stats3['errors']}")
    assert stats3["uploaded"] == 1
    assert stats3["skipped"] == 2

    import shutil
    shutil.rmtree(output_dir, ignore_errors=True)
    STATE_FILE.unlink(missing_ok=True)
    print("\nOK — Ejercicio 04 completado")
