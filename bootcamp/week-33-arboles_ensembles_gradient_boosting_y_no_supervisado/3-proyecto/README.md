# Proyecto — Observatorio, capa 32: árboles, ensembles y grupos

> En la semana 32 ajustaste un modelo lineal y lo validaste pliegue a pliegue. Esta semana lo pones a competir con un árbol, un bosque y un *gradient boosting*, con los mismos pliegues y la misma preparación. Y das el primer paso sin respuesta que acertar: agrupas tus etiquetas por cómo se parecen, con KMeans, y mides si esos grupos existen.

## Qué construyes

```
$ uv run observatorio competir notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65 · pliegues al azar
regresión del valor · MAE en cada pliegue
┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Modelo     ┃      1 ┃      2 ┃      3 ┃      4 ┃      5 ┃  Media ┃   Gana ┃
┡━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ referencia │ 20.275 │ 19.598 │ 19.820 │ 19.873 │ 20.209 │ 19.955 │        │
│ lineal     │ 20.366 │ 19.583 │ 19.807 │ 19.849 │ 20.227 │ 19.966 │ 3 de 5 │
│ árbol      │ 20.556 │ 19.718 │ 20.256 │ 20.080 │ 20.809 │ 20.284 │ 0 de 5 │
│ bosque     │ 21.139 │ 20.668 │ 20.496 │ 21.216 │ 21.165 │ 20.937 │ 0 de 5 │
│ boosting   │ 21.056 │ 20.740 │ 20.603 │ 21.060 │ 21.171 │ 20.926 │ 0 de 5 │
└────────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
regresión del valor: ningún modelo mejora la media de la referencia
clasificación del nivel · exactitud equilibrada en cada pliegue
┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Modelo     ┃     1 ┃     2 ┃     3 ┃     4 ┃     5 ┃ Media ┃   Gana ┃
┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ referencia │ 0.333 │ 0.333 │ 0.333 │ 0.333 │ 0.333 │ 0.333 │        │
│ lineal     │ 0.333 │ 0.333 │ 0.333 │ 0.333 │ 0.333 │ 0.333 │ 0 de 5 │
│ árbol      │ 0.328 │ 0.328 │ 0.339 │ 0.324 │ 0.327 │ 0.329 │ 1 de 5 │
│ bosque     │ 0.361 │ 0.349 │ 0.292 │ 0.317 │ 0.354 │ 0.335 │ 3 de 5 │
│ boosting   │ 0.334 │ 0.327 │ 0.313 │ 0.339 │ 0.352 │ 0.333 │ 3 de 5 │
└────────────┴───────┴───────┴───────┴───────┴───────┴───────┴────────┘
clasificación del nivel: el mejor es bosque, gana en 3 de 5 pliegues: no mejora la referencia
```

Con los datos de ejemplo, los modelos más flexibles salen **peor** que la referencia en la regresión: el árbol, el bosque y el boosting aprenden el ruido de cada entrenamiento y lo repiten en la prueba (teoría 02, sección 1). En la clasificación, el bosque tiene la mejor media por dos milésimas, y gana en tres pliegues de cinco: no basta.

```
$ uv run observatorio agrupar notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
Grupos de etiquetas
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Etiqueta ┃ Grupo ┃ Media ┃ Mediana ┃ Desviación ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━┩
│ Centro   │     1 │  38.2 │    38.7 │       23.1 │
│ Este     │     1 │  39.8 │    38.6 │       23.6 │
│ Norte    │     1 │  40.4 │    39.1 │       23.2 │
│ Oeste    │     1 │  39.3 │    37.9 │       22.8 │
│ Sur      │     2 │  40.7 │    41.8 │       22.8 │
└──────────┴───────┴───────┴─────────┴────────────┘
2 grupos · silueta 0.28: grupos que se solapan
```

KMeans devuelve dos grupos porque se los pides. La silueta, 0,28, dice que se solapan: las cinco zonas se parecen demasiado para separarlas (teoría 04, sección 4).

