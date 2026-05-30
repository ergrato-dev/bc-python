"""MetadataGenerator — genera título, descripción y capítulos con GPT."""
from __future__ import annotations

import json
from openai import OpenAI
from .config import AIConfig

client = OpenAI()

MOCK_TITLE = "Producción Audiovisual Profesional — Studio BC Argentina"
MOCK_DESC = {
    "snippet": "Descubre el proceso completo de producción audiovisual de Studio BC con más de 10 años de experiencia.",
    "full_description": "Studio BC es un estudio audiovisual líder en Argentina. Ofrecemos servicios completos desde preproducción hasta distribución digital.",
    "call_to_action": "Contactanos para tu próximo proyecto audiovisual.",
}
MOCK_CHAPTERS = [
    {"start_s": 0.0, "timestamp": "0:00", "title": "Introducción a Studio BC"},
    {"start_s": 4.2, "timestamp": "0:04", "title": "Experiencia y trayectoria"},
]


class MetadataGenerator:
    def __init__(self, config: AIConfig | None = None) -> None:
        self._cfg = config or AIConfig()

    def generate_title(self, description: str, tags: list[str] | None = None) -> str:
        """
        Genera un título SEO de máximo 70 caracteres.

        TODO:
        - Si dry_run: return MOCK_TITLE
        - Prompt con reglas de título SEO (max 70 chars, keyword al inicio)
        - model=cfg.text_model, max_tokens=80, temperature=0.4
        - Retornar resultado limpio (strip, strip de comillas)[:70]

        Referencia: ejercicio 04 — generate_title()
        """
        if self._cfg.dry_run:
            return MOCK_TITLE
        raise NotImplementedError

    def generate_description(self, description: str, transcript: str = "") -> dict[str, str]:
        """
        Genera snippet + full_description + call_to_action.

        TODO:
        - Si dry_run: return MOCK_DESC
        - Prompt que pide JSON con los tres campos
        - response_format={"type": "json_object"}, max_tokens=600

        Referencia: ejercicio 04 — generate_description()
        """
        if self._cfg.dry_run:
            return MOCK_DESC
        raise NotImplementedError

    def generate_chapters(self, segments: list[dict[str, object]]) -> list[dict[str, object]]:
        """
        Genera capítulos titulados desde segmentos Whisper.

        TODO:
        - Si dry_run: return MOCK_CHAPTERS
        - Agrupar segmentos en bloques de min_chapter_s segundos
        - Pedir a GPT títulos breves para cada bloque
        - Retornar [{start_s, timestamp, title}]

        Referencia: teoría 05 — generate_chapters_with_gpt()
        """
        if self._cfg.dry_run:
            return MOCK_CHAPTERS
        raise NotImplementedError

    def format_youtube_description(
        self,
        desc: dict[str, str],
        chapters: list[dict[str, object]],
    ) -> str:
        lines: list[str] = [str(desc.get("full_description", "")), ""]
        if chapters:
            lines.append("CAPÍTULOS:")
            for ch in chapters:
                lines.append(f"{ch['timestamp']} {ch['title']}")
            lines.append("")
        cta = str(desc.get("call_to_action", ""))
        if cta:
            lines.append(cta)
        return "\n".join(lines)
