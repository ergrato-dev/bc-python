# Rúbrica de Evaluación — Semana 24: Procesamiento de Audio

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica qué es dBFS y cómo pydub normaliza al target de -14 dBFS (estándar streaming) | 8 |
| Describe cómo Whisper genera segmentos con timestamps y qué campos contiene cada segmento | 7 |
| Explica la diferencia entre SRT y WebVTT, y en qué contexto se usa cada uno | 7 |
| Describe qué es `split_on_silence()` y qué parámetros controlan la detección | 8 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Carga un audio, lo corta en segmentos, aplica fade in/out y exporta a MP3 | 10 |
| Normaliza un audio a -14 dBFS y detecta segmentos de silencio con umbral ajustable | 10 |
| Lee y modifica metadatos ID3 (título, artista, año) de un archivo MP3 con mutagen | 10 |
| Transcribe audio con Whisper y genera un archivo `.srt` válido con timestamps | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| El pipeline `studio-audio-pipeline` produce `.srt` y `.vtt` para cada audio de `drop/` | 12 |
| El pipeline normaliza el audio antes de transcribir (mejora accuracy de Whisper) | 8 |
| Los timestamps en SRT/VTT coinciden con los segmentos de Whisper (±0.1s) | 7 |
| mypy --strict pasa sin errores en `src/` | 3 |