| Pieza | Qué hace |
|---|---|
| `core/ensembles.py` | `candidates` da cinco modelos, de más sencillo a más flexible; `compete` los mide con los mismos pliegues; `Contest` dice cuál tiene la mejor media y si gana a la referencia en todos los pliegues |
| `core/clustering.py` | `profiles` resume cada etiqueta; `cluster` las agrupa con KMeans y mide la silueta |
| `competir INSTANTANEA` | Una tabla por tarea, con `--huella`, `--pliegues` y `--tiempo` |
| `agrupar INSTANTANEA` | La tabla de grupos y la silueta, con `--huella` y `--grupos` |

Sin dependencias nuevas: los árboles, los ensembles y KMeans están en scikit-learn 1.9.1.

```
src/observatorio/
├── cli.py                  # modificado: competir y agrupar
└── core/
    ├── ensembles.py        # nuevo: sin reexportar en core/__init__.py
    └── clustering.py       # nuevo: sin reexportar en core/__init__.py
tests/
├── test_ensembles.py       # nuevo: los tests del bootcamp
├── test_clustering.py      # nuevo: los tests del bootcamp
├── test_my_ensembles.py    # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes week-33
├── test_notebook.py        # modificado: la imagen week-33-notebook
└── test_package.py         # modificado: ensembles y clustering en core, y la versión 0.33.0
pyproject.toml              # modificado: la versión
compose.yaml                # modificado: las imágenes week-33
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-33`. El `starter/` trae la capa 31 resuelta: `core/validation.py` y el comando `ajustar`. **Tú** escribes `ensembles.py`, `clustering.py`, `competir` y `agrupar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-32` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-33
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/3-proyecto/starter
cp $STARTER/tests/test_ensembles.py $STARTER/tests/test_clustering.py $STARTER/tests/test_my_ensembles.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_notebook.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `test_ensembles.py`, con 51 tests; `test_clustering.py`, con 26 (uno con Hypothesis); y `test_my_ensembles.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` y `test_notebook.py`, las imágenes `week-33`; `test_package.py`, `ensembles` y `clustering` son módulos de `core` y la versión es `0.33.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ImportError: cannot import name 'clustering' from 'observatorio.core' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee los dos archivos de tests. Fíjate en:

- `bump()`, en `test_ensembles.py`: el valor es alto en el tercio del medio de las posiciones y bajo en los otros dos. Una recta no puede dibujar eso; un árbol, con dos cortes, sí (teoría 01). `signal()` y `noise()` vienen de `test_validation.py`;
- `test_compete_uses_the_same_folds_and_preparation_for_every_model`: calcula a mano cada modelo con `KFold` y la semilla. Si un modelo usara otros pliegues, la comparación no sería justa;
- `test_improves_looks_at_the_best_not_at_any_model`: "mejora" se decide con el modelo de mejor media, no con cualquiera que gane;
- `test_cluster_scales_the_profiles`: cuatro etiquetas en las que, sin escalar, la desviación decide sola los grupos (teoría 04, sección 2);
- `test_cluster_is_repeatable`: sin semilla, KMeans empieza por otros centros cada vez.

### 4. El módulo `ensembles.py`

Crea `src/observatorio/core/ensembles.py`:

```python
"""Árboles y ensembles frente al modelo lineal y la referencia, en los mismos pliegues.

Qué: compete mide cinco modelos (la referencia, el lineal, un árbol, un bosque y un
gradient boosting) con la misma preparación y los mismos pliegues de validation, y dice
cuál tiene la mejor media y en cuántos pliegues gana cada uno a la referencia.
Para qué: un modelo más flexible no es mejor por serlo; solo lo es si gana, pliegue a
pliegue, con tus datos.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `competir`.
"""

from dataclasses import dataclass
from statistics import mean
from typing import Literal

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from observatorio.core.learning import SEED
from observatorio.core.validation import INPUTS, folds, ordered, prepare

