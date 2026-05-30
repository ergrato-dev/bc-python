# Generación Automática de Metadata

## 1. Pipeline de Metadata Completo

Para un asset de video, la metadata SEO típicamente incluye:

```
título       → max 60-70 caracteres, keyword al inicio
descripción  → 150-300 caracteres (snippet) + detallada
tags         → 10-15 palabras clave
capítulos    → timestamps + título (solo YouTube/Vimeo)
transcripción → texto completo con timestamps
```

---

## 2. Generar Título SEO

```python
import json
from openai import OpenAI

client = OpenAI()


def generate_title(description: str, category: str = "", tags: list[str] | None = None) -> str:
    context = description
    if category:
        context += f"\nCategoría: {category}"
    if tags:
        context += f"\nTags principales: {', '.join(tags[:5])}"

    prompt = f"""Genera un título SEO para un video con este contexto:
{context}

Reglas:
- Máximo 70 caracteres
- Incluye la keyword principal al inicio
- Atractivo y descriptivo, no clickbait
- En español
- Sin comillas ni caracteres especiales

Devuelve SOLO el título (sin JSON, sin markdown):"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.4,
    )
    return (response.choices[0].message.content or "").strip().strip('"')
```

---

## 3. Generar Descripción SEO

```python
def generate_description(
    description: str,
    transcript: str = "",
    tags: list[str] | None = None,
    include_snippet: bool = True,
) -> dict[str, str]:
    context_parts = [f"Contenido: {description}"]
    if transcript:
        context_parts.append(f"Transcripción (primeros 500 chars): {transcript[:500]}")
    if tags:
        context_parts.append(f"Keywords: {', '.join(tags[:8])}")

    prompt = f"""Genera metadata de descripción SEO para este video:
{chr(10).join(context_parts)}

Devuelve SOLO JSON (sin markdown):
{{
  "snippet": "descripción corta de 150-160 caracteres para metadescripción",
  "full_description": "descripción completa de 200-400 palabras para plataforma, con keywords naturalmente integradas",
  "call_to_action": "frase de cierre breve (ej: Suscríbete para más contenido)"
}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=600,
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content or "{}")
```

---

## 4. Generar Capítulos desde Transcripción

```python
def generate_chapters_with_gpt(
    segments: list[dict[str, object]],
    min_chapter_s: float = 60.0,
) -> list[dict[str, object]]:
    """Usa GPT para nombrar capítulos agrupados desde segmentos Whisper."""
    # Agrupar segmentos en bloques de al menos min_chapter_s
    groups: list[dict[str, object]] = []
    current_start = float(str(segments[0]["start"])) if segments else 0.0
    current_texts: list[str] = []

    for seg in segments:
        current_texts.append(str(seg["text"]))
        if float(str(seg["end"])) - current_start >= min_chapter_s:
            groups.append({
                "start_s": current_start,
                "text": " ".join(current_texts),
            })
            current_start = float(str(seg["end"]))
            current_texts = []

    if current_texts:
        groups.append({"start_s": current_start, "text": " ".join(current_texts)})

    if not groups:
        return []

    # Pedir títulos en batch
    texts_for_gpt = [str(g["text"])[:300] for g in groups]
    prompt = f"""Para cada sección del siguiente video, genera un título de capítulo corto (máximo 5 palabras):

{chr(10).join(f"{i+1}. {t}" for i, t in enumerate(texts_for_gpt))}

Devuelve SOLO JSON (sin markdown):
{{"titles": ["título 1", "título 2", ...]}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=200,
    )
    titles_data = json.loads(response.choices[0].message.content or '{"titles": []}')
    titles = titles_data.get("titles", [])

    return [
        {
            "start_s": float(str(g["start_s"])),
            "timestamp": _fmt_mm_ss(float(str(g["start_s"]))),
            "title": titles[i] if i < len(titles) else f"Sección {i+1}",
        }
        for i, g in enumerate(groups)
    ]


def _fmt_mm_ss(s: float) -> str:
    return f"{int(s // 60)}:{int(s % 60):02d}"
```

---

## 5. Metadata Completa en un Solo Objeto

```python
from dataclasses import dataclass, field


@dataclass
class AssetMetadata:
    title: str = ""
    snippet: str = ""
    full_description: str = ""
    call_to_action: str = ""
    tags: list[str] = field(default_factory=list)
    category: str = ""
    transcription: str = ""
    chapters: list[dict[str, object]] = field(default_factory=list)
    language: str = "es"

    def to_youtube_description(self) -> str:
        lines: list[str] = [self.full_description, ""]
        if self.chapters:
            lines.append("CAPÍTULOS:")
            for ch in self.chapters:
                lines.append(f"{ch['timestamp']} {ch['title']}")
            lines.append("")
        if self.call_to_action:
            lines.append(self.call_to_action)
        return "\n".join(lines)

    def to_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "snippet": self.snippet,
            "full_description": self.full_description,
            "tags": self.tags,
            "category": self.category,
            "transcription": self.transcription,
            "chapters": self.chapters,
            "language": self.language,
        }
```

---

## 6. Función Principal `analyze_asset`

```python
def analyze_asset(
    description: str,
    transcript_data: dict[str, object] | None = None,
) -> AssetMetadata:
    transcription = str(transcript_data.get("text", "")) if transcript_data else ""
    segments = list(transcript_data.get("segments", [])) if transcript_data else []  # type: ignore[arg-type]

    tags = generate_tags(f"{description} {transcription[:300]}")
    category = classify_category(description)
    title = generate_title(description, category, tags)
    desc_data = generate_description(description, transcription, tags)
    chapters = generate_chapters_with_gpt(segments) if segments else []

    return AssetMetadata(
        title=title,
        snippet=str(desc_data.get("snippet", "")),
        full_description=str(desc_data.get("full_description", "")),
        call_to_action=str(desc_data.get("call_to_action", "")),
        tags=tags,
        category=category,
        transcription=transcription,
        chapters=chapters,
        language=str(transcript_data.get("language", "es")) if transcript_data else "es",
    )
```

---

## Resumen

| Artefacto | Función | Modelo |
|-----------|---------|--------|
| Título SEO | `generate_title()` | `gpt-4o-mini` |
| Descripción | `generate_description()` | `gpt-4o-mini` |
| Tags | `generate_tags()` | `gpt-4o-mini` |
| Categoría | `classify_category()` | `gpt-4o-mini` |
| Capítulos | `generate_chapters_with_gpt()` | `gpt-4o-mini` |
| Análisis visual | `analyze_image_structured()` | `gpt-4o` |
| Transcripción | Whisper API | `whisper-1` |
