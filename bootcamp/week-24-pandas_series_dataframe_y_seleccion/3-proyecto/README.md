# Proyecto — Observatorio, capa 23: elegir medidas con pandas

⏱️ 6 h 30 min · Capa 23 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

`informe` escribe todas las medidas; `estadisticas` las resume. Te falta poder **preguntar**: ¿qué medidas de Norte y Sur pasan de 9? ¿Cuáles son las más altas? Esta semana tu Observatorio gana un comando, `filtrar`, que convierte la serie en un `DataFrame` de pandas, elige filas por etiqueta y por valor, las ordena y las guarda en un CSV que el propio Observatorio sabe leer.

```
$ uv run observatorio filtrar -e Norte -e Sur --desde 9 --ordenar -o elegidas.csv medidas.txt
error: línea 10: 'Sur 9,5'
         etiqueta  valor  nivel
posición
6           Norte   48.9  medio
1           Norte   12.5  medio
7             Sur    9.5   bajo
3 de 7 medidas · Norte 2, Sur 1
guardadas en elegidas.csv
```

| Pieza | Qué hace |
|---|---|
| `pandas==3.1.0` | Nueva dependencia de producción |
| `pandas-stubs==3.1.0.261029` | Los tipos de pandas para mypy, solo en desarrollo |
| `core/frames.py` | La serie como tabla y, sobre ella, los niveles, el filtro, el orden, los conteos y la escritura |
| `filtrar RUTA [-e ETIQUETA]... [--desde X] [--hasta Y] [--ordenar] [-n FILAS] [-o CSV]` | El comando nuevo, que importa pandas **solo** cuando se ejecuta |

```
src/observatorio/
├── cli.py                  # modificado: filtrar y frame_text
└── core/
    └── frames.py           # nuevo: pandas, sin reexportar en core/__init__.py
tests/
├── test_frames.py          # nuevo: los tests del bootcamp
├── test_my_frames.py       # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes de la semana 24
└── test_package.py         # modificado: frames en core, pandas, pandas-stubs y 0.24.0
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-24`. El `starter/` trae la capa 22 resuelta: `core/arrays.py` y el comando `estadisticas`. **Tú** escribes `frames.py` y el comando.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-23` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-24
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-24-pandas_series_dataframe_y_seleccion/3-proyecto/starter
cp $STARTER/tests/test_frames.py $STARTER/tests/test_my_frames.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `tests/test_frames.py`, con 51 tests, y `tests/test_my_frames.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` (las imágenes se llaman `week-24`) y `test_package.py` (`frames` es un módulo de `core`, `pandas==3.1.0` está en las dependencias, `pandas-stubs` en las de desarrollo y la versión es `0.24.0`).

### 3. Tests en rojo y las dependencias nuevas

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'pandas'
...
ERROR tests/test_frames.py
ERROR tests/test_my_frames.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Dos dependencias: pandas para el programa y sus tipos para mypy (teoría 05, sección 1).

```bash
uv add pandas==3.1.0
uv add --dev pandas-stubs==3.1.0.261029
```

```
 + pandas==3.1.0
 + python-dateutil==4.0.0
 + tzdata==2026.6
```

```
 + pandas-stubs==3.1.0.261029
```

pandas trae `python-dateutil`, para leer fechas, y esta trae `tzdata`, la base de datos de zonas horarias. NumPy ya estaba: `estadisticas` lo añadió la semana pasada.

```bash
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.frames'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Ahora falta tu módulo. Antes de escribirlo, lee `tests/test_frames.py` entero. Fíjate en:

- `table(...)`, que construye la tabla esperada, y `pd.testing.assert_frame_equal`, que compara valores, tipos e índice;
- los cinco tests con `@given`, que comparan lo nuevo con lo que ya tenías: `Scale.level`, `Series.where`, `Series.most_common` y la lectura de archivos;
- `test_by_value_keeps_ties_in_order_in_a_long_frame`, con 100 filas: lo vas a necesitar en el paso 12;
- el último, `test_importing_the_cli_does_not_load_pandas`, que en otro proceso comprueba que importar la CLI no carga pandas.