BASELINE = "referencia"
# Profundidad del árbol y hojas mínimas del bosque: sin límite, los dos memorizan el ruido.
DEPTH = 4
LEAF = 5
TREES = 100


@dataclass(frozen=True)
class Contest:
    """La métrica de cada modelo en cada pliegue; la referencia, con su nombre."""

    task: str
    metric: str
    higher_is_better: bool
    scores: dict[str, tuple[float, ...]]

    @property
    def means(self) -> dict[str, float]:
        """La media de los pliegues de cada modelo, en el orden de scores."""
        return {name: mean(values) for name, values in self.scores.items()}

    @property
    def wins(self) -> dict[str, int]:
        """En cuántos pliegues gana cada modelo a la referencia. Empatar no es ganar."""
        baseline = self.scores[BASELINE]
        sign = 1 if self.higher_is_better else -1
        return {
            name: sum(
                sign * (score - other) > 0 for score, other in zip(values, baseline, strict=True)
            )
            for name, values in self.scores.items()
            if name != BASELINE
        }

    @property
    def best(self) -> str:
        """El modelo con la mejor media; en un empate, el primero (el más sencillo)."""
        means = self.means
        pick = max if self.higher_is_better else min
        return pick(means, key=means.__getitem__)

    @property
    def improves(self) -> bool:
        """Si el mejor no es la referencia y le gana en todos los pliegues."""
        best = self.best
        return best != BASELINE and self.wins[best] == len(self.scores[BASELINE])


def candidates(target: Literal["valor", "nivel"]) -> dict[str, BaseEstimator]:
    """Los cinco modelos, de más sencillo a más flexible, con la semilla fija."""
    if target == "valor":
        return {
            BASELINE: DummyRegressor(strategy="mean"),
            "lineal": Ridge(),
            "árbol": DecisionTreeRegressor(max_depth=DEPTH, random_state=SEED),
            "bosque": RandomForestRegressor(TREES, min_samples_leaf=LEAF, random_state=SEED),
            "boosting": HistGradientBoostingRegressor(random_state=SEED),
        }
    return {
        BASELINE: DummyClassifier(strategy="most_frequent"),
        "lineal": LogisticRegression(),
        "árbol": DecisionTreeClassifier(max_depth=DEPTH, random_state=SEED),
        "bosque": RandomForestClassifier(TREES, min_samples_leaf=LEAF, random_state=SEED),
        "boosting": HistGradientBoostingClassifier(random_state=SEED),
    }


def compete(
    frame: pd.DataFrame,
    target: Literal["valor", "nivel"],
    n_splits: int = 5,
    by_time: bool = False,
) -> Contest:
    """Mide los cinco modelos del valor (MAE) o del nivel (exactitud equilibrada) con los
    mismos pliegues y la misma preparación."""
    rows = ordered(frame)
    x, y = rows[INPUTS], rows[target]
    if target == "valor":
        task, metric, scoring = "regresión del valor", "MAE", "neg_mean_absolute_error"
    else:
        task, metric = "clasificación del nivel", "exactitud equilibrada"
        scoring = "balanced_accuracy"
    sign = -1 if target == "valor" else 1
    scores = {}
    for name, model in candidates(target).items():
        pipeline = Pipeline([("prepare", prepare()), ("model", model)])
        values = cross_val_score(pipeline, x, y, scoring=scoring, cv=folds(n_splits, by_time))
        scores[name] = tuple(float(sign * value) for value in values)
    return Contest(task, metric, target != "valor", scores)
