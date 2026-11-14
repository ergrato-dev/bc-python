"""Ejercicio 03 · Modelos preentrenados de Hugging Face.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import csv
from pathlib import Path

import torch
import torch.nn.functional as F
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from transformers import AutoModel, AutoModelForSequenceClassification, AutoTokenizer, pipeline

print("Ejercicio 03 · Modelos preentrenados")

# Las 300 notas de mantenimiento del Observatorio de ejemplo: etiqueta;tipo;texto.
with Path("notas.csv").open(encoding="utf-8") as file:
    rows = list(csv.DictReader(file, delimiter=";"))
texts, kinds = [row["texto"] for row in rows], [row["tipo"] for row in rows]
print(f"{len(rows)} notas · tipos: {sorted(set(kinds))}")

SPANISH = ("Recognai/bert-base-spanish-wwm-cased-xnli", "e44f774ea40ee8202311d9e5448263f176e04796")
MULTILINGUAL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "e8f8c211226b894fcb81acc59f3b34ba3efd5f42",
)
# Los nombres que lee el modelo: palabras con tildes, como en una frase.
LABELS = {"averia": "avería", "limpieza": "limpieza", "calibracion": "calibración"}

# ============================================
# PASO 1: Clasificar sin entrenar (zero-shot)
# ============================================
# Descomenta las siguientes líneas:
# Descarga el modelo en español (unos 440 MB, una sola vez).
# classifier = pipeline(
#     "zero-shot-classification", model=SPANISH[0], revision=SPANISH[1], device="cpu"
# )
# La frase con la que se entrenó este modelo (está en su ficha del Hub).
# TEMPLATE = "Este ejemplo es {}."
# for text in texts[:4]:
#     result = classifier(text, list(LABELS.values()), hypothesis_template=TEMPLATE)
#     print(f"{result['labels'][0]:>11} {result['scores'][0]:.2f} · {text}")

# ============================================
# PASO 2: ¿Cuánto acierta?
# ============================================
# Descomenta las siguientes líneas:
# for template in [TEMPLATE, "Esta nota trata de una {}."]:
#     results = classifier(texts[:60], list(LABELS.values()), hypothesis_template=template)
#     guesses = [result["labels"][0] for result in results]
#     hits = sum(guess == LABELS[kind] for guess, kind in zip(guesses, kinds, strict=False))
#     print(f"«{template}» · 60 notas, sin ver ni un ejemplo: acierta {hits / 60:.2f}")
#     for kind, name in LABELS.items():
#         print(f"  dice {name} {guesses.count(name)} veces; lo es {kinds[:60].count(kind)}")

# ============================================
# PASO 3: Lo que hace el pipeline por dentro
# ============================================
# Descomenta las siguientes líneas:
# Una pareja de frases: ¿la primera implica la segunda? El modelo da tres puntuaciones.
# tokenizer = AutoTokenizer.from_pretrained(SPANISH[0], revision=SPANISH[1])
# model = AutoModelForSequenceClassification.from_pretrained(SPANISH[0], revision=SPANISH[1])
# model.eval()
# print(f"salidas del modelo: {model.config.id2label}")
# for name in LABELS.values():
#     inputs = tokenizer(texts[0], TEMPLATE.format(name), return_tensors="pt")
#     with torch.no_grad():
#         logits = model(**inputs).logits[0]
#     probabilities = logits.softmax(dim=0)
#     print(
#         f"  «{TEMPLATE.format(name)}» · "
#         + " ".join(
#             f"{model.config.id2label[i]} {p:.2f}" for i, p in enumerate(probabilities.tolist())
#         )
#     )
# parameters = sum(p.numel() for p in model.parameters())
# print(f"{parameters:,} parámetros".replace(",", "."))

# ============================================
# PASO 4: Una frase, un vector (embeddings)
# ============================================
# Descomenta las siguientes líneas:
# encoder_tokenizer = AutoTokenizer.from_pretrained(MULTILINGUAL[0], revision=MULTILINGUAL[1])
# encoder = AutoModel.from_pretrained(MULTILINGUAL[0], revision=MULTILINGUAL[1]).eval()


# def embed(sentences: list[str]) -> torch.Tensor:
#     """Un vector por frase: la media de los vectores de sus piezas, sin el relleno."""
#     inputs = encoder_tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
#     with torch.no_grad():
#         pieces = encoder(**inputs).last_hidden_state
#     mask = inputs["attention_mask"].unsqueeze(-1).float()
#     return (pieces * mask).sum(dim=1) / mask.sum(dim=1)


# QUERY = "El equipo no da datos"
# OTHERS = [
#     "El sensor dejó de enviar lecturas",
#     "La estación no transmite mediciones",
#     "Se limpió el filtro lleno de polvo",
#     "Hoy hace sol en Norte",
# ]
# vectors = embed([QUERY, *OTHERS])
# print(f"vectores de {vectors.shape[1]} números")
# for sentence, score in zip(
#     OTHERS, F.cosine_similarity(vectors[:1], vectors[1:]).tolist(), strict=True
# ):
#     print(f"  {score:.2f} · {sentence}")

# ============================================
# PASO 5: Buscar por significado
# ============================================
# Descomenta las siguientes líneas:
# notes = embed(texts)
# for query in ["problema eléctrico", "suciedad en la entrada de aire"]:
#     scores = F.cosine_similarity(embed([query]), notes)
#     print(f"«{query}»:")
#     for index in scores.topk(3).indices.tolist():
#         print(f"  {scores[index]:.2f} · {texts[index]}")

# ============================================
# PASO 6: Pocas etiquetas: embeddings frente a TF-IDF
# ============================================
# Descomenta las siguientes líneas:
# Las 30 primeras notas para entrenar (10 de cada tipo), las 100 últimas para probar.
# train, test = texts[:30], texts[200:]
# Y notas que dicen lo mismo con palabras que no salen en las de entrenamiento.
# PARAPHRASES = [
#     ("averia", "Monitor muerto, ni prende"),
#     ("averia", "Sin corriente desde ayer"),
#     ("limpieza", "Barrimos mugre acumulada"),
#     ("limpieza", "Aspiramos suciedad"),
#     ("calibracion", "Corregimos el desvío del aparato"),
#     ("calibracion", "Afinamos la medición"),
# ]
# bag = TfidfVectorizer().fit(train)
# for name, features in [
#     ("tf-idf", bag.transform),
#     ("embeddings", lambda batch: embed(batch).numpy()),
# ]:
#     fitted = LogisticRegression(max_iter=1000).fit(features(train), kinds[:30])
#     accuracy = fitted.score(features(test), kinds[200:])
#     guesses = fitted.predict(features([text for _, text in PARAPHRASES]))
#     hits = sum(guess == kind for guess, (kind, _) in zip(guesses, PARAPHRASES, strict=True))
#     print(f"{name:>10} · 30 notas · prueba {accuracy:.2f} · con otras palabras {hits} de 6")
