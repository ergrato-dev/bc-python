# Proyecto — studio-art-pipeline

## Descripción

Pipeline de procesamiento de imágenes para Studio BC: recibe archivos en `drop/`,
genera variantes web/social/thumb con watermark y los exporta a `output/`.

## Comandos

```bash
pip install -e .

# Procesar todas las imágenes en drop/ (una pasada)
python -m studio_art process

# Modo daemon: monitorear drop/ con watchdog
python -m studio_art watch

# Ver resumen de archivos procesados
python -m studio_art stats
```

## Estructura de salida

```
output/
├── web/          # 1200×800 WebP 85 — proporcional
├── social/       # 1080×1080 WebP 85 — cuadrado (crop)
├── thumb/        # 300×300 WebP 80 — cuadrado (crop)
└── print/        # 3000×2000 TIFF — proporcional
```

## Requisitos

- Los thumbnails deben preservar proporciones (web, print) o hacer crop centrado (social, thumb)
- El watermark de logo se aplica a las variantes web y social
- Las imágenes corruptas no interrumpen el batch
- mypy --strict pasa sin errores en `src/`

## Archivos a completar

| Archivo | TODOs |
|---------|-------|
| `src/thumbnailer.py` | `generate_thumb()`, `batch_generate()` |
| `src/watermarker.py` | `apply_logo()`, `apply_text()` |
| `src/pipeline.py` | `process_image()` — orquesta thumbnail + watermark |
| `src/__main__.py` | comandos `process`, `watch`, `stats` |
