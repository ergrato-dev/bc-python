# Semana 23: Procesamiento de Imágenes

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Abrir, transformar y guardar imágenes con Pillow (`Image`, `ImageOps`, `ImageDraw`)
- Convertir entre formatos: JPG, PNG, WebP, TIFF; leer RAW con `rawpy`
- Generar thumbnails en múltiples resoluciones para web, social y print
- Aplicar watermarks (logo + texto) con alpha compositing
- Procesar lotes de cientos de imágenes con `concurrent.futures` y barra de progreso

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Pillow — Fundamentos](1-teoria/01-pillow-fundamentos.md) | Image.open, modos de color, resize, crop, rotate, save |
| 02 | [Formatos y Conversión](1-teoria/02-formatos-conversion.md) | JPG, PNG, WebP, TIFF, RAW (rawpy), EXIF con piexif |
| 03 | [Thumbnails Múltiples Resoluciones](1-teoria/03-thumbnails-resoluciones.md) | Tamaños web/social/print, LANCZOS, ImageOps.fit |
| 04 | [Watermarks y Overlays](1-teoria/04-watermarks-overlays.md) | Logo overlay, texto con ImageDraw, alpha compositing |
| 05 | [Batch Processing](1-teoria/05-batch-processing.md) | ThreadPoolExecutor, progress bar con Rich, error handling |

---

## Estructura de la Semana

```
week-23-procesamiento_imagenes/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-resize-y-crop/
│   ├── 02-conversion-formatos/
│   ├── 03-watermark/
│   └── 04-batch-thumbnails/
├── 3-proyecto/
│   ├── README.md           # studio-art-pipeline
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: fundamentos + formatos | 1.5h |
| 2 | Teoría: thumbnails + watermarks + batch | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `Pillow` | Operaciones de imagen: resize, crop, draw, composite |
| `rawpy` | Decodificación de archivos RAW (CR2, NEF, ARW) |
| `piexif` | Lectura y escritura de metadatos EXIF |
| `imageio` | I/O de imágenes en múltiples formatos |
| `rich` | Progress bar para batch processing |

---

## Navegación

← [Semana 22 — Automatización del Sistema de Archivos](../week-22-automatizacion_sistema_archivos/README.md) · [Semana 24 — Procesamiento de Audio](../week-24-procesamiento_audio/README.md) →
