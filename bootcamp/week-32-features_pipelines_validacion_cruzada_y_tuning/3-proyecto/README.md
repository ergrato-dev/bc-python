# Proyecto — Observatorio, capa 31: tu modelo ajustado

> En la semana 31 entrenaste un modelo con un reparto y lo comparaste con una referencia. Esta semana preparas las entradas dentro de un **pipeline**, eliges la regularización con **validación cruzada**, y mides el resultado en cinco pliegues, cada uno frente a la referencia, sin que la búsqueda vea con qué se mide.

## Qué construyes

```
$ uv run observatorio ajustar notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65 · pliegues al azar
regresión del valor · MAE en cada pliegue
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Pliegue ┃ Modelo ┃ Referencia ┃ ¿Mejora? ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│       1 │ 20.342 │     20.275 │ no       │
│       2 │ 19.581 │     19.598 │ sí       │
│       3 │ 19.807 │     19.820 │ sí       │
│       4 │ 19.854 │     19.873 │ sí       │
│       5 │ 20.220 │     20.209 │ no       │
│   media │ 19.961 │     19.955 │          │
└─────────┴────────┴────────────┴──────────┘
regresión del valor: con alpha=100, gana en 3 de 5 pliegues: el modelo no mejora la referencia
clasificación del nivel · exactitud equilibrada en cada pliegue
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Pliegue ┃ Modelo ┃ Referencia ┃ ¿Mejora? ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│       1 │  0.333 │      0.333 │ no       │
│       2 │  0.333 │      0.333 │ no       │
│       3 │  0.333 │      0.333 │ no       │
│       4 │  0.333 │      0.333 │ no       │
│       5 │  0.333 │      0.333 │ no       │
│   media │  0.333 │      0.333 │          │
└─────────┴────────┴────────────┴──────────┘
clasificación del nivel: con C=0.01, gana en 0 de 5 pliegues: el modelo no mejora la referencia
```

Con los datos de ejemplo, la regresión gana en tres pliegues de cinco, por centésimas: con un solo reparto, según la semilla, habrías dicho que mejora. Y la búsqueda elige la regularización más fuerte en los dos modelos: sin nada que aprender, lo mejor es parecerse a la referencia (teoría 05, sección 4).

| Pieza | Qué hace |
|---|---|
| `core/validation.py` | `ordered` pone las medidas con valor en orden de llegada; `prepare` codifica la etiqueta y escala la posición; `folds` reparte al azar o por tiempo; `validate` ajusta y mide un modelo y su referencia en cada pliegue |
| `ajustar INSTANTANEA` | Escribe una tabla por modelo, con `--huella`, `--pliegues` y `--tiempo` |

Sin dependencias nuevas: todo está en scikit-learn 1.9.1.

```
src/observatorio/
├── cli.py                  # modificado: ajustar
└── core/
    └── validation.py       # nuevo: sin reexportar en core/__init__.py
tests/
├── test_validation.py      # nuevo: los tests del bootcamp
├── test_my_validation.py   # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes week-32
├── test_notebook.py        # modificado: la imagen week-32-notebook
└── test_package.py         # modificado: validation en core y la versión 0.32.0
pyproject.toml              # modificado: la versión
compose.yaml                # modificado: las imágenes week-32
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-32`. El `starter/` trae la capa 30 resuelta: `core/learning.py` y el comando `modelo`. **Tú** escribes `validation.py` y `ajustar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-31` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-32
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-32-features_pipelines_validacion_cruzada_y_tuning/3-proyecto/starter
cp $STARTER/tests/test_validation.py $STARTER/tests/test_my_validation.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_notebook.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `test_validation.py`, con 56 tests (uno con Hypothesis), y `test_my_validation.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` y `test_notebook.py`, las imágenes `week-32`; `test_package.py`, `validation` es un módulo de `core` y la versión es `0.32.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ImportError: cannot import name 'validation' from 'observatorio.core' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `tests/test_validation.py` entero. Fíjate en:

- `signal()` y `noise()`, los datos de prueba: en `signal` la etiqueta decide el valor, y las etiquetas se **turnan** para que cada pliegue, al azar o por tiempo, tenga de las tres; en `noise` no hay nada que aprender;
- `test_prepare_does_not_learn_from_rows_it_was_not_fitted_on`: la preparación se ajusta con unas filas y se aplica a otras (teoría 02);
- `test_validate_value_baseline_is_the_mean_of_each_training_fold` y `test_validate_value_by_time_trains_only_with_the_past`, que calculan a mano lo que debe dar la referencia en cada pliegue, al azar y por tiempo;
- `test_validate_tunes_inside_each_fold`: cuenta con qué filas se ajusta la búsqueda. Si no fuera anidada, no habría una búsqueda por pliegue (teoría 05);
- `test_random_folds_test_every_row_once`, con Hypothesis: para cualquier número de pliegues y de filas, cada fila prueba una vez.

### 4. El módulo `validation.py`

Crea `src/observatorio/core/validation.py`:

```python
"""Validación cruzada de un modelo ajustado, con todo el preprocesado dentro del pipeline.

Qué: validate prepara las entradas (la etiqueta en one-hot y la posición escalada) dentro de
un Pipeline, elige la fuerza de la regularización con GridSearchCV y mide el resultado en
varios pliegues, cada uno frente a un modelo Dummy medido en los mismos pliegues.
Para qué: un solo reparto da un número que cambia con la semilla; varios pliegues dicen si
la mejora se repite o fue suerte. El ajuste va dentro de cada pliegue (validación anidada):
si eligiera la regularización mirando los pliegues con los que se mide, la medida saldría
optimista.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `validar`.
"""

