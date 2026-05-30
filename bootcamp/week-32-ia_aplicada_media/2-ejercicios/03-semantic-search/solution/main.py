"""
Ejercicio 03: Búsqueda Semántica con Embeddings — SOLUCIÓN
==========================================================
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

import numpy as np
from openai import OpenAI

client = OpenAI()


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding


def get_embeddings_batch(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    va, vb = np.array(a), np.array(b)
    norm_a, norm_b = np.linalg.norm(va), np.linalg.norm(vb)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(va, vb) / (norm_a * norm_b))


@dataclass
class AssetIndex:
    descriptions: list[str] = field(default_factory=list)
    embeddings: list[list[float]] = field(default_factory=list)

    def add_batch(self, texts: list[str]) -> None:
        self.descriptions.extend(texts)
        self.embeddings.extend(get_embeddings_batch(texts))

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        if not self.embeddings:
            return []
        query_emb = get_embedding(query)
        scores = [
            (desc, cosine_similarity(query_emb, emb))
            for desc, emb in zip(self.descriptions, self.embeddings)
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]


def _mock_embed(text: str) -> list[float]:
    seed = sum(ord(c) for c in text) % 1000
    np.random.seed(seed)
    return np.random.randn(1536).tolist()


ASSETS = [
    "Spot publicitario de verano para cadena de supermercados. Escenas en playa y familia.",
    "Documental sobre glaciares de la Patagonia. Narración sobre cambio climático.",
    "Entrevista al director de arte de la película 'Luz del Sur'.",
    "Cobertura del festival de jazz en Buenos Aires. Actuaciones en vivo.",
    "Tutorial de edición de video con DaVinci Resolve. Corrección de color.",
    "Spot institucional del Ministerio de Educación sobre lectura en familia.",
    "Resumen del campeonato de fútbol juvenil. Mejores goles.",
    "Documental sobre artesanos de cerámica en Jujuy. Técnicas ancestrales.",
]


if __name__ == "__main__":
    dry_run = not os.getenv("OPENAI_API_KEY")

    index = AssetIndex()
    if dry_run:
        print("Modo dry-run")
        index.descriptions = ASSETS
        index.embeddings = [_mock_embed(t) for t in ASSETS]
    else:
        index.add_batch(ASSETS)

    queries = ["video para el verano con familia", "naturaleza y medio ambiente", "música en vivo"]
    for query in queries:
        print(f"\nQuery: '{query}'")
        if dry_run:
            q_emb = _mock_embed(query)
            results = sorted(
                [(d, cosine_similarity(q_emb, e)) for d, e in zip(index.descriptions, index.embeddings)],
                key=lambda x: x[1], reverse=True,
            )[:3]
        else:
            results = index.search(query, top_k=3)
        for desc, score in results:
            print(f"  {score:.3f} — {desc[:60]}")

    print("\nOK — Ejercicio 03 completado")
