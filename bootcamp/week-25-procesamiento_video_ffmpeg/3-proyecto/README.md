# Proyecto — studio-post-pipeline

## Descripción

Pipeline de post-producción para Studio BC: recibe video RAW en `drop/`,
extrae metadata, genera proxy + thumbnail + web encode y archiva el original.

## Comandos

```bash
pip install -e .

# Procesar todos los videos en drop/
python -m studio_post process

# Modo daemon: monitorear drop/
python -m studio_post watch

# Inspeccionar metadata de un video
python -m studio_post info video.mp4
```

## Estructura de salida

```
output/
├── proxy/      # 25% resolución, H.264 veryfast
├── thumbs/     # frame en segundo 5, JPG
├── web/        # H.264 CRF 23, 1080p max, faststart
├── archive/    # original movido aquí
└── meta/       # {video}_meta.json con toda la metadata
```

## Requisitos

- El proxy debe ser exactamente 25% de la resolución original
- El web encode no supera 1080p (1920×1080) — si el original es menor, mantener resolución
- La metadata se guarda antes de cualquier procesamiento
- mypy --strict pasa sin errores en `src/`

## Archivos a completar

| Archivo | TODOs |
|---------|-------|
| `src/inspector.py` | `ffprobe_json()`, `get_video_info()`, `save_metadata()` |
| `src/encoder.py` | `generate_proxy()`, `generate_web()`, `extract_thumbnail()` |
| `src/pipeline.py` | `process_video()` — orquesta todo |
| `src/__main__.py` | comandos `process`, `watch`, `info` |
