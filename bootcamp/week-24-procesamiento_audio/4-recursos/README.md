# Recursos — Semana 24: Procesamiento de Audio

## Documentación oficial

- [pydub — Docs](https://github.com/jiaaro/pydub) — GitHub principal (con ejemplos)
- [pydub — API reference](https://github.com/jiaaro/pydub/blob/master/API.markdown) — todas las operaciones
- [mutagen — Docs](https://mutagen.readthedocs.io/) — ID3, Vorbis, MP4 tags
- [openai-whisper — GitHub](https://github.com/openai/whisper) — modelos, opciones, benchmarks
- [librosa — Docs](https://librosa.org/doc/) — análisis de audio, BPM, espectro
- [WebVTT specification](https://www.w3.org/TR/webvtt1/) — estándar W3C para subtítulos web

## Artículos y guías

- [pydub tutorial (Towards Data Science)](https://towardsdatascience.com/audio-manipulation-with-pydub-e6a6e578d7ba) — operaciones comunes
- [Whisper explained](https://openai.com/research/whisper) — paper original de OpenAI
- [Understanding dBFS](https://www.izotope.com/en/learn/what-is-dbfs.html) — iZotope explica decibeles digitales
- [SRT subtitle format](https://wiki.videolan.org/SubRip/) — especificación completa SRT
- [Loudness standards: -14 dBFS](https://support.spotify.com/article/loud-and-clear/) — Spotify loudness normalization

## Videos

- [Python Audio Processing with pydub](https://www.youtube.com/watch?v=ifH2IxQ8NnY) — tutorial completo
- [OpenAI Whisper Tutorial](https://www.youtube.com/watch?v=ABFqbY_rmEk) — transcripción local paso a paso
- [Audio normalization explained](https://www.youtube.com/watch?v=Y8V91r2GF_E) — conceptos de loudness

## Herramientas del proyecto

| Herramienta | Versión | Propósito |
|-------------|---------|-----------|
| `pydub` | ≥0.25 | Edición de audio: corte, mezcla, fade, normalización |
| `mutagen` | ≥1.47 | Metadatos ID3/Vorbis/MP4 |
| `openai-whisper` | ≥20231117 | Transcripción ASR local |
| `ffmpeg` | sistema | Backend de codecs para pydub |
| `librosa` | ≥0.10 | Análisis: BPM, onset, espectro |
| `watchdog` | ≥4.0 | Monitoreo de drop/ |

## Complementario

- [ffmpeg — Official Docs](https://ffmpeg.org/documentation.html) — el motor detrás de pydub
- [Audacity (free)](https://www.audacityteam.org/) — editor de audio visual para inspeccionar resultados
- [Adobe Podcast Enhance](https://podcast.adobe.com/enhance) — mejora de calidad de voz (referencia comparativa)