### 4. La serie como tabla

Crea `src/observatorio/core/frames.py`:

```python
"""La serie como tabla de pandas: seleccionar, ordenar, contar y escribir sin bucles.

Este módulo importa pandas, que tarda en cargarse: core/__init__.py no lo reexporta, y la
CLI lo importa solo dentro del comando que lo usa.
"""

from collections.abc import Collection
from pathlib import Path

import pandas as pd

from observatorio.core.model import Scale, Series

# Las columnas de medidas.csv, en español, y las del DataFrame, en inglés.
FILE_COLUMNS = {"etiqueta": "label", "valor": "value"}


def frame_of(series: Series) -> pd.DataFrame:
    """Una fila por medida, con label (str) y value (float64, NaN si falta); índice desde 1."""
    return pd.DataFrame(
        {
            "label": pd.Series([m.label for m in series], dtype="str"),
            "value": pd.Series([m.value for m in series], dtype="float64"),
        }
    ).set_axis(pd.RangeIndex(1, len(series) + 1, name="position"))
```

- Cada columna nace como `Series` **con su tipo**. Sin `dtype`, una serie vacía daría dos columnas `float64` (teoría 02, sección 2), y `test_frame_of_an_empty_series_keeps_the_columns_and_types` lo comprueba.
- `None` pasa a NaN al crear la columna `float64`, como en `values_array` de la semana 23.
- `set_axis` pone el índice: la posición de cada medida, desde 1. Así, al filtrar, cada fila sigue diciendo qué medida es. Un `RangeIndex` no guarda los números: solo el inicio, el final y el paso.
- Las columnas se llaman en inglés, como el resto del código; `FILE_COLUMNS` las traduce a los nombres de `medidas.csv` (paso 7).

`frames.py` **no** se añade a `core/__init__.py`: cualquier `from observatorio.core import ...` cargaría pandas. Lo comprueban `test_frames_is_not_reexported_from_core` y el último test.

### 5. Niveles sin bucle

```python
def with_levels(frame: pd.DataFrame, scale: Scale) -> pd.DataFrame:
    """Una copia con la columna level, como Scale.level pero sin bucle de Python."""
    # right=False: cada intervalo incluye su borde izquierdo, así un valor igual a low ya es
    # "medio" y uno igual a high, "alto", como en classify.
    levels = pd.cut(
        frame["value"],
        bins=[float("-inf"), scale.low, scale.high, float("inf")],
        labels=["bajo", "medio", "alto"],
        right=False,
    )
    return frame.assign(level=levels.astype("str").where(levels.notna(), "sin dato"))
```

- `pd.cut` reparte la columna entera en tres intervalos: `[-inf, low)`, `[low, high)` y `[high, inf)` (teoría 04, sección 3). Con `right=True`, el valor por defecto, 10 sería `"bajo"`: `test_with_levels_borders_like_classify` prueba los cuatro bordes.
- `cut` devuelve una columna `category` con NaN donde falta el valor. `astype("str")` la pasa a texto y `where(..., "sin dato")` rellena las que faltan.
- `assign` devuelve una tabla **nueva**: quien llama a `with_levels` conserva la suya (teoría 04, sección 5).

### 6. Elegir, ordenar y contar

