# Proyecto — Observatorio, capa 35: clasificar las notas de texto libre

> Hasta ahora tu Observatorio solo leía números. Esta semana lee lo que escriben las personas: las notas de texto libre de tu dominio. Entrenas un tokenizador BPE con tus notas, construyes un Transformer pequeño con PyTorch y lo comparas, en las mismas notas de prueba, con TF-IDF y con la referencia. Sin descargar ningún modelo: los tests y la CI no dependen de Hugging Face.

## Qué construyes

```
$ uv run observatorio clasificar notas.csv
notas.csv: 300 notas · 3 tipos: averia 100, calibracion 100, limpieza 100
reparto al azar por tipo · 180 para entrenar, 60 para validar, 60 para prueba
tokenizador BPE de 200 piezas, entrenado con las notas de entrenamiento · «Visita a Centro, se revisó el equipo.» → visita · a · centro · , · se · reviso · el · equipo · .
transformer de 1 capa, 2 cabezas de atención, vectores de 16 · 6243 parámetros
Pérdida en validación (entropía cruzada)
┏━━━━━━━┳━━━━━━━━━┓
┃ Época ┃ Pérdida ┃
┡━━━━━━━╇━━━━━━━━━┩
│     1 │  0.9995 │
│     5 │  0.4213 │
│     9 │  0.2887 │
│    13 │  0.3241 │
│    17 │  0.3440 │
└───────┴─────────┘
paró en la época 17; se queda con la 7, pérdida 0.2747
Acierto en prueba
┏━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Modelo      ┃ Acierto ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━┩
│ referencia  │   0.333 │
│ tf-idf      │   0.950 │
│ transformer │   0.933 │
└─────────────┴─────────┘
gana tf-idf: acierta más que la referencia (el tipo más frecuente)
```

Con las notas de ejemplo, TF-IDF acierta 57 de 60 y el Transformer 56: una nota de diferencia. Ninguno pasa de 0,95, porque un 15 % de las notas no dice qué se hizo (teoría 05, sección 5).

| Pieza | Qué hace |
|---|---|
| `scripts/generar_notas.py` | Genera `notas.csv` (`etiqueta;tipo;texto`) con las frases de tu dominio |
| `core/language.py` | `read_notes` valida las notas; `tokenizer`, `encode` y `pieces` para el BPE; `Encoder`, el Transformer; `classify` reparte, entrena y mide; `predict` clasifica notas nuevas; `Classification` guarda el resultado |
| `core/convolution.py` | `fit` recibe la función de pérdida: `MSELoss` por defecto, `CrossEntropyLoss` para clasificar |
| `clasificar NOTAS` | El reparto, el tokenizador, la red, la pérdida de validación, el acierto de cada modelo y el veredicto, con `--vocabulario`, `--epocas`, `--paciencia`, `--semilla` y `--nota` |

Una dependencia nueva: `tokenizers`, la biblioteca de tokenizadores de Hugging Face (unos 3 MB, en Rust). No trae `transformers` ni ningún modelo.

```
scripts/
└── generar_notas.py          # nuevo: viene en el starter, lo adaptas a tu dominio
notas.csv                     # nuevo: tus notas
src/observatorio/
├── cli.py                    # modificado: clasificar
└── core/
    ├── convolution.py        # modificado: fit con loss_function
    └── language.py           # nuevo: sin reexportar en core/__init__.py
tests/
├── test_language.py          # nuevo: los tests del bootcamp
├── test_my_language.py       # nuevo: los tuyos
├── test_delivery.py          # modificado: las imágenes week-36
├── test_notebook.py          # modificado: la imagen week-36-notebook
└── test_package.py           # modificado: tokenizers fijada, la versión 0.36.0
pyproject.toml                # modificado: tokenizers y la versión
uv.lock                       # modificado
compose.yaml                  # modificado: las imágenes week-36
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-36`. El `starter/` trae la capa 34 resuelta: `core/convolution.py` y `pronosticar`. **Tú** escribes las notas, `language.py` y `clasificar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-35` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-36
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/3-proyecto/starter
cp $STARTER/tests/test_language.py $STARTER/tests/test_my_language.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_notebook.py $STARTER/tests/test_package.py tests/
cp $STARTER/scripts/generar_notas.py scripts/
git status --short
```

- **Nuevos:** `test_language.py`, con 58 tests; `test_my_language.py`, con un ejemplo; y `scripts/generar_notas.py`.
- **Modificados:** `test_delivery.py` y `test_notebook.py`, las imágenes `week-36`; `test_package.py`, `tokenizers==0.23.3` entre las dependencias y la versión `0.36.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'tokenizers'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `test_language.py`. Fíjate en:

- `easy()`: notas en las que el tipo se ve en dos palabras. Con ellas, TF-IDF y el Transformer **tienen** que acertar todo;
- `test_encoder_does_not_look_at_the_padding`: la misma nota con 48 o con 5 piezas da las mismas puntuaciones. Sin la máscara, o con la media de todas las piezas, no;
- `test_encoder_cares_about_the_order`: las mismas piezas en otro orden dan otro resultado. Sin posiciones, no (teoría 03, sección 2);
- `test_classify_trains_the_tokenizer_only_with_the_training_notes`: un espía en lugar de `language.tokenizer`, que comprueba qué notas recibe;
- `test_the_baseline_is_the_most_frequent_type_in_training`: con 40 averías de 80 notas, la referencia acierta la mitad;
- `test_classify_counts_hits_exactly`: el acierto es un número exacto de notas entre 12, sin redondeos de `float32`.

### 4. La dependencia

```bash
uv add tokenizers==0.23.3
uv run python -c "import tokenizers; print(tokenizers.__version__)"
```

```
0.23.3
```

`uv add` trae también `huggingface-hub`, `hf-xet` y `tqdm`: `tokenizers` puede descargar tokenizadores del Hub, aunque tu proyecto no lo hace. Las versiones de `uv.lock` deben tener al menos dos semanas (`docs/stack-versions.md`); si alguna es más nueva, bájala con `uv lock --upgrade-package <paquete>==<versión>`.

### 5. `fit` con otra pérdida

En `src/observatorio/core/convolution.py`, `fit` recibe la función de pérdida en lugar de usar siempre `MSELoss`:

```python
def fit(
    model: nn.Module,
    train: tuple[torch.Tensor, torch.Tensor],
    validation: tuple[torch.Tensor, torch.Tensor],
    epochs: int = EPOCHS,
    patience: int = PATIENCE,
    loss_function: nn.Module | None = None,
) -> tuple[tuple[float, ...], int]:
    """Entrena por mini-lotes y mide la validación tras cada época. Para tras `patience`
    épocas sin mejorar y devuelve el modelo a su mejor época. Devuelve la pérdida en
    validación de cada época y el índice de la mejor. La pérdida es MSELoss si no se da
    otra: CrossEntropyLoss para clasificar (semana 36)."""
    optimizer = torch.optim.Adam(model.parameters(), lr=RATE)
    loss_function = loss_function or nn.MSELoss()
```

El resto de `fit` no cambia. `None` por defecto, y no `nn.MSELoss()`: un valor por defecto se crea una sola vez, al definir la función, y lo compartirían todas las llamadas. `pronosticar` sigue igual, y sus 58 tests también.

### 6. Tus notas

Abre `scripts/generar_notas.py` y cambia `LABELS`, `PIECES`, `HINTS` y `VAGUE` por los de tu dominio (teoría 05, sección 1): tus etiquetas, al menos tres tipos de nota y frases que alguien de tu dominio escribiría. Mantén las pistas engañosas y las notas vagas: sin ellas, todos los modelos aciertan 1,000 y la comparación no dice nada. Si tienes notas reales, mejor: escríbelas en `notas.csv` con las mismas tres columnas.

```bash
uv run python scripts/generar_notas.py 300 notas.csv
head -4 notas.csv
```

```
etiqueta;tipo;texto
Centro;averia;Visita a Centro, se revisó el equipo.
Centro;limpieza;En Centro se quitó el polvo acumulado en la entrada, queda limpio.
Centro;calibracion;El analizador de Centro tenía deriva y se corrigió el cero, tras la limpieza, se anotó el nuevo factor.
```

Esas son las de ejemplo; las tuyas, con tu dominio. `notas.csv` sí va al repositorio: son tus datos de ejemplo, como `medidas.csv`.

### 7. El módulo `language.py`

Crea `src/observatorio/core/language.py`:

```python
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
```

Por partes:

- **`read_notes`** lee con `dtype=str` y `keep_default_na=False`, quita espacios y valida (teoría 05, sección 1). La línea del error es `índice + 2`: la cabecera es la 1.
- **`tokenizer`** es el BPE de la teoría 01, sección 5, con `[PAD]` en el 0 y `[UNK]` en el 1, y relleno y corte a `LENGTH` piezas. **`encode`** devuelve un tensor de enteros `(notas, LENGTH)`; **`pieces`**, lo que escribe `clasificar` para la primera nota.
- **`Encoder`** es la teoría 03, sección 3: dos `nn.Embedding` (piezas y posiciones), un `nn.TransformerEncoder` de `LAYERS` capas con `batch_first=True`, la máscara del relleno, la media sin relleno y una `nn.Linear` con una puntuación por tipo. `forward` calcula la máscara con `ids == 0`: el relleno es siempre el 0.
- **`classify`**: dos `train_test_split` estratificados; la referencia con el tipo más frecuente de entrenamiento; TF-IDF con regresión logística; el tokenizador **solo con las notas de entrenamiento**; la semilla antes de crear la red; y `fit` con `nn.CrossEntropyLoss()`. El acierto del Transformer, en aciertos entre notas (teoría 05, sección 4).
- **`predict`** usa `softmax` y se queda con el tipo más probable; sin textos, devuelve una lista vacía (`encode([])` no tiene forma de lote).
- **`Classification.winner`** usa `max` sobre el diccionario: en un empate, el primero que se insertó, la referencia o TF-IDF.

```bash
uv run pytest -q tests/test_language.py
```

```
14 failed, 44 passed
```

Fallan los del comando. `uv run mypy` ya pasa.

### 8. El comando `clasificar`

En `src/observatorio/cli.py`, después de `pronosticar`:

```python
@app.command()
def clasificar(
    notas: Annotated[Path, typer.Argument(metavar="NOTAS", help="Un CSV con etiqueta;tipo;texto.")],
    vocabulario: Annotated[
        int, typer.Option(min=50, max=5000, help="Piezas del tokenizador BPE.")
    ] = 200,
    epocas: Annotated[int, typer.Option(min=1, max=1000, help="Épocas como máximo.")] = 100,
    paciencia: Annotated[
        int, typer.Option(min=1, help="Épocas sin mejorar en validación antes de parar.")
    ] = 10,
    semilla: Annotated[
        int, typer.Option(help="La semilla del reparto, de los pesos y de los lotes.")
    ] = 31,
    nota: Annotated[
        list[str] | None, typer.Option(help="Un texto nuevo que clasificar; se puede repetir.")
    ] = None,
) -> None:
    """Clasifica las notas de texto libre: un Transformer frente a TF-IDF y la referencia."""
    # Importar aquí: PyTorch y tokenizers tardan en cargarse.
    from observatorio.core import language

    try:
        notes = language.read_notes(notas)
        result, model, vocabulary = language.classify(
            notes, vocabulario, epocas, paciencia, semilla
        )
    except OSError as problem:
        raise fail(f"no se puede usar {problem.filename}: {problem.strerror}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    counts = notes["tipo"].value_counts()
    kinds = ", ".join(f"{kind} {counts[kind]}" for kind in result.classes)
    out.print(f"{notas.name}: {len(notes)} notas · {len(result.classes)} tipos: {kinds}")
    train, validation, test = result.sizes
    out.print(
        f"reparto al azar por tipo · {train} para entrenar, {validation} para validar,"
        f" {test} para prueba"
    )
    first = notes["texto"].iloc[0]
    out.print(
        f"tokenizador BPE de {result.vocabulary} piezas, entrenado con las notas de"
        f" entrenamiento · «{first}» → {' · '.join(language.pieces(vocabulary, first))}"
    )
    out.print(
        f"transformer de {language.LAYERS} capa, {language.HEADS} cabezas de atención,"
        f" vectores de {language.DIMENSION} · {result.parameters} parámetros"
    )
    out.print(loss_table(result.losses, "Pérdida en validación (entropía cruzada)"))
    epochs = len(result.losses)
    stop = f"paró en la época {epochs}" if epochs < epocas else f"entrenó {epochs} épocas"
    out.print(
        f"{stop}; se queda con la {result.best + 1}, pérdida {result.losses[result.best]:.4f}"
    )
    table = Table(title="Acierto en prueba")
    table.add_column("Modelo")
    table.add_column("Acierto", justify="right")
    for name, accuracy in result.accuracy.items():
        table.add_row(name, f"{accuracy:.3f}")
    out.print(table)
    if result.improves:
        out.print(f"gana {result.winner}: acierta más que la referencia (el tipo más frecuente)")
    else:
        out.print("ningún modelo acierta más que la referencia (el tipo más frecuente)")
    texts = nota or []
    for text, (kind, chance) in zip(
        texts, language.predict(model, vocabulary, result.classes, texts), strict=True
    ):
        out.print(f"«{text}» → {kind} (transformer, {chance:.0%})")
```

