# Watermarks y Overlays

## Objetivos

- Aplicar un logo PNG con transparencia sobre una imagen
- Agregar texto con posición, opacidad y fuente
- Entender alpha compositing con `Image.paste()`
- Crear watermarks resistentes a eliminación simple

---

## 1. Alpha compositing básico

`Image.paste(overlay, position, mask)` — el tercer argumento es la máscara:
- Si `mask` es una imagen en modo `L` o `RGBA`, controla la opacidad píxel a píxel.
- Para un PNG con transparencia, `mask=overlay` usa su canal alpha.

```python
from PIL import Image

def apply_logo(
    base: Image.Image,
    logo: Image.Image,
    position: tuple[int, int],
) -> Image.Image:
    result = base.copy()
    if base.mode != "RGBA":
        result = result.convert("RGBA")

    # El logo ya tiene canal alpha si es PNG con transparencia
    logo_rgba = logo.convert("RGBA")
    result.paste(logo_rgba, position, mask=logo_rgba)

    return result.convert("RGB")  # convertir de vuelta para guardar como JPG
```

---

## 2. Logo en esquina con margen

```python
from PIL import Image
from enum import Enum
from typing import Literal

Corner = Literal["top-left", "top-right", "bottom-left", "bottom-right"]

def place_logo(
    base: Image.Image,
    logo: Image.Image,
    corner: Corner = "bottom-right",
    margin: int = 20,
    max_logo_ratio: float = 0.15,  # máximo 15% del ancho base
) -> Image.Image:
    # Redimensionar logo si es muy grande
    max_w = int(base.width * max_logo_ratio)
    logo_resized = logo.copy()
    logo_resized.thumbnail((max_w, max_w), Image.LANCZOS)

    lw, lh = logo_resized.size
    bw, bh = base.size

    positions = {
        "top-left":     (margin, margin),
        "top-right":    (bw - lw - margin, margin),
        "bottom-left":  (margin, bh - lh - margin),
        "bottom-right": (bw - lw - margin, bh - lh - margin),
    }
    pos = positions[corner]
    return apply_logo(base, logo_resized, pos)
```

---

## 3. Watermark de texto

```python
from PIL import Image, ImageDraw, ImageFont

def text_watermark(
    base: Image.Image,
    text: str,
    opacity: int = 80,   # 0-255
    font_size: int = 36,
) -> Image.Image:
    result = base.convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    # Calcular posición centrada
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (result.width - text_w) // 2
    y = (result.height - text_h) // 2

    draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))

    result = Image.alpha_composite(result, overlay)
    return result.convert("RGB")
```

---

## 4. Watermark diagonal (más resistente)

```python
from PIL import Image, ImageDraw, ImageFont
import math

def diagonal_watermark(
    base: Image.Image,
    text: str,
    opacity: int = 60,
    font_size: int = 48,
    step: int = 300,  # repetición en px
) -> Image.Image:
    result = base.convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    # Tile de texto en diagonal
    for y in range(-result.height, result.height * 2, step):
        for x in range(-result.width, result.width * 2, step):
            draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))

    # Rotar el overlay 45°
    rotated = overlay.rotate(-30, expand=False)
    result = Image.alpha_composite(result, rotated)
    return result.convert("RGB")
```

---

## 5. Pipeline completo: thumbnail + watermark

```python
from pathlib import Path
from PIL import Image, ImageOps

def process_with_watermark(
    src: Path,
    logo_path: Path,
    dest_dir: Path,
) -> Path:
    with Image.open(src) as img:
        # Corregir orientación EXIF
        img = ImageOps.exif_transpose(img)

        # Generar thumbnail web
        img.thumbnail((1200, 800), Image.LANCZOS)

        # Aplicar watermark de logo
        with Image.open(logo_path) as logo:
            result = place_logo(img, logo, corner="bottom-right")

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.with_suffix(".webp").name
    result.save(dest, "WEBP", quality=85)
    return dest
```

---

## ✅ Resumen

| Técnica | Método | Cuándo |
|---------|--------|--------|
| Logo PNG con alpha | `paste(logo, pos, mask=logo)` | Branding sobre fotos |
| Texto con opacidad | `alpha_composite()` + RGBA overlay | Copyright, créditos |
| Watermark diagonal | Tile rotado con `rotate(-30)` | Protección de imágenes |
| Ajustar tamaño del logo | `thumbnail()` relativo al base | Proporciones consistentes |