```python
def select(
    frame: pd.DataFrame,
    *,
    labels: Collection[str] = (),
    low: float | None = None,
    high: float | None = None,
) -> pd.DataFrame:
    """Las filas con alguna de labels (todas si no hay) y value entre low y high, incluidos."""
    keep = pd.Series(True, index=frame.index)
    if labels:
        keep &= frame["label"].isin(labels)
    # Un NaN comparado con cualquier número da False: filtrar por valor quita las sin dato.
    if low is not None:
        keep &= frame["value"] >= low
    if high is not None:
        keep &= frame["value"] <= high
    return frame.loc[keep]


def by_value(frame: pd.DataFrame) -> pd.DataFrame:
    """Las filas de mayor a menor valor, las sin dato al final y los empates en su orden."""
    # kind="stable": el quicksort por defecto desordena los empates a partir de unas decenas.
    return frame.sort_values("value", ascending=False, na_position="last", kind="stable")


def label_counts(frame: pd.DataFrame) -> dict[str, int]:
    """Cuántas medidas hay de cada etiqueta, de la más frecuente a la menos."""
    # value_counts deja los empates en el orden en que aparece cada etiqueta, como
    # Counter.most_common: lo vigila un test con Hypothesis.
    counts = frame["label"].value_counts()
    return {str(label): int(count) for label, count in counts.items()}
```

- `select` empieza con una máscara toda `True` y le va quitando filas con `&=`, una condición por filtro que te pasen. Sin filtros, devuelve todas.
- `isin` compara con varias etiquetas a la vez; `>=` y `<=` incluyen los bordes, como `between`.
- `frame.loc[keep]` conserva el índice: la fila 6 sigue siendo la 6.
- `kind="stable"` en `by_value`: con 4 filas no se nota; con 60 sí (teoría 04, sección 1).
- `label_counts` devuelve `str` e `int` de Python, no `numpy.int64` (teoría 05, sección 2).

`select` y `by_value` son dos funciones, no una con un parámetro `ordenar`: cada una hace una cosa, y se encadenan.

### 7. Guardar

Al final del archivo:

```python
def write_frame(frame: pd.DataFrame, path: Path) -> None:
    """Escribe label y value como medidas.csv: etiqueta;valor, coma decimal y NA si falta."""
    frame[list(FILE_COLUMNS.values())].rename(
        columns={new: old for old, new in FILE_COLUMNS.items()}
    ).to_csv(path, sep=";", decimal=",", na_rep="NA", index=False)
```

Solo las columnas `label` y `value`, renombradas a `etiqueta` y `valor`: el archivo que sale es un `.csv` que tu Observatorio sabe leer, con `informe -f`, `estadisticas` o el propio `filtrar`. `level` no se guarda: se calcula al leer, con la escala de quien lee.

`test_write_frame_reads_back_the_same_series` lo comprueba con Hypothesis: escribe una serie cualquiera, la lee con `open_file` y `Series.parse`, y exige las mismas medidas, sin errores.

```bash
uv run pytest -q
```

```
16 failed, 810 passed
```

Todos los tests de `frames.py` pasan. Fallan los del comando, que aún no existe, el de la versión y los dos de las imágenes de `compose.yaml`.

### 8. El comando `filtrar`

Cambia `week-23` por `week-24` en las dos imágenes de `compose.yaml`. Quedan 14.

En `src/observatorio/cli.py`, añade pandas al bloque de tipos **solo para mypy**:

```python
if TYPE_CHECKING:
    # Solo para mypy: en ejecución no se importan NumPy ni pandas al cargar la CLI. Desde
    # Python 3.14 las anotaciones se evalúan cuando alguien las pide, así que `Stats` y
    # `pd.DataFrame` pueden aparecer en las firmas sin estar importados de verdad.
    import pandas as pd

    from observatorio.core.arrays import Counts, Floats, Stats
```

Detrás de `estadisticas`, la función que escribe la tabla y el comando:

