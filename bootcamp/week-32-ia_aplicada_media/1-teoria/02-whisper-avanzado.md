# Whisper — Transcripción Avanzada

## 1. Transcripción Básica

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()


def transcribe(audio_path: Path) -> str:
    with audio_path.open("rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="es",  # omitir para detección automática
        )
    return result.text
```

---

## 2. `verbose_json` — Timestamps y Segmentos

```python
def transcribe_with_timestamps(audio_path: Path) -> dict[str, object]:
    with audio_path.open("rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            language="es",
        )

    return {
        "text": result.text,
        "language": result.language,
        "duration": result.duration,
        "words": [
            {
                "word": w.word,
                "start": w.start,
                "end": w.end,
            }
            for w in (result.words or [])
        ],
        "segments": [
            {
                "id": s.id,
                "start": s.start,
                "end": s.end,
                "text": s.text.strip(),
            }
            for s in (result.segments or [])
        ],
    }
```

Ejemplo de salida:

```json
{
  "text": "Hola, bienvenidos a Studio BC. Hoy vamos a ver el proceso de producción.",
  "language": "es",
  "duration": 12.4,
  "words": [
    {"word": "Hola,", "start": 0.0, "end": 0.4},
    {"word": "bienvenidos", "start": 0.4, "end": 1.1}
  ],
  "segments": [
    {"id": 0, "start": 0.0, "end": 5.2, "text": "Hola, bienvenidos a Studio BC."},
    {"id": 1, "start": 5.2, "end": 12.4, "text": "Hoy vamos a ver el proceso de producción."}
  ]
}
```

---

## 3. Generar SRT a partir de Segmentos

```python
def format_timestamp_srt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def segments_to_srt(segments: list[dict[str, object]]) -> str:
    lines: list[str] = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_srt(float(str(seg["start"])))
        end = format_timestamp_srt(float(str(seg["end"])))
        lines.append(f"{i}\n{start} --> {end}\n{seg['text']}\n")
    return "\n".join(lines)


def segments_to_vtt(segments: list[dict[str, object]]) -> str:
    lines = ["WEBVTT\n"]
    for seg in segments:
        start = format_timestamp_srt(float(str(seg["start"]))).replace(",", ".")
        end = format_timestamp_srt(float(str(seg["end"]))).replace(",", ".")
        lines.append(f"{start} --> {end}\n{seg['text']}\n")
    return "\n".join(lines)
```

---

## 4. Generar Capítulos desde Segmentos

Los capítulos de YouTube/Vimeo requieren timestamps en formato `MM:SS` al inicio de la descripción:

```python
def generate_chapters_from_segments(
    segments: list[dict[str, object]],
    min_chapter_duration_s: float = 60.0,
) -> list[dict[str, object]]:
    """Agrupa segmentos en capítulos de duración mínima."""
    chapters: list[dict[str, object]] = []
    current_start = 0.0
    current_texts: list[str] = []

    for seg in segments:
        current_texts.append(str(seg["text"]))
        seg_end = float(str(seg["end"]))

        if seg_end - current_start >= min_chapter_duration_s:
            chapters.append({
                "start_s": current_start,
                "timestamp": _format_mm_ss(current_start),
                "title": _summarize_chapter(current_texts),
            })
            current_start = seg_end
            current_texts = []

    if current_texts:
        chapters.append({
            "start_s": current_start,
            "timestamp": _format_mm_ss(current_start),
            "title": _summarize_chapter(current_texts),
        })

    return chapters


def _format_mm_ss(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"


def _summarize_chapter(texts: list[str]) -> str:
    """Nombre provisional — en producción se usa GPT para resumir."""
    combined = " ".join(texts)
    return combined[:50] + "..." if len(combined) > 50 else combined
```

---

## 5. Extraer Audio de Video para Transcribir

```python
import subprocess
from pathlib import Path


def extract_audio(video_path: Path, output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = video_path.with_suffix(".mp3")
    subprocess.run([
        "ffmpeg", "-i", str(video_path),
        "-vn", "-acodec", "libmp3lame", "-q:a", "4",
        str(output_path), "-y",
    ], check=True, capture_output=True)
    return output_path
```

---

## 6. Límites y Formatos Soportados

| Parámetro | Valor |
|-----------|-------|
| Tamaño máximo de archivo | 25 MB |
| Formatos soportados | mp3, mp4, mpeg, mpga, m4a, wav, webm |
| Modelos disponibles | `whisper-1` |
| Idiomas | 57 idiomas + detección automática |

Para archivos grandes: dividir con `pydub` en chunks de 24 MB antes de enviar.

---

## Resumen

| Operación | API |
|-----------|-----|
| Transcripción simple | `response_format="text"` → `result.text` |
| Con timestamps | `response_format="verbose_json"` + `timestamp_granularities` |
| Segmentos | `result.segments` → lista de `{start, end, text}` |
| Palabras | `result.words` → lista de `{word, start, end}` |
| SRT/VTT | Construir desde `segments` con `format_timestamp_srt()` |
