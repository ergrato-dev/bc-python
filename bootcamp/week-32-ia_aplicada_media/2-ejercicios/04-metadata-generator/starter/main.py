"""
Ejercicio 04: Generación Automática de Metadata
================================================
Genera título SEO, descripción, tags y capítulos para un asset de video
a partir de su descripción visual y transcripción.

Requisitos: pip install openai
            export OPENAI_API_KEY=sk-...

Ejecutar: python main.py
"""
from __future__ import annotations

import json
import os
from openai import OpenAI

client = OpenAI()


def generate_tags(description: str, max_tags: int = 10) -> list[str]:
    """
    Genera tags SEO para el asset.

    TODO:
    prompt = f"Genera {max_tags} tags SEO para: {description}\\n
               Devuelve SOLO JSON: {{\"tags\": [\"tag1\", ...]}}"
    client.chat.completions.create(model="gpt-4o-mini", response_format=json_object, ...)
    Retornar result.get("tags", [])[:max_tags]
    """
    raise NotImplementedError


def generate_title(description: str, tags: list[str] | None = None) -> str:
    """
    Genera un título SEO (máx 70 chars).

    TODO: prompt con reglas de título SEO, max_tokens=100, temperature=0.4
    Limpiar la respuesta de comillas y markdown
    """
    raise NotImplementedError


def generate_description(description: str, transcript: str = "") -> dict[str, str]:
    """
    Genera snippet (150 chars) y descripción completa (300 palabras).

    TODO: prompt con ambas en un solo JSON
    response_format={"type": "json_object"}
    Retornar {"snippet": ..., "full_description": ...}
    """
    raise NotImplementedError


def format_chapters_for_youtube(chapters: list[dict[str, object]]) -> str:
    """
    Formatea capítulos para descripción de YouTube.
    Ejemplo: "0:00 Introducción\n1:30 Proceso de grabación"
    """
    # TODO: iterar chapters y construir "timestamp title" por línea
    raise NotImplementedError


# ── Mock para dry-run ─────────────────────────────────────────────────────────

MOCK_TAGS = ["studio-bc", "produccion-audiovisual", "post-produccion", "video-profesional", "estudio"]
MOCK_TITLE = "Producción Audiovisual Profesional en Studio BC — Proceso Completo"
MOCK_DESC = {
    "snippet": "Descubre el proceso completo de producción audiovisual de Studio BC, desde la preproducción hasta la entrega final.",
    "full_description": "Studio BC es un estudio de producción audiovisual que combina tecnología de punta con talento creativo...",
}
MOCK_CHAPTERS = [
    {"timestamp": "0:00", "title": "Introducción"},
    {"timestamp": "1:30", "title": "Proceso de grabación"},
    {"timestamp": "4:00", "title": "Post-producción"},
]

SAMPLE_DESCRIPTION = "Video institucional de Studio BC mostrando el proceso completo de producción audiovisual."
SAMPLE_TRANSCRIPT = "Bienvenidos a Studio BC. Somos un estudio de producción audiovisual con más de 10 años de experiencia."


if __name__ == "__main__":
    dry_run = not os.getenv("OPENAI_API_KEY")

    if dry_run:
        print("Modo dry-run")
        tags = MOCK_TAGS
        title = MOCK_TITLE
        desc = MOCK_DESC
        chapters_fmt = format_chapters_for_youtube(MOCK_CHAPTERS) if not dry_run else "0:00 Introducción\n1:30 Proceso"
    else:
        tags = generate_tags(SAMPLE_DESCRIPTION)
        title = generate_title(SAMPLE_DESCRIPTION, tags)
        desc = generate_description(SAMPLE_DESCRIPTION, SAMPLE_TRANSCRIPT)
        chapters_fmt = format_chapters_for_youtube(MOCK_CHAPTERS)

    print(f"Título: {title}")
    print(f"Tags ({len(tags)}): {tags}")
    print(f"Snippet: {desc.get('snippet', '')[:100]}...")
    print(f"Capítulos:\n{chapters_fmt}")

    assert len(title) <= 70
    assert len(tags) > 0
    assert "snippet" in desc
    print("\nOK — Ejercicio 04 completado")