```python
def frame_text(frame: pd.DataFrame) -> str:
    """La tabla de pandas con las columnas en español, un decimal y "sin dato" si falta."""
    return (
        frame.rename(columns={"label": "etiqueta", "value": "valor", "level": "nivel"})
        .rename_axis("posición")
        .to_string(na_rep="sin dato", float_format=lambda value: f"{value:.1f}")
    )


@app.command()
def filtrar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    etiquetas: Annotated[
        list[str] | None,
        typer.Option("--etiqueta", "-e", help="Solo esta etiqueta; repítela para elegir varias."),
    ] = None,
    desde: Annotated[float | None, typer.Option(help="Solo valores desde este, incluido.")] = None,
    hasta: Annotated[float | None, typer.Option(help="Solo valores hasta este, incluido.")] = None,
    ordenar: Annotated[bool, typer.Option("--ordenar", help="De mayor a menor valor.")] = False,
    filas: Annotated[
        int, typer.Option("--filas", "-n", min=1, help="Cuántas filas escribe, como mucho.")
    ] = ROWS,
    salida: Annotated[
        Path | None,
        typer.Option("--salida", "-o", metavar="CSV", help="Guarda las medidas elegidas."),
    ] = None,
) -> None:
    """Elige medidas con pandas, por etiqueta y por valor; las ordena o las guarda."""
    # Importar aquí, como NumPy en `estadisticas`: pandas tarda en cargarse.
    from observatorio.core import frames

    try:
        lines = open_file(ruta).lines()
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {error}")
    frame = frames.with_levels(frames.frame_of(series), SCALE)
    chosen = frames.select(frame, labels=etiquetas or (), low=desde, high=hasta)
    if ordenar:
        chosen = frames.by_value(chosen)
    if chosen.empty:
        out.print("ninguna medida cumple el filtro")
    else:
        out.print(frame_text(chosen.head(filas)))
    if len(chosen) > filas:
        out.print(f"… y {len(chosen) - filas} más (usa --filas para verlas)")
    counts = ", ".join(f"{label} {n}" for label, n in frames.label_counts(chosen).items())
    out.print(f"{len(chosen)} de {len(frame)} medidas" + (f" · {counts}" if counts else ""))
    if salida is not None:
        try:
            frames.write_frame(chosen, salida)
        except OSError as problem:
            raise fail(f"no se pudo guardar {salida}: {problem}", 2) from problem
        out.print(f"guardadas en {salida}")
    if errors:
        raise typer.Exit(1)
```

- `frame_text` usa la tabla de texto de pandas (`to_string`), no una de Rich: las columnas en español, un decimal y `"sin dato"` en lugar de `NaN`.
- `-e` se repite: `-e Norte -e Sur` llega como `["Norte", "Sur"]`; sin ninguno, `None`, y `etiquetas or ()` lo convierte en "todas".
- `--desde` y `--hasta` son `float | None`: `None` significa "sin límite". `select` recibe exactamente eso.
- `--filas`, con el mismo `ROWS = 20` que `informe`: escribir 100 000 filas no sirve a nadie. `min=1` porque `head(0)` daría una tabla vacía con cabecera.
- `-o` guarda **todas** las elegidas, no solo las que se escriben.
- pandas lanza `OSError` si no puede escribir: una carpeta que no existe, sin permiso o una ruta que es una carpeta. Cualquiera de ellas acaba en `error: no se pudo guardar ...` y código 2.
- Los errores de las líneas, a stderr y código 1, como en `informe` y `estadisticas`.

Actualiza también el docstring del módulo: ahora son doce comandos, con `filtrar`.

```bash
uv run pytest -q
```

```
1 failed, 825 passed
```

### 9. Probarlo y medirlo

```bash
uv run observatorio filtrar medidas.txt
uv run observatorio filtrar -e Norte -e Sur --desde 9 --ordenar -o elegidas.csv medidas.txt
uv run observatorio informe -f elegidas.csv
```

La primera escribe las 7 medidas válidas con su nivel. La segunda da la salida de "Qué construyes", y la tercera lee el CSV que acaba de escribir: tres medidas, sin errores.

```
           etiqueta    valor     nivel
posición
1             Norte     12.5     medio
2               Sur      8.0      bajo
3            Centro sin dato  sin dato
4           Oriente     55.1      alto
5         Occidente     61.0      alto
6             Norte     48.9     medio
7               Sur      9.5      bajo
7 de 7 medidas · Norte 2, Sur 2, Centro 1, Oriente 1, Occidente 1
```

La posición es la de cada medida, no la línea del archivo: la línea mala es la 10, pero no es una medida y no tiene posición.

