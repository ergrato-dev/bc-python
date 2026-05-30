# Semana 25: Procesamiento de Video con FFmpeg

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Construir grafos de procesamiento de video con `ffmpeg-python` (nodes + streams)
- Transcodificar entre codecs: H.264, H.265/HEVC, AV1, ProRes
- Generar proxies de baja resolución para flujos de edición no destructivos
- Extraer clips por timecode, thumbnails y audio separado
- Leer metadata técnica (codec, resolución, framerate, bitrate) con ffprobe y pymediainfo

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [ffmpeg-python — Fundamentos](1-teoria/01-ffmpeg-python-fundamentos.md) | Nodes, streams, input/output, run(), overwrite |
| 02 | [Transcodificación](1-teoria/02-transcodificacion.md) | H.264, H.265, AV1, ProRes; CRF, bitrate, preset |
| 03 | [Proxies y Extracción](1-teoria/03-proxies-extraccion.md) | Proxy low-res, clips por timecode, thumbnails, audio split |
| 04 | [Filtros de Video](1-teoria/04-filtros-video.md) | scale, fps, crop, drawtext, overlay, concat |
| 05 | [Metadata y MediaInfo](1-teoria/05-metadata-mediainfo.md) | ffprobe JSON, pymediainfo, resolución, framerate, codec |

---

## Estructura de la Semana

```
week-25-procesamiento_video_ffmpeg/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-transcodificacion-basica/
│   ├── 02-extraccion-clips/
│   ├── 03-filtros-escala/
│   └── 04-metadata-proxy/
├── 3-proyecto/
│   ├── README.md           # studio-post-pipeline
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: fundamentos + transcodificación | 1.5h |
| 2 | Teoría: proxies + filtros + metadata | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Herramienta | Rol |
|-------------|-----|
| `ffmpeg` | Motor de procesamiento de video (sistema) |
| `ffmpeg-python` | API Python fluent para ffmpeg |
| `pymediainfo` | Lectura de metadata de video/audio |
| `subprocess` + `ffprobe` | Extracción de metadata JSON |

---

## Requisito del sistema

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Verificar
ffmpeg -version && ffprobe -version
```

---

## Navegación

← [Semana 24 — Procesamiento de Audio](../week-24-procesamiento_audio/README.md) · [Semana 26 — Cloud Storage](../week-26-cloud_storage/README.md) →