from dataclasses import dataclass
from typing import Literal

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import GridSearchCV, KFold, TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from observatorio.core.learning import SEED, known

# El orden en el tiempo: la carga y, dentro de ella, la posición de cada medida.
ORDER = ["carga", "posicion"]
INPUTS = ["etiqueta", "posicion"]
# Los valores que se prueban para alpha (Ridge) y C (logística), de diez en diez. Van al
# revés: alpha alto regulariza mucho; C alto, poco.
STRENGTHS = [0.01, 0.1, 1.0, 10.0, 100.0]


@dataclass(frozen=True)
class CrossValidation:
    """Una métrica en cada pliegue: la del modelo ajustado y la de la referencia."""

    task: str
    metric: str
    higher_is_better: bool
    model: tuple[float, ...]
    baseline: tuple[float, ...]
    params: dict[str, float]

    @property
    def beats(self) -> tuple[bool, ...]:
        """Si el modelo es mejor que la referencia en cada pliegue. Empatar no es ganar."""
        pairs = zip(self.model, self.baseline, strict=True)
        if self.higher_is_better:
            return tuple(model > baseline for model, baseline in pairs)
        return tuple(model < baseline for model, baseline in pairs)

    @property
    def improves(self) -> bool:
        """Solo si gana en todos los pliegues: una mejora que no se repite puede ser suerte."""
        return all(self.beats)


def ordered(frame: pd.DataFrame) -> pd.DataFrame:
    """Las medidas con valor, en el orden en que llegaron: carga y posición."""
    missing = set(ORDER) - set(frame.columns)
    if missing:
        raise ValueError(f"a la instantánea le faltan las columnas {', '.join(sorted(missing))}")
    return known(frame).sort_values(ORDER, kind="stable")


def prepare() -> ColumnTransformer:
    """La etiqueta en one-hot y la posición escalada. Sin ajustar: cada pliegue lo ajusta
    con su entrenamiento, y una etiqueta que no vio da una fila de ceros, no un error."""
    return ColumnTransformer(
        [
            ("etiqueta", OneHotEncoder(handle_unknown="ignore"), ["etiqueta"]),
            ("posicion", StandardScaler(), ["posicion"]),
        ]
    )


def folds(n_splits: int, by_time: bool) -> KFold | TimeSeriesSplit:
    """Pliegues al azar, con la semilla, o por tiempo: cada prueba, después de su
    entrenamiento."""
    if by_time:
        return TimeSeriesSplit(n_splits=n_splits)
    return KFold(n_splits=n_splits, shuffle=True, random_state=SEED)


