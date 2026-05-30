# Embeddings y Búsqueda Semántica

## 1. ¿Qué es un Embedding?

Un **embedding** es una representación vectorial de un texto (o imagen). Textos semánticamente similares tienen vectores cercanos en el espacio vectorial, aunque usen palabras diferentes.

```
"spot publicitario de verano"  → [0.02, -0.15, 0.83, ...]  (1536 dimensiones)
"anuncio para la época estival" → [0.03, -0.14, 0.81, ...]  (similar → cercano)
"receta de pollo al horno"     → [-0.55, 0.22, -0.19, ...]  (diferente → lejano)
```

---

## 2. Generar Embeddings con OpenAI

```python
from openai import OpenAI
import numpy as np

client = OpenAI()


def embed(text: str, model: str = "text-embedding-3-small") -> list[float]:
    response = client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding


def embed_batch(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    """Más eficiente que llamar embed() en loop — una sola llamada a la API."""
    response = client.embeddings.create(
        model=model,
        input=texts,
    )
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
```

---

## 3. Similitud Coseno

```python
import numpy as np


def cosine_similarity(a: list[float], b: list[float]) -> float:
    va = np.array(a)
    vb = np.array(b)
    norm_a = np.linalg.norm(va)
    norm_b = np.linalg.norm(vb)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(va, vb) / (norm_a * norm_b))


def find_most_similar(
    query: str,
    candidates: list[str],
    top_k: int = 3,
) -> list[tuple[str, float]]:
    query_embedding = embed(query)
    candidate_embeddings = embed_batch(candidates)

    scores = [
        (text, cosine_similarity(query_embedding, emb))
        for text, emb in zip(candidates, candidate_embeddings)
    ]
    return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
```

Resultado: coseno en `[-1, 1]`. Valores > 0.8 = muy similar; < 0.5 = diferente.

---

## 4. Índice de Búsqueda en Memoria

Para buscar sobre una colección fija de assets:

```python
from dataclasses import dataclass, field


@dataclass
class AssetIndex:
    assets: list[str] = field(default_factory=list)
    embeddings: list[list[float]] = field(default_factory=list)

    def add(self, text: str) -> None:
        self.assets.append(text)
        self.embeddings.append(embed(text))

    def add_batch(self, texts: list[str]) -> None:
        self.assets.extend(texts)
        self.embeddings.extend(embed_batch(texts))

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        if not self.embeddings:
            return []
        query_emb = embed(query)
        scores = [
            (asset, cosine_similarity(query_emb, emb))
            for asset, emb in zip(self.assets, self.embeddings)
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

    def save(self, path: "Path") -> None:
        import json
        path.write_text(json.dumps({
            "assets": self.assets,
            "embeddings": self.embeddings,
        }))

    @classmethod
    def load(cls, path: "Path") -> "AssetIndex":
        import json
        data = json.loads(path.read_text())
        idx = cls()
        idx.assets = data["assets"]
        idx.embeddings = data["embeddings"]
        return idx
```

---

## 5. Uso Práctico — Búsqueda de Assets

```python
from pathlib import Path

# Construir índice de las descripciones de los assets
index = AssetIndex()
index.add_batch([
    "Spot publicitario de verano para Canal 9 con escenas de playa",
    "Documental sobre producción artesanal de queso en la Patagonia",
    "Entrevista al director de fotografía sobre técnicas de iluminación",
    "Cobertura del festival de cine independiente 2024",
    "Tutorial de edición de video para redes sociales",
])
index.save(Path("asset_index.json"))

# Buscar
results = index.search("video de playa para verano", top_k=2)
for asset, score in results:
    print(f"{score:.3f} — {asset}")
# 0.891 — Spot publicitario de verano para Canal 9 con escenas de playa
# 0.623 — Tutorial de edición de video para redes sociales
```

---

## 6. Modelos de Embedding Disponibles

| Modelo | Dimensiones | Costo | Uso recomendado |
|--------|-------------|-------|-----------------|
| `text-embedding-3-small` | 1536 | $0.02/1M tokens | Búsqueda y clasificación general |
| `text-embedding-3-large` | 3072 | $0.13/1M tokens | Máxima precisión |
| `text-embedding-ada-002` | 1536 | $0.10/1M tokens | Legacy — usar 3-small |

`text-embedding-3-small` tiene mejor performance que `ada-002` a menor costo.

---

## Resumen

| Concepto | Implementación |
|----------|----------------|
| Generar embedding | `client.embeddings.create(model=..., input=texto)` |
| Batch eficiente | `input=["texto1", "texto2"]` en una sola llamada |
| Similitud | `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))` |
| Índice en memoria | Lista de embeddings + búsqueda por coseno |
| Persistir índice | JSON con `assets` + `embeddings` |
