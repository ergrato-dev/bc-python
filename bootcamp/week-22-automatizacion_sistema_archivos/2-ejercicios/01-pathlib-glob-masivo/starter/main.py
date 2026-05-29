"""
Ejercicio 01 — pathlib: Glob y Operaciones Masivas

Contexto: Studio BC recibió un lote de entregables en `sample_files/`.
Los archivos tienen extensiones mezcladas (.JPEG, .MP4, .MOV) y
algunas carpetas ocultas. Necesitamos auditarlos y normalizar extensiones.

Instrucciones:
1. Completá `count_by_extension()` — cuenta archivos por extensión (rglob)
2. Completá `normalize_jpeg()` — renombra todos los .JPEG → .jpg
3. Completá `find_large_files()` — lista archivos mayores a `min_bytes`
4. Completá `build_tree_report()` — retorna un str multi-línea con la estructura
"""

from pathlib import Path
from collections import defaultdict


def count_by_extension(folder: Path) -> dict[str, int]:
    """Retorna {'.ext': cantidad} para todos los archivos en folder (recursivo)."""
    # TODO: usar rglob("*"), filtrar is_file(), agrupar por suffix.lower()
    raise NotImplementedError


def normalize_jpeg(folder: Path) -> list[Path]:
    """Renombra todos los archivos .JPEG a .jpg. Retorna la lista de nuevos paths."""
    # TODO: glob o rglob para .JPEG, usar Path.rename() con .with_suffix(".jpg")
    raise NotImplementedError


def find_large_files(folder: Path, min_bytes: int) -> list[Path]:
    """Retorna archivos cuyo tamaño supera min_bytes."""
    # TODO: rglob("*"), filtrar is_file() y stat().st_size > min_bytes
    raise NotImplementedError


def build_tree_report(folder: Path, indent: int = 0) -> str:
    """Retorna un string con la estructura de árbol del folder."""
    # TODO: iterar folder.iterdir(), recursión para subdirectorios
    raise NotImplementedError


# ── Setup de muestra ──────────────────────────────────────────────────────────
def create_sample_files(root: Path) -> None:
    """Crea archivos de muestra para probar las funciones."""
    files = [
        "canal9/spot_verano.MP4",
        "canal9/logo.JPEG",
        "trademax/demo.mov",
        "trademax/brief.pdf",
        "bcstudio/reel.mp4",
        "bcstudio/photos/frame01.JPEG",
        "bcstudio/photos/frame02.jpg",
    ]
    for rel in files:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"\x00" * (1024 * (len(rel) % 10 + 1)))


if __name__ == "__main__":
    import tempfile, json

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        create_sample_files(root)

        print("=== count_by_extension ===")
        counts = count_by_extension(root)
        for ext, n in sorted(counts.items()):
            print(f"  {ext:10} {n}")

        print("\n=== normalize_jpeg ===")
        renamed = normalize_jpeg(root)
        for p in renamed:
            print(f"  → {p.name}")

        print("\n=== find_large_files (> 5 KB) ===")
        large = find_large_files(root, min_bytes=5 * 1024)
        for p in large:
            print(f"  {p.name} ({p.stat().st_size} bytes)")

        print("\n=== build_tree_report ===")
        print(build_tree_report(root))
