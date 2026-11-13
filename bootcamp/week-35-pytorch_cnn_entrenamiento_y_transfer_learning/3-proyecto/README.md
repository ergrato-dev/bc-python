# Proyecto — Observatorio, capa 34: una red convolucional que pronostica

> En la semana 34 entrenaste una red que predecía el valor a partir de la etiqueta y la posición. Esta semana haces otra pregunta: ¿los últimos valores dicen el siguiente? Cortas tu serie en ventanas, la repartes por tiempo, entrenas una red convolucional por mini-lotes con parada temprana, guardas sus pesos y los reutilizas para una sola etiqueta: *transfer learning*.

## Qué construyes

```
$ uv run observatorio pronosticar notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
serie de todas las etiquetas · ventanas de 8 valores · 1320 para entrenar, 283 para validar, 283 para prueba
red convolucional, desde cero · 41 parámetros, 41 entrenables
Pérdida en validación (MSE del valor escalado)
┏━━━━━━━┳━━━━━━━━━┓
┃ Época ┃ Pérdida ┃
┡━━━━━━━╇━━━━━━━━━┩
│     1 │  0.9423 │
│     4 │  0.9515 │
│     7 │  0.9582 │
│    10 │  0.9716 │
│    13 │  0.9897 │
└───────┴─────────┘
paró en la época 13; se queda con la 3, pérdida 0.9417
pronóstico del siguiente valor · MAE en prueba: red 19.216 · referencia 19.140: la red no mejora la referencia
```

Con los datos de ejemplo, la pérdida de validación sube desde el principio, la parada temprana se queda con la época 3, y en prueba la red no mejora la referencia: los valores de ejemplo no dependen de los anteriores (teoría 05, sección 5).

| Pieza | Qué hace |
|---|---|
| `core/convolution.py` | `windows` corta la serie; `cnn` construye la red; `fit` entrena por lotes con parada temprana; `forecast` reparte por tiempo, escala, entrena y mide; `freeze`, `count`, `save` y `load` para el *transfer learning*; `Forecast` guarda el resultado |
| `pronosticar INSTANTANEA` | La tabla de la pérdida de validación, dónde paró y el veredicto, con `--huella`, `--etiqueta`, `--ventana`, `--epocas`, `--paciencia`, `--semilla`, `--guardar` y `--desde` |
| `loss_table` | Ahora recibe las pérdidas y el título, y enseña seis épocas como mucho |

Ninguna dependencia nueva: PyTorch ya está desde la semana 34.

