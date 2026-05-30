"""
Ejercicio 01 — Resize y Crop

Contexto: El estudio necesita preparar fotos de clientes en tres tamaños:
banner web (1200×400), cuadrado para redes (800×800) y thumbnail (200×200).

Instrucciones:
1. Completá `resize_exact()` — redimensiona a tamaño exacto (puede distorsionar)
2. Completá `resize_fit()` — redimensiona preservando proporciones (bounding box)
3. Completá `crop_center()` — recorta al centro con las dimensiones dadas
4. Completá `make_banner()` — combina fit + crop para lograr 1200×400

Todas las funciones deben retornar un nuevo Image sin modificar el original.
"""

from pathlib import Path
from PIL import Image


def resize_exact(img: Image.Image, width: int, height: int) -> Image.Image:
    """Redimensiona a width×height exacto con LANCZOS."""
    # TODO: img.resize((width, height), Image.LANCZOS)
    raise NotImplementedError


def resize_fit(img: Image.Image, max_width: int, max_height: int) -> Image.Image:
    """Redimensiona preservando proporciones. Copia del original."""
    # TODO: img.copy(), luego thumbnail()
    raise NotImplementedError


def crop_center(img: Image.Image, width: int, height: int) -> Image.Image:
    """Recorta la imagen al centro con las dimensiones indicadas."""
    # TODO: calcular (left, upper, right, lower) desde el centro
    # left = (img.width - width) // 2, etc.
    raise NotImplementedError


def make_banner(img: Image.Image, width: int = 1200, height: int = 400) -> Image.Image:
    """
    Genera un banner 1200×400:
    1. Redimensionar para que el alto sea al menos `height` (preservar ratio)
    2. Crop al centro para obtener exactamente width×height
    """
    # TODO: calcular el ancho escalado que preserve ratio para alto=height
    # Luego llamar resize_exact y crop_center
    raise NotImplementedError


# ── Helpers de muestra ────────────────────────────────────────────────────────
def create_sample_image(width: int = 2400, height: int = 1600) -> Image.Image:
    """Crea una imagen de muestra con gradiente de colores."""
    import random
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    assert pixels is not None
    for x in range(width):
        for y in range(height):
            r = int(x / width * 255)
            g = int(y / height * 255)
            b = 128
            pixels[x, y] = (r, g, b)
    return img


if __name__ == "__main__":
    import tempfile
    from PIL import ImageDraw

    src = create_sample_image()
    print(f"Original: {src.size}")

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)

        exact = resize_exact(src, 800, 600)
        print(f"resize_exact(800,600): {exact.size}")
        exact.save(out / "exact.jpg")

        fit = resize_fit(src, 800, 600)
        print(f"resize_fit(800,600): {fit.size}")
        fit.save(out / "fit.jpg")

        cropped = crop_center(src, 800, 800)
        print(f"crop_center(800,800): {cropped.size}")
        cropped.save(out / "cropped.jpg")

        banner = make_banner(src)
        print(f"make_banner(1200,400): {banner.size}")
        banner.save(out / "banner.jpg")

        print("✓ Todas las imágenes guardadas correctamente")
