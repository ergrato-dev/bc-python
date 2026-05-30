# Pillow — Fundamentos

## Objetivos

- Abrir, inspeccionar y guardar imágenes con `Image`
- Entender los modos de color: RGB, RGBA, L, CMYK
- Aplicar transformaciones básicas: resize, crop, rotate, flip
- Dibujar texto y formas con `ImageDraw`

---

## 1. Abrir y guardar

```python
from PIL import Image
from pathlib import Path

# Abrir
img = Image.open("foto.jpg")
print(img.size)    # (1920, 1080) — (ancho, alto)
print(img.mode)    # "RGB"
print(img.format)  # "JPEG"

# Guardar en otro formato
img.save("foto.png")
img.save("foto.webp", quality=85)
img.save("foto.jpg", quality=90, optimize=True)

# Abrir desde bytes (ej: descargado con httpx)
import io
data = Path("foto.jpg").read_bytes()
img = Image.open(io.BytesIO(data))
```

---

## 2. Modos de color

| Modo | Descripción | Canal | Uso |
|------|-------------|-------|-----|
| `RGB` | Rojo, Verde, Azul | 3 × 8 bit | Fotos para web/pantalla |
| `RGBA` | RGB + Alpha (transparencia) | 4 × 8 bit | PNG con transparencia |
| `L` | Luminosidad (escala de grises) | 1 × 8 bit | Máscaras, imágenes en B&N |
| `CMYK` | Cyan, Magenta, Amarillo, Negro | 4 × 8 bit | Impresión profesional |
| `P` | Paleta indexada | 1 × 8 bit | GIF, PNG optimizados |

Conversiones:
```python
img_rgb  = img.convert("RGB")   # elimina alpha (RGBA → RGB)
img_gray = img.convert("L")     # escala de grises
img_rgba = img.convert("RGBA")  # agrega canal alpha (todos 255)
```

Regla práctica: antes de guardar como JPG, siempre convertir a `"RGB"` — JPG no soporta RGBA.

---

## 3. Resize

```python
from PIL import Image

img = Image.open("foto.jpg")

# Tamaño exacto (puede distorsionar)
resized = img.resize((800, 600), Image.LANCZOS)

# Preservar proporciones con thumbnail (modifica in-place, nunca agranda)
thumb = img.copy()
thumb.thumbnail((400, 400), Image.LANCZOS)
# thumb.size será <= (400, 400) preservando el aspect ratio

# Preservar proporciones con resize manual
def resize_keep_ratio(img: Image.Image, max_width: int, max_height: int) -> Image.Image:
    img.thumbnail((max_width, max_height), Image.LANCZOS)
    return img
```

Filtros de downsampling:

| Filtro | Calidad | Velocidad | Uso |
|--------|---------|-----------|-----|
| `NEAREST` | Baja | Muy rápida | Debug, pixel art |
| `BILINEAR` | Media | Rápida | Vista previa |
| `BICUBIC` | Alta | Media | Thumbnails |
| `LANCZOS` | Muy alta | Lenta | Producción, impresión |

---

## 4. Crop

```python
# box = (left, upper, right, lower) — en píxeles
cropped = img.crop((100, 50, 700, 450))
print(cropped.size)  # (600, 400)

# Crop centrado
def center_crop(img: Image.Image, width: int, height: int) -> Image.Image:
    w, h = img.size
    left   = (w - width)  // 2
    upper  = (h - height) // 2
    right  = left + width
    lower  = upper + height
    return img.crop((left, upper, right, lower))
```

---

## 5. Rotate y Flip

```python
# Rotar (el fondo se rellena con negro por defecto)
rotated = img.rotate(90, expand=True)          # 90° anti-horario
rotated = img.rotate(45, expand=True, fillcolor=(255, 255, 255))

# Flip
from PIL import ImageOps
flipped_h = ImageOps.mirror(img)  # espejo horizontal
flipped_v = ImageOps.flip(img)    # espejo vertical
```

---

## 6. ImageDraw — texto y formas

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.open("foto.jpg").copy()
draw = ImageDraw.Draw(img)

# Rectángulo
draw.rectangle([(10, 10), (200, 100)], outline=(255, 0, 0), width=3)

# Texto básico (fuente por defecto del sistema)
draw.text((20, 20), "Studio BC", fill=(255, 255, 255))

# Texto con fuente custom (TrueType)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=36)
except OSError:
    font = ImageFont.load_default()
draw.text((20, 20), "Studio BC", fill=(255, 255, 255), font=font)
```

---

## ✅ Resumen

| Operación | API |
|-----------|-----|
| Abrir | `Image.open(path)` |
| Guardar | `img.save(path, quality=N)` |
| Convertir modo | `img.convert("RGB")` |
| Redimensionar (exacto) | `img.resize((w, h), Image.LANCZOS)` |
| Redimensionar (proporcional) | `img.thumbnail((max_w, max_h), Image.LANCZOS)` |
| Recortar | `img.crop((left, upper, right, lower))` |
| Rotar | `img.rotate(degrees, expand=True)` |
| Dibujar | `ImageDraw.Draw(img).text(pos, text, fill=color)` |
