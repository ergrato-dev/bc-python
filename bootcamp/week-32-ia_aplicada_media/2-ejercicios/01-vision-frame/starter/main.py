"""
Ejercicio 01: GPT-4o Vision — Análisis de Frame
================================================
Analiza una imagen con GPT-4o Vision y extrae metadata estructurada en JSON.

Requisitos: pip install openai
            export OPENAI_API_KEY=sk-...

Ejecutar: python main.py
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from openai import OpenAI

client = OpenAI()


def encode_image(path: Path) -> str:
    """Codifica una imagen en base64."""
    # TODO: leer los bytes de path y codificar en base64
    raise NotImplementedError


def analyze_frame(image_path: Path) -> dict[str, object]:
    """
    Envía el frame a GPT-4o Vision y devuelve un dict con:
    - description: str
    - topic: str
    - category: str (publicidad|documental|entrevista|evento|deportes|otro)
    - mood: str
    - suggested_tags: list[str]

    TODO:
    1. Codificar la imagen con encode_image()
    2. Construir el mensaje con content = [{"type": "text", ...}, {"type": "image_url", ...}]
    3. Llamar a client.chat.completions.create con model="gpt-4o",
       response_format={"type": "json_object"}
    4. Parsear y devolver el JSON
    """
    raise NotImplementedError


def analyze_frames_batch(image_paths: list[Path]) -> list[dict[str, object]]:
    """Analiza múltiples frames y devuelve una lista de resultados."""
    # TODO: llamar analyze_frame() para cada path
    raise NotImplementedError


# ── Modo dry-run para tests sin API key ───────────────────────────────────────

MOCK_RESULT: dict[str, object] = {
    "description": "Estudio de grabación profesional con pantalla verde y equipo de iluminación LED.",
    "topic": "producción audiovisual",
    "category": "institucional",
    "mood": "profesional",
    "suggested_tags": ["studio", "produccion", "video", "iluminacion", "chromakey"],
}


if __name__ == "__main__":
    import os
    dry_run = not os.getenv("OPENAI_API_KEY")

    if dry_run:
        print("Modo dry-run (sin OPENAI_API_KEY)")
        result = MOCK_RESULT
    else:
        test_image = Path("test_frame.jpg")
        if not test_image.exists():
            print("Crea test_frame.jpg o coloca una imagen JPG en el directorio")
            raise SystemExit(1)
        result = analyze_frame(test_image)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    assert "description" in result
    assert "suggested_tags" in result
    assert isinstance(result["suggested_tags"], list)
    print("\nOK — Ejercicio 01 completado")