def validate(
    frame: pd.DataFrame,
    target: Literal["valor", "nivel"],
    n_splits: int = 5,
    by_time: bool = False,
) -> CrossValidation:
    """Ajusta y mide el modelo del valor (Ridge, con MAE) o del nivel (logística, con
    exactitud equilibrada) en cada pliegue, junto a su referencia."""
    rows = ordered(frame)
    if target == "valor":
        task, metric, scoring = "regresión del valor", "MAE", "neg_mean_absolute_error"
        model, grid = Ridge(), {"model__alpha": STRENGTHS}
        baseline: DummyRegressor | DummyClassifier = DummyRegressor(strategy="mean")
    else:
        task, metric = "clasificación del nivel", "exactitud equilibrada"
        scoring = "balanced_accuracy"
        model, grid = LogisticRegression(), {"model__C": STRENGTHS}
        baseline = DummyClassifier(strategy="most_frequent")
    x, y = rows[INPUTS], rows[target]
    pipeline = Pipeline([("prepare", prepare()), ("model", model)])
    search = GridSearchCV(pipeline, grid, scoring=scoring, cv=folds(n_splits, by_time))
    # Validación anidada: en cada pliegue, GridSearchCV elige con su entrenamiento.
    tuned = cross_val_score(search, x, y, scoring=scoring, cv=folds(n_splits, by_time))
    guessed = cross_val_score(baseline, x, y, scoring=scoring, cv=folds(n_splits, by_time))
    # scikit-learn da los errores en negativo, para que más sea siempre mejor: aquí, en positivo.
    sign = -1 if target == "valor" else 1
    params = search.fit(x, y).best_params_
    return CrossValidation(
        task,
        metric,
        target != "valor",
        tuple(float(sign * score) for score in tuned),
        tuple(float(sign * score) for score in guessed),
        {name.removeprefix("model__"): value for name, value in params.items()},
    )
```

Por partes:

- **`CrossValidation`** guarda la métrica de cada pliegue, del modelo y de la referencia. `beats` dice en qué pliegues gana el modelo (empatar no es ganar), e `improves` exige ganar en **todos** (teoría 03, sección 4). `params` guarda el hiperparámetro elegido, sin el prefijo `model__`.
- **`ordered`** reutiliza `known` de la semana 31 (las medidas con valor, con sus comprobaciones) y ordena por carga y posición: `TimeSeriesSplit` solo mira el orden de las filas. `kind="stable"` respeta el orden original entre medidas iguales.
- **`prepare`** devuelve un `ColumnTransformer` **nuevo y sin ajustar**: la etiqueta en one-hot, con `handle_unknown="ignore"`, y la posición escalada. Sustituye a `features` de la semana 31: ya no se crean las columnas con todas las medidas, sino con el entrenamiento de cada pliegue (teoría 01, sección 4).
- **`folds`** da `KFold` con mezcla y semilla, o `TimeSeriesSplit`. Cada llamada da un objeto nuevo, pero con los mismos argumentos reparte igual: modelo y referencia se miden en los **mismos** pliegues.
- **`validate`** monta el pipeline del modelo, envuelve el pipeline en `GridSearchCV`, y mide la búsqueda (no el pipeline) con `cross_val_score`: validación anidada (teoría 05, sección 2). La referencia se mide con los mismos pliegues. Al final, `search.fit` con todas las medidas da el hiperparámetro que el comando muestra.
- **`sign`**: scikit-learn da el MAE en negativo (`neg_mean_absolute_error`) para que más sea siempre mejor. Se le cambia el signo para mostrarlo como un error normal, y `higher_is_better` vale `False`.

```bash
uv run pytest -q
uv run mypy
```

```
17 failed, 1197 passed
...
Success: no issues found in ... source files
```

Fallan los del comando, la versión y las imágenes.

### 5. El comando `ajustar`

En `src/observatorio/cli.py`, añade `CrossValidation` a los imports del bloque `if TYPE_CHECKING:`:

```python
    from observatorio.core.validation import CrossValidation
```

Y después de `modelo`:

```python
def cross_validation_table(validation: CrossValidation) -> Table:
    """Una fila por pliegue y otra con la media: el modelo, la referencia y quién gana."""
    table = Table(title=f"{validation.task} · {validation.metric} en cada pliegue")
    table.add_column("Pliegue", justify="right")
    table.add_column("Modelo", justify="right")
    table.add_column("Referencia", justify="right")
    table.add_column("¿Mejora?")
    rows = zip(validation.model, validation.baseline, validation.beats, strict=True)
    for number, (model, baseline, beats) in enumerate(rows, start=1):
        table.add_row(str(number), f"{model:.3f}", f"{baseline:.3f}", "sí" if beats else "no")
    model_mean = sum(validation.model) / len(validation.model)
    baseline_mean = sum(validation.baseline) / len(validation.baseline)
    table.add_row("media", f"{model_mean:.3f}", f"{baseline_mean:.3f}", "", style="bold")
    return table


