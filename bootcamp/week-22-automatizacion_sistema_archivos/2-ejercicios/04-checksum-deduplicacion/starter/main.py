"""
Ejercicio 04 — Checksums y Deduplicación

Contexto: El estudio recibe los mismos archivos por múltiples canales
(email, USB, FTP). Hay que detectar duplicados y mantener un registro
de archivos ya procesados para evitar reprocesamiento.

Instrucciones:
1. Completá `sha256()` — calcula hash en chunks (no cargar todo en RAM)
2. Completá `find_duplicates()` — agrupa paths con el mismo checksum
3. Completá `load_registry()` / `save_registry()` — lee/escribe JSON atómico
4. Completá `process_new_files()` — salta procesados, marca los nuevos
"""

import hashlib
import json
from pathlib import Path


def sha256(path: Path, chunk_size: int = 65536) -> str:
    """Calcula SHA-256 de un archivo leyendo en chunks."""
    # TODO: hashlib.sha256(), abrir en modo "rb", leer chunks con walrus :=
    raise NotImplementedError


def find_duplicates(folder: Path) -> dict[str, list[Path]]:
    """
    Retorna {checksum: [path1, path2, ...]} solo para checksums con > 1 archivo.
    """
    # TODO: calcular sha256 para cada archivo, agrupar, filtrar len > 1
    raise NotImplementedError


REGISTRY_FILE = Path(".processed.json")


def load_registry() -> dict[str, str]:
    """Lee {checksum: dest_path} desde REGISTRY_FILE. Retorna {} si no existe."""
    # TODO: si REGISTRY_FILE.exists(): json.loads(REGISTRY_FILE.read_text())
    raise NotImplementedError


def save_registry(registry: dict[str, str]) -> None:
    """Escribe el registro de forma atómica (escribe a .tmp, luego rename)."""
    # TODO: tmp = REGISTRY_FILE.with_suffix(".tmp")
    # tmp.write_text(json.dumps(registry, indent=2))
    # tmp.rename(REGISTRY_FILE)
    raise NotImplementedError


def process_new_files(files: list[Path]) -> tuple[list[Path], list[Path]]:
    """
    Para cada archivo:
    - Si su checksum ya está en el registro: agregar a `skipped`
    - Si es nuevo: "procesarlo" (imprimir), registrarlo, agregar a `processed`

    Retorna (processed, skipped).
    """
    # TODO: load_registry(), iterar files, sha256(), is_processed check
    raise NotImplementedError


# ── Muestra ───────────────────────────────────────────────────────────────────
def create_sample(folder: Path) -> None:
    folder.mkdir(exist_ok=True)
    content_a = b"contenido del video A" * 100
    content_b = b"contenido del audio B" * 80

    (folder / "video_original.mp4").write_bytes(content_a)
    (folder / "video_copia.mp4").write_bytes(content_a)    # duplicado
    (folder / "audio_original.wav").write_bytes(content_b)
    (folder / "audio_backup.wav").write_bytes(content_b)   # duplicado
    (folder / "brief.pdf").write_bytes(b"brief unico")


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory(dir=".") as tmp:
        folder = Path(tmp) / "entregables"
        create_sample(folder)

        print("=== Duplicados ===")
        dups = find_duplicates(folder)
        for digest, paths in dups.items():
            print(f"  {digest[:12]}... → {[p.name for p in paths]}")

        print("\n=== Procesamiento (1ra vez) ===")
        files = list(folder.glob("*"))
        proc, skip = process_new_files(files)
        print(f"  Procesados: {len(proc)}, Saltados: {len(skip)}")

        print("\n=== Procesamiento (2da vez — idempotente) ===")
        proc2, skip2 = process_new_files(files)
        print(f"  Procesados: {len(proc2)}, Saltados: {len(skip2)}")

    REGISTRY_FILE.unlink(missing_ok=True)
