"""
Ejercicio 04: Generación Automática de Metadata — SOLUCIÓN
==========================================================
"""
from __future__ import annotations

import json
import os
from openai import OpenAI

client = OpenAI()


def generate_tags(description: str, max_tags: int = 10) -> list[str]:
    prompt = f"""Genera {max_tags} tags SEO para este video audiovisual:
{description}

Devuelve SOLO JSON (sin markdown):
{{"tags": ["tag1", "tag2", ...]}}

Reglas: solo minúsculas, sin espacios (usar guiones), mezcla español e inglés."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=200,
        temperature=0.2,
    )
    result = json.loads(response.choices[0].message.content or "{}")
    return result.get("tags", [])[:max_tags]


def generate_title(description: str, tags: list[str] | None = None) -> str:
    ctx = description
    if tags:
        ctx += f"\nKeywords: {', '.join(tags[:5])}"

    prompt = f"""Genera un título SEO para este video:
{ctx}

Reglas: máximo 70 caracteres, keyword al inicio, en español, sin comillas.
Devuelve SOLO el título:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
        temperature=0.4,
    )
    return (response.choices[0].message.content or "").strip().strip('"')[:70]


def generate_description(description: str, transcript: str = "") -> dict[str, str]:
    ctx = description
    if transcript:
        ctx += f"\nTranscripción: {transcript[:300]}"

    prompt = f"""Genera metadata de descripción SEO para este video:
{ctx}

Devuelve SOLO JSON (sin markdown):
{{
  "snippet": "descripción de 150-160 caracteres para snippet",
  "full_description": "descripción completa de 200-300 palabras"
}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=500,
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content or "{}")


def format_chapters_for_youtube(chapters: list[dict[str, object]]) -> str:
    return "\n".join(f"{ch['timestamp']} {ch['title']}" for ch in chapters)


MOCK_TAGS = ["studio-bc", "produccion-audiovisual", "video-profesional", "post-produccion"]
MOCK_TITLE = "Producción Audiovisual en Studio BC — Proceso Completo"
MOCK_DESC = {
    "snippet": "Descubre el proceso completo de producción audiovisual de Studio BC.",
    "full_description": "Studio BC es un estudio de producción con más de 10 años de experiencia...",
}
MOCK_CHAPTERS = [
    {"timestamp": "0:00", "title": "Introducción"},
    {"timestamp": "1:30", "title": "Proceso de grabación"},
]

SAMPLE_DESCRIPTION = "Video institucional de Studio BC mostrando el proceso de producción audiovisual."
SAMPLE_TRANSCRIPT = "Bienvenidos a Studio BC. Somos un estudio con más de 10 años de experiencia."


if __name__ == "__main__":
    dry_run = not os.getenv("OPENAI_API_KEY")

    if dry_run:
        tags, title, desc = MOCK_TAGS, MOCK_TITLE, MOCK_DESC
    else:
        tags = generate_tags(SAMPLE_DESCRIPTION)
        title = generate_title(SAMPLE_DESCRIPTION, tags)
        desc = generate_description(SAMPLE_DESCRIPTION, SAMPLE_TRANSCRIPT)

    chapters_fmt = format_chapters_for_youtube(MOCK_CHAPTERS)

    print(f"Título: {title}")
    print(f"Tags: {tags}")
    print(f"Snippet: {desc.get('snippet', '')}")
    print(f"Capítulos:\n{chapters_fmt}")

    assert len(title) <= 70
    assert len(tags) > 0
    assert "snippet" in desc
    print("\nOK — Ejercicio 04 completado")
