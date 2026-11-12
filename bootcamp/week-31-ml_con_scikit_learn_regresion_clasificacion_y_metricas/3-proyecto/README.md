# Proyecto — Observatorio, capa 30: tu primer modelo

> Abre la fase 5. En la semana 30 preguntaste si tus etiquetas difieren; esta semana preguntas si saber la etiqueta ayuda a **predecir**. Entrenas una regresión del valor y una clasificación del nivel con scikit-learn, las mides con medidas que no vieron y las comparas con una referencia que no sabe nada.

## Qué construyes

```
$ uv run observatorio modelo notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
regresión del valor · 1420 para entrenar, 474 para probar
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Métrica ┃ Modelo ┃ Referencia ┃ ¿Mejora? ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ MAE     │ 20.103 │     20.066 │ no       │
│ RMSE    │ 23.232 │     23.162 │ no       │
│ R²      │ -0.006 │     -0.000 │ no       │
└─────────┴────────┴────────────┴──────────┘
regresión del valor: el modelo no mejora la referencia
clasificación del nivel · 1420 para entrenar, 474 para probar
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Métrica               ┃ Modelo ┃ Referencia ┃ ¿Mejora? ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ exactitud equilibrada │  0.333 │      0.333 │ no       │
│ exactitud             │  0.502 │      0.502 │ no       │
│ F1 macro              │  0.223 │      0.223 │ no       │
└───────────────────────┴────────┴────────────┴──────────┘
clasificación del nivel: el modelo no mejora la referencia
```

Con los datos de ejemplo del starter, ninguno de los dos modelos mejora su referencia: es la misma conclusión que el informe de la semana 30, "ninguna zona difiere", por otro camino (teoría 05, sección 6). Con los datos de tu dominio puede salir otra cosa.

| Pieza | Qué hace |
|---|---|
| `core/learning.py` | `known` quita las medidas sin valor; `features` convierte la etiqueta en columnas one-hot; `split` reparte con semilla y estratificado por nivel; `regress` y `classify` entrenan cada modelo y su referencia y devuelven sus métricas en prueba |
| `modelo INSTANTANEA` | Escribe una tabla por modelo, con `--huella`, `--prueba` y `--semilla` |
| `.pre-commit-config.yaml` | El gancho de espacios finales deja de tocar los SVG de matplotlib |

Una dependencia nueva: **scikit-learn 1.9.1**.

```
src/observatorio/
├── cli.py                  # modificado: modelo
└── core/
    └── learning.py         # nuevo: sin reexportar en core/__init__.py
tests/
├── test_learning.py        # nuevo: los tests del bootcamp
├── test_my_learning.py     # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes week-31 y el gancho de los SVG
├── test_notebook.py        # modificado: la imagen week-31-notebook
└── test_package.py         # modificado: learning en core, scikit-learn y la versión 0.31.0
pyproject.toml              # modificado: scikit-learn, mypy y la versión
.pre-commit-config.yaml     # modificado: exclude en trailing-whitespace
compose.yaml                # modificado: las imágenes week-31
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-31`. El `starter/` trae la capa 29 resuelta: `core/findings.py`, el comando `hallazgos` y el informe de ejemplo. **Tú** escribes `learning.py` y `modelo`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-30` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-31
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/3-proyecto/starter
cp $STARTER/tests/test_learning.py $STARTER/tests/test_my_learning.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_notebook.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `test_learning.py`, con 47 tests (uno con Hypothesis), y `test_my_learning.py`, con un ejemplo.
- **Modificados:** `test_delivery.py`, las imágenes `week-31` y un test para el gancho de los SVG; `test_notebook.py`, la imagen `week-31-notebook`; `test_package.py`, `learning` es un módulo de `core`, scikit-learn está fijado y la versión es `0.31.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'sklearn'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `tests/test_learning.py` entero. Fíjate en:

- `signal()`, los datos de prueba: la etiqueta decide el valor (Norte, bajo; Sur, medio; Centro, alto), con ruido. Un modelo que solo ve la etiqueta **puede** acertar;
- `test_regress_model_learns_only_from_training`, que calcula a mano lo que debe predecir la regresión: la media de cada etiqueta **en el entrenamiento**;
- `test_classify_balanced_accuracy_sees_through_an_unbalanced_level`: 90 % de nivel medio, la exactitud de la referencia es 0,9 y la equilibrada 1/3 (teoría 04, sección 5);
- `test_classify_does_not_see_the_value`: el valor decide el nivel y la etiqueta no dice nada. Si el valor se colara entre las entradas, el modelo acertaría (teoría 05, sección 2);
- `test_split_never_loses_or_repeats_a_row`, con Hypothesis: para cualquier proporción y semilla, cada medida está en una sola parte.

### 4. scikit-learn

```bash
uv add scikit-learn==1.9.1
uv lock --upgrade-package threadpoolctl==3.7.0
git diff pyproject.toml
```

- `uv add` fija la versión en `pyproject.toml` y añade a `uv.lock` scikit-learn y lo que necesita: joblib, narwhals y threadpoolctl. NumPy y SciPy ya los tenías.
- La segunda línea baja threadpoolctl a 3.7.0: la 3.8.0 se publicó hace menos de dos semanas, y el bootcamp no fija versiones tan nuevas (`docs/stack-versions.md`).

scikit-learn no publica tipos: con `strict = true`, mypy se niega a usarlo. Al final de `pyproject.toml`:

```toml
[[tool.mypy.overrides]]
# scikit-learn no publica tipos (ni py.typed ni paquete de stubs): mypy trata lo que viene
# de sklearn como Any. Tus funciones sí van anotadas, y mypy las sigue revisando.
module = ["sklearn.*"]
ignore_missing_imports = true
```

```bash
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.learning'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

El error cambia: scikit-learn ya está; falta tu módulo.

### 5. El módulo `learning.py`

Crea `src/observatorio/core/learning.py`:

```python
"""Un modelo predictivo de la instantánea, juzgado contra una referencia que no sabe nada.

Qué: split separa las medidas con valor en entrenamiento y prueba, regress predice el valor
con una regresión lineal y classify el nivel con una regresión logística; las dos usan solo
la etiqueta, y cada métrica se compara con la de un modelo Dummy que ignora las entradas.
Para qué: un modelo solo aporta si predice mejor que no saber nada. La media de todo (para
el valor) o el nivel más frecuente (para el nivel) son ese "no saber nada": si tu modelo no
los mejora en medidas que no vio al entrenar, no ha aprendido nada útil de tus datos.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `modelo`.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import train_test_split

COLUMNS = {"etiqueta", "valor", "nivel"}
# La semilla por defecto: el mismo reparto en cada ejecución, y en los tests.
SEED = 31


@dataclass(frozen=True)
class Score:
    """Una métrica en las medidas de prueba: la del modelo y la de la referencia."""

    name: str
    model: float
    baseline: float
    higher_is_better: bool

    @property
    def improves(self) -> bool:
        """Si el modelo es mejor que la referencia en esta métrica. Empatar no es mejorar."""
        if self.higher_is_better:
            return self.model > self.baseline
        return self.model < self.baseline


@dataclass(frozen=True)
class Evaluation:
    """Un modelo evaluado: la primera métrica es la que decide."""

    task: str
    train_size: int
    test_size: int
    scores: tuple[Score, ...]

    @property
    def improves(self) -> bool:
        return self.scores[0].improves


def known(frame: pd.DataFrame) -> pd.DataFrame:
    """Las medidas con valor: sin él no hay nada que predecir ni que comparar.

    Lanza ValueError si faltan columnas, o si algún nivel tiene menos de dos medidas: el
    reparto estratificado necesita al menos una en entrenamiento y otra en prueba.
    """
    missing = COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"a la instantánea le faltan las columnas {', '.join(sorted(missing))}")
    rows = frame[frame["valor"].notna()]
    counts = rows["nivel"].value_counts()
    if len(counts) < 2 or counts.min() < 2:
        raise ValueError("hacen falta dos niveles, cada uno con al menos dos medidas con valor")
    return rows


def features(frame: pd.DataFrame) -> pd.DataFrame:
    """Las entradas del modelo: una columna 0/1 por etiqueta. Nunca el valor ni el nivel:
    son lo que se predice."""
    return pd.get_dummies(frame["etiqueta"], dtype="float64")


def split(
    frame: pd.DataFrame, test_size: float = 0.25, seed: int = SEED
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Entrenamiento y prueba, con la misma proporción de cada nivel en las dos partes."""
    rows = known(frame)
    train, test = train_test_split(
        rows, test_size=test_size, random_state=seed, stratify=rows["nivel"]
    )
    return train, test


