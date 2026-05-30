"""
Ejercicio 01: GPT-4o Vision — SOLUCIÓN
=======================================
"""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path

from openai import OpenAI

client = OpenAI()


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def analyze_frame(image_path: Path) -> dict[str, object]:
    b64 = encode_image(image_path)
    ext = image_path.suffix.lower().lstrip(".")
    mime = f"image/{ext}" if ext in {"jpg", "jpeg", "png", "webp"} else "image/jpeg"

    prompt = """Analiza este frame de video y responde SOLO con JSON válido (sin markdown):
{
  "description": "descripción detallada del contenido visual",
  "topic": "tema principal",
  "category": "una de: publicidad, documental, entrevista, evento, deportes, institucional, otro",
  "mood": "tono emocional: profesional, alegre, dramático, neutral, etc.",
  "suggested_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ],
        }],
        max_tokens=500,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content or "{}")


def analyze_frames_batch(image_paths: list[Path]) -> list[dict[str, object]]:
    return [analyze_frame(p) for p in image_paths]


MOCK_RESULT: dict[str, object] = {
    "description": "Estudio de grabación profesional con pantalla verde y equipo de iluminación LED.",
    "topic": "producción audiovisual",
    "category": "institucional",
    "mood": "profesional",
    "suggested_tags": ["studio", "produccion", "video", "iluminacion", "chromakey"],
}


if __name__ == "__main__":
    dry_run = not os.getenv("OPENAI_API_KEY")

    if dry_run:
        print("Modo dry-run")
        result = MOCK_RESULT
    else:
        test_image = Path("test_frame.jpg")
        if not test_image.exists():
            print("Crea test_frame.jpg")
            raise SystemExit(1)
        result = analyze_frame(test_image)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    assert "description" in result
    assert isinstance(result["suggested_tags"], list)
    print("\nOK — Ejercicio 01 completado")