```

Por partes:

- **`Contest`** guarda la métrica de cada modelo en cada pliegue, con la referencia dentro, como un modelo más. `means` da la media de cada uno; `wins`, en cuántos pliegues gana cada uno a la referencia (empatar no es ganar, y `sign` da la vuelta cuando menos es mejor); `best`, el de mejor media: `max` o `min` devuelven el **primero** en un empate, el más sencillo. `improves` exige que el mejor no sea la referencia y que le gane en **todos** los pliegues, como `ajustar`.
- **`candidates`** da los cinco modelos en orden, de más sencillo a más flexible. El árbol, limitado a 4 niveles (`DEPTH`); el bosque, 100 árboles con al menos 5 medidas por hoja (`LEAF`); el boosting, con los valores por defecto de `HistGradientBoosting*`. Los tres con `random_state=SEED`: sin semilla, el bosque y el boosting dan otro número cada vez (teorías 02 y 03).
- **`compete`** reutiliza `ordered`, `prepare`, `folds` e `INPUTS` de la semana 32: las mismas medidas, la misma preparación y los **mismos** pliegues para los cinco. Aquí no hay búsqueda de hiperparámetros: los valores de `candidates` son razonables, y una búsqueda por modelo multiplicaría el tiempo por veinticinco. Si la quieres, ya sabes hacerla anidada (semana 32).

```bash
uv run pytest -q tests/test_ensembles.py
```

```
13 failed, 38 passed
```

Fallan los del comando. `uv run mypy` todavía da errores: `test_clustering.py` importa un módulo que no existe.

### 5. El comando `competir`

En `src/observatorio/cli.py`, añade `Contest` a los imports del bloque `if TYPE_CHECKING:`:

```python
    from observatorio.core.ensembles import Contest
```

Y después de `ajustar`:

```python
def contest_table(contest: Contest) -> Table:
    """Una fila por modelo: la métrica en cada pliegue, la media y en cuántos gana a la
    referencia."""
    folds = len(next(iter(contest.scores.values())))
    table = Table(title=f"{contest.task} · {contest.metric} en cada pliegue")
    table.add_column("Modelo")
    for number in range(1, folds + 1):
        table.add_column(str(number), justify="right")
    table.add_column("Media", justify="right")
    table.add_column("Gana", justify="right")
    wins = contest.wins
    for name, scores in contest.scores.items():
        won = f"{wins[name]} de {folds}" if name in wins else ""
        cells = [f"{score:.3f}" for score in scores]
        table.add_row(name, *cells, f"{contest.means[name]:.3f}", won)
    return table