- Las notas son un CSV propio, no la instantánea de `extraer`: sin `--huella`.
- Dos errores: no se puede leer el archivo (`OSError`, código 2) o las notas no valen (`ValueError`, código 1).
- `--vocabulario` va de 50 a 5000 piezas: con menos de 50, casi solo hay letras sueltas. Con pocas notas, el tokenizador puede quedarse por debajo de lo pedido: la línea del tokenizador dice cuántas piezas tiene de verdad.
- `--nota` se puede repetir: `list[str] | None`. Cada nota nueva sale con su tipo y su probabilidad.
- `loss_table` es la de la semana 35: seis épocas como mucho.

Actualiza el docstring del módulo: "veintisiete comandos", con `clasificar` entre `pronosticar` y `borrar`.

```bash
uv run pytest -q
uv run observatorio clasificar notas.csv --vocabulario 49; echo $?
```

```
4 failed, 1455 passed
...
│ Invalid value for '--vocabulario': 49 is not in the range 50<=x<=5000.       │
...
2
```

Fallan la versión y las imágenes.

### 9. Versión e imágenes

En `pyproject.toml`, `version = "0.36.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-36-test`, `local/observatorio:week-36` y `local/observatorio:week-36-notebook`.

```bash
uv run pytest -q
docker compose build app api
docker images local/observatorio
```

```
1459 passed
...
local/observatorio:week-36        ...   2.55GB
local/observatorio:week-35        ...   2.5GB
```

`tokenizers` añade unos 50 MB a la imagen. Con `transformers` y un modelo de 470 MB, serían más de 3 GB.

### 10. Tu clasificación, con tus notas

Ejecuta `clasificar` con **tus** notas, y con varias opciones:

```bash
uv run observatorio clasificar notas.csv
uv run observatorio clasificar notas.csv --semilla 7
uv run observatorio clasificar notas.csv --vocabulario 60
uv run observatorio clasificar notas.csv --vocabulario 1000
uv run observatorio clasificar notas.csv --nota "<una nota nueva de tu dominio>" --nota "<otra>"
```

Con las notas de ejemplo:

```
$ uv run observatorio clasificar notas.csv --vocabulario 60
tokenizador BPE de 60 piezas, entrenado con las notas de entrenamiento · «Visita a Centro, se revisó el equipo.» → vi · si · ta · a · c · en · tro · , · se · re · vi · s · o · el · e · qui · po · .
...
$ uv run observatorio clasificar notas.csv --vocabulario 1000
tokenizador BPE de 356 piezas, entrenado con las notas de entrenamiento · «Visita a Centro, se revisó el equipo.» → visita · a · centro · , · se · reviso · el · equipo · .
...
```

- ¿Quién gana, y por cuántas notas? Con `--semilla 7`, con las de ejemplo, TF-IDF y el Transformer aciertan 52 de 60 y gana TF-IDF por el desempate. ¿Y con las tuyas?
- Con `--vocabulario 60`, ¿cómo parte el tokenizador tus palabras? ¿Cambia el acierto?
- Con `--vocabulario 1000`, ¿cuántas piezas tiene de verdad? ¿Por qué no llega a 1000?
- ¿En qué época para el Transformer, y con cuál se queda?
- Con `--nota`, escribe dos notas con palabras que **no** salgan en `notas.csv`. ¿Acierta? ¿Con qué probabilidad? Compáralo con lo que hizo el modelo afinado del ejercicio 04.

Añade a `informe/README.md`, en **Siguientes pasos**, una línea con el resultado de `clasificar` y qué harías para clasificar notas reales de tu dominio (ejercicios 03 y 04).

### 11. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_language.py tests/test_my_language.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `language.py` | `keep_default_na=False` por `keep_default_na=True` | |
| `language.py` | `{empty[0] + 2}` por `{empty[0] + 1}` | |
| `language.py` | quitar `normalizers.StripAccents(), ` | |
| `language.py` | borrar la línea `model.pre_tokenizer = pre_tokenizers.Whitespace()` | |
| `language.py` | quitar ` + self.positions.weight[: ids.shape[1]]` | |
| `language.py` | `self.encoder(x, src_key_padding_mask=padding)` por `self.encoder(x)` | |
| `language.py` | `(x * keep).sum(dim=1) / keep.sum(dim=1).clamp(min=1)` por `x.mean(dim=1)` | |
| `language.py` | quitar `stratify=targets, ` del primer `train_test_split` | |
| `language.py` | `vocabulary = tokenizer(train_texts, size)` por `vocabulary = tokenizer(texts, size)` | |
| `language.py` | `(ids[validation], y[validation])` por `(ids[train], y[train])` en la llamada a `fit` | |
| `language.py` | `return self.winner != BASELINE` por `return self.accuracy[BASELINE] < 1` | |
| `cli.py` | `notes, vocabulario, epocas, paciencia, semilla` por `notes, vocabulario, epocas, paciencia, 31` | |

