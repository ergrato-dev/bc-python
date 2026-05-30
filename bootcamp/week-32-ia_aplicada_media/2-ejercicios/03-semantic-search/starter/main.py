"""
Ejercicio 03: Búsqueda Semántica con Embeddings
===============================================
Construye un índice de assets y búscalos por similitud semántica.

Requisitos: pip install openai numpy
            export OPENAI_API_KEY=sk-...

Ejecutar: python main.py
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from openai import OpenAI
import numpy as np

client = OpenAI()


# ── Funciones base ────────────────────────────────────────────────────────────

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Genera el embedding de un texto."""
    # TODO: client.embeddings.create(model=model, input=text)
    # TODO: retornar response.data[0].embedding
    raise NotImplementedError


def get_embeddings_batch(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    """Genera embeddings de una lista de textos en una sola llamada."""
    # TODO: client.embeddings.create(model=model, input=texts)
    # TODO: retornar lista ordenada por item.index
    raise NotImplementedError


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calcula la similitud coseno entre dos vectores."""
    # TODO: np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb))
    # Manejar el caso de vectores de norma cero
    raise NotImplementedError


# ── Índice de búsqueda ────────────────────────────────────────────────────────

@dataclass
class AssetIndex:
    descriptions: list[str] = field(default_factory=list)
    embeddings: list[list[float]] = field(default_factory=list)

    def add_batch(self, texts: list[str]) -> None:
        """Agrega múltiples textos al índice con una sola llamada a la API."""
        # TODO: extender descriptions, obtener embeddings con get_embeddings_batch
        raise NotImplementedError

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        """
        Busca los textos más similares a query.
        Devuelve lista de (descripción, score) ordenada por score desc.
        """
        # TODO: obtener embedding del query
        # TODO: calcular cosine_similarity con cada embedding del índice
        # TODO: ordenar y devolver top_k
        raise NotImplementedError


# ── Mock para dry-run ─────────────────────────────────────────────────────────

MOCK_EMBEDDINGS: dict[str, list[float]] = {}  # Se llena en el main si dry_run


def _mock_embed(text: str) -> list[float]:
    """Genera un embedding ficticio basado en hashing del texto."""
    seed = sum(ord(c) for c in text) % 1000
    np.random.seed(seed)
    return np.random.randn(1536).tolist()


ASSETS = [
    "Spot publicitario de verano para cadena de supermercados. Escenas en playa y familia.",
    "Documental sobre glaciares de la Patagonia. Narración en off sobre cambio climático.",
    "Entrevista al director de arte de la película 'Luz del Sur'. Habla sobre diseño de producción.",
    "Cobertura del festival de jazz en Buenos Aires. Actuaciones en vivo y entrevistas.",
    "Tutorial de edición de video con DaVinci Resolve. Corrección de color avanzada.",
    "Spot institucional del Ministerio de Educación sobre lectura en familia.",
    "Resumen del campeonato de fútbol juvenil. Mejores goles y análisis técnico.",
    "Documental sobre artesanos de cerámica en Jujuy. Técnicas ancestrales.",
]


if __name__ == "__main__":
    dry_run = not os.getenv("OPENAI_API_KEY")

    index = AssetIndex()

    if dry_run:
        print("Modo dry-run — usando embeddings ficticios")
        index.descriptions = ASSETS
        index.embeddings = [_mock_embed(t) for t in ASSETS]
    else:
        index.add_batch(ASSETS)

    print("=== Búsqueda semántica ===")
    queries = [
        "video para el verano con familia",
        "naturaleza y medio ambiente",
        "música en vivo",
    ]
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