def regress(frame: pd.DataFrame, test_size: float = 0.25, seed: int = SEED) -> Evaluation:
    """Predice el valor de cada medida de prueba; la referencia predice siempre la media."""
    train, test = split(frame, test_size, seed)
    x = features(known(frame))
    x_train, x_test = x.loc[train.index], x.loc[test.index]
    y_train, y_test = train["valor"], test["valor"]
    model = LinearRegression().fit(x_train, y_train)
    baseline = DummyRegressor(strategy="mean").fit(x_train, y_train)
    predicted, guessed = model.predict(x_test), baseline.predict(x_test)
    scores = (
        Score(
            "MAE",
            mean_absolute_error(y_test, predicted),
            mean_absolute_error(y_test, guessed),
            False,
        ),
        Score(
            "RMSE",
            root_mean_squared_error(y_test, predicted),
            root_mean_squared_error(y_test, guessed),
            False,
        ),
        Score("R²", r2_score(y_test, predicted), r2_score(y_test, guessed), True),
    )
    return Evaluation("regresión del valor", len(train), len(test), scores)


def classify(frame: pd.DataFrame, test_size: float = 0.25, seed: int = SEED) -> Evaluation:
    """Predice el nivel de cada medida de prueba; la referencia predice el más frecuente."""
    train, test = split(frame, test_size, seed)
    x = features(known(frame))
    x_train, x_test = x.loc[train.index], x.loc[test.index]
    y_train, y_test = train["nivel"].to_numpy(), test["nivel"].to_numpy()
    model = LogisticRegression().fit(x_train, y_train)
    baseline = DummyClassifier(strategy="most_frequent").fit(x_train, y_train)
    predicted: np.ndarray = model.predict(x_test)
    guessed: np.ndarray = baseline.predict(x_test)
    scores = (
        # Equilibrada primero: la exactitud premia acertar siempre el nivel más frecuente.
        Score(
            "exactitud equilibrada",
            balanced_accuracy_score(y_test, predicted),
            balanced_accuracy_score(y_test, guessed),
            True,
        ),
        Score(
            "exactitud",
            accuracy_score(y_test, predicted),
            accuracy_score(y_test, guessed),
            True,
        ),
        Score(
            "F1 macro",
            f1_score(y_test, predicted, average="macro", zero_division=0),
            f1_score(y_test, guessed, average="macro", zero_division=0),
            True,
        ),
    )
    return Evaluation("clasificación del nivel", len(train), len(test), scores)