@app.command()
def competir(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    pliegues: Annotated[int, typer.Option(min=2, max=10, help="En cuántas partes se reparte.")] = 5,
    tiempo: Annotated[
        bool, typer.Option(help="Pliegues por tiempo: cada prueba, después de su entrenamiento.")
    ] = False,
) -> None:
    """Compara la referencia, el modelo lineal, un árbol, un bosque y un boosting, pliegue a
    pliegue."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import ensembles, findings

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        contests = [
            ensembles.compete(frame, "valor", pliegues, tiempo),
            ensembles.compete(frame, "nivel", pliegues, tiempo),
        ]
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    order = "por tiempo" if tiempo else "al azar"
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest} · pliegues {order}")
    for contest in contests:
        out.print(contest_table(contest))
        best = contest.best
        if best == ensembles.BASELINE:
            out.print(f"{contest.task}: ningún modelo mejora la media de la referencia")
            continue
        verdict = "mejora" if contest.improves else "no mejora"
        out.print(
            f"{contest.task}: el mejor es {best}, gana en {contest.wins[best]} de"
            f" {pliegues} pliegues: {verdict} la referencia"
        )
```

- La tabla tiene una columna por pliegue: con `--pliegues 3`, tres. La referencia deja vacía la columna "Gana": no compite consigo misma.
- Si el de mejor media es la referencia, no tiene sentido decir en cuántos pliegues se gana a sí misma: lo dice así, y pasa a la tarea siguiente con `continue`.
- Tarda: son cinco modelos por cinco pliegues, dos veces. El bosque es el más lento.

```bash
uv run pytest -q tests/test_ensembles.py
uv run observatorio competir notebooks/instantanea.csv --pliegues 3 --tiempo
```

```
51 passed
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65 · pliegues por tiempo
regresión del valor · MAE en cada pliegue
┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Modelo     ┃      1 ┃      2 ┃      3 ┃  Media ┃   Gana ┃
┡━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ referencia │ 20.175 │ 19.908 │ 19.199 │ 19.761 │        │
│ lineal     │ 20.176 │ 20.016 │ 19.155 │ 19.783 │ 1 de 3 │
│ árbol      │ 20.164 │ 19.907 │ 37.027 │ 25.699 │ 2 de 3 │
│ bosque     │ 20.369 │ 20.003 │ 19.689 │ 20.020 │ 0 de 3 │
│ boosting   │ 20.420 │ 20.841 │ 19.914 │ 20.392 │ 0 de 3 │
└────────────┴────────┴────────┴────────┴────────┴────────┘
regresión del valor: ningún modelo mejora la media de la referencia
clasificación del nivel · exactitud equilibrada en cada pliegue
┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Modelo     ┃     1 ┃     2 ┃     3 ┃ Media ┃   Gana ┃
┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ referencia │ 0.333 │ 0.333 │ 0.333 │ 0.333 │        │
│ lineal     │ 0.333 │ 0.333 │ 0.333 │ 0.333 │ 0 de 3 │
│ árbol      │ 0.333 │ 0.333 │ 0.305 │ 0.324 │ 0 de 3 │
│ bosque     │ 0.335 │ 0.333 │ 0.333 │ 0.334 │ 1 de 3 │
│ boosting   │ 0.333 │ 0.318 │ 0.333 │ 0.328 │ 0 de 3 │
└────────────┴───────┴───────┴───────┴───────┴────────┘
clasificación del nivel: el mejor es bosque, gana en 1 de 3 pliegues: no mejora la referencia
```

Mira el árbol **por tiempo**, en el pliegue 3: un error de 37, casi el doble que la referencia, y aun así gana en dos pliegues de tres. Un árbol no extrapola: las posiciones de la última prueba son más altas que todas las que vio, y las 473 caen en la misma hoja, la última, que guarda **una sola** medida de entrenamiento: predice 1,4 para todas (teoría 01, sección 5). Por eso `competir` decide con la **media** quién es el mejor, y con los **pliegues** si mejora.

### 6. El módulo `clustering.py`

Crea `src/observatorio/core/clustering.py`:

```python
"""Grupos de etiquetas que se parecen, sin decirle al modelo cuáles son.

