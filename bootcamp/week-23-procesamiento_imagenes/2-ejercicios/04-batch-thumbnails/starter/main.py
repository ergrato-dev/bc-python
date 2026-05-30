"""
Ejercicio 04 — Batch Processing con Progress Bar

Contexto: El estudio recibe 20+ imágenes y necesita generar thumbnails
web (1200×800) y social (1080×1080) para todas en paralelo.

Instrucciones:
1. Completá `generate_thumb()` — genera un thumbnail según el perfil dado
2. Completá `process_batch()` — usa ThreadPoolExecutor + Rich progress bar
3. El procesamiento NO debe interrumpirse si una imagen falla
4. Al final, imprimir resumen: N procesadas, N errores

Instalar: pip install Pillow rich
"""

from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps

from rich.progress import Progress, BarColumn, MofNCompleteColumn, TimeElapsedColumn, TextColumn


@dataclass(frozen=True)
class ThumbProfile:
    name: str
    width: int
    height: int
    fit: bool = False
    quality: int = 85


PROFILES = [
    ThumbProfile("web",    1200, 800,  fit=False, quality=85),
    ThumbProfile("social", 1080, 1080, fit=True,  quality=85),
    ThumbProfile("thumb",  300,  300,  fit=True,  quality=80),
]


def generate_thumb(src: Path, dest_dir: Path, profile: ThumbProfile) -> Path:
    """
    Genera un thumbnail de src según profile.
    Guarda en dest_dir/{profile.name}/{src.stem}.webp
    Retorna el path de destino.
    """
    # TODO:
    # 1. out_dir = dest_dir / profile.name; out_dir.mkdir(parents=True, exist_ok=True)
    # 2. dest = out_dir / src.with_suffix(".webp").name
    # 3. Abrir imagen, corregir orientación con ImageOps.exif_transpose()
    # 4. Si profile.fit: ImageOps.fit(img, (profile.width, profile.height), Image.LANCZOS)
    #    Si no: img.thumbnail((profile.width, profile.height), Image.LANCZOS)
    # 5. img.convert("RGB").save(dest, "WEBP", quality=profile.quality)
    # 6. retornar dest
    raise NotImplementedError


def process_batch(
    sources: list[Path],
    dest_dir: Path,
    profiles: list[ThumbProfile] | None = None,
    max_workers: int = 4,
) -> tuple[int, int]:
    """
    Procesa todas las imágenes en paralelo generando todos los perfiles.
    Retorna (n_processed, n_errors).
    """
    if profiles is None:
        profiles = PROFILES

    # Crear lista de tareas (src, perfil)
    tasks = [(src, profile) for src in sources for profile in profiles]

    processed = 0
    errors = 0

    # TODO:
    # with Progress(...) as progress:
    #   task = progress.add_task("Generando thumbnails...", total=len(tasks))
    #   with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     futures = {executor.submit(generate_thumb, src, dest_dir, p): (src, p) for src, p in tasks}
    #     for future in as_completed(futures):
    #       try: future.result(); processed += 1
    #       except Exception as e: errors += 1; progress.console.print(...)
    #       finally: progress.advance(task)
    raise NotImplementedError


# ── Muestra ───────────────────────────────────────────────────────────────────
def create_test_images(folder: Path, count: int = 20) -> list[Path]:
    folder.mkdir(exist_ok=True)
    paths = []
    for i in range(count):
        img = Image.new("RGB", (2000, 1500), color=(i * 12 % 255, i * 7 % 255, 180))
        p = folder / f"foto_{i:03d}.jpg"
        img.save(p, quality=90)
        paths.append(p)
    return paths


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        sources = create_test_images(tmp_path / "input", count=20)

        print(f"Procesando {len(sources)} imágenes × {len(PROFILES)} perfiles = {len(sources)*len(PROFILES)} thumbnails")
        n_ok, n_err = process_batch(sources, tmp_path / "output")
        print(f"\nResultado: {n_ok} OK · {n_err} errores")
