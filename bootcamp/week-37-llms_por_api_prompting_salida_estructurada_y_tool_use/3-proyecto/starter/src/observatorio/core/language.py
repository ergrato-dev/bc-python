"""Clasificar las notas de texto libre: un Transformer pequeño frente a TF-IDF y la referencia.

Qué: read_notes lee y valida notas.csv; tokenizer entrena un tokenizador BPE (subpalabras)
con tus notas; encode convierte textos en identificadores; Encoder es un Transformer de una
capa (embeddings, posiciones, atención y una capa lineal); classify reparte las notas,
entrena el tokenizador, TF-IDF con regresión logística y el Transformer, y mide el acierto
en prueba de los tres; predict dice el tipo de notas nuevas.
Para qué: es el NLP de la semana 36, sin descargar nada: el tokenizador y la red aprenden
solo de tus notas, así que los tests y la CI no dependen del Hub de Hugging Face.
Impacto: importa torch y tokenizers: core/__init__.py no lo reexporta, y la CLI lo importa
solo en `clasificar`.
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from tokenizers import Tokenizer, normalizers, pre_tokenizers
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from torch import nn

from observatorio.core.convolution import count, fit
from observatorio.core.learning import SEED

COLUMNS = ("etiqueta", "tipo", "texto")
# Piezas del tokenizador; la de relleno es la 0, la que usa Encoder para no mirar el relleno.
VOCABULARY = 200
PAD, UNKNOWN = "[PAD]", "[UNK]"
# Piezas por nota: las cortas se rellenan y las largas se cortan.
LENGTH = 48
# Tamaño de cada vector, cabezas de atención y capas del Transformer.
DIMENSION = 16
HEADS = 2
LAYERS = 1
EPOCHS = 100
PATIENCE = 10
# Reparto al azar, con la misma proporción de cada tipo en las tres partes.
TEST_SHARE = 0.2
VALIDATION_SHARE = 0.2
# Con menos notas de un tipo, alguna parte se quedaría sin él.
MINIMUM = 5
BASELINE, BAG, TRANSFORMER = "referencia", "tf-idf", "transformer"


@dataclass(frozen=True)
class Classification:
    """Los tipos, el reparto, el tokenizador y la red, y el acierto en prueba de cada modelo."""

    classes: tuple[str, ...]
    sizes: tuple[int, int, int]
    vocabulary: int
    parameters: int
    losses: tuple[float, ...]
    best: int
    accuracy: dict[str, float]

    @property
    def winner(self) -> str:
        """El modelo que más acierta; en un empate, el primero (la referencia va primero)."""
        return max(self.accuracy, key=self.accuracy.__getitem__)

    @property
    def improves(self) -> bool:
        """Si algún modelo acierta más que la referencia."""
        return self.winner != BASELINE


def read_notes(path: Path) -> pd.DataFrame:
    """Las notas de un CSV con etiqueta;tipo;texto. ValueError si faltan columnas, si hay
    textos o tipos vacíos, o si algún tipo tiene menos de MINIMUM notas."""
    # dtype=str y sin NA: una nota que dice "NA" es un texto, no un valor que falta.
    notes = pd.read_csv(path, sep=";", dtype=str, keep_default_na=False, encoding="utf-8")
    missing = [column for column in COLUMNS if column not in notes.columns]
    if missing:
        raise ValueError(f"a {path.name} le faltan las columnas: {', '.join(missing)}")
    notes = notes.assign(texto=notes["texto"].str.strip(), tipo=notes["tipo"].str.strip())
    empty = notes.index[(notes["texto"] == "") | (notes["tipo"] == "")]
    if len(empty):
        # +2: la cabecera es la línea 1 y el índice empieza en 0.
        raise ValueError(f"{path.name}: la línea {empty[0] + 2} no tiene texto o tipo")
    counts = notes["tipo"].value_counts()
    if len(counts) < 2:
        raise ValueError(f"{path.name}: hacen falta al menos dos tipos para clasificar")
    if counts.min() < MINIMUM:
        raise ValueError(
            f"{path.name}: el tipo {counts.idxmin()} tiene {counts.min()} notas;"
            f" hacen falta al menos {MINIMUM}"
        )
    return notes


def tokenizer(texts: list[str], size: int = VOCABULARY) -> Tokenizer:
    """Un tokenizador BPE entrenado con texts: minúsculas y sin tildes, y piezas que juntan
    las letras más frecuentes hasta tener `size`. Rellena y corta a LENGTH piezas."""
    model = Tokenizer(BPE(unk_token=UNKNOWN))
    model.normalizer = normalizers.Sequence(
        [normalizers.NFD(), normalizers.StripAccents(), normalizers.Lowercase()]
    )
    # Antes de juntar letras, separa por espacios y signos: ninguna pieza cruza dos palabras.
    model.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = BpeTrainer(vocab_size=size, special_tokens=[PAD, UNKNOWN], show_progress=False)
    model.train_from_iterator(texts, trainer)
    model.enable_padding(pad_id=0, pad_token=PAD, length=LENGTH)
    model.enable_truncation(LENGTH)
    return model


def encode(model: Tokenizer, texts: list[str]) -> torch.Tensor:
    """Los identificadores de las piezas de cada texto, con forma (textos, LENGTH)."""
    return torch.tensor([encoding.ids for encoding in model.encode_batch(texts)])


def pieces(model: Tokenizer, text: str) -> list[str]:
    """Las piezas en las que el tokenizador parte un texto, sin el relleno."""
    return [piece for piece in model.encode(text).tokens if piece != PAD]


class Encoder(nn.Module):
    """Un Transformer que clasifica textos: cada pieza es un vector, se le suma el de su
    posición, la atención mezcla cada vector con los de las demás piezas, y la media de los
    vectores (sin el relleno) pasa por una capa lineal con una puntuación por tipo."""

    def __init__(self, vocabulary: int, classes: int, dimension: int = DIMENSION) -> None:
        super().__init__()
        self.tokens = nn.Embedding(vocabulary, dimension, padding_idx=0)
        self.positions = nn.Embedding(LENGTH, dimension)
        layer = nn.TransformerEncoderLayer(
            dimension, HEADS, dim_feedforward=2 * dimension, dropout=0.1, batch_first=True
        )
        # enable_nested_tensor=False: el atajo para el relleno avisa con una cabeza por capa
        # impar y no acelera nada con textos tan cortos.
        self.encoder = nn.TransformerEncoder(layer, LAYERS, enable_nested_tensor=False)
        self.output = nn.Linear(dimension, classes)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        padding = ids == 0
        x = self.tokens(ids) + self.positions.weight[: ids.shape[1]]
        # La máscara: ninguna pieza presta atención al relleno.
        x = self.encoder(x, src_key_padding_mask=padding)
        keep = (~padding).unsqueeze(-1).float()
        scores: torch.Tensor = self.output((x * keep).sum(dim=1) / keep.sum(dim=1).clamp(min=1))
        return scores


def classify(
    notes: pd.DataFrame,
    size: int = VOCABULARY,
    epochs: int = EPOCHS,
    patience: int = PATIENCE,
    seed: int = SEED,
) -> tuple[Classification, Encoder, Tokenizer]:
    """Reparte las notas, entrena TF-IDF y el Transformer con las de entrenamiento y mide el
    acierto en prueba de los dos y de la referencia (el tipo más frecuente)."""
    texts = notes["texto"].tolist()
    classes = sorted(set(notes["tipo"]))
    targets = np.array([classes.index(kind) for kind in notes["tipo"]])
    rest, test = train_test_split(
        np.arange(len(texts)), test_size=TEST_SHARE, stratify=targets, random_state=seed
    )
    train, validation = train_test_split(
        rest,
        test_size=VALIDATION_SHARE / (1 - TEST_SHARE),
        stratify=targets[rest],
        random_state=seed,
    )
    train_texts = [texts[i] for i in train]
    accuracy = {BASELINE: float((targets[test] == np.bincount(targets[train]).argmax()).mean())}
    bag = make_pipeline(TfidfVectorizer(strip_accents="unicode"), LogisticRegression(max_iter=1000))
    bag.fit(train_texts, targets[train])
    accuracy[BAG] = float(bag.score([texts[i] for i in test], targets[test]))
    # El tokenizador aprende solo de entrenamiento: como el escalado, no mira la prueba.
    vocabulary = tokenizer(train_texts, size)
    ids, y = encode(vocabulary, texts), torch.tensor(targets)
    torch.manual_seed(seed)
    model = Encoder(vocabulary.get_vocab_size(), len(classes))
    losses, best = fit(
        model,
        (ids[train], y[train]),
        (ids[validation], y[validation]),
        epochs,
        patience,
        nn.CrossEntropyLoss(),
    )
    model.eval()
    with torch.no_grad():
        hits = (model(ids[test]).argmax(dim=1) == y[test]).sum().item()
    # Aciertos entre notas, en float de Python: un float32 de torch rompería los empates
    # (52 / 60 en float32 es 0.86666667, más que el 0.8666... de TF-IDF).
    accuracy[TRANSFORMER] = hits / len(test)
    result = Classification(
        tuple(classes),
        (len(train), len(validation), len(test)),
        vocabulary.get_vocab_size(),
        count(model),
        losses,
        best,
        accuracy,
    )
    return result, model, vocabulary


def predict(
    model: Encoder, vocabulary: Tokenizer, classes: tuple[str, ...], texts: list[str]
) -> list[tuple[str, float]]:
    """El tipo más probable de cada texto y su probabilidad; sin textos, ninguno."""
    if not texts:
        return []
    model.eval()
    with torch.no_grad():
        probabilities = model(encode(vocabulary, texts)).softmax(dim=1)
    chances, indices = probabilities.max(dim=1)
    return [(classes[i], p) for i, p in zip(indices.tolist(), chances.tolist(), strict=True)]
