# Auto-Tagging y Clasificación

## 1. Tagging con Prompting Directo

La forma más simple: pedir tags a GPT con el contexto del asset.

```python
import json
from openai import OpenAI

client = OpenAI()


def generate_tags(description: str, max_tags: int = 10) -> list[str]:
    prompt = f"""Genera tags SEO para un video con esta descripción:

{description}

Devuelve SOLO un JSON con esta estructura (sin markdown):
{{"tags": ["tag1", "tag2", ...]}}

Reglas:
- Máximo {max_tags} tags
- Solo minúsculas, sin tildes, sin espacios (usar guiones)
- Ordenados de mayor a menor relevancia
- Incluir tags en español e inglés si aplica"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=300,
        temperature=0.2,
    )
    result = json.loads(response.choices[0].message.content or "{}")
    return result.get("tags", [])[:max_tags]
```

---

## 2. Clasificación con Taxonomía Fija

Cuando hay una lista definida de categorías:

```python
STUDIO_CATEGORIES = [
    "publicidad",
    "documental",
    "entretenimiento",
    "noticias",
    "deportes",
    "educativo",
    "institucional",
    "videoclip",
    "cobertura-evento",
]


def classify_category(description: str) -> str:
    categories_str = "\n".join(f"- {c}" for c in STUDIO_CATEGORIES)
    prompt = f"""Clasifica este video en UNA de las siguientes categorías:

{categories_str}

Descripción del video:
{description}

Responde SOLO con el nombre exacto de la categoría (sin markdown, sin explicación)."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20,
        temperature=0.0,
    )
    result = (response.choices[0].message.content or "").strip().lower()
    return result if result in STUDIO_CATEGORIES else "entretenimiento"
```

---

## 3. Clasificación con Embeddings

Para clasificaciones frecuentes y sin llamadas extra a la API:

```python
import numpy as np


def cosine_similarity(a: list[float], b: list[float]) -> float:
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb)))


class EmbeddingClassifier:
    """Clasifica textos usando similitud con ejemplos precalculados."""

    def __init__(self) -> None:
        from openai import OpenAI
        self._client = OpenAI()
        self._labels: list[str] = []
        self._embeddings: list[list[float]] = []

    def add_label(self, label: str, examples: list[str]) -> None:
        """Agrega una categoría con varios ejemplos descriptivos."""
        embs = self._embed_batch(examples)
        # Embedding representativo = promedio de los ejemplos
        avg = (np.mean([np.array(e) for e in embs], axis=0)).tolist()
        self._labels.append(label)
        self._embeddings.append(avg)

    def predict(self, text: str) -> tuple[str, float]:
        """Devuelve (label, confidence)."""
        query_emb = self._embed(text)
        scores = [cosine_similarity(query_emb, emb) for emb in self._embeddings]
        best_idx = int(np.argmax(scores))
        return self._labels[best_idx], scores[best_idx]

    def _embed(self, text: str) -> list[float]:
        resp = self._client.embeddings.create(model="text-embedding-3-small", input=text)
        return resp.data[0].embedding

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        resp = self._client.embeddings.create(model="text-embedding-3-small", input=texts)
        return [item.embedding for item in sorted(resp.data, key=lambda x: x.index)]


# Uso
classifier = EmbeddingClassifier()
classifier.add_label("publicidad", [
    "spot publicitario de producto",
    "anuncio de televisión para marca comercial",
    "campaña de marketing audiovisual",
])
classifier.add_label("documental", [
    "documental sobre naturaleza o historia",
    "reportaje periodístico largo formato",
    "investigación periodística audiovisual",
])

label, confidence = classifier.predict("Campaña de verano para marca de ropa")
# → ("publicidad", 0.87)
```

---

## 4. Few-Shot Prompting para Tagging Preciso

Incluir ejemplos en el prompt mejora la calidad:

```python
FEW_SHOT_EXAMPLES = """
Descripción: "Spot de 30 segundos para lanzamiento de nuevo modelo de auto. Escenas en ruta y ciudad."
Tags: ["publicidad", "automocion", "spot-30s", "lanzamiento-producto", "urban-driving", "commercial"]

Descripción: "Entrevista al chef Juan García sobre gastronomía patagónica. 45 minutos de duración."
Tags: ["entrevista", "gastronomia", "chef", "patagonia", "cocina-regional", "formato-largo"]
"""


def generate_tags_few_shot(description: str) -> list[str]:
    prompt = f"""Genera tags SEO para videos audiovisuales. Usa estos ejemplos como guía:

{FEW_SHOT_EXAMPLES}

Descripción: "{description}"
Tags (devuelve SOLO el JSON {{"tags": [...]}} sin markdown):"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=200,
        temperature=0.1,
    )
    result = json.loads(response.choices[0].message.content or "{}")
    return result.get("tags", [])
```

---

## 5. Pipeline de Tagging Completo

```python
def tag_asset(
    description: str,
    transcript: str = "",
    frames_analysis: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    # Consolidar contexto
    context_parts = [f"Descripción visual: {description}"]
    if transcript:
        context_parts.append(f"Transcripción: {transcript[:500]}")
    if frames_analysis:
        topics = [str(f.get("topic", "")) for f in frames_analysis if f.get("topic")]
        context_parts.append(f"Temas visuales: {', '.join(set(topics))}")

    context = "\n".join(context_parts)

    return {
        "tags": generate_tags_few_shot(context),
        "category": classify_category(context),
    }
```

---

## Resumen

| Técnica | Cuándo |
|---------|--------|
| Prompt directo | Tagging flexible con contexto libre |
| Taxonomía fija + GPT | Clasificación en categorías predefinidas |
| Embeddings + coseno | Clasificación sin llamada extra a la API |
| Few-shot | Mejorar precisión con 2-3 ejemplos en el prompt |
