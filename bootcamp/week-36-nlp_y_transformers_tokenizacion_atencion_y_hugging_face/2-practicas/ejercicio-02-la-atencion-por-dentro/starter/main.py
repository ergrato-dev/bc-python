"""Ejercicio 02 · La atención por dentro.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import math

import torch
import torch.nn.functional as F
from torch import nn
from transformers import AutoModel, AutoTokenizer

print("Ejercicio 02 · La atención por dentro")
torch.set_printoptions(precision=2, sci_mode=False)

# Cinco palabras con vectores de 2 números hechos a mano: el primero es "cuánto de
# limpieza", el segundo "cuánto de avería".
WORDS = ["filtro", "polvo", "sensor", "responde", "no"]
X = torch.tensor([[1.0, 0.1], [0.9, 0.2], [0.2, 0.8], [0.1, 1.0], [0.0, 0.3]])
print(f"{len(WORDS)} palabras, vectores de {X.shape[1]} números")


def show(weights: torch.Tensor, rows: list[str], columns: list[str]) -> None:
    """Una tabla de pesos: una fila por palabra que mira, una columna por palabra mirada."""
    print(" " * 9 + "".join(f"{c:>9}" for c in columns))
    for name, row in zip(rows, weights, strict=True):
        print(f"{name:>9}" + "".join(f"{v:9.2f}" for v in row.tolist()))


# ============================================
# PASO 1: Palabras parecidas, vectores parecidos
# ============================================
# Descomenta las siguientes líneas:
# El producto escalar mide cuánto apuntan dos vectores hacia el mismo lado.
# similarity = F.cosine_similarity(X.unsqueeze(1), X.unsqueeze(0), dim=2)
# show(similarity, WORDS, WORDS)
# Un nn.Embedding es una tabla de vectores que se aprenden, como cualquier peso. Empieza al
# azar: la semilla fija ese azar.
# torch.manual_seed(36)
# table = nn.Embedding(len(WORDS), 2)
# sensor = [round(v, 2) for v in table.weight[2].tolist()]
# print(f"nn.Embedding: {tuple(table.weight.shape)} · el vector de 'sensor': {sensor}")

# ============================================
# PASO 2: La atención a mano
# ============================================
# Descomenta las siguientes líneas:
# Cada palabra compara su vector con el de todas (X @ X.T), divide por la raíz del tamaño,
# y softmax convierte cada fila en pesos que suman 1.
# scores = X @ X.T / math.sqrt(X.shape[1])
# weights = scores.softmax(dim=1)
# show(weights, WORDS, WORDS)
# print(f"cada fila suma {[round(s, 2) for s in weights.sum(dim=1).tolist()]}")
# La salida de cada palabra es la media de todos los vectores, con esos pesos.
# mixed = weights @ X
# print(f"'no' antes: {X[4]} · después: {mixed[4]}")

# ============================================
# PASO 3: Consultas, claves y valores
# ============================================
# Descomenta las siguientes líneas:
# Tres capas lineales: la consulta (qué busco), la clave (qué ofrezco) y el valor (qué doy).
# torch.manual_seed(36)
# query, key, value = nn.Linear(2, 4), nn.Linear(2, 4), nn.Linear(2, 4)
# with torch.no_grad():
#     q, k, v = query(X), key(X), value(X)
#     by_hand = (q @ k.T / math.sqrt(4)).softmax(dim=1) @ v
#     fused = F.scaled_dot_product_attention(q, k, v)
# print(f"q, k, v: {tuple(q.shape)} · salida: {tuple(by_hand.shape)}")
# print(
#     f"¿a mano igual que scaled_dot_product_attention? {torch.allclose(by_hand, fused, atol=1e-6)}"
# )

# ============================================
# PASO 4: No mirar el relleno
# ============================================
# Descomenta las siguientes líneas:
# Un lote de dos notas: la segunda tiene 3 palabras y 2 de relleno al final.
# padding = torch.tensor([False, False, False, True, True])
# masked = scores.masked_fill(padding, float("-inf")).softmax(dim=1)
# show(masked[:3], WORDS[:3], WORDS[:3] + ["[PAD]", "[PAD]"])
# print(f"lo que reciben las dos de relleno: {masked[:, 3:].sum().item():.2f}")

# ============================================
# PASO 5: No mirar el futuro
# ============================================
# Descomenta las siguientes líneas:
# Un modelo que escribe texto solo puede mirar las palabras anteriores: máscara triangular.
# future = torch.ones(5, 5, dtype=torch.bool).triu(diagonal=1)
# causal = scores.masked_fill(future, float("-inf")).softmax(dim=1)
# show(causal, WORDS, WORDS)
# with torch.no_grad():
#     same = torch.allclose(
#         (q @ k.T / 2).masked_fill(future, float("-inf")).softmax(dim=1) @ v,
#         F.scaled_dot_product_attention(q, k, v, is_causal=True),
#         atol=1e-6,
#     )
# print(f"¿igual que is_causal=True? {same}")

# ============================================
# PASO 6: La atención no ve el orden
# ============================================
# Descomenta las siguientes líneas:
# Desordena las palabras: cada una recibe lo mismo que antes, solo cambia de sitio.
# order = torch.tensor([4, 3, 2, 1, 0])
# with torch.no_grad():
#     shuffled = F.scaled_dot_product_attention(q[order], k[order], v[order])
# print(f"¿mismas salidas, en otro orden? {torch.allclose(shuffled, fused[order], atol=1e-6)}")
# Por eso se suma a cada vector el de su posición. El original de 2017, con senos y cosenos:
# positions = torch.arange(5).unsqueeze(1)
# frequencies = 1 / 10000 ** (torch.arange(0, 2, 2) / 2)
# encoding = torch.cat([torch.sin(positions * frequencies), torch.cos(positions * frequencies)], 1)
# print(f"posiciones 0 a 4: {[[round(n, 2) for n in row] for row in encoding.tolist()]}")
# placed = X + encoding
# with torch.no_grad():
#     before = F.scaled_dot_product_attention(query(placed), key(placed), value(placed))
#     after = F.scaled_dot_product_attention(
#         query(X[order] + encoding), key(X[order] + encoding), value(X[order] + encoding)
#     )
# print(f"con posiciones, ¿mismas salidas en otro orden? {torch.allclose(after, before[order])}")

# ============================================
# PASO 7: Varias cabezas
# ============================================
# Descomenta las siguientes líneas:
# Cada cabeza hace su propia atención con una parte del vector, y luego se juntan.
# attention = nn.MultiheadAttention(embed_dim=16, num_heads=2, batch_first=True)
# batch = torch.randn(3, 5, 16)
# with torch.no_grad():
#     output, heads = attention(batch, batch, batch, average_attn_weights=False)
# parameters = sum(p.numel() for p in attention.parameters())
# print(f"entrada {tuple(batch.shape)} · salida {tuple(output.shape)} · pesos {tuple(heads.shape)}")
# print(f"parámetros: {parameters} = 4 x 16 x 16 (q, k, v y salida) + 4 x 16")

# ============================================
# PASO 8: La atención de un modelo de verdad
# ============================================
# Descomenta las siguientes líneas:
# Descarga el modelo multilingüe (unos 470 MB, una sola vez) y pide los pesos de atención.
# NAME, REVISION = (
#     "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
#     "e8f8c211226b894fcb81acc59f3b34ba3efd5f42",
# )
# tokenizer = AutoTokenizer.from_pretrained(NAME, revision=REVISION)
# model = AutoModel.from_pretrained(NAME, revision=REVISION, attn_implementation="eager").eval()
# inputs = tokenizer("El sensor de Norte no responde.", return_tensors="pt")
# with torch.no_grad():
#     attentions = model(**inputs, output_attentions=True).attentions
# tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
# print(f"{len(attentions)} capas · pesos de cada una: {tuple(attentions[0].shape)}")
# La capa 6, media de sus 12 cabezas: a qué piezas mira "▁responde".
# look = attentions[5][0].mean(dim=0)[tokens.index("▁responde")]


# def top(weights: torch.Tensor, count: int = 3) -> str:
#     best = weights.topk(count)
#     pairs = zip(best.values.tolist(), best.indices.tolist(), strict=True)
#     return ", ".join(f"{tokens[i]} {w:.2f}" for w, i in pairs)


# print(f"'▁responde' mira sobre todo a: {top(look)}")
# <s> y </s> recogen la atención que no va a ninguna parte. Sin ellas:
# words = look.clone()
# words[[0, -1]] = 0
# print(f"sin <s> ni </s>: {top(words)}")