Los doce mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el tokenizador entrenado con todas las notas, ¿qué test falla? Ejecuta `clasificar` con tus notas: ¿cambia el acierto? ¿Por qué esa fuga no la vería nadie sin un test (teoría 05, sección 3)?
- Con `x.mean(dim=1)`, ¿qué test falla? ¿Por qué el resultado de una nota dependería entonces de la nota más larga de su lote?

En el *bootcamp* se probaron 28 mutantes. Dos sobreviven y son **equivalentes**: no cambian ningún resultado.

- Calcular la referencia con el tipo más frecuente de **prueba**: con el reparto estratificado, prueba y entrenamiento tienen las mismas proporciones.
- Borrar `model.eval()` antes de medir la prueba: `fit` ya deja el modelo en modo evaluación.

Después, en `tests/test_my_language.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con tus tipos, tus frases y las funciones de `test_language.py` (`easy`, `write`, `outcome`). Ideas:

- dos tipos de tu dominio que se distinguen por una palabra, y los dos modelos aciertan;
- dos notas iguales con tipos distintos, y ningún modelo las acierta las dos;
- una palabra de tu dominio con tildes y mayúsculas, y las mismas piezas sin ellas;
- un tipo con menos de 5 notas, y el error de `read_notes`;
- `clasificar --nota` con una nota de tu dominio, y su tipo;
- notas que solo se distinguen por el orden de las palabras, y TF-IDF no puede.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1464 tests en verde.

### 12. README y pull request

En el `README.md` de tu repositorio, añade una sección "Notas": qué notas tiene tu dominio y de dónde salen, cómo ejecutar `clasificar`, qué tres modelos compara y el veredicto con tus notas en dos frases.

Commits sugeridos, en este orden:

1. `test: add note classification tests`
2. `build: add tokenizers dependency`
3. `refactor: accept a loss function in fit`
4. `feat: add notes for my domain`
5. `feat: add language module`
6. `feat: add clasificar command`
7. `chore: bump version to 0.36.0`
8. `docs: add classification results to the report`
9. `test: add my language tests`

```bash
git push -u origin week-36
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-36` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `clasificar` con tus notas (por defecto, con otra semilla y con dos `--nota`), y tu lectura en tres frases: ¿quién gana y por cuántas notas?, ¿se mantiene con otra semilla?, ¿acierta notas con otras palabras?
3. La tabla de mutantes del paso 11 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'tokenizers'` | Falta el paso 4: `uv add tokenizers==0.23.3` |
| `TypeError: fit() takes from 3 to 5 positional arguments but 6 were given` | Falta el paso 5: `loss_function` en `fit` |
| `RuntimeError: The size of tensor a (3) must match the size of tensor b (...)` | `fit` sigue usando `MSELoss`: la pérdida es `loss_function or nn.MSELoss()` |
| `test_encoder_does_not_look_at_the_padding` falla | Falta `src_key_padding_mask=padding`, o la media incluye el relleno |
| `test_encoder_cares_about_the_order` falla | Falta sumar `self.positions.weight[: ids.shape[1]]` |
| `test_tokenizer_starts_with_padding_and_unknown` falla | `special_tokens=[PAD, UNKNOWN]`, en ese orden |
| `test_the_cli_loads_tokenizers_only_for_clasificar` falla | Importas `language` al principio de `cli.py`: va dentro de `clasificar` |
| `clasificar` acierta 1,000 con todos los modelos | Tus notas son demasiado fáciles: añade pistas engañosas y notas vagas |

## Entrega

1. Rama `week-36` con `notas.csv`, `core/language.py`, `fit` con `loss_function`, el comando `clasificar`, `tokenizers==0.23.3`, las imágenes `week-36`, la versión `0.36.0` y al menos 6 tests tuyos en `test_my_language.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Notas", e `informe/README.md` con el resultado en **Siguientes pasos**.
4. *Pull request* `week-36` → `main` con lo que pide el paso 12.

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Afinar un Transformer](../2-practicas/ejercicio-04-afinar-un-transformer/README.md) | **Proyecto** | [Semana 36](../README.md) |
