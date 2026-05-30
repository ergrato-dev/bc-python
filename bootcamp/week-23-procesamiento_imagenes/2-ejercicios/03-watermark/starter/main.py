"""
Ejercicio 03 — Watermark con Alpha Compositing

Contexto: Studio BC quiere proteger sus imágenes con un logo en la
esquina inferior derecha y un texto de copyright centrado semitransparente.

Instrucciones:
1. Completá `apply_logo_watermark()` — logo PNG sobre imagen base
2. Completá `apply_text_watermark()` — texto centrado con opacidad
3. Completá `apply_both()` — logo + texto combinados
4. El logo NO debe distorsionar si es más grande que el 15% del base

Nota: las imágenes de muestra se generan sintéticamente (no necesitan archivos reales).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def apply_logo_watermark(
    base: Image.Image,
    logo: Image.Image,
    corner: str = "bottom-right",
    margin: int = 20,
    max_ratio: float = 0.15,
) -> Image.Image:
    """
    Aplica logo en la esquina indicada.
    corner: "top-left" | "top-right" | "bottom-left" | "bottom-right"
    max_ratio: tamaño máximo del logo como fracción del ancho base
    """
    # TODO:
    # 1. Redimensionar logo si es > max_ratio * base.width
    # 2. Calcular posición según corner y margin
    # 3. result = base.copy().convert("RGBA")
    # 4. logo_rgba = logo.convert("RGBA")
    # 5. result.paste(logo_rgba, pos, mask=logo_rgba)
    # 6. return result.convert("RGB")
    raise NotImplementedError


def apply_text_watermark(
    base: Image.Image,
    text: str = "© Studio BC",
    opacity: int = 80,
    font_size: int = 32,
) -> Image.Image:
    """Agrega texto centrado con opacidad sobre la imagen."""
    # TODO:
    # 1. result = base.convert("RGBA")
    # 2. overlay = Image.new("RGBA", result.size, (0,0,0,0))
    # 3. draw = ImageDraw.Draw(overlay)
    # 4. calcular posición centrada con draw.textbbox()
    # 5. draw.text(pos, text, font=font, fill=(255,255,255,opacity))
    # 6. result = Image.alpha_composite(result, overlay)
    # 7. return result.convert("RGB")
    raise NotImplementedError


def apply_both(
    base: Image.Image,
    logo: Image.Image,
    copyright_text: str = "© Studio BC",
) -> Image.Image:
    """Aplica logo en esquina inferior derecha y texto en parte inferior."""
    # TODO: llamar apply_logo_watermark, luego apply_text_watermark sobre el resultado
    raise NotImplementedError


# ── Imágenes de muestra ──────────────────────────────────────────────────────
def make_photo(w: int = 1200, h: int = 800) -> Image.Image:
    img = Image.new("RGB", (w, h))
    pixels = img.load()
    assert pixels is not None
    for x in range(w):
        for y in range(h):
            pixels[x, y] = (int(x / w * 200), int(y / h * 200), 120)
    return img


def make_logo(size: int = 200) -> Image.Image:
    logo = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    draw.ellipse([(20, 20), (size - 20, size - 20)], fill=(255, 255, 255, 200))
    draw.text((size // 2, size // 2), "BC", fill=(0, 0, 0, 255), anchor="mm")
    return logo


if __name__ == "__main__":
    import tempfile

    photo = make_photo()
    logo = make_logo()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)

        result_logo = apply_logo_watermark(photo, logo)
        result_logo.save(out / "with_logo.jpg", quality=90)
        print(f"Logo watermark: {(out / 'with_logo.jpg').stat().st_size} bytes")

        result_text = apply_text_watermark(photo)
        result_text.save(out / "with_text.jpg", quality=90)
        print(f"Text watermark: {(out / 'with_text.jpg').stat().st_size} bytes")

        result_both = apply_both(photo, logo)
        result_both.save(out / "with_both.jpg", quality=90)
        print(f"Both watermarks: {(out / 'with_both.jpg').stat().st_size} bytes")

        print("✓ Watermarks aplicados correctamente")
