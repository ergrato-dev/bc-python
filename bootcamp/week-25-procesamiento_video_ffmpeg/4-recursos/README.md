# Recursos — Semana 25: Procesamiento de Video con FFmpeg

## Webgrafía

### Documentación oficial

| Recurso | URL | Por qué vale la pena |
|---------|-----|----------------------|
| FFmpeg Documentation | https://ffmpeg.org/ffmpeg.html | Referencia completa de opciones CLI |
| ffmpeg-python API Docs | https://kkroening.github.io/ffmpeg-python/ | Node graph, streams, filtros |
| FFmpeg Filters Guide | https://ffmpeg.org/ffmpeg-filters.html | Catálogo de filtros con ejemplos |
| ffprobe JSON output | https://ffmpeg.org/ffprobe.html | Campos disponibles en `-print_format json` |
| pymediainfo | https://pymediainfo.readthedocs.io/ | Wrapper Python para MediaInfo |

### Artículos y guías

| Recurso | Tema |
|---------|------|
| [H.264 Encoding Guide — trac.ffmpeg.org](https://trac.ffmpeg.org/wiki/Encode/H.264) | CRF, preset, tune: guía oficial |
| [H.265/HEVC Guide](https://trac.ffmpeg.org/wiki/Encode/H.265) | Diferencias con H.264, 10-bit |
| [FFmpeg Seeking](https://trac.ffmpeg.org/wiki/Seeking) | `-ss` antes vs después del input |
| [Creating multiple outputs](https://trac.ffmpeg.org/wiki/Creating%20multiple%20outputs) | Un input → varios outputs |
| [Scaling — FFmpeg Wiki](https://trac.ffmpeg.org/wiki/Scaling) | scale filter, aspect ratio, SAR |
| [StreamingLearningCenter — CRF](https://www.streaminglearningcenter.com/articles/pros-and-cons-of-crf-encoding.html) | CRF vs CBR vs VBR en detalle |

---

## Stack técnico de la semana

```
ffmpeg-python      # node graph API — ffmpeg.input().filter().output().run()
pymediainfo        # lectura de metadatos de streams multimedia
ffprobe            # herramienta CLI incluida en FFmpeg para inspección JSON
```

### Instalación rápida

```bash
# Ubuntu/Debian
sudo apt install ffmpeg mediainfo

# Python packages
pip install ffmpeg-python pymediainfo
```

---

## Videos y tutoriales

| Canal / Recurso | Contenido |
|-----------------|-----------|
| [FFmpeg Tutorials — YouTube: Vladimir Panteleev](https://www.youtube.com/c/vpzom) | Hands-on FFmpeg desde cero |
| [OBS Project Blog](https://obsproject.com/blog) | Encoding settings para streaming real |
| [Demuxed Conference Talks](https://www.youtube.com/@Demuxed) | Video engineering avanzado |
| [Cloudinary Blog — Video](https://cloudinary.com/blog/category/video) | Transcoding, adaptive streaming |

---

## Herramientas complementarias

| Herramienta | Uso |
|-------------|-----|
| `mediainfo` (CLI) | Inspeccionar streams sin Python |
| `mkvtoolnix` | Manipulación de contenedores MKV |
| `HandBrake` (GUI) | Probar perfiles de encoding visualmente |
| `VLC` | Preview inmediato de archivos generados |
| `ffplay` | Preview ligero incluido en FFmpeg |

---

## Lecturas recomendadas

- **"Video Codec Bible" — Jan Ozer (Streaming Media)** — CRF, bitrate ladders, ABR
- **Netflix Tech Blog: `per-title encoding`** — Cómo Netflix elige CRF por contenido
- **AWS Elemental — Video Encoding Basics** — Conceptos sólidos de I/P/B frames, GOP

---

## Navegación

← [Teoría](../1-teoria/) · [Proyecto](../3-proyecto/)
