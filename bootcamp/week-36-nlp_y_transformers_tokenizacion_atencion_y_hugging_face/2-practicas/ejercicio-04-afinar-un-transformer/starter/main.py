"""Ejercicio 04 · Afinar un Transformer preentrenado.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import csv
from pathlib import Path

import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from transformers import AutoModelForSequenceClassification, AutoTokenizer, logging, pipeline

print("Ejercicio 04 · Afinar un Transformer")
# Solo los errores: el aviso de "pesos nuevos sin entrenar" del paso 2 lo explica el README.
logging.set_verbosity_error()

with Path("notas.csv").open(encoding="utf-8") as file:
    rows = list(csv.DictReader(file, delimiter=";"))
texts, kinds = [row["texto"] for row in rows], [row["tipo"] for row in rows]
CLASSES = sorted(set(kinds))
targets = torch.tensor([CLASSES.index(kind) for kind in kinds])
# Pocas etiquetas: 30 notas para entrenar, 30 para validar y las 100 últimas para probar.
TRAIN, VALIDATION, TEST = slice(0, 30), slice(100, 130), slice(200, 300)
PARAPHRASES = [
    ("averia", "Monitor muerto, ni prende"),
    ("averia", "Sin corriente desde ayer"),
    ("limpieza", "Barrimos mugre acumulada"),
    ("limpieza", "Aspiramos suciedad"),
    ("calibracion", "Corregimos el desvío del aparato"),
    ("calibracion", "Afinamos la medición"),
]
others = [text for _, text in PARAPHRASES]
print(
    f"{len(rows)} notas · 30 para entrenar, 30 para validar, 100 de prueba · 6 con otras palabras"
)

NAME, REVISION = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "e8f8c211226b894fcb81acc59f3b34ba3efd5f42",
)
tokenizer = AutoTokenizer.from_pretrained(NAME, revision=REVISION)


def tokens(batch: list[str]) -> dict[str, torch.Tensor]:
    return dict(tokenizer(batch, padding=True, truncation=True, return_tensors="pt"))


def scores(model: torch.nn.Module, batch: list[str]) -> torch.Tensor:
    """Las puntuaciones de cada nota, sin calcular gradientes."""
    model.eval()
    with torch.no_grad():
        return model(**tokens(batch)).logits


def report(name: str, model: torch.nn.Module) -> None:
    """El acierto en prueba y cuántas de las 6 notas con otras palabras acierta."""
    accuracy = (scores(model, texts[TEST]).argmax(dim=1) == targets[TEST]).float().mean()
    guesses = [CLASSES[i] for i in scores(model, others).argmax(dim=1).tolist()]
    hits = sum(guess == kind for guess, (kind, _) in zip(guesses, PARAPHRASES, strict=True))
    print(f"{name:>16} · prueba {accuracy:.2f} · con otras palabras {hits} de 6")


def train(model: torch.nn.Module, epochs: int, rate: float) -> None:
    """El bucle de la semana 35: lotes de 8, Adam, entropía cruzada, solo lo no congelado."""
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=rate)
    generator = torch.Generator().manual_seed(36)
    for epoch in range(epochs):
        model.train()
        for batch in torch.randperm(30, generator=generator).split(8):
            optimizer.zero_grad()
            output = model(**tokens([texts[i] for i in batch]), labels=targets[batch])
            # Con labels, el modelo ya calcula la entropía cruzada.
            output.loss.backward()
            optimizer.step()
        validation = scores(model, texts[VALIDATION]).argmax(dim=1) == targets[VALIDATION]
        print(f"  época {epoch + 1} · validación {validation.float().mean():.2f}")


def fresh() -> torch.nn.Module:
    """El modelo preentrenado con una salida nueva de 3 tipos, sin entrenar."""
    torch.manual_seed(36)
    return AutoModelForSequenceClassification.from_pretrained(
        NAME,
        revision=REVISION,
        num_labels=len(CLASSES),
        id2label=dict(enumerate(CLASSES)),
        label2id={kind: i for i, kind in enumerate(CLASSES)},
    )


# ============================================
# PASO 1: La referencia: TF-IDF con 30 notas
# ============================================
# Descomenta las siguientes líneas:
# bag = TfidfVectorizer().fit(texts[TRAIN])
# fitted = LogisticRegression(max_iter=1000).fit(bag.transform(texts[TRAIN]), kinds[TRAIN])
# accuracy = fitted.score(bag.transform(texts[TEST]), kinds[TEST])
# hits = sum(g == k for g, (k, _) in zip(fitted.predict(bag.transform(others)), PARAPHRASES))
# print(f"{'tf-idf':>16} · prueba {accuracy:.2f} · con otras palabras {hits} de 6")

# ============================================
# PASO 2: Un cuerpo preentrenado y una salida nueva
# ============================================
# Descomenta las siguientes líneas:
# model = fresh()
# print(type(model).__name__)
# total = sum(p.numel() for p in model.parameters())
# embeddings = model.bert.embeddings.word_embeddings.weight.numel()
# head = sum(p.numel() for p in model.classifier.parameters())
# print(
#     f"{total:,} parámetros · {embeddings:,} son la tabla de piezas · salida {head:,}".replace(
#         ",", "."
#     )
# )
# report("sin entrenar", model)

# ============================================
# PASO 3: Congelar el cuerpo y entrenar la salida
# ============================================
# Descomenta las siguientes líneas:
# for parameter in model.bert.parameters():
#     parameter.requires_grad_(False)
# trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
# print(f"entrenables: {trainable:,}".replace(",", "."))
# train(model, epochs=5, rate=1e-2)
# report("solo la salida", model)

# ============================================
# PASO 4: Afinar todo el modelo
# ============================================
# Descomenta las siguientes líneas:
# Desde el modelo preentrenado otra vez, sin congelar nada y con un ritmo doscientas veces menor:
# un ritmo grande borraría lo que el modelo ya sabe.
# model = fresh()
# train(model, epochs=5, rate=5e-5)
# report("afinado", model)

# ============================================
# PASO 5: Qué dice de notas nuevas
# ============================================
# Descomenta las siguientes líneas:
# probabilities = scores(model, others).softmax(dim=1)
# for text, row in zip(others, probabilities, strict=True):
#     best = row.argmax().item()
#     print(f"  {CLASSES[best]:>11} {row[best]:.2f} · {text}")

# ============================================
# PASO 6: Guardar y volver a cargar
# ============================================
# Descomenta las siguientes líneas:
# folder = Path("modelo-afinado")
# model.save_pretrained(folder)
# tokenizer.save_pretrained(folder)
# print(sorted(path.name for path in folder.iterdir()))
# weights = (folder / "model.safetensors").stat().st_size / 1e6
# print(f"model.safetensors: {weights:.0f} MB")
# pipeline lee la carpeta: el modelo, el tokenizador y los nombres de los tipos.
# classifier = pipeline("text-classification", model=str(folder), device="cpu")
# for text in ["El sensor de Norte se quemó", "Se limpió la carcasa"]:
#     (guess,) = classifier(text)
#     print(f"  {guess['label']:>11} {guess['score']:.2f} · {text}")
