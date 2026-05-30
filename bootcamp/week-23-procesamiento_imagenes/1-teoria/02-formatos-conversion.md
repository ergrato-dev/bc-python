# Formatos y Conversión

## Objetivos

- Conocer las características de JPG, PNG, WebP, TIFF para producción
- Convertir entre formatos con opciones de calidad y compresión
- Leer archivos RAW con `rawpy`
- Leer y escribir metadatos EXIF con `piexif`

---

## 1. Comparativa de formatos

| Formato | Compresión | Alpha | Uso principal |
|---------|-----------|-------|---------------|
| JPG | Con pérdida | No | Fotos web, social media |
| PNG | Sin pérdida | Sí | Logos, gráficos con transparencia |
| WebP | Con/sin pérdida | Sí | Web moderno (mejor ratio que JPG/PNG) |
| TIFF | Sin pérdida | Sí | Archivo, impresión, masterizado |
| GIF | Sin pérdida | Índice | Animaciones simples |

---

## 2. Guardar con calidad óptima

```python
from PIL import Image

img = Image.open("foto.jpg")

# JPG — calidad 85-95 es el rango profesional
img.convert("RGB").save("output.jpg", quality=90, optimize=True, progressive=True)

# PNG — sin pérdida, comprimir con nivel 6 (0-9)
img.convert("RGBA").save("output.png", optimize=True, compress_level=6)

# WebP — excelente para web, 20-40% más pequeño que JPG a misma calidad
img.convert("RGB").save("output.webp", quality=85, method=6)

# WebP lossless
img.save("output_lossless.webp", lossless=True)

# TIFF — para archivo
img.save("output.tiff", compression="lzw")
```

---

## 3. Detectar formato y convertir en lote

```python
from pathlib import Path
from PIL import Image

CONVERT_MAP = {".jpeg": ".jpg", ".JPEG": ".jpg", ".PNG": ".png"}

def normalize_extension(path: Path) -> Path:
    new_path = path.with_suffix(path.suffix.lower())
    if new_path != path:
        path.rename(new_path)
    return new_path

def convert_to_webp(src: Path, dest_dir: Path, quality: int = 85) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.with_suffix(".webp").name
    with Image.open(src) as img:
        img.convert("RGB").save(dest, "WEBP", quality=quality)
    return dest
```

---

## 4. Leer archivos RAW con rawpy

Los archivos RAW (`.cr2` Canon, `.nef` Nikon, `.arw` Sony) no son JPG. Contienen datos crudos del sensor. `rawpy` los decodifica a RGB:

```python
import rawpy
import numpy as np
from PIL import Image

def raw_to_pillow(raw_path: str) -> Image.Image:
    with rawpy.imread(raw_path) as raw:
        # postprocess convierte a numpy array uint8 RGB
        rgb_array = raw.postprocess(
            use_camera_wb=True,     # balance de blancos de la cámara
            half_size=False,        # resolución completa
            no_auto_bright=False,   # auto-brillo
            output_bps=8,           # 8 bits por canal
        )
    return Image.fromarray(rgb_array)

# Uso
img = raw_to_pillow("foto.cr2")
img.save("foto_from_raw.jpg", quality=95)
```

---

## 5. Metadatos EXIF con piexif

EXIF almacena datos de cámara (apertura, ISO, fecha, GPS) dentro del archivo de imagen.

```python
import piexif
from pathlib import Path

# Leer EXIF
exif_dict = piexif.load("foto.jpg")

# Campos comunes en Exif IFD
exif = exif_dict.get("Exif", {})
iso = exif.get(piexif.ExifIFD.ISOSpeedRatings)
dt  = exif.get(piexif.ExifIFD.DateTimeOriginal)
print(f"ISO: {iso}, Fecha: {dt}")

# Leer GPS
gps = exif_dict.get("GPS", {})
lat = gps.get(piexif.GPSIFD.GPSLatitude)

# Eliminar EXIF (para proteger privacidad)
from PIL import Image
img = Image.open("foto.jpg")
data = list(img.getdata())
img_no_exif = Image.new(img.mode, img.size)
img_no_exif.putdata(data)
img_no_exif.save("foto_sin_exif.jpg", quality=92)
```

---

## 6. Tamaños de archivo y trade-offs

Para una imagen de 6 MP (3000×2000):

| Formato | Tamaño típico | Calidad |
|---------|---------------|---------|
| TIFF sin comprimir | ~18 MB | Perfecto |
| PNG lossless | ~6 MB | Perfecto |
| JPG quality=95 | ~3 MB | Excelente |
| JPG quality=85 | ~1.5 MB | Muy buena |
| WebP quality=85 | ~1 MB | Muy buena |
| WebP lossless | ~4 MB | Perfecto |

---

## ✅ Resumen

| Necesidad | Formato |
|-----------|---------|
| Foto web | WebP quality=85 o JPG quality=90 |
| Logo/gráfico con transparencia | PNG |
| Archivo sin pérdida | TIFF LZW |
| RAW de cámara → editable | rawpy → JPG/TIFF |
| Quitar metadatos privados | Reconstruir con `putdata()` |