Qué: profiles resume cada etiqueta (media, mediana y desviación de sus valores) y cluster
reparte esos perfiles en k grupos con KMeans, después de escalarlos, y mide con la
silueta lo separados que quedan.
Para qué: es aprendizaje no supervisado: no hay una respuesta que acertar. KMeans siempre
devuelve k grupos, también con datos sin estructura; la silueta dice si merecen ese nombre.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `agrupar`.
"""

from dataclasses import dataclass

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from observatorio.core.learning import SEED

# Desde qué silueta se habla de grupos separados: de -1 (mal repartidos) a 1 (muy separados).
SEPARATED = 0.5


@dataclass(frozen=True)
class Clustering:
    """El grupo de cada etiqueta, numerado desde 1 por orden alfabético, y la silueta."""

    groups: dict[str, int]
    silhouette: float

    @property
    def separated(self) -> bool:
        """Si la silueta llega a SEPARATED: por debajo, los grupos se solapan."""
        return self.silhouette >= SEPARATED


def profiles(frame: pd.DataFrame) -> pd.DataFrame:
    """Una fila por etiqueta, en orden alfabético: la media, la mediana y la desviación de
    sus valores, sin las medidas que no lo tienen. Con una sola medida no hay desviación: 0."""
    table = (
        frame.dropna(subset=["valor"])
        .groupby("etiqueta")
        .agg(media=("valor", "mean"), mediana=("valor", "median"), desviacion=("valor", "std"))
    )
    return table.fillna({"desviacion": 0.0})


def cluster(frame: pd.DataFrame, k: int = 2) -> Clustering:
    """Reparte las etiquetas en k grupos con KMeans sobre sus perfiles escalados."""
    table = profiles(frame)
    if not 2 <= k < len(table):
        raise ValueError(f"con {len(table)} etiquetas, los grupos van de 2 a {len(table) - 1}")
    # Escalar: si no, la columna con números más grandes decidiría sola las distancias.
    pipeline = make_pipeline(StandardScaler(), KMeans(k, n_init=10, random_state=SEED))
    found = pipeline.fit_predict(table)
    silhouette = float(silhouette_score(pipeline[:-1].transform(table), found))
    # KMeans numera los grupos al azar: aquí, por orden de aparición, para que no cambien.
    numbers: dict[int, int] = {}
    for group in found:
        numbers.setdefault(int(group), len(numbers) + 1)
    groups = {str(label): numbers[int(group)] for label, group in zip(table.index, found)}
    return Clustering(groups, silhouette)
```

Por partes:

- **`profiles`** resume cada etiqueta en tres números: media, mediana y desviación. `groupby` las ordena por orden alfabético. Una etiqueta con una sola medida no tiene desviación (`NaN`), y KMeans no admite huecos: se rellena con 0. Aquí no se usa `known`: sus comprobaciones son para clasificar niveles, y agrupar no los necesita.
- **`cluster`** comprueba `k`: con 5 etiquetas, de 2 a 4. Con 1, todo es un grupo; con 5, cada etiqueta es el suyo, y la silueta no se puede calcular.
- **`StandardScaler`** antes de KMeans: las distancias mezclan las tres columnas, y sin escalar mandaría la que tiene números más grandes (teoría 04, sección 2).
- **`n_init=10, random_state=SEED`**: KMeans empieza con centros al azar y puede quedarse en un mal reparto. Prueba diez comienzos, se queda con el mejor, y siempre los mismos.
- **La silueta** se mide con los perfiles **escalados**, los mismos que vio KMeans: `pipeline[:-1]` es el pipeline sin su último paso.
- **La numeración**: KMeans llama a los grupos 0, 1, 2… en un orden que depende de cómo empezó. Aquí se renumeran por orden de aparición: el grupo de la primera etiqueta es el 1, el siguiente grupo nuevo, el 2… El mismo reparto da siempre los mismos números.

```bash
uv run pytest -q
uv run mypy
```

```
12 failed, 1280 passed
...
Success: no issues found in ... source files
```

Fallan los de `agrupar`, la versión y las imágenes.

### 7. El comando `agrupar`

Añade `Clustering` a los imports del bloque `if TYPE_CHECKING:`:

```python
    from observatorio.core.clustering import Clustering
```

Y después de `competir`:

```python
def clustering_table(frame: pd.DataFrame, clustering: Clustering) -> Table:
    """Una fila por etiqueta: su grupo y su perfil."""
    table = Table(title="Grupos de etiquetas")
    for name in ("Etiqueta", "Grupo", "Media", "Mediana", "Desviación"):
        table.add_column(name, justify="left" if name == "Etiqueta" else "right")
    for label, row in frame.iterrows():
        table.add_row(
            str(label),
            str(clustering.groups[str(label)]),
            f"{row['media']:.1f}",
            f"{row['mediana']:.1f}",
            f"{row['desviacion']:.1f}",
        )
    return table


@app.command()
def agrupar(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    grupos: Annotated[
        int, typer.Option("--grupos", "-g", min=2, help="En cuántos grupos se reparten.")
    ] = 2,
) -> None:
    """Agrupa las etiquetas que se parecen con KMeans, y mide con la silueta si se separan."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import clustering, findings

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        result = clustering.cluster(frame, grupos)
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(clustering_table(clustering.profiles(frame), result))
    verdict = "grupos separados" if result.separated else "grupos que se solapan"
    out.print(f"{grupos} grupos · silueta {result.silhouette:.2f}: {verdict}")
