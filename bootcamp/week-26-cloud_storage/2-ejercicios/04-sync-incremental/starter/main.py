"""
Ejercicio 04: Sincronización Incremental con Checksums
=======================================================
Implementa un sync incremental local → S3 usando SHA-256 para detectar cambios.
Solo sube archivos nuevos o modificados; registra el estado en .sync_state.json.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

import boto3


BUCKET = "studio-bc-dev-sandbox"
STATE_FILE = Path(".sync_state.json")

SyncState = dict[str, dict[str, str]]


def sha256_file(path: Path) -> str:
    """Calcula el SHA-256 del archivo en chunks de 64 KB."""
    # TODO: hashlib.sha256() + loop f.read(65536)
    raise NotImplementedError


def load_state(state_path: Path = STATE_FILE) -> SyncState:
    """Carga el estado desde el JSON. Devuelve {} si no existe."""
    # TODO: state_path.read_text() y json.loads
    raise NotImplementedError


def save_state(state: SyncState, state_path: Path = STATE_FILE) -> None:
    """Guarda el estado de forma atómica (escribe en .tmp y hace replace)."""
    # TODO: tmp = state_path.with_suffix(".tmp") → write_text → replace
    raise NotImplementedError


def needs_upload(path: Path, state: SyncState) -> bool:
    """True si el archivo es nuevo o su SHA-256 cambió respecto al estado guardado."""
    # TODO: comparar sha256_file(path) con state.get(str(path), {}).get("sha256")
    raise NotImplementedError


def sync_to_s3(
    local_dir: Path,
    bucket: str,
    prefix: str,
    extensions: set[str] | None = None,
) -> dict[str, int]:
    """
    Sincroniza local_dir → S3/prefix.
    Devuelve {"uploaded": n, "skipped": n, "errors": n}.
    """
    # TODO: iterar local_dir.rglob("*"), filtrar por extensiones
    # TODO: si needs_upload → s3.upload_file → mark_synced en state
    # TODO: salvar state al final
    raise NotImplementedError


# ── Ejercicio ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Crear árbol local de prueba
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

    # Limpieza
    import shutil
    shutil.rmtree(output_dir, ignore_errors=True)
    STATE_FILE.unlink(missing_ok=True)
    print("\nOK — Ejercicio 04 completado")
