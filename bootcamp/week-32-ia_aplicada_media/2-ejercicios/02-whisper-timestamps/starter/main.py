"""
Ejercicio 02: Whisper — Transcripción con Timestamps
====================================================
Transcribe un archivo de audio y extrae segmentos con timestamps.
Genera SRT y capítulos simples.

Requisitos: pip install openai
            export OPENAI_API_KEY=sk-...

Ejecutar: python main.py
"""
from __future__ import annotations

import os
from pathlib import Path
from openai import OpenAI

client = OpenAI()


def transcribe_with_segments(audio_path: Path) -> dict[str, object]:
    """
    Transcribe el audio con response_format="verbose_json" y timestamp_granularities.
    Devuelve: {text, language, duration, segments: [{id, start, end, text}]}

    TODO:
    with audio_path.open("rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            language="es",
        )
    Construir y retornar el dict con text, language, duration, segments
    """
    raise NotImplementedError


def format_timestamp_srt(seconds: float) -> str:
    """Convierte segundos a formato HH:MM:SS,mmm para SRT."""
    # TODO: calcular h, m, s, ms y formatear con f-string
    raise NotImplementedError


def segments_to_srt(segments: list[dict[str, object]]) -> str:
    """
    Convierte la lista de segmentos a formato SRT.
    Cada entrada: número\\nSTART --> END\\ntexto\\n
    """
    # TODO: iterar con enumerate(segments, 1), construir líneas SRT
    raise NotImplementedError


def generate_simple_chapters(
    segments: list[dict[str, object]],
    min_chapter_s: float = 60.0,
) -> list[dict[str, object]]:
    """
    Agrupa segmentos en capítulos de duración mínima min_chapter_s.
    Devuelve list de {timestamp: "M:SS", title: "primeras palabras..."}.
    """
    # TODO: acumular segmentos hasta alcanzar min_chapter_s
    # timestamp: f"{int(start//60)}:{int(start%60):02d}"
    # title: primeras 50 chars del texto acumulado
    raise NotImplementedError


# ── Mock para dry-run ─────────────────────────────────────────────────────────

MOCK_TRANSCRIPT: dict[str, object] = {
    "text": "Bienvenidos a Studio BC. Hoy presentamos el proceso de post-producción para nuestros clientes.",
    "language": "es",
    "duration": 8.4,
    "segments": [
        {"id": 0, "start": 0.0, "end": 4.0, "text": "Bienvenidos a Studio BC."},
        {"id": 1, "start": 4.0, "end": 8.4, "text": "Hoy presentamos el proceso de post-producción para nuestros clientes."},
    ],
}


if __name__ == "__main__":
    dry_run = not os.getenv("OPENAI_API_KEY")

    if dry_run:
        print("Modo dry-run")
        data = MOCK_TRANSCRIPT
    else:
        audio_path = Path("test_audio.mp3")
        if not audio_path.exists():
            print("Crea test_audio.mp3 antes de ejecutar")
            raise SystemExit(1)
        data = transcribe_with_segments(audio_path)

    print(f"Texto: {data['text']}")
    print(f"Idioma: {data['language']} | Duración: {data['duration']}s")
    print(f"Segmentos: {len(data['segments'])}")

    segments = data["segments"]  # type: ignore[assignment]
    srt = segments_to_srt(segments)
    print(f"\nSRT:\n{srt}")
    assert "00:00:00,000" in srt or "-->" in srt

    chapters = generate_simple_chapters(segments, min_chapter_s=3.0)
    print(f"Capítulos: {chapters}")

    print("\nOK — Ejercicio 02 completado")