```

Por partes:

- **`Score`** guarda una métrica del modelo y la de su referencia, y sabe si más es mejor (exactitud, R²) o peor (MAE, RMSE). `improves` es estricto: empatar con la referencia no es mejorar.
- **`Evaluation`** decide con su **primera** métrica: MAE en la regresión, exactitud equilibrada en la clasificación. Las demás se muestran para entender, no para decidir.
- **`known`** deja fuera las medidas sin valor (su nivel es "sin dato") y comprueba lo que `train_test_split` necesitará para estratificar: al menos dos niveles, y dos medidas de cada uno. El mensaje sale en español, no el de scikit-learn.
- **`features`** es one-hot de la etiqueta, y nada más (teoría 03, sección 2, y teoría 05, sección 2). Las columnas se crean con todas las medidas antes de repartir: no es una fuga, porque no usan el valor ni el nivel.
- **`split`** reparte con semilla y estratificado por nivel (teoría 02, sección 3). `train` y `test` conservan el índice de la instantánea: `x.loc[train.index]` toma sus mismas filas de `features`.
- **`regress`** y **`classify`** hacen lo mismo con otro modelo y otras métricas: entrenar el modelo y su referencia con `x_train`, predecir `x_test`, y medir las dos predicciones con cada métrica, primero lo real (teoría 03, sección 3).
- **`zero_division=0`**: un modelo que nunca predice un nivel no tiene precisión en él; sin esto, scikit-learn avisa con `UndefinedMetricWarning` y la cuenta como 0 igualmente.

```bash
uv run pytest -q
uv run mypy
```

```
12 failed, 1145 passed
...
Success: no issues found in ... source files
```

Fallan los del comando, los de la versión, las imágenes y el gancho.

### 6. El comando `modelo`

En `src/observatorio/cli.py`, añade `Evaluation` a los imports del bloque `if TYPE_CHECKING:`:

```python
    from observatorio.core.learning import Evaluation
```

Y después de `hallazgos`:

```python
def evaluation_table(evaluation: Evaluation) -> Table:
    """Una fila por métrica: el modelo, la referencia y si el modelo la mejora."""
    table = Table(
        title=f"{evaluation.task} · {evaluation.train_size} para entrenar,"
        f" {evaluation.test_size} para probar"
    )
    table.add_column("Métrica")
    table.add_column("Modelo", justify="right")
    table.add_column("Referencia", justify="right")
    table.add_column("¿Mejora?")
    for score in evaluation.scores:
        table.add_row(
            score.name,
            f"{score.model:.3f}",
            f"{score.baseline:.3f}",
            "sí" if score.improves else "no",
        )
    return table


