# Semana 24: Procesamiento de Audio

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Manipular audio con `pydub`: cortar, concatenar, mezclar, exportar
- Normalizar volumen, aplicar fades y detectar segmentos de silencio
- Leer y escribir metadatos ID3 (artista, título, BPM) con `mutagen`
- Transcribir audio a texto con OpenAI Whisper (modelo local)
- Generar archivos de subtítulos SRT y WebVTT desde timestamps

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [pydub — Fundamentos](1-teoria/01-pydub-fundamentos.md) | AudioSegment, slice, concat, export, formatos |
| 02 | [Normalización y Efectos](1-teoria/02-normalizacion-efectos.md) | normalize, gain, fade, split_on_silence, overlay |
| 03 | [Formatos y Metadata](1-teoria/03-formatos-metadata.md) | MP3/WAV/FLAC/OGG, ID3 con mutagen, conversión |
| 04 | [Transcripción con Whisper](1-teoria/04-transcripcion-whisper.md) | openai-whisper modelo local, segmentos con timestamps |
| 05 | [Subtítulos SRT y VTT](1-teoria/05-subtitulos-srt-vtt.md) | Formato SRT/VTT, generar desde transcripción Whisper |

---

## Estructura de la Semana

```
week-24-procesamiento_audio/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-pydub-operaciones/
│   ├── 02-normalizacion-silencio/
│   ├── 03-metadata-id3/
│   └── 04-transcripcion/
├── 3-proyecto/
│   ├── README.md           # studio-audio-pipeline
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: pydub + normalización | 1.5h |
| 2 | Teoría: formatos + Whisper + subtítulos | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `pydub` | Edición de audio: corte, mezcla, fade, normalización |
| `mutagen` | Lectura y escritura de metadatos ID3/Vorbis |
| `openai-whisper` | Transcripción automática de voz a texto (local) |
| `librosa` | Análisis de audio: BPM, espectro, detección de onset |
| `ffmpeg` | Backend de pydub para codecs (MP3, AAC, FLAC) |

---

## Navegación

← [Semana 23 — Procesamiento de Imágenes](../week-23-procesamiento_imagenes/README.md) · [Semana 25 — Procesamiento de Video con FFmpeg](../week-25-procesamiento_video_ffmpeg/README.md) →
