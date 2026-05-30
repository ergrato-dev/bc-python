"""AutoTagger — genera tags y categoría con GPT."""
from __future__ import annotations

import json
from openai import OpenAI
from .config import AIConfig

client = OpenAI()

STUDIO_CATEGORIES = [
    "publicidad", "documental", "entrevista", "cobertura-evento",
    "deportes", "educativo", "institucional", "videoclip", "otro",
]

MOCK_TAGS = ["studio-bc", "produccion-audiovisual", "video-profesional", "post-produccion", "argentina"]
MOCK_CATEGORY = "institucional"


class AutoTagger:
    def __init__(self, config: AIConfig | None = None) -> None:
        self._cfg = config or AIConfig()

    def generate_tags(self, description: str, transcript: str = "") -> list[str]:
        """
        Genera tags SEO para el asset.

        TODO:
        - Si dry_run: return MOCK_TAGS
        - Combinar descripción + transcript[:300] como contexto
        - Prompt que pide JSON {"tags": [...]} con reglas SEO
        - model=cfg.text_model, response_format=json_object, max_tokens=200
        - Retornar result.get("tags", [])[:cfg.max_tags]

        Referencia: ejercicio 04 — generate_tags()
        """
        if self._cfg.dry_run:
            return MOCK_TAGS
        raise NotImplementedError

    def classify(self, description: str) -> str:
        """
        Clasifica el asset en una de las categorías de STUDIO_CATEGORIES.

        TODO:
        - Si dry_run: return MOCK_CATEGORY
        - Prompt que muestra las categorías y pide la más apropiada
        - model=cfg.text_model, max_tokens=20, temperature=0.0
        - Retornar resultado limpio o "otro" si no coincide

        Referencia: teoría 04 — classify_category()
        """
        if self._cfg.dry_run:
            return MOCK_CATEGORY
        raise NotImplementedError