```

- `--grupos` (o `-g`) empieza en 2: Typer rechaza 1 con código 2. El máximo depende de tus etiquetas: lo comprueba `cluster`, con código 1.
- `frame.iterrows()` recorre los perfiles fila a fila: cinco filas, una por etiqueta, sin problema de velocidad.

Actualiza el docstring del módulo: "veinticuatro comandos", con `competir` y `agrupar` entre `ajustar` y `borrar`.

```bash
uv run pytest -q
uv run observatorio agrupar notebooks/instantanea.csv -g 5; echo $?
```

```
4 failed, 1288 passed
error: con 5 etiquetas, los grupos van de 2 a 4
1
```

### 8. Versión e imágenes

En `pyproject.toml`, `version = "0.33.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-33-test`, `local/observatorio:week-33` y `local/observatorio:week-33-notebook`.

```bash
uv run pytest -q
```

```
1292 passed
```

### 9. Tus modelos y tus grupos, con tus datos

Ejecuta los dos comandos con **tu** instantánea, y compáralos con `ajustar` de la semana 32:

```bash
uv run observatorio competir notebooks/instantanea.csv
uv run observatorio competir notebooks/instantanea.csv --tiempo
uv run observatorio agrupar notebooks/instantanea.csv
uv run observatorio agrupar notebooks/instantanea.csv -g 3
```

- ¿Qué modelo tiene la mejor media? Si es el árbol, el bosque o el boosting y gana en todos los pliegues, tu dominio tiene algo que una recta no dibuja: ¿qué puede ser?
- ¿Empeora algún modelo con `--tiempo`? Si es un árbol, mira si es el último pliegue: no extrapola.
- ¿Qué silueta da `agrupar` con 2 y con 3 grupos? Si alguna pasa de 0,5, ¿tienen sentido esos grupos en tu dominio? Si ninguna pasa, ¿cuadra con lo que dijo `hallazgos` en la semana 30?

Añade a `informe/README.md`, en **Siguientes pasos**, una línea con el resultado de `competir` y otra con el de `agrupar`. `test_informe.py` sigue pasando: no comprueba esa sección.

### 10. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_ensembles.py tests/test_clustering.py tests/test_my_ensembles.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `ensembles.py` | en `wins`, `> 0` por `>= 0` | |
| `ensembles.py` | en `best`, `max if self.higher_is_better else min` por `min if self.higher_is_better else max` | |
| `ensembles.py` | `DEPTH = 4` por `DEPTH = None` | |
| `ensembles.py` | `LEAF = 5` por `LEAF = 1` | |
| `ensembles.py` | `"boosting": HistGradientBoostingRegressor(random_state=SEED)` por `"boosting": RandomForestRegressor(random_state=SEED)` | |
| `ensembles.py` | `scoring = "balanced_accuracy"` por `scoring = "accuracy"` | |
| `ensembles.py` | en `compete`, `cv=folds(n_splits, by_time)` por `cv=folds(n_splits, False)` | |
| `clustering.py` | `make_pipeline(StandardScaler(), KMeans(...))` por `make_pipeline(KMeans(...))` | |
| `clustering.py` | `n_init=10, random_state=SEED` por `n_init=1` | |
| `clustering.py` | `silhouette_score(pipeline[:-1].transform(table), found)` por `silhouette_score(table, found)` | |
| `clustering.py` | `numbers.setdefault(int(group), len(numbers) + 1)` por `numbers.setdefault(int(group), int(group) + 1)` | |
| `cli.py` | en `agrupar`, `clustering.cluster(frame, grupos)` por `clustering.cluster(frame)` | |