```
src/observatorio/
├── cli.py                    # modificado: loss_table y pronosticar
└── core/
    └── convolution.py        # nuevo: sin reexportar en core/__init__.py
tests/
├── test_convolution.py       # nuevo: los tests del bootcamp
├── test_my_convolution.py    # nuevo: los tuyos
├── test_delivery.py          # modificado: las imágenes week-35
├── test_notebook.py          # modificado: la imagen week-35-notebook
└── test_package.py           # modificado: convolution en core, la versión 0.35.0
pyproject.toml                # modificado: la versión
compose.yaml                  # modificado: las imágenes week-35
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-35`. El `starter/` trae la capa 33 resuelta: PyTorch desde el índice de CPU, `core/neural.py` y `red`. **Tú** escribes `convolution.py` y `pronosticar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-34` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-35
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-35-pytorch_cnn_entrenamiento_y_transfer_learning/3-proyecto/starter
cp $STARTER/tests/test_convolution.py $STARTER/tests/test_my_convolution.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_notebook.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `test_convolution.py`, con 58 tests, y `test_my_convolution.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` y `test_notebook.py`, las imágenes `week-35`; `test_package.py`, `convolution` es un módulo de `core` y la versión es `0.35.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ImportError: cannot import name 'convolution' from 'observatorio.core' (...)
E   ModuleNotFoundError: No module named 'observatorio.core.convolution'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `test_convolution.py`. Fíjate en:

- `wave()`: un valor que sube y baja cada 12 posiciones. Con ella, la red **tiene** que ganar a la referencia; con `noise()`, no puede;
- `by_hand()` y `test_fit_is_the_loop_by_hand`: el bucle de la teoría 03 por mini-lotes, con la misma semilla. Sin `zero_grad()`, sin barajar o con otro tamaño de lote, las pérdidas no coinciden;
- `test_fit_returns_the_model_at_its_best_epoch`: tras `fit`, la pérdida de validación del modelo es la de su mejor época, no la de la última;
- `test_forecast_baseline_is_the_mean_of_what_training_sees`: con un valor que crece, la referencia sale de los valores que ven las ventanas de entrenamiento, y de nada más;
- `test_forecast_follows_the_order_of_arrival`: las mismas medidas desordenadas dan el mismo resultado: `forecast` las ordena por carga y posición;
- `test_load_rejects_what_is_not_only_weights`: una red guardada entera (con `pickle`) no se carga.

### 4. El módulo `convolution.py`

Crea `src/observatorio/core/convolution.py`:

```python
"""Una red convolucional que pronostica el siguiente valor de la serie, a partir de los anteriores.

Qué: windows corta la serie en ventanas (unos cuantos valores seguidos y el que viene después),
cnn construye la red (una capa Conv1d, ReLU y una capa lineal), fit la entrena con mini-lotes
y parada temprana, y forecast reparte por tiempo, escala, entrena y mide el MAE en prueba
frente a la referencia. save y load guardan y cargan los pesos; freeze congela la capa
convolucional para reentrenar solo la salida con otros datos (transfer learning).
Para qué: es el entrenamiento de verdad de la semana 35: lotes, validación, quedarse con la
mejor época, y reutilizar una red ya entrenada en lugar de empezar de cero.
Impacto: importa torch: core/__init__.py no lo reexporta, y la CLI lo importa solo en
`pronosticar`.
"""

import copy
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from observatorio.core.learning import SEED
from observatorio.core.neural import tensor
from observatorio.core.validation import ordered

# Valores de cada ventana, filtros de la capa convolucional y tamaño de cada filtro.
WINDOW = 8
CHANNELS = 4
KERNEL = 3
# Épocas como máximo, ritmo de Adam, medidas por lote y épocas sin mejorar antes de parar.
EPOCHS = 100
RATE = 0.01
BATCH = 32
PATIENCE = 10
# Las primeras ventanas entrenan, las siguientes validan y las últimas son la prueba.
TRAIN_SHARE = 0.7
VALIDATION_SHARE = 0.15
# Con menos ventanas, la validación y la prueba tendrían una o dos.
MINIMUM = 20


@dataclass(frozen=True)
class Forecast:
    """La pérdida en validación de cada época, la mejor, y el MAE en prueba de la red y de la
    referencia."""

    parameters: int
    trainable: int
    sizes: tuple[int, int, int]
    losses: tuple[float, ...]
    best: int
    mae: float
    baseline: float

    @property
    def improves(self) -> bool:
        """Si la red se equivoca menos que la referencia en prueba. Empatar no es mejorar."""
        return self.mae < self.baseline


def windows(values: np.ndarray, size: int) -> tuple[torch.Tensor, torch.Tensor]:
    """Cada tramo de `size` valores seguidos, con forma (ventanas, 1 canal, size), y el valor
    que viene justo después, con forma (ventanas, 1)."""
    x = np.lib.stride_tricks.sliding_window_view(values[:-1], size)
    return tensor(x).unsqueeze(1), tensor(values[size:]).reshape(-1, 1)


def cnn(size: int, channels: int = CHANNELS) -> nn.Sequential:
    """Una capa convolucional (channels filtros de KERNEL valores), ReLU, y una capa lineal
    que mira lo que han visto todos los filtros en toda la ventana."""
    return nn.Sequential(
        nn.Conv1d(1, channels, KERNEL),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(channels * (size - KERNEL + 1), 1),
    )


def freeze(model: nn.Sequential) -> None:
    """Congela la capa convolucional: sus pesos ya no cambian al entrenar."""
    for parameter in model[0].parameters():
        parameter.requires_grad_(False)


