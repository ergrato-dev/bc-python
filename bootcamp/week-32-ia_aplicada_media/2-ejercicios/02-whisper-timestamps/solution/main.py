"""
Ejercicio 02: Whisper — Transcripción con Timestamps — SOLUCIÓN
================================================================
"""
from __future__ import annotations

import os
from pathlib import Path

from openai import OpenAI

client = OpenAI()


def transcribe_with_segments(audio_path: Path) -> dict[str, object]:
    with audio_path.open("rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            language="es",
        )
    return {
        "text": result.text,
        "language": result.language,
        "duration": result.duration,
        "segments": [
            {"id": s.id, "start": s.start, "end": s.end, "text": s.text.strip()}
            for s in (result.segments or [])
        ],
    }


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


def generate_simple_chapters(
    segments: list[dict[str, object]],
    min_chapter_s: float = 60.0,
) -> list[dict[str, object]]:
    chapters: list[dict[str, object]] = []
    current_start = float(str(segments[0]["start"])) if segments else 0.0
    current_texts: list[str] = []

    for seg in segments:
        current_texts.append(str(seg["text"]))
        if float(str(seg["end"])) - current_start >= min_chapter_s:
            text = " ".join(current_texts)
            chapters.append({
                "timestamp": f"{int(current_start // 60)}:{int(current_start % 60):02d}",
                "title": text[:50] + "..." if len(text) > 50 else text,
            })
            current_start = float(str(seg["end"]))
            current_texts = []

    if current_texts:
        text = " ".join(current_texts)
        chapters.append({
            "timestamp": f"{int(current_start // 60)}:{int(current_start % 60):02d}",
            "title": text[:50] + "..." if len(text) > 50 else text,
        })

    return chapters


MOCK_TRANSCRIPT: dict[str, object] = {
    "text": "Bienvenidos a Studio BC. Hoy presentamos el proceso de post-producción.",
    "language": "es",
    "duration": 8.4,
    "segments": [
        {"id": 0, "start": 0.0, "end": 4.0, "text": "Bienvenidos a Studio BC."},
        {"id": 1, "start": 4.0, "end": 8.4, "text": "Hoy presentamos el proceso de post-producción."},
    ],
}


if __name__ == "__main__":
    dry_run = not os.getenv("OPENAI_API_KEY")
    data = MOCK_TRANSCRIPT if dry_run else transcribe_with_segments(Path("test_audio.mp3"))

    print(f"Texto: {data['text']}")
    segments = data["segments"]  # type: ignore[assignment]
    srt = segments_to_srt(segments)
    print(f"SRT:\n{srt}")
    assert "-->" in srt

    chapters = generate_simple_chapters(segments, min_chapter_s=3.0)
    print(f"Capítulos: {chapters}")
    print("\nOK — Ejercicio 02 completado")
