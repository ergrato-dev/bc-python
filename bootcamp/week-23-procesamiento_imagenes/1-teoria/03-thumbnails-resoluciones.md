# Thumbnails en Múltiples Resoluciones

## Objetivos

- Definir perfiles de resolución para web, social media y print
- Usar `Image.thumbnail()` e `ImageOps.fit()` correctamente
- Generar variantes con preservación de aspect ratio
- Estructurar la salida de un generador de thumbnails

---

## 1. Perfiles de resolución Studio BC

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ThumbProfile:
    name: str
    max_width: int
    max_height: int
    format: str    # "WEBP", "JPEG"
    quality: int
    fit: bool = False  # True = recortar para llenar exactamente

PROFILES: list[ThumbProfile] = [
    ThumbProfile("web",    1200, 800,  "WEBP", 85),
    ThumbProfile("social", 1080, 1080, "WEBP", 85, fit=True),
    ThumbProfile("thumb",  300,  300,  "WEBP", 80, fit=True),
    ThumbProfile("print",  3000, 2000, "TIFF", 100),
]
```

---

## 2. thumbnail() vs fit()

**`Image.thumbnail()`** — reduce sin recortar, nunca agranda:
```python
img = Image.open("foto.jpg")  # 4000 × 3000
img.thumbnail((1200, 800), Image.LANCZOS)
print(img.size)  # (1067, 800) — preserva ratio, cabe en el bounding box
```

**`ImageOps.fit()`** — recorta para llenar exactamente las dimensiones:
```python
from PIL import ImageOps

img = Image.open("foto.jpg")  # 4000 × 3000
fitted = ImageOps.fit(img, (1080, 1080), Image.LANCZOS)
print(fitted.size)  # (1080, 1080) — cuadrado perfecto, puede recortar bordes
```

Cuándo usar cada uno:

| Método | Resultado | Cuándo |
|--------|-----------|--------|
| `thumbnail()` | Proporcional, bounding box | Web, artículos, galerías |
| `ImageOps.fit()` | Exacto con crop | Social media, grids, avatares |

---

## 3. Generador de thumbnails

```python
from pathlib import Path
from PIL import Image, ImageOps

def generate_thumbnails(
    src: Path,
    dest_dir: Path,
    profiles: list[ThumbProfile],
) -> dict[str, Path]:
    results: dict[str, Path] = {}

    with Image.open(src) as original:
        # Asegurar RGB para formatos que no soportan RGBA
        if original.mode in ("RGBA", "P"):
            base = original.convert("RGB")
        else:
            base = original.copy()

        for profile in profiles:
            out_dir = dest_dir / profile.name
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / src.with_suffix(f".{profile.format.lower()}").name

            img = base.copy()

            if profile.fit:
                img = ImageOps.fit(img, (profile.max_width, profile.max_height), Image.LANCZOS)
            else:
                img.thumbnail((profile.max_width, profile.max_height), Image.LANCZOS)

            save_kwargs: dict = {"quality": profile.quality}
            img.save(out_path, profile.format, **save_kwargs)
            results[profile.name] = out_path

    return results
```

---

## 4. Detectar orientación EXIF y corregir

Las cámaras rotan imágenes en EXIF sin girar los píxeles. Pillow 10+ lo corrige automáticamente. Para versiones anteriores:

```python
from PIL import ImageOps

def auto_orient(img: Image.Image) -> Image.Image:
    # Corrige la orientación EXIF automáticamente
    return ImageOps.exif_transpose(img)
```

Siempre aplicar `exif_transpose()` antes de generar thumbnails para evitar imágenes rotadas incorrectamente.

---

## 5. Calcular dimensiones finales sin abrir la imagen

```python
from PIL import Image

def thumbnail_size(
    src_w: int, src_h: int, max_w: int, max_h: int
) -> tuple[int, int]:
    ratio = min(max_w / src_w, max_h / src_h)
    return int(src_w * ratio), int(src_h * ratio)

# Ejemplo: imagen 4000×3000, thumbnail 1200×800
print(thumbnail_size(4000, 3000, 1200, 800))  # (1067, 800)
```

---

## ✅ Resumen

| Perfil | Dimensiones | Método | Formato |
|--------|-------------|--------|---------|
| Web | 1200×800 | `thumbnail()` | WebP 85 |
| Social | 1080×1080 | `ImageOps.fit()` | WebP 85 |
| Thumb | 300×300 | `ImageOps.fit()` | WebP 80 |
| Print | 3000×2000 | `thumbnail()` | TIFF |
