# Glosario — Semana 25: Procesamiento de Video con FFmpeg

## Conceptos de codificación

| Término | Definición |
|---------|------------|
| **Codec** | Algoritmo de compresión/descompresión de video (H.264, H.265, AV1, ProRes) |
| **Contenedor** | Formato de archivo que encapsula streams de video, audio y metadatos (MP4, MKV, MOV) |
| **Bitrate** | Cantidad de datos por segundo que ocupa el video comprimido (Mbps / kbps) |
| **CRF** | Constant Rate Factor — control de calidad constante; valor menor = más calidad y mayor tamaño |
| **Preset** | Velocidad de encoding vs eficiencia de compresión: `ultrafast`→`veryslow` en libx264/libx265 |
| **GOP** | Group of Pictures — secuencia que comienza con un keyframe (I-frame) |
| **I-frame** | Intra-coded frame: fotograma completo, sin referencia a otros (keyframe) |
| **P-frame** | Predicted frame: codifica solo diferencias respecto al frame anterior |
| **B-frame** | Bidirectional frame: referencia frames anteriores y posteriores |
| **Chroma subsampling** | Reducción de resolución del canal de color: 4:2:0 (streaming), 4:2:2 (edit), 4:4:4 (mastering) |

## Formatos y perfiles

| Término | Definición |
|---------|------------|
| **H.264 / AVC** | Advanced Video Coding — codec dominante para web y distribución; `libx264` en FFmpeg |
| **H.265 / HEVC** | High Efficiency Video Coding — 40–50% mejor compresión que H.264; `libx265` |
| **AV1** | Codec open-source de Alliance for Open Media; mejor compresión que HEVC, más lento de encodear |
| **ProRes** | Codec de edición de Apple (ProRes 422, 4444) — alta calidad, archivos grandes, sin pérdida perceptual |
| **Proxy** | Copia de baja resolución (ej. 25% del original) para edición fluida en post-producción |
| **Web-ready** | Video optimizado para streaming: `movflags=+faststart` mueve el átomo `moov` al inicio del MP4 |
| **faststart** | Flag de MP4 que permite reproducción antes de descarga completa (progressive download) |

## FFmpeg / ffprobe

| Término | Definición |
|---------|------------|
| **Node graph** | Modelo de ffmpeg-python donde inputs, filtros y outputs son nodos conectados por streams |
| **Stream specifier** | Selector de stream en FFmpeg: `v:0` (primer video), `a:1` (segundo audio), `s:0` (subtítulos) |
| **Filter graph** | Cadena de filtros de video/audio aplicados en secuencia o en paralelo con `[in][out]` |
| **`-ss` (seek)** | Posición de inicio de lectura; antes del input es más rápido (keyframe seek), después es preciso |
| **`-to` / `-t`** | `-to` es posición absoluta de fin; `-t` es duración relativa desde el inicio de la lectura |
| **`-vframes 1`** | Extrae un solo fotograma de video (usado para thumbnails) |
| **`avg_frame_rate`** | Campo de ffprobe con FPS como fracción "num/den" (ej. `"30000/1001"` ≈ 29.97 fps) |
| **`ffprobe`** | Herramienta de inspección incluida en FFmpeg; con `-print_format json` devuelve metadatos estructurados |

## Post-producción

| Término | Definición |
|---------|------------|
| **Timecode** | Referencia de tiempo en formato `HH:MM:SS:FF` (horas:minutos:segundos:frames) |
| **Ingest** | Proceso de ingesta: recibir, inspeccionar y registrar archivos de media recién llegados |
| **Transcode** | Recodificar un archivo de un codec/perfil a otro |
| **Remux** | Cambiar contenedor sin recodificar streams (ej. MKV → MP4 sin pérdida de calidad) |
| **Burn-in** | Incrustar texto o subtítulos directamente en los píxeles del video (no como stream separado) |
| **LUT** | Look-Up Table — tabla de corrección de color que mapea valores de entrada a valores de salida |
| **Aspect ratio** | Relación ancho/alto: 16:9 (widescreen), 4:3 (legacy), 2.39:1 (cinemascope) |
| **SAR / DAR** | Sample Aspect Ratio (píxeles no cuadrados) / Display Aspect Ratio (relación de visualización final) |

## Metadatos

| Término | Definición |
|---------|------------|
| **Stream** | Cada pista de datos dentro de un contenedor: video, audio, subtítulos, capítulos |
| **codec_name** | Nombre del codec del stream en formato ffprobe (ej. `"h264"`, `"aac"`, `"hevc"`) |
| **bit_depth** | Bits por canal de color: 8-bit (SDR), 10-bit (HDR, ProRes HQ), 12-bit (RAW cinema) |
| **color_space** | Espacio de color del video: `bt709` (HD), `bt2020` (HDR/UHD), `smpte170m` (SD NTSC) |
| **pymediainfo** | Librería Python que envuelve la herramienta `MediaInfo` para extraer metadatos de media |