def count(model: nn.Module, trainable: bool = False) -> int:
    """Cuántos parámetros tiene la red; con trainable, solo los que el entrenamiento cambia."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad or not trainable)


def fit(
    model: nn.Module,
    train: tuple[torch.Tensor, torch.Tensor],
    validation: tuple[torch.Tensor, torch.Tensor],
    epochs: int = EPOCHS,
    patience: int = PATIENCE,
) -> tuple[tuple[float, ...], int]:
    """Entrena por mini-lotes y mide la validación tras cada época. Para tras `patience`
    épocas sin mejorar y devuelve el modelo a su mejor época. Devuelve la pérdida en
    validación de cada época y el índice de la mejor."""
    optimizer = torch.optim.Adam(model.parameters(), lr=RATE)
    loss_function = nn.MSELoss()
    # shuffle: otro orden en cada época, con la semilla de torch.
    loader = DataLoader(TensorDataset(*train), batch_size=BATCH, shuffle=True)
    losses: list[float] = []
    best, best_state = 0, copy.deepcopy(model.state_dict())
    for epoch in range(epochs):
        model.train()
        for x, y in loader:
            optimizer.zero_grad()
            loss_function(model(x), y).backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            loss = loss_function(model(validation[0]), validation[1]).item()
        if loss < min(losses, default=float("inf")):
            # deepcopy: state_dict son los tensores de la red, que el entrenamiento sigue cambiando.
            best, best_state = epoch, copy.deepcopy(model.state_dict())
        losses.append(loss)
        if epoch - best >= patience:
            break
    model.load_state_dict(best_state)
    return tuple(losses), best


def forecast(
    frame: pd.DataFrame,
    window: int = WINDOW,
    epochs: int = EPOCHS,
    patience: int = PATIENCE,
    seed: int = SEED,
    label: str | None = None,
    start: nn.Sequential | None = None,
) -> tuple[Forecast, nn.Sequential]:
    """Entrena una red que pronostica cada valor con los `window` anteriores, en orden de
    llegada, y la mide en prueba frente a la media. Con label, solo la serie de esa etiqueta;
    con start, reentrena esa red con su capa convolucional congelada."""
    rows = ordered(frame)
    if label is not None:
        rows = rows[rows["etiqueta"] == label]
    values = rows["valor"].to_numpy()
    if len(values) < window + MINIMUM:
        raise ValueError(
            f"hacen falta al menos {window + MINIMUM} valores para ventanas de {window},"
            f" y hay {len(values)}"
        )
    # Por tiempo, sin barajar: la red solo ve el pasado de lo que pronostica.
    total = len(values) - window
    train_end, validation_end = (
        int(total * TRAIN_SHARE),
        int(total * (TRAIN_SHARE + VALIDATION_SHARE)),
    )
    # El escalado sale solo de los valores que ven las ventanas de entrenamiento.
    seen = values[: train_end + window]
    center, spread = float(seen.mean()), float(seen.std(ddof=1))
    x, y = windows((values - center) / spread, window)
    torch.manual_seed(seed)
    model = cnn(window) if start is None else start
    if start is not None:
        freeze(model)
    losses, best = fit(
        model,
        (x[:train_end], y[:train_end]),
        (x[train_end:validation_end], y[train_end:validation_end]),
        epochs,
        patience,
    )
    model.eval()
    with torch.no_grad():
        predicted = model(x[validation_end:]) * spread + center
    actual = tensor(values[window + validation_end :]).reshape(-1, 1)
    result = Forecast(
        count(model),
        count(model, trainable=True),
        (train_end, validation_end - train_end, total - validation_end),
        losses,
        best,
        float((predicted - actual).abs().mean()),
        float((actual - center).abs().mean()),
    )
    return result, model


def save(model: nn.Sequential, window: int, path: Path) -> None:
    """Guarda los pesos y la ventana, no el objeto: load no ejecuta nada al leerlos."""
    # open: si no se puede escribir, un OSError como los de cualquier archivo.
    with path.open("wb") as file:
        torch.save({"window": window, "state": model.state_dict()}, file)


def load(path: Path) -> tuple[nn.Sequential, int]:
    """La red y su ventana. weights_only: solo tensores y números; un archivo con otra cosa
    (código que pickle ejecutaría) lanza pickle.UnpicklingError."""
    checkpoint = torch.load(path, weights_only=True)
    model = cnn(checkpoint["window"])
    model.load_state_dict(checkpoint["state"])
    return model, checkpoint["window"]
```

Por partes:

- **`Forecast`** guarda los parámetros (todos y los entrenables), cuántas ventanas tiene cada parte, la pérdida de validación de cada época, el índice de la mejor, y el MAE en prueba de la red y de la referencia. `improves`, como en `Training`: empatar no es mejorar.
- **`windows`** usa `sliding_window_view` (teoría 02, sección 4) y añade el canal con `unsqueeze(1)`: `Conv1d` espera `(ventanas, canales, longitud)`. Reutiliza `tensor` de `neural.py`, que ya convierte a `float32`.
- **`cnn`**: `Conv1d(1, 4, 3)`, ReLU, `Flatten` y una `Linear` cuyo tamaño de entrada sale de la fórmula de la teoría 01: 4 canales × (ventana − 3 + 1).
- **`freeze`** y **`count`**: congelar la capa 0 y contar parámetros (teoría 04, sección 2).
- **`fit`** es el bucle de la teoría 03, sección 6: lotes de 32 barajados, validación tras cada época, una copia de la mejor y parada tras `patience` épocas sin mejorar. Al final, `load_state_dict` devuelve la red a su mejor época. Con parámetros congelados, Adam los ignora: no tienen gradiente.
- **`forecast`** junta todo, en el orden de la teoría 05: ordena con `ordered` (semana 32), filtra la etiqueta, comprueba que hay al menos `window + MINIMUM` valores, reparte por tiempo, escala con lo que ve el entrenamiento, fija la semilla (para los pesos y para el orden de los lotes), entrena, y mide en prueba deshaciendo el escalado. Con `start`, entrena esa red con sus filtros congelados.
- **`save`** guarda un diccionario con la ventana y el `state_dict`, nunca la red; abre el archivo con `path.open("wb")` para que un error de escritura sea un `OSError` como cualquier otro. **`load`** usa `weights_only=True` (teoría 03, sección 7) y reconstruye la red con la ventana guardada.

```bash
uv run pytest -q tests/test_convolution.py
```

```
16 failed, 42 passed
```

Fallan los del comando. `uv run mypy` ya pasa.

### 5. El comando `pronosticar`

En `src/observatorio/cli.py`, añade `import math` a los imports del principio (entre `logging` y `sys`), y quita `from observatorio.core.neural import Training` del bloque `if TYPE_CHECKING:`: `loss_table` ya no lo necesita. Cambia `loss_table` para que sirva a los dos comandos:

```python
def loss_table(losses: tuple[float, ...], title: str) -> Table:
    """La pérdida en seis épocas como mucho: la primera, unas repartidas y la última."""
    epochs = len(losses)
    # ceil: con 13 épocas, cada 3 (1, 4, 7, 10 y 13); con epochs // 5, cada 2, y saldrían 7.
    shown = sorted({*range(0, epochs, math.ceil(epochs / 5)), epochs - 1})
    table = Table(title=title)
    table.add_column("Época", justify="right")
    table.add_column("Pérdida", justify="right")
    for index in shown:
        table.add_row(str(index + 1), f"{losses[index]:.4f}")
    return table
```

En `red`, la llamada pasa a ser:

```python
    out.print(loss_table(training.losses, "Pérdida en entrenamiento (MSE del valor escalado)"))
```

Con 300 épocas, `math.ceil(300 / 5)` y `300 // 5` dan lo mismo: `red` escribe la misma tabla. Con 13, `13 // 5` es 2 y saldrían siete filas.

Y después de `red`:

```python
@app.command()
def pronosticar(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    etiqueta: Annotated[
        str | None, typer.Option(help="Solo la serie de esta etiqueta; sin ella, todas.")
    ] = None,
    ventana: Annotated[
        int, typer.Option(min=3, max=100, help="Cuántos valores anteriores mira la red.")
    ] = 8,
    epocas: Annotated[int, typer.Option(min=1, max=1000, help="Épocas como máximo.")] = 100,
    paciencia: Annotated[
        int, typer.Option(min=1, help="Épocas sin mejorar en validación antes de parar.")
    ] = 10,
    semilla: Annotated[
        int, typer.Option(help="La semilla de los pesos y de los lotes: la misma, la misma red.")
    ] = 31,
    guardar: Annotated[
        Path | None, typer.Option(help="El archivo en el que guardar los pesos de la red.")
    ] = None,
    desde: Annotated[
        Path | None,
        typer.Option(help="Los pesos de otra red: congela sus filtros y reentrena la salida."),
    ] = None,
) -> None:
    """Entrena una red convolucional que pronostica cada valor con los anteriores."""
    # Importar aquí: PyTorch tarda en cargarse. pickle, para el error de un archivo de pesos
    # que trae algo más que pesos.
    import pickle

    from observatorio.core import convolution, findings

    start = None
    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        if desde is not None:
            # La ventana es la de la red guardada: sus capas tienen ese tamaño.
            start, ventana = convolution.load(desde)
        result, model = convolution.forecast(
            frame, ventana, epocas, paciencia, semilla, etiqueta, start
        )
        if guardar is not None:
            convolution.save(model, ventana, guardar)
    except OSError as problem:
        raise fail(f"no se puede usar {problem.filename}: {problem.strerror}", 2) from problem
    except pickle.UnpicklingError as problem:
        raise fail(f"{desde} no es un archivo de pesos: weights_only no lo carga", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    train, validation, test = result.sizes
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(
        f"serie de {etiqueta or 'todas las etiquetas'} · ventanas de {ventana} valores"
        f" · {train} para entrenar, {validation} para validar, {test} para prueba"
    )
    origin = "filtros congelados de " + desde.name if desde else "desde cero"
    out.print(
        f"red convolucional, {origin} · {result.parameters} parámetros,"
        f" {result.trainable} entrenables"
    )
    out.print(loss_table(result.losses, "Pérdida en validación (MSE del valor escalado)"))
    epochs = len(result.losses)
    stop = f"paró en la época {epochs}" if epochs < epocas else f"entrenó {epochs} épocas"
    out.print(
        f"{stop}; se queda con la {result.best + 1}, pérdida {result.losses[result.best]:.4f}"
    )
    verdict = "mejora" if result.improves else "no mejora"
    out.print(
        f"pronóstico del siguiente valor · MAE en prueba: red {result.mae:.3f}"
        f" · referencia {result.baseline:.3f}: la red {verdict} la referencia"
    )
    if guardar is not None:
        out.print(f"pesos guardados en {guardar}")
```

- La ventana va de 3 (el tamaño del filtro) a 100. Con `--desde`, la ventana es la de los pesos guardados: sus capas tienen ese tamaño, y la línea "ventanas de N valores" lo dice.
- Tres errores con código 2: no se puede leer la instantánea o los pesos, no se pueden escribir los pesos (`OSError`, con su nombre de archivo y su motivo), o el archivo de pesos trae algo más que pesos (`pickle.UnpicklingError`). Y con código 1, la huella o pocos valores (`ValueError`).
- `paró en la época N` si la parada temprana cortó antes de `--epocas`; si no, `entrenó N épocas`. En las dos, la mejor época y su pérdida, que puede no estar en la tabla.

Actualiza el docstring del módulo: "veintiséis comandos", con `pronosticar` entre `red` y `borrar`.

```bash
uv run pytest -q
uv run observatorio pronosticar notebooks/instantanea.csv --ventana 2; echo $?
```

```
4 failed, 1396 passed
...
│ Invalid value for '--ventana': 2 is not in the range 3<=x<=100.              │
...
2
```

Fallan la versión y las imágenes.

### 6. Versión e imágenes

En `pyproject.toml`, `version = "0.35.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-35-test`, `local/observatorio:week-35` y `local/observatorio:week-35-notebook`.

```bash
uv run pytest -q
docker compose build app api
docker images local/observatorio
```

```
1400 passed
...
local/observatorio:week-35        ...   2.5GB
local/observatorio:week-34        ...   2.5GB
```

Sin dependencias nuevas, la imagen no crece.

### 7. Tu pronóstico, con tus datos

Ejecuta `pronosticar` con **tu** instantánea, y con varias opciones:

```bash
uv run observatorio pronosticar notebooks/instantanea.csv
uv run observatorio pronosticar notebooks/instantanea.csv --ventana 24
uv run observatorio pronosticar notebooks/instantanea.csv --paciencia 50
uv run observatorio pronosticar notebooks/instantanea.csv --semilla 7
uv run observatorio pronosticar notebooks/instantanea.csv --guardar pesos.pt
uv run observatorio pronosticar notebooks/instantanea.csv --etiqueta <una-etiqueta>
uv run observatorio pronosticar notebooks/instantanea.csv --etiqueta <una-etiqueta> --desde pesos.pt
```

Con los datos de ejemplo y la etiqueta Sur:

```
serie de Sur · ventanas de 8 valores · 243 para entrenar, 52 para validar, 53 para prueba
red convolucional, desde cero · 41 parámetros, 41 entrenables
...
pronóstico del siguiente valor · MAE en prueba: red 18.151 · referencia 18.104: la red no mejora la referencia
...
red convolucional, filtros congelados de pesos.pt · 41 parámetros, 25 entrenables
...
pronóstico del siguiente valor · MAE en prueba: red 17.948 · referencia 18.104: la red mejora la referencia
```

- ¿Baja la pérdida de validación, o sube desde el principio? ¿En qué época para, y con cuál se queda?
- ¿Mejora la red a la referencia? ¿Por cuánto? Compáralo con lo que dijo `red` la semana pasada.
- Con `--ventana 24`, ¿cambia algo? Si tu dominio tiene un ciclo, ¿de cuántas medidas es?
- Con `--paciencia 50`, ¿se queda con otra época? Con los datos de ejemplo, entrena 53 épocas y se queda con la misma, la 3.
- Con `--desde`, ¿cuántos parámetros entrena? Con la etiqueta Sur, "mejora" por 0,16; pero desde cero con `--semilla 7` da 17,889, y también "mejora". Con 53 valores de prueba, ¿significa algo (teoría 05, sección 5)?

`pesos.pt` es un archivo tuyo, de unos pocos KB: no lo subas al repositorio. Añade `*.pt` a tu `.gitignore`.

Añade a `informe/README.md`, en **Siguientes pasos**, una línea con el resultado de `pronosticar` y si cambia con otra semilla.

### 8. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_convolution.py tests/test_my_convolution.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `convolution.py` | borrar la línea `optimizer.zero_grad()` | |
| `convolution.py` | `shuffle=True` por `shuffle=False` | |
| `convolution.py` | borrar la línea `model.load_state_dict(best_state)` | |
| `convolution.py` | en el bucle, `copy.deepcopy(model.state_dict())` por `model.state_dict()` | |
| `convolution.py` | `if epoch - best >= patience:` por `if epoch - best > patience:` | |
| `convolution.py` | `seen = values[: train_end + window]` por `seen = values` | |
| `convolution.py` | borrar las dos líneas `if start is not None:` y `freeze(model)` | |
| `convolution.py` | `rows = ordered(frame)` por `rows = frame.dropna(subset=["valor"])` | |
| `convolution.py` | `torch.load(path, weights_only=True)` por `torch.load(path, weights_only=False)` | |
| `convolution.py` | después de `x, y = windows(...)`, barajar: `order = torch.randperm(len(y))` y `x, y = x[order], y[order]` | |
| `convolution.py` | `model(x[validation_end:]) * spread + center` por `model(x[validation_end:]) * spread` | |
| `cli.py` | `math.ceil(epochs / 5)` por `max(1, epochs // 5)` | |

Los doce mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el mutante que baraja las ventanas antes de repartir, ¿qué test falla? Ejecuta `pronosticar` con tu instantánea: ¿cambia el veredicto? ¿Por qué ese error no lo vería nadie sin un test (teoría 05, sección 2)?
- Sin `model.load_state_dict(best_state)`, ¿con qué época se queda la red? ¿Qué número de la salida de `pronosticar` deja de ser verdad?

Después, en `tests/test_my_convolution.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las etiquetas y los valores de tu dominio y las funciones de `test_validation.py` (`frame_of`, `noise`, `write`) y de `test_convolution.py` (`wave`, `two_labels`). Ideas:

- un ciclo de tu dominio (un día, una semana) y la red gana a la referencia por mucho;
- valores al azar de tu dominio, y la red no gana por más de una unidad;
- una etiqueta con pocas medidas, y el error de "hacen falta al menos";
- `--guardar` con una etiqueta y `--desde` con otra, y los parámetros entrenables;
- una tendencia que sube, y la referencia que sale solo de lo que ve el entrenamiento;
- `pronosticar` con la huella de tu instantánea, y el veredicto que esperas.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1405 tests en verde.

### 9. README y pull request

En el `README.md` de tu repositorio, añade una sección "Pronóstico": cómo ejecutar `pronosticar`, qué red se entrena y con qué reparto, cómo guardar y reutilizar los pesos, y el veredicto con tus datos en dos frases.

Commits sugeridos, en este orden:

1. `test: add convolutional forecast tests`
2. `feat: add convolution module`
3. `feat: add pronosticar command`
4. `chore: bump version to 0.35.0`
5. `docs: add forecast results to the report`
6. `test: add my convolution tests`

```bash
git push -u origin week-35
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-35` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `pronosticar` con tu instantánea (por defecto, con una etiqueta desde cero y con `--desde`), y tu lectura en tres frases: ¿baja la pérdida de validación?, ¿mejora la red a la referencia?, ¿se mantiene con otra semilla?
3. La tabla de mutantes del paso 8 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `test_fit_is_the_loop_by_hand` falla | Falta `optimizer.zero_grad()`, o los lotes no son de `BATCH` con `shuffle=True`, o la pérdida no es `MSELoss` |
| `test_fit_returns_the_model_at_its_best_epoch` falla | Falta `model.load_state_dict(best_state)`, o la copia no usa `copy.deepcopy` |
| `test_forecast_baseline_is_the_mean_of_what_training_sees` falla | El escalado usa toda la serie: `seen = values[: train_end + window]` |
| `test_forecast_follows_the_order_of_arrival` falla | Falta `ordered(frame)`, o `torch.manual_seed(seed)` no va antes de crear la red |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied` | La `Linear` de `cnn` recibe `channels * (size - KERNEL + 1)` |
| `RuntimeError: Given groups=1, weight of size [4, 1, 3], expected input[...] to have 1 channels` | Falta `.unsqueeze(1)` en `windows`: `(ventanas, 1, tamaño)` |
| `RuntimeError: Error(s) in loading state_dict for Sequential` con `--desde` | Los pesos son de una red con otra forma: guárdalos otra vez con este `pronosticar` |
| `error: ... no es un archivo de pesos` | El archivo trae algo más que tensores: `save` guarda el `state_dict`, no la red |
| `test_the_cli_loads_torch_only_for_red` falla | Importas `convolution` o `torch` al principio de `cli.py`: va dentro de `pronosticar` |

## Entrega

1. Rama `week-35` con `core/convolution.py`, el comando `pronosticar`, `loss_table` con `math.ceil`, las imágenes `week-35`, la versión `0.35.0` y al menos 6 tests tuyos en `test_my_convolution.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Pronóstico", e `informe/README.md` con el resultado en **Siguientes pasos**.
4. *Pull request* `week-35` → `main` con lo que pide el paso 9.

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Transfer learning](../2-practicas/ejercicio-04-transfer-learning/README.md) | **Proyecto** | [Semana 35](../README.md) |
