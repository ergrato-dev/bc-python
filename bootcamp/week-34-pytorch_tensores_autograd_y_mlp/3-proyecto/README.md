# Proyecto — Observatorio, capa 33: una red neuronal con PyTorch

> En la semana 33 pusiste a competir cinco modelos de scikit-learn. Esta semana entrenas tu primera red neuronal, y el bucle de entrenamiento lo escribes tú: predecir, medir la pérdida, `backward()`, `step()`. Instalas PyTorch solo para CPU, pasas tu instantánea a tensores sin fugas, y la red se mide en prueba frente a la misma referencia de siempre.

## Qué construyes

```
$ uv run observatorio red notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
red de 16 neuronas ocultas y 129 parámetros · 300 épocas · ritmo 0.01
Pérdida en entrenamiento (MSE del valor escalado)
┏━━━━━━━┳━━━━━━━━━┓
┃ Época ┃ Pérdida ┃
┡━━━━━━━╇━━━━━━━━━┩
│     1 │  1.0149 │
│    61 │  0.9812 │
│   121 │  0.9769 │
│   181 │  0.9767 │
│   241 │  0.9766 │
│   300 │  0.9765 │
└───────┴─────────┘
regresión del valor · MAE en prueba: red 20.261 · referencia 20.066: la red no mejora la referencia
```

Con los datos de ejemplo, la pérdida apenas baja de 1,01 a 0,98, y en prueba la red se equivoca algo más que la referencia: no hay señal que aprender en la etiqueta ni en la posición, como dijeron `hallazgos`, `modelo`, `ajustar` y `competir` (teoría 05, sección 4).

| Pieza | Qué hace |
|---|---|
| `core/neural.py` | `mlp` construye la red; `train` la entrena época a época y devuelve la pérdida de cada una; `learn` reparte, prepara, escala el valor, entrena y mide el MAE en prueba; `Training` guarda el resultado |
| `red INSTANTANEA` | La tabla de la pérdida y el veredicto, con `--huella`, `--oculta`, `--epocas`, `--ritmo` y `--semilla` |
| `pyproject.toml` | PyTorch 2.15.0 desde el índice de CPU |

Una dependencia nueva: `torch==2.15.0`, solo para CPU (teoría 05, sección 1).

```
src/observatorio/
├── cli.py                  # modificado: red
└── core/
    └── neural.py           # nuevo: sin reexportar en core/__init__.py
tests/
├── test_neural.py          # nuevo: los tests del bootcamp
├── test_my_neural.py       # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes week-34
├── test_notebook.py        # modificado: la imagen week-34-notebook
└── test_package.py         # modificado: neural en core, torch fijado y del índice de CPU, la versión 0.34.0
pyproject.toml              # modificado: torch, el índice de CPU y la versión
uv.lock                     # modificado: torch y sus dependencias
compose.yaml                # modificado: las imágenes week-34
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-34`. El `starter/` trae la capa 32 resuelta: `core/ensembles.py`, `core/clustering.py`, `competir` y `agrupar`. **Tú** instalas PyTorch y escribes `neural.py` y `red`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-33` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-34
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-34-pytorch_tensores_autograd_y_mlp/3-proyecto/starter
cp $STARTER/tests/test_neural.py $STARTER/tests/test_my_neural.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_notebook.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `test_neural.py`, con 47 tests, y `test_my_neural.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` y `test_notebook.py`, las imágenes `week-34`; `test_package.py`, `neural` es un módulo de `core`, `torch` está fijado y viene del índice de CPU, y la versión es `0.34.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.neural'
E   ModuleNotFoundError: No module named 'torch'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `test_neural.py`. Fíjate en:

- `by_hand()` y `test_train_is_the_loop_by_hand`: el bucle de la teoría 03 escrito paso a paso, con la misma semilla. Si tu `train` olvida `zero_grad()` o usa otro optimizador, las pérdidas no coinciden. Sin este test, nada fallaría: la red entrenaría igual, peor;
- `test_learn_scales_the_value`: con el valor escalado, la primera pérdida ronda 1. Sin escalar, ronda el cuadrado de tus valores;
- `test_learn_memorizes_noise_but_does_not_generalize`: con valores al azar, la pérdida de entrenamiento baja (memoriza) y el error en prueba queda como el de la referencia;
- `test_the_cli_loads_torch_only_for_red`: como con FastAPI y scikit-learn, un proceso nuevo importa la CLI y comprueba que `torch` no se ha cargado.

### 4. PyTorch solo para CPU