@app.command()
def ajustar(
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
    """Ajusta la regresión y la clasificación, y las valida por pliegues frente a una referencia."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import findings, validation

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        validations = [
            validation.validate(frame, "valor", pliegues, tiempo),
            validation.validate(frame, "nivel", pliegues, tiempo),
        ]
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    order = "por tiempo" if tiempo else "al azar"
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest} · pliegues {order}")
    for result in validations:
        out.print(cross_validation_table(result))
        params = ", ".join(f"{name}={value:g}" for name, value in result.params.items())
        verdict = "mejora" if result.improves else "no mejora"
        out.print(
            f"{result.task}: con {params}, gana en {sum(result.beats)} de {len(result.model)}"
            f" pliegues: el modelo {verdict} la referencia"
        )
```

- La media de cada columna es una fila más, en negrita, sin veredicto: el veredicto es de los pliegues.
- `{value:g}` escribe `100` y `0.01`, sin ceros de sobra.
- Los dos modelos se ajustan **antes** de escribir nada, como en `modelo`. Tarda unos segundos: cada modelo son 5 búsquedas de 25 entrenamientos.
- `--pliegues` va de 2 a 10. Con pocas medidas y muchos pliegues, scikit-learn lanza un `ValueError` (en inglés), y el comando sale con código 1.
- El import va **dentro**: la CLI sigue arrancando sin scikit-learn.

Actualiza el docstring del módulo: "veintidós comandos", con `ajustar` entre `modelo` y `borrar`.

```bash
uv run pytest -q
uv run observatorio ajustar notebooks/instantanea.csv --pliegues 3 --tiempo
uv run observatorio ajustar notebooks/instantanea.csv --huella 0000; echo $?
```

```
4 failed, 1210 passed
...
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65 · pliegues por tiempo
regresión del valor · MAE en cada pliegue
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Pliegue ┃ Modelo ┃ Referencia ┃ ¿Mejora? ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│       1 │ 20.163 │     20.175 │ sí       │
│       2 │ 19.983 │     19.908 │ no       │
│       3 │ 19.161 │     19.199 │ sí       │
│   media │ 19.769 │     19.761 │          │
└─────────┴────────┴────────────┴──────────┘
regresión del valor: con alpha=100, gana en 2 de 3 pliegues: el modelo no mejora la referencia
...
error: la huella de instantanea.csv es 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65, no 0000
1
```

Por tiempo, con tres pliegues: el primero entrena con 475 medidas y prueba con las 473 siguientes; el último entrena con 1421. Otra vez gana en unos pliegues y pierde en otros.

### 6. Versión e imágenes

En `pyproject.toml`, `version = "0.32.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-32-test`, `local/observatorio:week-32` y `local/observatorio:week-32-notebook`.

```bash
uv run pytest -q
```

```
1214 passed
```

### 7. Tu modelo ajustado, con tus datos

Ejecuta `ajustar` con **tu** instantánea, al azar y por tiempo, y compáralo con `modelo` de la semana 31:

```bash
uv run observatorio modelo notebooks/instantanea.csv
uv run observatorio ajustar notebooks/instantanea.csv
uv run observatorio ajustar notebooks/instantanea.csv --tiempo
```

- ¿En cuántos pliegues gana cada modelo? Si `modelo` decía "mejora" y `ajustar` gana en tres de cinco, la mejora de la semana 31 era del reparto.
- ¿Qué `alpha` y qué `C` elige? Si es un extremo de la rejilla (0,01 o 100), piensa por qué (teoría 05, sección 4).
- ¿Cambia algo con `--tiempo`? Si empeora, tu dominio cambia con el tiempo, y los pliegues al azar lo esconden (ejercicio 03, paso 6).

Añade a `informe/README.md`, en **Siguientes pasos**, una línea con el resultado de `ajustar` y qué entrada derivada probarías en tu dominio (teoría 01, sección 6). `test_informe.py` sigue pasando: no comprueba esa sección.

### 8. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_validation.py tests/test_my_validation.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `validation.py` | en `beats`, `model > baseline` por `model >= baseline` | |
| `validation.py` | en `improves`, `all(self.beats)` por `any(self.beats)` | |
| `validation.py` | en `ordered`, quita `.sort_values(ORDER, kind="stable")` | |
| `validation.py` | `OneHotEncoder(handle_unknown="ignore")` por `OneHotEncoder()` | |
| `validation.py` | `StandardScaler()` por `"passthrough"` | |
| `validation.py` | `TimeSeriesSplit(n_splits=n_splits)` por `KFold(n_splits=n_splits)` | |
| `validation.py` | `shuffle=True, random_state=SEED` por `shuffle=False` | |
| `validation.py` | `DummyRegressor(strategy="mean")` por `DummyRegressor(strategy="median")` | |
| `validation.py` | `cross_val_score(search, ...)` por `cross_val_score(pipeline, ...)` en `tuned` | |
| `validation.py` | en `guessed`, `cv=folds(n_splits, by_time)` por `cv=folds(n_splits, False)` | |
| `validation.py` | en `guessed`, `sign * score` por `score` | |
| `cli.py` | en `ajustar`, `validation.validate(frame, "nivel", pliegues, tiempo)` por `validation.validate(frame, "nivel", pliegues)` | |

Los doce mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el de `cross_val_score(pipeline, ...)`, solo falla un test. Ejecuta `ajustar` con tu instantánea con ese mutante puesto: ¿qué mide ahora cada pliegue? ¿Por qué la tabla ya no corresponde al `alpha` que muestra la última línea?
- Con el de `shuffle=False`, ¿qué test falla? Tu instantánea viene en orden de llegada: sin mezclar, cada pliegue es un trozo seguido. ¿En qué se parece eso a `--tiempo`, y en qué no?

Después, en `tests/test_my_validation.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las etiquetas y los valores de tu dominio y las funciones de `test_validation.py` (`frame_of`, `signal`, `noise`, `write`). Ideas:

- etiquetas de tu dominio que deciden el valor, y el modelo gana en todos los pliegues;
- una tendencia con la posición (tu dominio a lo largo del día), y el modelo la aprende;
- etiquetas que no dicen nada, y la búsqueda elige la regularización más fuerte;
- una etiqueta que solo aparece al final, con `by_time=True`, y `validate` no falla;
- una instantánea sin `carga`, y el `ValueError` de `ordered`;
- `ajustar --pliegues 3 --tiempo` con tu instantánea, y tres filas por tabla.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1219 tests en verde.

### 9. README y pull request

En el `README.md` de tu repositorio, añade una sección "Modelo ajustado": cómo ejecutar `ajustar`, qué entradas usa cada modelo, qué hiperparámetro se busca y el veredicto con tus datos en una frase.

Commits sugeridos, en este orden:

1. `test: add validation tests`
2. `feat: add validation module`
3. `feat: add ajustar command`
4. `chore: bump version to 0.32.0`
5. `docs: add tuned model results to the report`
6. `test: add my validation tests`

```bash
git push -u origin week-32
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-32` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `ajustar` con tu instantánea, al azar y por tiempo, y tu lectura en dos frases: ¿mejora la referencia en todos los pliegues?, ¿qué dice el hiperparámetro elegido?
3. La tabla de mutantes del paso 8 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'validation' from 'observatorio.core'` | Falta el paso 4, o el archivo no está en `src/observatorio/core/` |
| `ValueError: Found unknown categories` | Falta `handle_unknown="ignore"`: un pliegue tiene una etiqueta que su entrenamiento no vio |
| `ValueError: Invalid parameter 'alpha'` | La rejilla sin el paso: `model__alpha`, y el paso del pipeline se llama `"model"` |
| `test_validate_tunes_inside_each_fold` falla | Mides el pipeline, no la búsqueda: `cross_val_score(search, ...)` |
| `test_validate_value_errors_are_positive` falla | Falta cambiar el signo con `sign` |
| `a la instantánea le faltan las columnas carga, posicion` | Tu instantánea no viene de `extraer` (semana 29): regenérala |
| `Cannot have number of splits n_splits=10 greater than the number of samples` | Muy pocas medidas para tantos pliegues: baja `--pliegues` |
| `UserWarning: y_pred contains classes not in y_true` con `--tiempo` | Un pliegue de prueba no tiene algún nivel: es un aviso, no un error. Con más medidas desaparece |
| `ajustar` tarda mucho | Cada modelo son 5 búsquedas de 25 entrenamientos. Con decenas de miles de medidas, baja `--pliegues` |

## Entrega

1. Rama `week-32` con `core/validation.py`, el comando `ajustar`, las imágenes `week-32`, la versión `0.32.0` y al menos 6 tests tuyos en `test_my_validation.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Modelo ajustado", e `informe/README.md` con el resultado en **Siguientes pasos**.
4. *Pull request* `week-32` → `main` con lo que pide el paso 9.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Ajuste de hiperparámetros](../2-practicas/ejercicio-04-ajuste-de-hiperparametros/README.md) | **Proyecto · Tu modelo ajustado** | [Webgrafía](../4-recursos/webgrafia/README.md) |