Ahora con el archivo grande de la semana 22:

```bash
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
time uv run observatorio filtrar -e Norte --desde 20 --ordenar perfil/grande.txt > /dev/null
uv run observatorio filtrar -e Norte --desde 20 --ordenar perfil/grande.txt | tail -2
```

```
real	0m0.760s
```

```
… y 14215 más (usa --filas para verlas)
14235 de 100000 medidas · Norte 14235
```

Mide cada pieza con `timeit` en un `uv run python`, como en la semana 23. En la máquina del bootcamp, con 100 000 medidas:

| Operación | Python puro | pandas |
|---|---|---|
| Convertir la serie | — | 11,5 ms (`frame_of`) |
| Niveles | 8,2 ms (`scale.level` en una comprensión) | 3,5 ms (`with_levels`) |
| Filtrar por etiqueta y valor | 6,1 ms (`series.where`) | 3,0 ms (`select`) |
| Contar etiquetas | 8,7 ms (`series.most_common`) | 6,0 ms (`label_counts`) |
| Ordenar por valor | 24,2 ms (`sorted` con `key`) | 13,7 ms (`by_value`) |
| Analizar el texto | 103 ms (`Series.parse`) | 11 ms (`pd.read_csv`, sin validar) |

pandas gana en cada operación, pero poco, y convertir cuesta casi lo que se gana. El total lo sigue dominando analizar el texto, que haces con `Series.parse` porque valida (teoría 05, sección 5). Apunta tus números: van al *pull request*.

Comprueba que los demás comandos no pagan:

```bash
uv run python -c "import sys, observatorio.cli; print('pandas' in sys.modules)"
time uv run observatorio informe -f perfil/grande.txt > /dev/null
```

```
False
real	0m0.650s
```

### 10. La versión

En `pyproject.toml`, `version = "0.24.0"`, y:

```bash
uv lock
uv run pytest -q
uv run observatorio --version
```

```
826 passed
observatorio 0.24.0
```

### 11. Calidad, cobertura y Docker

```bash
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
docker images local/observatorio
```

`mypy` estricto pasa gracias a `pandas-stubs`. Pruébalo: `uv remove --dev pandas-stubs` y `uv run mypy` dan `Library stubs not installed for "pandas"`; vuelve a añadirlo. `coverage report` debe dar 100 % en `frames.py` y en `cli.py`. `alembic check` sigue en `No new upgrade operations detected.`.

En `docker images`, compara `week-23` y `week-24`:

```
week-24        508MB
week-23        395MB
```

113 MB más: pandas trae compilado su propio código en C y Cython. `pandas-stubs` no entra en la imagen `runtime`: es de desarrollo.

### 12. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `frames.py` | `right=False` por `right=True` | |
| `frames.py` | quita `.where(levels.notna(), "sin dato")` | |
| `frames.py` | `frame["value"] >= low` por `frame["value"] > low` | |
| `frames.py` | `return frame.loc[keep]` por `return frame.loc[keep].reset_index(drop=True)` | |
| `frames.py` | quita `, kind="stable"` en `by_value` | |
| `frames.py` | `na_position="last"` por `na_position="first"` | |
| `frames.py` | `value_counts()` por `value_counts().sort_index()` | |
| `frames.py` | `na_rep="NA"` por `na_rep=""` | |
| `cli.py` | mueve `from observatorio.core import frames` al principio del archivo | |
| `cli.py` | `labels=etiquetas or ()` por `labels=()` | |

Los diez mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- ¿Por qué `test_by_value_keeps_ties_in_their_order`, con tres filas, no mata el quinto, y quién lo mata?
- El último lo mata `test_filtrar_by_label_and_value`. ¿Qué tiene su archivo de datos (fíjate en `Centro;20`) para que el filtro por etiqueta cambie el resultado? Sin esa línea, el filtro por valor ya quitaba las mismas filas y el mutante sobrevivía.