En `pyproject.toml`, **antes** de `[build-system]`, añade:

```toml
[[tool.uv.index]]
# Las ruedas de PyTorch solo para CPU: las de PyPI traen CUDA para Linux, más de 2 GB que
# tu proyecto no usa. `explicit`: de este índice solo sale lo que pide [tool.uv.sources].
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cpu" }
```

Después:

```bash
uv add torch==2.15.0
uv run python -c "import torch; print(torch.__version__)"
```

```
2.15.0+cpu
```

- `uv add` fija la versión en `dependencies` y añade a `uv.lock` torch y lo que necesita: filelock, fsspec, jinja2, networkx, sympy… En Linux y Windows, la versión `+cpu`; en macOS, la normal, que ya es solo para CPU.
- El orden importa: con el índice **después** de `uv add`, uv ya habría instalado la versión con CUDA. Si te pasó, añade el índice y ejecuta `uv lock --upgrade-package torch`.
- Sin `explicit = true`, `uv add` falla con `No solution found`: uv buscaría en ese índice paquetes que solo están completos en PyPI (teoría 05, sección 1).

```bash
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.neural'
E   ImportError: cannot import name 'neural' from 'observatorio.core' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

### 5. El módulo `neural.py`

Crea `src/observatorio/core/neural.py`:

```python
"""Una red neuronal pequeña (un MLP) en PyTorch, entrenada con un bucle escrito a mano.

Qué: mlp construye la red (una capa oculta con ReLU), train la entrena época a época
(predicción, pérdida, gradientes, paso del optimizador) y learn reparte las medidas,
prepara las entradas y el valor con el entrenamiento, entrena y mide el MAE en prueba
frente a la referencia, que predice siempre la media.
Para qué: scikit-learn esconde el bucle en `fit`; en PyTorch lo escribes tú, y ves cómo
baja la pérdida. Es el mismo bucle que entrena las redes grandes de la semana 35.
Impacto: importa torch, que tarda en cargarse: core/__init__.py no lo reexporta, y la CLI
lo importa solo en `red`.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from torch import nn

from observatorio.core.learning import SEED, split
from observatorio.core.validation import INPUTS, prepare

# Neuronas de la capa oculta, épocas (pasadas por todo el entrenamiento) y ritmo de
# aprendizaje de Adam: valores pequeños que entrenan en un segundo con miles de medidas.
HIDDEN = 16
EPOCHS = 300
RATE = 0.01


@dataclass(frozen=True)
class Training:
    """La pérdida de cada época y el MAE en prueba de la red y de la referencia."""

    parameters: int
    losses: tuple[float, ...]
    mae: float
    baseline: float

    @property
    def learned(self) -> bool:
        """Si la pérdida de la última época es menor que la de la primera."""
        return self.losses[-1] < self.losses[0]

    @property
    def improves(self) -> bool:
        """Si la red se equivoca menos que la referencia en prueba. Empatar no es mejorar."""
        return self.mae < self.baseline


def tensor(values: object) -> torch.Tensor:
    """Una tabla o una columna como tensor de float32, el tipo con el que trabaja nn."""
    return torch.from_numpy(np.asarray(values, dtype=np.float32))


def mlp(inputs: int, hidden: int = HIDDEN) -> nn.Sequential:
    """Entradas, una capa oculta con ReLU y una salida: el valor predicho."""
    return nn.Sequential(nn.Linear(inputs, hidden), nn.ReLU(), nn.Linear(hidden, 1))


def train(
    model: nn.Module, x: torch.Tensor, y: torch.Tensor, epochs: int, rate: float
) -> tuple[float, ...]:
    """Entrena con todas las medidas a la vez en cada época; devuelve la pérdida de cada una."""
    optimizer = torch.optim.Adam(model.parameters(), lr=rate)
    loss_function = nn.MSELoss()
    losses = []
    model.train()
    for _ in range(epochs):
        # Los gradientes se acumulan: sin ponerlos a cero, cada paso sumaría los anteriores.
        optimizer.zero_grad()
        loss = loss_function(model(x), y)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return tuple(losses)


def learn(
    frame: pd.DataFrame,
    hidden: int = HIDDEN,
    epochs: int = EPOCHS,
    rate: float = RATE,
    seed: int = SEED,
) -> Training:
    """Entrena un MLP que predice el valor y lo mide en prueba frente a la media."""
    train_rows, test_rows = split(frame, seed=seed)
    # sparse_threshold=0: siempre una matriz densa, aunque haya muchas etiquetas.
    prepared = prepare().set_params(sparse_threshold=0.0).fit(train_rows[INPUTS])
    x_train = tensor(prepared.transform(train_rows[INPUTS]))
    x_test = tensor(prepared.transform(test_rows[INPUTS]))
    # El valor también se escala: una red que empieza prediciendo cerca de 0 tardaría
    # cientos de épocas solo en llegar a valores de 50. Se escala con el entrenamiento.
    center, spread = float(train_rows["valor"].mean()), float(train_rows["valor"].std())
    y_train = tensor((train_rows["valor"] - center) / spread).reshape(-1, 1)
    y_test = tensor(test_rows["valor"]).reshape(-1, 1)
    # La semilla fija los pesos iniciales: sin ella, cada ejecución da otra red.
    torch.manual_seed(seed)
    model = mlp(x_train.shape[1], hidden)
    losses = train(model, x_train, y_train, epochs, rate)
    model.eval()
    with torch.no_grad():
        predicted = model(x_test) * spread + center
    return Training(
        sum(parameter.numel() for parameter in model.parameters()),
        losses,
        float((predicted - y_test).abs().mean()),
        float((y_test - center).abs().mean()),
    )
```

Por partes:

- **`Training`** guarda cuántos parámetros tiene la red, la pérdida de cada época y el MAE en prueba de la red y de la referencia. `learned` dice si la pérdida bajó; `improves`, si la red gana a la referencia. Empatar no es mejorar, como en `Score` de la semana 31.
- **`tensor`** convierte una tabla de NumPy o pandas en un tensor `float32`: las capas no aceptan `float64` (teoría 01). `from_numpy` no copia: `np.asarray` ya ha creado un array nuevo.
- **`mlp`** es la red de la teoría 04: entradas, una capa oculta de `hidden` neuronas con ReLU, y una salida.
- **`train`** es el bucle de la teoría 03, con Adam y el error cuadrático medio, y **todas** las medidas en cada época, sin mini-lotes: más sencillo, y con miles de medidas caben de sobra. Guarda `loss.item()`, no `loss`: un número, sin el grafo (teoría 02, sección 5).
- **`learn`** junta todo, en el orden de la teoría 05: reparte con `split` (semana 31), prepara las entradas con `prepare` (semana 32) ajustado **solo** con el entrenamiento, escala el valor con la media y la desviación del entrenamiento, fija la semilla, entrena, y predice en prueba deshaciendo el escalado. La referencia predice siempre la media del entrenamiento: su MAE es la distancia media de cada valor de prueba a esa media.

```bash
uv run pytest -q tests/test_neural.py
```

```
12 failed, 35 passed
```

Fallan los del comando. `uv run mypy` ya pasa.

### 6. El comando `red`

En `src/observatorio/cli.py`, añade `Training` a los imports del bloque `if TYPE_CHECKING:`:

```python
    from observatorio.core.neural import Training
```

Y después de `agrupar`:

```python
def loss_table(training: Training) -> Table:
    """La pérdida de entrenamiento en seis épocas: la primera, cuatro intermedias y la última."""
    epochs = len(training.losses)
    shown = sorted({*range(0, epochs, max(1, epochs // 5)), epochs - 1})
    table = Table(title="Pérdida en entrenamiento (MSE del valor escalado)")
    table.add_column("Época", justify="right")
    table.add_column("Pérdida", justify="right")
    for index in shown:
        table.add_row(str(index + 1), f"{training.losses[index]:.4f}")
    return table


@app.command()
def red(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    oculta: Annotated[int, typer.Option(min=1, help="Neuronas de la capa oculta.")] = 16,
    epocas: Annotated[
        int, typer.Option(min=1, max=10_000, help="Pasadas por todo el entrenamiento.")
    ] = 300,
    ritmo: Annotated[
        float, typer.Option(min=0.0001, max=1.0, help="El ritmo de aprendizaje de Adam.")
    ] = 0.01,
    semilla: Annotated[
        int, typer.Option(help="La semilla del reparto y de los pesos: la misma, la misma red.")
    ] = 31,
) -> None:
    """Entrena una red neuronal pequeña que predice el valor, y la compara con la referencia."""
    # Importar aquí: PyTorch tarda aún más que scikit-learn en cargarse.
    from observatorio.core import findings, neural

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        training = neural.learn(frame, oculta, epocas, ritmo, semilla)
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(
        f"red de {oculta} neuronas ocultas y {training.parameters} parámetros"
        f" · {epocas} épocas · ritmo {ritmo}"
    )
    out.print(loss_table(training))
    if not training.learned:
        out.print("la pérdida no bajó: prueba otro --ritmo o más --epocas")
    verdict = "mejora" if training.improves else "no mejora"
    out.print(
        f"regresión del valor · MAE en prueba: red {training.mae:.3f}"
        f" · referencia {training.baseline:.3f}: la red {verdict} la referencia"
    )
```

- **`loss_table`** no escribe 300 filas: escribe seis épocas, la primera, cuatro repartidas y la última. Con `--epocas 3`, las tres. `max(1, …)`: con menos de 5 épocas, `epochs // 5` sería 0, y `range` no admite un paso 0.
- **`--ritmo`** va de 0,0001 a 1: por debajo no aprende en ningún número razonable de épocas, y por encima de 1 Adam salta sin control.
- Si la pérdida no bajó, `red` lo avisa antes del veredicto: un veredicto de una red que no aprendió no dice nada de tus datos.

Actualiza el docstring del módulo: "veinticinco comandos", con `red` entre `agrupar` y `borrar`.

```bash
uv run pytest -q
uv run observatorio red notebooks/instantanea.csv --oculta 0; echo $?
```

```
4 failed, 1337 passed
...
│ Invalid value for '--oculta': 0 is not in the range x>=1.                    │
...
2
```

Fallan la versión y las imágenes.

### 7. Versión e imágenes

En `pyproject.toml`, `version = "0.34.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-34-test`, `local/observatorio:week-34` y `local/observatorio:week-34-notebook`.

```bash
uv run pytest -q
docker compose build app api
docker images local/observatorio
```

```
1341 passed
...
REPOSITORY           TAG             ...   SIZE
local/observatorio   week-34         ...   2.5GB
local/observatorio   week-34-test    ...   2.76GB
local/observatorio   week-33         ...   1.25GB
```

La imagen `runtime` dobla su tamaño, de 1,25 GB a 2,5 GB: PyTorch ocupa más que todo lo demás junto. Con la versión de CUDA serían varios GB más. El `Dockerfile` no cambia: `uv sync --locked` instala lo que dice `uv.lock`, y `uv.lock` ya apunta a las ruedas de CPU. La CI tarda algo más: descarga unos 200 MB de PyTorch en cada ejecución.

### 8. Tu red, con tus datos

Ejecuta `red` con **tu** instantánea y con varias opciones:

```bash
uv run observatorio red notebooks/instantanea.csv
uv run observatorio red notebooks/instantanea.csv --oculta 64 --epocas 2000
uv run observatorio red notebooks/instantanea.csv --ritmo 0.5
uv run observatorio red notebooks/instantanea.csv --semilla 7
uv run observatorio competir notebooks/instantanea.csv
```

- ¿Baja la pérdida? ¿Cuánto, desde la primera época hasta la última?
- ¿Mejora la red a la referencia? Compara su MAE con la media de la referencia y del mejor modelo en `competir`: ¿quién gana?
- Con `--oculta 64 --epocas 2000`, ¿baja más la pérdida de entrenamiento? ¿Y el MAE en prueba? Si uno baja y el otro no, ¿qué está pasando (teoría 04, sección 5)?
- Con `--semilla 7`, ¿cambia el veredicto? `red` mide con **un** reparto, no con pliegues: una diferencia de unas centésimas con la referencia puede ser suerte del reparto. Con los datos de ejemplo, `--epocas 50 --ritmo 0.0001` da "la red mejora la referencia" por dos centésimas, con una red que casi no ha entrenado.

Añade a `informe/README.md`, en **Siguientes pasos**, una línea con el resultado de `red` y si cambia con otra semilla.

### 9. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_neural.py tests/test_my_neural.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `neural.py` | borrar la línea `optimizer.zero_grad()` | |
| `neural.py` | `nn.ReLU()` por `nn.Identity()` | |
| `neural.py` | borrar la línea `torch.manual_seed(seed)` | |
| `neural.py` | `center, spread = float(...), float(...)` por `center, spread = 0.0, 1.0` | |
| `neural.py` | en `learned`, `<` por `<=` | |
| `neural.py` | `nn.MSELoss()` por `nn.L1Loss()` | |
| `neural.py` | `torch.optim.Adam(` por `torch.optim.SGD(` | |
| `neural.py` | `model(x_test) * spread + center` por `model(x_test) * spread` | |
| `neural.py` | `prepare().set_params(sparse_threshold=0.0)` por `prepare()` | |
| `neural.py` | `split(frame, seed=seed)` por `split(frame)` | |
| `cli.py` | en `loss_table`, `epochs // 5` por `epochs // 6` | |
| `cli.py` | `neural.learn(frame, oculta, epocas, ritmo, semilla)` por `neural.learn(frame, oculta, epocas, ritmo)` | |

Los doce mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Sin `optimizer.zero_grad()`, ¿qué test falla? Ejecuta `red` con tu instantánea con ese mutante: ¿da algún error? ¿Cómo cambia la tabla de la pérdida? ¿Por qué es el fallo más peligroso de PyTorch?
- Con el mutante que no escala el valor, ejecuta `red`: ¿en cuánto empieza la pérdida, y en cuánto acaba? ¿Por qué Adam con ritmo 0,01 no llega en 300 épocas (ejercicio 03, paso 6)?

Después, en `tests/test_my_neural.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las etiquetas y los valores de tu dominio y las funciones de `test_validation.py` (`frame_of`, `signal`, `noise`, `write`), de `test_ensembles.py` (`bump`) y de `test_neural.py` (`line`). Ideas:

- etiquetas de tu dominio que deciden el valor, y la red mejora la referencia;
- valores al azar de tu dominio, y la red no mejora por más de una unidad;
- un valor que sube y baja con la posición, y la red gana a la referencia por mucho;
- un ritmo de 1 con tus datos, y la pérdida no baja o salta;
- `--oculta 4`, y la tabla dice el número de parámetros que calculas a mano;
- `red` con la huella de tu instantánea, y el veredicto que esperas.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1346 tests en verde.

### 10. README y pull request

En el `README.md` de tu repositorio, añade una sección "Red neuronal": cómo ejecutar `red`, cómo se instala PyTorch solo para CPU y por qué, qué red se entrena, y el veredicto con tus datos en dos frases.

Commits sugeridos, en este orden:

1. `test: add neural network tests`
2. `build: add torch from the pytorch cpu index`
3. `feat: add neural module`
4. `feat: add red command`
5. `chore: bump version to 0.34.0`
6. `docs: add network results to the report`
7. `test: add my neural tests`

```bash
git push -u origin week-34
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-34` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `red` con tu instantánea (por defecto y con `--oculta 64 --epocas 2000`), y tu lectura en tres frases: ¿baja la pérdida?, ¿mejora la red a la referencia y al mejor modelo de `competir`?, ¿se mantiene con otra semilla?
3. La tabla de mutantes del paso 9 y las respuestas a sus dos preguntas.
4. El tamaño de tu imagen `week-34` frente a la `week-33`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `No solution found when resolving dependencies` al hacer `uv add torch` | Falta `explicit = true` en `[[tool.uv.index]]` |
| `torch.__version__` sin `+cpu` en Linux | Añadiste el índice después de `uv add`: `uv lock --upgrade-package torch` y `uv sync` |
| `test_torch_comes_from_the_cpu_index` falla | El nombre del índice tiene que ser `pytorch-cpu`, con la URL y `explicit = true` exactos |
| `RuntimeError: mat1 and mat2 must have the same dtype` | Falta `dtype=np.float32` en `tensor` |
| `ValueError: setting an array element with a sequence` con muchas etiquetas | Falta `set_params(sparse_threshold=0.0)`: `prepare()` devolvió una matriz dispersa |
| `test_train_is_the_loop_by_hand` falla | Falta `optimizer.zero_grad()`, o el optimizador no es Adam, o la pérdida no es `MSELoss` |
| `test_learn_uses_the_seed_for_the_split_and_the_weights` falla | Falta `torch.manual_seed(seed)` justo antes de `mlp(...)`, o `split` sin `seed=seed` |
| `UserWarning: Using a target size ... different to the input size` | Falta `.reshape(-1, 1)` en `y_train` |
| `test_the_cli_loads_torch_only_for_red` falla | Importas `neural` o `torch` al principio de `cli.py`: va dentro de `red` |
| La CI tarda mucho más en `uv sync` | Descarga PyTorch: unos 200 MB. Es normal |

## Entrega

1. Rama `week-34` con PyTorch 2.15.0 desde el índice de CPU, `core/neural.py`, el comando `red`, las imágenes `week-34`, la versión `0.34.0` y al menos 6 tests tuyos en `test_my_neural.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Red neuronal", e `informe/README.md` con el resultado en **Siguientes pasos**.
4. *Pull request* `week-34` → `main` con lo que pide el paso 10.

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Un MLP](../2-practicas/ejercicio-04-un-mlp/README.md) | **Proyecto** | [Semana 34](../README.md) |