Los doce mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con `DEPTH = None`, ¿qué test falla? Ejecuta `competir` con tu instantánea con ese mutante puesto: ¿cómo cambia el error del árbol? ¿Por qué un árbol sin límite no se equivoca nada en entrenamiento y tanto en prueba?
- Con el de `StandardScaler`, ejecuta `agrupar` con tu instantánea: ¿cambian los grupos? ¿Qué columna de tus perfiles tiene los números más grandes, y por qué decide ella?

Después, en `tests/test_my_ensembles.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las etiquetas y los valores de tu dominio y las funciones de `test_validation.py` (`frame_of`, `signal`, `noise`, `write`) y de `test_ensembles.py` (`bump`). Ideas:

- un valor de tu dominio que sube y baja a lo largo del día, y un árbol gana al lineal;
- etiquetas de tu dominio que deciden el valor, y los cinco modelos ganan a la referencia;
- valores al azar, y `compete` no mejora;
- dos grupos de etiquetas de tu dominio que se separan, y `separated` es `True`;
- una etiqueta con una sola medida, y `cluster` no falla;
- `agrupar -g 3` con tu instantánea, y tres números de grupo en la tabla.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1297 tests en verde.

### 11. README y pull request

En el `README.md` de tu repositorio, añade una sección "Modelos y grupos": cómo ejecutar `competir` y `agrupar`, qué cinco modelos compiten, con qué se agrupan las etiquetas, y el veredicto con tus datos en dos frases.

Commits sugeridos, en este orden:

1. `test: add ensembles and clustering tests`
2. `feat: add ensembles module`
3. `feat: add competir command`
4. `feat: add clustering module`
5. `feat: add agrupar command`
6. `chore: bump version to 0.33.0`
7. `docs: add model and cluster results to the report`
8. `test: add my ensembles tests`

```bash
git push -u origin week-33
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-33` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `competir` (al azar y por tiempo) y de `agrupar` con tu instantánea, y tu lectura en tres frases: ¿algún modelo mejora la referencia?, ¿cuál tiene la mejor media y por qué crees que es ese?, ¿hay grupos de verdad?
3. La tabla de mutantes del paso 10 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'ensembles' from 'observatorio.core'` | Falta el paso 4, o el archivo no está en `src/observatorio/core/` |
| `test_compete_is_repeatable` falla | Falta `random_state=SEED` en algún modelo de `candidates` |
| `test_candidates_go_from_simple_to_flexible` falla | Los nombres o el orden de `candidates`: `referencia`, `lineal`, `árbol`, `bosque`, `boosting`, con tilde |
| `test_best_in_a_tie_is_the_first` falla | `max(means, key=means.__getitem__)`: con `sorted` o `reverse`, un empate puede devolver otro |
| `ValueError: Input X contains NaN` en `cluster` | Una etiqueta con una sola medida: falta `fillna({"desviacion": 0.0})` |
| `test_cluster_numbers_the_groups_in_alphabetical_order` falla | Devuelves los números de KMeans: renuméralos por orden de aparición |
| `UserWarning: y_pred contains classes not in y_true` con `--tiempo` | Un pliegue de prueba no tiene algún nivel: es un aviso, no un error |
| `competir` tarda mucho | Cinco modelos por pliegue, y el bosque entrena 100 árboles. Con decenas de miles de medidas, baja `--pliegues` |

## Entrega

1. Rama `week-33` con `core/ensembles.py`, `core/clustering.py`, los comandos `competir` y `agrupar`, las imágenes `week-33`, la versión `0.33.0` y al menos 6 tests tuyos en `test_my_ensembles.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Modelos y grupos", e `informe/README.md` con los resultados en **Siguientes pasos**.
4. *Pull request* `week-33` → `main` con lo que pide el paso 11.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Agrupar y reducir](../2-practicas/ejercicio-04-agrupar-y-reducir/README.md) | **Proyecto · Árboles, ensembles y grupos** | [Webgrafía](../4-recursos/webgrafia/README.md) |