Un test que pasa con y sin la línea que dice probar no prueba esa línea.

### 13. Tus tests

En `tests/test_my_frames.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con los valores de tu dominio y las funciones de `test_frames.py` (`table`, `frame_rows`, `write`). Ideas:

- los bordes de **tu** escala con `with_levels`: un valor igual a tu `LOW` y otro igual a tu `HIGH`;
- `select` con `low` mayor que `high`: tabla vacía, sin error;
- que `select` con `labels` y sin ellas dé lo mismo cuando pides todas tus etiquetas (con Hypothesis);
- que `by_value` deje la tabla con las mismas filas, solo en otro orden (`sort_index()` y `assert_frame_equal`);
- un archivo de tu dominio que vuelve igual tras `filtrar -o` y otra lectura;
- que `filtrar` con un `.csv` dé lo mismo que con el `.txt` equivalente.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 948 tests en verde.

### 14. README y pull request

En el `README.md` de tu repositorio, añade una sección "Filtrar": qué escribe `filtrar`, sus opciones, que el CSV de `-o` se puede volver a leer, y por qué pandas solo se importa en ese comando.

Commits sugeridos, en este orden:

1. `test: add frame tests`
2. `build: add pandas and pandas-stubs`
3. `feat: add frames module`
4. `feat: add filtrar command`
5. `chore: bump version to 0.24.0`
6. `test: add my frame tests`

```bash
git push -u origin week-24
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-24` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. Dos o tres llamadas a `filtrar` con tus datos que respondan preguntas de tu dominio, y el CSV de `-o` leído con `informe`.
3. Tu tabla de tiempos del paso 9.
4. El tamaño de la imagen antes y después.
5. La tabla de mutantes del paso 12 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Falta el paso 3: `uv add pandas==3.1.0` |
| `test_dependencies_are_pinned` falla | Lo añadiste con `--dev` o sin versión: `uv remove --dev pandas` y `uv add pandas==3.1.0` |
| `test_dev_tools_are_pinned` falla | Falta `pandas-stubs` en `dev`, o lo pusiste en las dependencias del programa |
| mypy: `Library stubs not installed for "pandas"` | `uv add --dev pandas-stubs==3.1.0.261029` |
| `test_frame_of_an_empty_series_keeps_the_columns_and_types` falla | Creas las columnas con listas: usa `pd.Series(..., dtype=...)` |
| `test_with_levels_borders_like_classify` falla en 10.0 o en 50.0 | Falta `right=False` en `pd.cut` |
| `test_with_levels_level_is_text` falla con `category` | Falta `astype("str")` |
| `test_select_by_label_keeps_the_positions` falla en el índice | No reinicies el índice: `frame.loc[keep]` tal cual |
| `test_changing_a_selection_does_not_change_the_frame` falla | Tienes pandas 2: comprueba `uv run python -c "import pandas; print(pandas.__version__)"` |
| `test_importing_the_cli_does_not_load_pandas` falla | El `from observatorio.core import frames` está fuera de `filtrar`, o `import pandas as pd` no está dentro de `if TYPE_CHECKING:` |
| `test_filtrar_writes_every_measurement_with_its_level` falla con `12.34` | Falta `float_format` en `frame_text`: sin él, pandas escribe todos los decimales |
| `docker compose run --rm app` falla con `No module named 'pandas'` | Reconstruye la imagen: `docker compose build app api` |

## Entrega

1. Rama `week-24` con `core/frames.py`, el comando `filtrar`, `pandas==3.1.0` en las dependencias, `pandas-stubs` en las de desarrollo, las imágenes `week-24`, la versión `0.24.0` y al menos 6 tests tuyos en `test_my_frames.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Filtrar".
4. *Pull request* `week-24` → `main` con lo que pide el paso 14.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · De Python a pandas](../2-practicas/ejercicio-04-de-python-a-pandas/README.md) | **Proyecto · Elegir medidas con pandas** | [Rúbrica de la semana 24](../rubrica-evaluacion.md) |
