"""Ejercicio 01 · Embeddings: del texto a vectores que se pueden comparar.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
El paso 5 usa el modelo multilingüe de la semana 36: si no lo tienes, lo descarga (470 MB).
"""

import numpy as np
import torch
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import normalize
from transformers import AutoModel, AutoTokenizer

MULTILINGUAL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "e8f8c211226b894fcb81acc59f3b34ba3efd5f42",
)

NOTES = [
    "El sensor de Norte dejó de enviar lecturas, queda fuera de servicio.",
    "El analizador de Sur no transmite datos desde ayer, hay que cambiar la pieza.",
    "La estación Este se apagó por un corte de energía.",
    "En Oeste se limpió el filtro lleno de polvo.",
    "En Centro se quitó el polvo acumulado en la entrada.",
    "El filtro de Sur estaba sucio y se lavó con agua.",
    "Se corrigió la deriva del cero en Norte.",
    "Se ajustó la ganancia del analizador de Este con el gas patrón.",
    "La calibración de Oeste dio un nuevo factor de escala.",
]
KINDS = ["averia"] * 3 + ["limpieza"] * 3 + ["calibracion"] * 3
QUERIES = {
    "el aparato no funciona": "averia",
    "se cortó la electricidad": "averia",
    "había suciedad en la toma de aire": "limpieza",
    "se puso a punto el instrumento con una referencia": "calibracion",
}

print("Ejercicio 01 · Embeddings")


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """El coseno del ángulo entre dos vectores: 1, misma dirección; 0, nada en común."""
    norms = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / norms) if norms else 0.0


# ============================================
# PASO 1: Contar palabras
# ============================================
# Descomenta las siguientes líneas:
# counter = CountVectorizer(strip_accents="unicode")
# counts = counter.fit_transform(NOTES[3:6]).toarray()
# print("vocabulario:", " ".join(counter.get_feature_names_out()))
# print(counts)
# print(f"coseno nota 1 y nota 2: {cosine(counts[0], counts[1]):.2f}")
# print(f"coseno nota 1 y nota 3: {cosine(counts[0], counts[2]):.2f}")

# ============================================
# PASO 2: TF-IDF, las palabras raras pesan más
# ============================================
# Descomenta las siguientes líneas:
# tfidf = TfidfVectorizer(strip_accents="unicode")
# weights = tfidf.fit_transform(NOTES).toarray()
# words = tfidf.get_feature_names_out()
# print(f"{len(NOTES)} notas · {len(words)} palabras distintas")
# first = sorted(zip(weights[3], words, strict=True), reverse=True)
# print(
#     "nota 4:",
#     " · ".join(f"{word} {weight:.2f}" for weight, word in first if weight > 0),
# )
# query = tfidf.transform(["se cortó la electricidad"]).toarray()[0]
# print("«se cortó la electricidad» comparte con las notas:", " ".join(words[query > 0]))

# ============================================
# PASO 3: LSA, de muchas palabras a pocos números
# ============================================
# Descomenta las siguientes líneas:
# lsa = TruncatedSVD(4, random_state=0)
# reduced = lsa.fit_transform(weights)
# print(f"de {weights.shape[1]} a {reduced.shape[1]} números por nota", end="")
# print(f" · conservan el {lsa.explained_variance_ratio_.sum():.0%} de la varianza")
# for i, j in [(3, 4), (3, 6)]:
#     print(
#         f"notas {i + 1} y {j + 1}: TF-IDF {cosine(weights[i], weights[j]):.2f}"
#         f" · LSA {cosine(reduced[i], reduced[j]):.2f}"
#     )

# ============================================
# PASO 4: Longitud 1, el coseno es un producto
# ============================================
# Descomenta las siguientes líneas:
# unit = normalize(reduced)
# print("longitudes:", np.round(np.linalg.norm(unit, axis=1), 3)[:3])
# a, b = unit[3], unit[6]
# print(f"producto {a @ b:.3f} · coseno {cosine(reduced[3], reduced[6]):.3f}")
# print(f"distancia de coseno {1 - a @ b:.3f} · euclídea² {np.sum((a - b) ** 2):.3f}")

# ============================================
# PASO 5: Un modelo preentrenado
# ============================================
# Descomenta las siguientes líneas:
# tokenizer = AutoTokenizer.from_pretrained(MULTILINGUAL[0], revision=MULTILINGUAL[1])
# encoder = AutoModel.from_pretrained(MULTILINGUAL[0], revision=MULTILINGUAL[1]).eval()


# def embed(sentences: list[str]) -> np.ndarray:
#     """Un vector por frase: la media de los vectores de sus piezas, sin el relleno, y longitud 1."""
#     inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
#     with torch.no_grad():
#         pieces = encoder(**inputs).last_hidden_state
#     mask = inputs["attention_mask"].unsqueeze(-1).float()
#     mean = (pieces * mask).sum(dim=1) / mask.sum(dim=1)
#     return normalize(mean.numpy())


# vectors = embed(NOTES)
# print(f"vectores de {vectors.shape[1]} números")
# pair = embed(["se cortó la electricidad", NOTES[2]])
# print(
#     f"«se cortó la electricidad» y la nota 3: TF-IDF {cosine(query, weights[2]):.2f}",
#     end="",
# )
# print(f" · modelo {pair[0] @ pair[1]:.2f}")

# ============================================
# PASO 6: Buscar con los dos
# ============================================
# Descomenta las siguientes líneas:
# right = {"TF-IDF": 0, "modelo": 0}
# for text, kind in QUERIES.items():
#     lexical = tfidf.transform([text]).toarray()[0]
#     by_words = int(np.argmax([cosine(lexical, row) for row in weights]))
#     by_meaning = int(np.argmax(vectors @ embed([text])[0]))
#     right["TF-IDF"] += KINDS[by_words] == kind
#     right["modelo"] += KINDS[by_meaning] == kind
#     print(f"«{text}»")
#     print(f"   TF-IDF → {NOTES[by_words]}")
#     print(f"   modelo → {NOTES[by_meaning]}")
# print(
#     " · ".join(
#         f"{name} acierta el tipo {hits} de {len(QUERIES)}"
#         for name, hits in right.items()
#     )
# )
