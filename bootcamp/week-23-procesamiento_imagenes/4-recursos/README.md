# Recursos — Semana 23: Procesamiento de Imágenes

## Documentación oficial

- [Pillow — Handbook](https://pillow.readthedocs.io/en/stable/handbook/index.html) — referencia completa
- [Pillow — Image module](https://pillow.readthedocs.io/en/stable/reference/Image.html) — Image.open, resize, crop, paste
- [Pillow — ImageOps](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html) — fit, flip, mirror, exif_transpose
- [Pillow — ImageDraw](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html) — text, shapes, draw
- [rawpy — Documentation](https://letmaik.github.io/rawpy/api/) — procesar archivos RAW
- [piexif — Documentation](https://piexif.readthedocs.io/) — leer/escribir EXIF
- [WebP — Google Developers](https://developers.google.com/speed/webp) — por qué usar WebP

## Artículos y guías

- [Real Python — Image Processing with Pillow](https://realpython.com/image-processing-with-the-python-pillow-library/) — tutorial completo
- [Alpha compositing explained](https://en.wikipedia.org/wiki/Alpha_compositing) — matemática detrás del paste con mask
- [LANCZOS resampling](https://en.wikipedia.org/wiki/Lanczos_resampling) — por qué es el filtro de mayor calidad
- [EXIF metadata standard](https://www.exif.org/Exif2-2.PDF) — especificación oficial EXIF 2.2
- [ICC color profiles](https://www.color.org/index.xalter) — gestión de color en producción

## Videos

- [Pillow Tutorial (Python Image Processing)](https://www.youtube.com/watch?v=6Qs3wObeWwc) — walkthrough completo
- [Python Image Processing for beginners](https://www.youtube.com/watch?v=jqOaRjMRWfw) — casos prácticos
- [WebP vs JPG vs PNG](https://www.youtube.com/watch?v=DfvJpfYiqaE) — comparativa visual de formatos

## Herramientas del proyecto

| Herramienta | Versión | Propósito |
|-------------|---------|-----------|
| `Pillow` | ≥10 | Procesamiento de imágenes |
| `rawpy` | ≥0.21 | Decodificación de archivos RAW |
| `piexif` | ≥1.1 | Metadatos EXIF |
| `watchdog` | ≥4.0 | Monitoreo de drop/ |
| `typer` | ≥0.12 | CLI del pipeline |
| `rich` | ≥13 | Progress bar y output |

## Complementario

- [Squoosh (Google)](https://squoosh.app/) — herramienta visual para comparar formatos y calidad
- [ImageMagick](https://imagemagick.org/) — alternativa CLI para batch processing avanzado
- [Aspect ratio calculator](https://calculateaspectratio.com/) — útil para verificar proporciones