@app.command()
def modelo(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    prueba: Annotated[
        float,
        typer.Option(min=0.1, max=0.5, help="Parte de las medidas que se aparta para probar."),
    ] = 0.25,
    semilla: Annotated[int, typer.Option(help="La semilla del reparto: la misma, el mismo.")] = 31,
) -> None:
    """Entrena una regresión y una clasificación con la etiqueta, y las compara con una referencia."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import findings, learning

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        evaluations = [
            learning.regress(frame, prueba, semilla),
            learning.classify(frame, prueba, semilla),
        ]
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    for evaluation in evaluations:
        out.print(evaluation_table(evaluation))
        verdict = "mejora" if evaluation.improves else "no mejora"
        out.print(f"{evaluation.task}: el modelo {verdict} la referencia")
```

- Reutiliza `read_snapshot` de la semana 30: la misma lectura, la misma huella, el mismo `--huella`.
- Los dos modelos se entrenan **antes** de escribir nada: si falla uno, no queda media salida en la terminal.
- `--prueba` va de 0,1 a 0,5; fuera de ese rango, Typer responde con un error de uso (código 2).
- El import va **dentro**: la CLI sigue arrancando sin cargar scikit-learn, y `test_importing_the_cli_does_not_load_sklearn` lo vigila.

Actualiza el docstring del módulo: "veintiún comandos", con `modelo` entre `hallazgos` y `borrar`.

```bash
uv run pytest -q
uv run observatorio modelo notebooks/instantanea.csv --prueba 0.2 --semilla 7
uv run observatorio modelo notebooks/instantanea.csv --huella 0000; echo $?
```

```
5 failed, 1152 passed
...
regresión del valor · 1515 para entrenar, 379 para probar
...
error: la huella de instantanea.csv es 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65, no 0000
1
```

Con otra semilla y otra proporción, otros números: mira cuánto cambian. Si el veredicto cambiara con la semilla, la diferencia entre el modelo y la referencia sería ruido (la semana 32 lo mide con validación cruzada).

### 7. Versión, imágenes y el gancho de las figuras

En `pyproject.toml`, `version = "0.31.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-31-test`, `local/observatorio:week-31` y `local/observatorio:week-31-notebook`.

En `.pre-commit-config.yaml`, debajo de `- id: trailing-whitespace`:

```yaml
        # Los SVG de matplotlib acaban muchas líneas en un espacio. Si el gancho los quitara,
        # la figura dejaría de ser la que escribe `hallazgos`, byte a byte.
        exclude: \.svg$
```

Desde la semana 30, `hallazgos` escribe `informe/diferencias.svg`, y matplotlib deja un espacio al final de muchas líneas. El gancho `trailing-whitespace` los quitaba en cada `pre-commit run --all-files`, y al regenerar el informe volvían: `git status` nunca quedaba limpio. Con `exclude`, el gancho no mira los `.svg`. Si tu `diferencias.svg` del repositorio ya perdió sus espacios, regenéralo:

```bash
uv run observatorio hallazgos notebooks/instantanea.csv informe
uv run pre-commit run --all-files
git status --short informe/
```

```bash
uv run pytest -q
```

```
1157 passed
```

### 8. Tu modelo, con tus datos

Ejecuta `modelo` con **tu** instantánea y mira las dos tablas con la teoría:

```bash
uv run observatorio modelo notebooks/instantanea.csv
```

- ¿Mejora alguno de los dos modelos su referencia? ¿Por cuánto? Compáralo con las diferencias de tu informe de la semana 30: si ningún par de etiquetas difería, lo normal es que no.
- ¿Cuál es el nivel más frecuente de tu dominio, y qué exactitud da la referencia con él?
- Si algo sale casi perfecto, busca la fuga antes de celebrarlo (teoría 05).

Añade a `informe/README.md`, en **Siguientes pasos**, una línea con el resultado de `modelo` y qué entradas crees que harían falta para predecir mejor en tu dominio. `test_informe.py` sigue pasando: no comprueba esa sección.

### 9. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_learning.py tests/test_my_learning.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `learning.py` | en `Score.improves`, `self.model > self.baseline` por `>=` | |
| `learning.py` | en `Evaluation.improves`, `self.scores[0]` por `self.scores[-1]` | |
| `learning.py` | `rows = frame[frame["valor"].notna()]` por `rows = frame` | |
| `learning.py` | `len(counts) < 2 or counts.min() < 2` por `len(counts) < 2` | |
| `learning.py` | `pd.get_dummies(frame["etiqueta"], ...)` por `pd.get_dummies(frame[["etiqueta", "valor"]], ...)` | |
| `learning.py` | quita `, stratify=rows["nivel"]` | |
| `learning.py` | `random_state=seed` por `random_state=SEED` | |
| `learning.py` | `DummyRegressor(strategy="mean")` por `DummyRegressor(strategy="median")` | |
| `learning.py` | `LinearRegression().fit(x_train, y_train)` por `.fit(x_test, y_test)` | |
| `learning.py` | en el F1 del modelo, `average="macro"` por `average="weighted"` | |
| `cli.py` | en `modelo`, `learning.regress(frame, prueba, semilla)` por `learning.regress(frame)` | |
| `cli.py` | en `evaluation_table`, `"sí" if score.improves else "no"` por `"sí"` | |

Los doce mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el de `.fit(x_test, y_test)`, ¿qué test falla? Con los datos de `signal()`, el modelo entrenado con la prueba **sigue mejorando** la referencia: ¿por qué? ¿Por qué ese modelo es inútil aunque sus métricas sean buenas?
- Con el de `get_dummies(frame[["etiqueta", "valor"]])`, fallan ocho tests. Ejecuta `modelo` con tu instantánea con ese mutante puesto: ¿qué exactitud equilibrada da? ¿Cuál de los ocho tests explica mejor **por qué** está mal?

Después, en `tests/test_my_learning.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las etiquetas, los valores y los niveles de tu dominio y las funciones de `test_learning.py` (`frame_of`, `signal`, `write`). Ideas:

- etiquetas de tu dominio que deciden el nivel, y el modelo mejora la referencia;
- etiquetas que no dicen nada del valor, y el modelo no la mejora;
- un nivel de tu dominio con una sola medida, y el `ValueError` de `known`;
- el nivel más frecuente de tu dominio, y la exactitud de la referencia calculada a mano;
- `modelo --huella` con la huella de tu instantánea, y con otra;
- que con tu instantánea, `features` tenga tantas columnas como etiquetas distintas.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1162 tests en verde.

### 10. README y pull request

En el `README.md` de tu repositorio, añade una sección "Modelo": cómo ejecutarlo, qué predice cada modelo y con qué entradas, y el veredicto con tus datos en una frase.

Commits sugeridos, en este orden:

1. `test: add learning tests`
2. `build: add scikit-learn`
3. `feat: add learning module`
4. `feat: add modelo command`
5. `chore: bump version to 0.31.0`
6. `fix: keep generated svg files out of trailing-whitespace`
7. `docs: add model results to the report`
8. `test: add my learning tests`

```bash
git push -u origin week-31
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-31` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `modelo` con tu instantánea, y tu lectura en dos frases: ¿mejora la referencia?, ¿por qué crees que sí o que no?
3. La tabla de mutantes del paso 9 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Falta el paso 4, o ejecutas sin `uv run` |
| `ModuleNotFoundError: No module named 'observatorio.core.learning'` | Falta el paso 5, o el archivo no está en `src/observatorio/core/` |
| `error: Skipping analyzing "sklearn.metrics": module is installed, but missing library stubs` | Falta el `[[tool.mypy.overrides]]` del paso 4 |
| `test_dependencies_are_pinned` falla | `uv add` sin `==1.9.1`, o lo añadiste a mano sin `uv lock` |
| `test_importing_the_cli_does_not_load_sklearn` falla | Importaste `learning` arriba de `cli.py`: va dentro de `modelo` |
| `test_regress_model_learns_only_from_training` falla | Entrenas con `x_test`, o creas `features` con otras filas que `split` |
| `test_classify_does_not_see_the_value` falla | `features` usa algo más que la etiqueta |
| `hacen falta dos niveles, cada uno con al menos dos medidas con valor` | Tu instantánea tiene un solo nivel, o uno con una medida: extrae una carga con más medidas, o revisa tus umbrales |
| `ConvergenceWarning` de `LogisticRegression` | Con muchas etiquetas puede necesitar más iteraciones: `LogisticRegression(max_iter=1000)` |
| `test_trailing_whitespace_leaves_the_figures_alone` falla | Falta el `exclude` del paso 7, o está en otro gancho |
| `git status` muestra `informe/diferencias.svg` después de `pre-commit` | El gancho le quitó los espacios antes del paso 7: regenera con `hallazgos` |

## Entrega

1. Rama `week-31` con `core/learning.py`, el comando `modelo`, el gancho de los SVG, las imágenes `week-31`, la versión `0.31.0` y al menos 6 tests tuyos en `test_my_learning.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Modelo", e `informe/README.md` con el resultado en **Siguientes pasos**.
4. *Pull request* `week-31` → `main` con lo que pide el paso 10.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Desbalance y fugas](../2-practicas/ejercicio-04-desbalance-y-fugas/README.md) | **Proyecto · Tu primer modelo** | [Webgrafía](../4-recursos/webgrafia/README.md) |
