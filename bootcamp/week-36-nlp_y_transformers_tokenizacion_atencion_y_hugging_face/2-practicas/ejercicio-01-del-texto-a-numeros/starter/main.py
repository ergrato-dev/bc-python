"""Ejercicio 01 · Del texto a números: palabras, TF-IDF y subpalabras.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import json
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from tokenizers import Tokenizer, normalizers, pre_tokenizers
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from transformers import AutoTokenizer

print("Ejercicio 01 · Del texto a números")

# Notas de mantenimiento de estaciones de calidad del aire.
NOTES = [
    "El sensor de Norte no responde desde la madrugada.",
    "En Sur se limpió el filtro lleno de polvo.",
    "El analizador de Centro se recalibró con gas de referencia.",
    "El sensor de Este dejó de enviar lecturas, se pidió un repuesto.",
    "En Oeste se cambió el filtro sucio, sin avería.",
    "El equipo de Norte tenía deriva y se corrigió el cero.",
    "La estación Sur perdió la conexión con el servidor.",
    "En Centro se quitó el polvo de la toma de aire.",
    "El sensor de Oeste marcaba valores altos y se ajustó con el patrón.",
    "El equipo de Este se apagó por un corte de energía.",
]
print(f"{len(NOTES)} notas · la primera: {NOTES[0]!r}")

# Los dos modelos de Hugging Face de la semana, cada uno fijado a una versión (revision):
# la misma descarga hoy y dentro de un año.
SPANISH = ("Recognai/bert-base-spanish-wwm-cased-xnli", "e44f774ea40ee8202311d9e5448263f176e04796")
MULTILINGUAL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "e8f8c211226b894fcb81acc59f3b34ba3efd5f42",
)

# ============================================
# PASO 1: Una bolsa de palabras a mano
# ============================================
# Descomenta las siguientes líneas:
# Cada nota, en minúsculas y partida por espacios: cuántas veces sale cada palabra.
# bags = [Counter(note.lower().replace(".", "").replace(",", "").split()) for note in NOTES]
# vocabulary = sorted(set().union(*bags))
# print(f"vocabulario: {len(vocabulary)} palabras · {vocabulary[:6]}")
# Una nota es un vector: un número por palabra del vocabulario, casi todos 0.
# vector = [bags[0][word] for word in vocabulary]
# print(f"nota 1: {len(vector)} números, {sum(1 for v in vector if v)} distintos de 0")
# print(f"las palabras de la nota 1: {dict(bags[0])}")

# ============================================
# PASO 2: TF-IDF con scikit-learn
# ============================================
# Descomenta las siguientes líneas:
# TF-IDF: cuántas veces sale una palabra en la nota, por lo rara que es en todas las notas.
# tfidf = TfidfVectorizer()
# matrix = tfidf.fit_transform(NOTES)
# print(f"matriz: {matrix.shape[0]} notas x {matrix.shape[1]} palabras")
# words = tfidf.get_feature_names_out()
# row = matrix[1].toarray()[0]
# top = sorted(zip(row, words, strict=True), reverse=True)[:4]
# print("nota 2, las palabras que más pesan:", ", ".join(f"{w} {v:.2f}" for v, w in top))
# print(f"'de' pesa {row[list(words).index('de')]:.2f}: sale en casi todas las notas")

# ============================================
# PASO 3: Lo que una bolsa no ve
# ============================================
# Descomenta las siguientes líneas:
# El orden no existe en una bolsa: estas dos notas dicen lo contrario y son el mismo vector.
# pair = ["se limpió el filtro, no el sensor", "se limpió el sensor, no el filtro"]
# counts = CountVectorizer().fit(NOTES + pair).transform(pair).toarray()
# print(f"¿mismo vector? {bool((counts[0] == counts[1]).all())}")
# Una palabra que no estaba al ajustar no existe: "recalibrado" no es "recalibró".
# seen = CountVectorizer().fit(NOTES)
# print(f"palabras conocidas en 'recalibrado ayer': {seen.transform(['recalibrado ayer']).sum()}")

# ============================================
# PASO 4: Subpalabras con BPE
# ============================================
# Descomenta las siguientes líneas:


# def bpe(size: int) -> Tokenizer:
#     """Un tokenizador BPE entrenado con las notas, sin tildes ni mayúsculas."""
#     model = Tokenizer(BPE(unk_token="[UNK]"))
#     model.normalizer = normalizers.Sequence(
#         [normalizers.NFD(), normalizers.StripAccents(), normalizers.Lowercase()]
#     )
#     model.pre_tokenizer = pre_tokenizers.Whitespace()
#     model.train_from_iterator(
#         NOTES, BpeTrainer(vocab_size=size, special_tokens=["[UNK]"], show_progress=False)
#     )
#     return model


# Empieza con las letras sueltas y junta una y otra vez la pareja más frecuente.
# for size in (40, 120, 250):
#     model = bpe(size)
#     print(
#         f"{model.get_vocab_size():>3} piezas · recalibrado → {model.encode('recalibrado').tokens}"
#     )
# merges = json.loads(model.to_str())["model"]["merges"]
# print(f"las primeras uniones: {merges[:6]}")

# ============================================
# PASO 5: Un tokenizador preentrenado: WordPiece
# ============================================
# Descomenta las siguientes líneas:
# Descarga solo el tokenizador (unos cientos de KB), no el modelo.
# spanish = AutoTokenizer.from_pretrained(SPANISH[0], revision=SPANISH[1])
# print(f"{type(spanish).__name__}: {spanish.vocab_size} piezas")
# for text in [NOTES[2], "recalibrado", "PM2.5 en µg/m³"]:
#     print(f"  {spanish.tokenize(text)}")

# ============================================
# PASO 6: Otro estilo: SentencePiece, en 50 idiomas
# ============================================
# Descomenta las siguientes líneas:
# multilingual = AutoTokenizer.from_pretrained(MULTILINGUAL[0], revision=MULTILINGUAL[1])
# print(f"{type(multilingual).__name__}: {multilingual.vocab_size} piezas")
# for text in [NOTES[2], "recalibrado", "PM2.5 en µg/m³"]:
#     print(f"  {multilingual.tokenize(text)}")

# ============================================
# PASO 7: Un lote para el modelo
# ============================================
# Descomenta las siguientes líneas:
# padding: todas las notas del lote con la misma longitud; truncation: ninguna más larga
# que max_length.
# batch = spanish(["Filtro sucio.", NOTES[0]], padding=True, truncation=True, max_length=8)
# for name, rows in batch.items():
#     print(f"{name}: {rows}")
# print(spanish.convert_ids_to_tokens(batch["input_ids"][0]))
# print(spanish.convert_ids_to_tokens(batch["input_ids"][1]))
# print(f"de vuelta a texto: {spanish.decode(batch['input_ids'][1], skip_special_tokens=True)!r}")
