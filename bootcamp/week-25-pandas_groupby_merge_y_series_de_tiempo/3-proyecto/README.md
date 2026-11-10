# Proyecto — Observatorio, capa 24: resumir medidas por grupos y por periodos

⏱️ 6 h 30 min · Capa 24 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

`filtrar` elige medidas, pero no las resume. Te faltan tres preguntas: ¿cuántas medidas tiene cada etiqueta y cuánto vale su media? ¿Qué cambió entre el archivo de ayer y el de hoy? ¿Cómo evoluciona cada etiqueta a lo largo del día? Esta semana tu Observatorio gana dos comandos con pandas: `resumir`, con `groupby` y `merge`, y `evolucion`, con `pivot` y `resample`.

```
$ uv run observatorio resumir medidas.txt
error: medidas.txt: línea 10: 'Sur 9,5'
           medidas  faltan    media   mínimo   máximo
etiqueta
Norte            2       0     30.7     12.5     48.9
Sur              2       0      8.8      8.0      9.5
Centro           0       1 sin dato sin dato sin dato
Oriente          1       0     55.1     55.1     55.1
Occidente        1       0     61.0     61.0     61.0
5 etiquetas · 7 medidas

$ uv run observatorio evolucion medidas.txt --inicio 2026-11-01T08:00:00 --periodo 3h
error: medidas.txt: línea 10: 'Sur 9,5'
etiqueta              Centro    Norte  Occidente  Oriente      Sur
periodo
2026-11-01 06:00:00 sin dato     12.5   sin dato sin dato sin dato
2026-11-01 09:00:00 sin dato sin dato   sin dato     55.1      8.0
2026-11-01 12:00:00 sin dato     48.9       61.0 sin dato      9.5
3 periodos · 7 medidas
```

| Pieza | Qué hace |
|---|---|
| `core/summaries.py` | Resumir por etiqueta (`summary`), comparar dos resúmenes (`compare`), leer una duración (`duration`), poner tiempo a la tabla (`timed`) y resumir por periodos (`evolution`) |
| `resumir RUTA [-c OTRA]` | Una fila por etiqueta; con `--contra`, las medias de los dos archivos y su cambio |
| `evolucion RUTA --inicio FECHA [--cada 1h] [--periodo 1D] [-n FILAS]` | La media de cada etiqueta en cada periodo |
| `NAMES` y `frame_text` | Un solo diccionario para poner en español las columnas y los índices de cualquier tabla |

No hay dependencias nuevas: pandas llegó la semana pasada.

```
src/observatorio/
├── cli.py                  # modificado: NAMES, frame_text, parsed, resumir y evolucion
└── core/
    └── summaries.py        # nuevo: pandas, sin reexportar en core/__init__.py
tests/
├── test_summaries.py       # nuevo: los tests del bootcamp
├── test_my_summaries.py    # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes de la semana 25
└── test_package.py         # modificado: summaries en core y 0.25.0
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-25`. El `starter/` trae la capa 23 resuelta: `core/frames.py` y el comando `filtrar`. **Tú** escribes `summaries.py` y los dos comandos.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-24` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-25
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-25-pandas_groupby_merge_y_series_de_tiempo/3-proyecto/starter
cp $STARTER/tests/test_summaries.py $STARTER/tests/test_my_summaries.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `tests/test_summaries.py`, con 52 tests, y `tests/test_my_summaries.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` (las imágenes se llaman `week-25`) y `test_package.py` (`summaries` es un módulo de `core` y la versión es `0.25.0`).

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.summaries'
...
ERROR tests/test_my_summaries.py
ERROR tests/test_summaries.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Falta tu módulo. Antes de escribirlo, lee `tests/test_summaries.py` entero. Fíjate en:

- `summary_table` y `means_table`, que construyen las tablas esperadas con los tipos exactos (teoría 05, sección 3);
- `test_summary_means_agree_with_series_means`, que compara con `Series.means` **como diccionarios**, y su comentario;
- `test_evolution_known_values`, que construye el índice esperado con `date_range` y nombra las columnas con `rename_axis`;
- `test_evolution_in_one_period_gives_the_means_of_summary`, con Hypothesis: lo vas a necesitar en el paso 12.

### 4. Un resumen por etiqueta

Crea `src/observatorio/core/summaries.py`:

```python
"""Resúmenes con pandas: por etiqueta, de dos archivos a la vez y por periodos de tiempo.

Trabaja sobre las tablas de frames.py. Como frames, importa pandas: core/__init__.py no lo
reexporta, y la CLI lo importa solo dentro de los comandos que lo usan.
"""

from datetime import datetime, timedelta

import pandas as pd


def summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Una fila por etiqueta, en el orden en que aparece: count, missing, mean, minimum, maximum.

    count son los valores que hay y missing los que faltan; una etiqueta sin ningún valor
    tiene count 0 y NaN en mean, minimum y maximum.
    """
    # sort=False: las etiquetas salen en el orden en que aparecen, como en Series.means.
    # Cada columna nueva es (columna de partida, función): count="count" no basta.
    table = frame.groupby("label", sort=False).agg(
        count=("value", "count"),
        size=("value", "size"),
        mean=("value", "mean"),
        minimum=("value", "min"),
        maximum=("value", "max"),
    )
    # size cuenta las filas y count solo los valores: la resta son los NaN de cada etiqueta.
    # La tabla es nueva, de agg: cambiarla aquí no toca la de nadie.
    table.insert(1, "missing", table.pop("size") - table["count"])
    return table
```

- `frame` es la tabla de `frames.frame_of`: columnas `label` y `value`.
- La agregación con nombre (teoría 01, sección 3) elige el nombre de cada columna. Se escribe sobre la tabla, con tuplas, y no sobre `["value"]`: así mypy sabe que devuelve un `DataFrame` (teoría 05, sección 2).
- `size` y `count` dan lo que falta. `pop` saca `size` de la tabla y la devuelve; `insert` pone `missing` en la posición 1, detrás de `count`.
- `insert` y `pop` cambian la tabla en lugar de crear otra. Aquí no importa: `table` acaba de salir de `agg` y nadie más la tiene. Con la tabla que recibes, `frame`, no lo harías nunca (teoría 04 de la semana 24).

### 5. Comparar dos resúmenes

```python
def compare(before: pd.DataFrame, after: pd.DataFrame) -> pd.DataFrame:
    """Las medias de dos resúmenes por etiqueta (before, after) y su diferencia (change).

    Salen todas las etiquetas de los dos, por orden alfabético: la que solo está en uno
    tiene NaN en el otro y en change.
    """
    # validate: cada etiqueta está una sola vez en cada resumen; si no, merge lanza
    # MergeError en lugar de multiplicar filas en silencio.
    joined = pd.merge(
        before["mean"].rename("before"),
        after["mean"].rename("after"),
        on="label",
        how="outer",
        validate="one_to_one",
    )
    return joined.assign(change=joined["after"] - joined["before"])
```

- Cruza dos `Series` por el nombre de su índice, `label` (teoría 02, sección 6). `rename` les da nombre a las columnas: sin él, las dos se llamarían `mean` y saldrían `mean_x` y `mean_y`.
- `how="outer"`: una etiqueta nueva o una que desapareció también es un cambio que quieres ver.
- `validate="one_to_one"` no debería fallar nunca con dos resúmenes de `summary`. Si falla, algo antes está mal, y prefieres saberlo.
- Una etiqueta sin valores tiene media NaN, y su `change` también.

### 6. Tiempo

Al final del archivo:

```python
def duration(text: str) -> timedelta:
    """Una duración escrita como en pandas ("1h", "90min", "1D") como timedelta.

    Lanza ValueError si el texto no es una duración o si no es mayor que cero.
    """
    problem = ValueError(f"no es una duración mayor que cero: {text!r}")
    try:
        value = pd.Timedelta(text)
    except ValueError as error:
        raise problem from error
    # Un texto vacío da NaT ("not a time") en lugar de un error: también se rechaza.
    if pd.isna(value) or value <= pd.Timedelta(0):
        raise problem
    return value.to_pytimedelta()


def timed(frame: pd.DataFrame, start: datetime, every: timedelta) -> pd.DataFrame:
    """Una copia con índice de tiempo (time): la primera medida en start y otra cada every."""
    return frame.set_axis(pd.date_range(start, periods=len(frame), freq=every, name="time"))


def evolution(frame: pd.DataFrame, period: timedelta) -> pd.DataFrame:
    """La media de cada etiqueta en cada periodo: una fila por periodo, una columna por etiqueta.

    frame necesita índice de tiempo (timed). Cada fila es el inicio de su periodo, contado
    desde la medianoche del primer día; un periodo sin valores de una etiqueta queda en NaN.
    """
    # pivot pasa cada etiqueta a una columna (por orden alfabético); resample agrupa las
    # filas por periodos, incluidos los que no tienen ninguna medida.
    return frame.pivot(columns="label", values="value").resample(period).mean()
```

- `duration` convierte lo que escribirá una persona en `--cada` y `--periodo`, con un solo mensaje para todo lo que no sirve (teoría 05, sección 4). `to_pytimedelta()` devuelve un `timedelta` de Python.
- Tus archivos no dicen **cuándo** se tomó cada medida. `timed` lo supone: la primera en `start` y una cada `every`. Cambia el índice con `set_axis`, que devuelve una tabla nueva.
- `evolution` es `pivot` y `resample` (teoría 04, sección 5, y su diagrama). `pivot` no falla nunca aquí: cada instante es distinto.

```bash
uv run pytest -q
```

```
22 failed, 857 passed
```

Todos los tests de `summaries.py` pasan. Fallan los de los comandos, que aún no existen, el de la versión y los dos de las imágenes de `compose.yaml`.

### 7. Las tablas en español

Cambia `week-24` por `week-25` en las dos imágenes de `compose.yaml`. Quedan 20.

En `src/observatorio/cli.py`, `frame_text` traducía tres columnas y llamaba `posición` a cualquier índice. Ahora habrá tablas con otras columnas y con la etiqueta o el periodo como índice. Sustituye `frame_text` por un diccionario y la nueva versión:

```python
# Los nombres de las columnas y de los índices de las tablas de pandas, en español. La
# clave admite int porque así lo pide `rename_axis` en pandas-stubs.
NAMES: dict[str | int, str] = {
    "position": "posición",
    "label": "etiqueta",
    "value": "valor",
    "level": "nivel",
    "count": "medidas",
    "missing": "faltan",
    "mean": "media",
    "minimum": "mínimo",
    "maximum": "máximo",
    "before": "antes",
    "after": "después",
    "change": "cambio",
    "time": "periodo",
}


def frame_text(frame: pd.DataFrame) -> str:
    """La tabla de pandas con los nombres en español, un decimal y "sin dato" si falta."""
    return (
        frame.rename(columns=NAMES)
        .rename_axis(index=NAMES, columns=NAMES)
        .to_string(na_rep="sin dato", float_format=lambda value: f"{value:.1f}")
    )
```

- `rename(columns=NAMES)` cambia las columnas que están en el diccionario y deja las demás.
- `rename_axis(index=NAMES, columns=NAMES)` cambia el **nombre** del índice (`position`, `label` o `time`) y el de las columnas (`label`, en la tabla de `evolution`).
- La anotación `dict[str | int, str]` es la que piden los *stubs* (teoría 05, sección 2).

Ejecuta los tests de `filtrar`: siguen en verde, porque su tabla tiene las mismas columnas y el índice `position`.

### 8. Los comandos `resumir` y `evolucion`

Junto a `ROWS = 20`, los valores por defecto de `evolucion`:

```python
# Tiempo entre dos medidas y tamaño de cada periodo en `evolucion`.
EVERY = "1h"
PERIOD = "1D"
```

Añade `from datetime import datetime` a los `import` del principio. Después de `filtrar`, una función para leer un archivo y los dos comandos:

```python
def parsed(ruta: Path) -> tuple[Series, list[str]]:
    """La serie de un archivo y sus errores, que escribe en stderr; código 2 si no se lee."""
    try:
        lines = open_file(ruta).lines()
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {ruta.name}: {error}")
    return series, errors


@app.command()
def resumir(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    contra: Annotated[
        Path | None,
        typer.Option("--contra", "-c", metavar="OTRA", help="Compara las medias con otro archivo."),
    ] = None,
) -> None:
    """Resume cada etiqueta con pandas, o compara sus medias con las de otro archivo."""
    # Importar aquí, como en `filtrar`: pandas tarda en cargarse.
    from observatorio.core import frames, summaries

    series, errors = parsed(ruta)
    table = summaries.summary(frames.frame_of(series))
    if contra is None:
        out.print(frame_text(table) if len(table) else "ninguna medida")
        out.print(f"{len(table)} etiquetas · {len(series)} medidas")
    else:
        other, other_errors = parsed(contra)
        errors += other_errors
        changes = summaries.compare(table, summaries.summary(frames.frame_of(other)))
        out.print(frame_text(changes) if len(changes) else "ninguna medida")
        out.print(f"{changes['change'].count()} de {len(changes)} etiquetas en los dos archivos")
    if errors:
        raise typer.Exit(1)


@app.command()
def evolucion(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    inicio: Annotated[
        datetime,
        typer.Option(help="Cuándo se tomó la primera medida, como 2026-11-01T08:00:00."),
    ],
    cada: Annotated[str, typer.Option(help="Tiempo entre dos medidas: 1h, 15min, 1D...")] = EVERY,
    periodo: Annotated[str, typer.Option(help="Tamaño de cada periodo: 3h, 1D, 7D...")] = PERIOD,
    filas: Annotated[
        int, typer.Option("--filas", "-n", min=1, help="Cuántos periodos escribe, como mucho.")
    ] = ROWS,
) -> None:
    """La media de cada etiqueta por periodos de tiempo, con pandas."""
    from observatorio.core import frames, summaries

    try:
        every, period = summaries.duration(cada), summaries.duration(periodo)
    except ValueError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = parsed(ruta)
    table = summaries.evolution(summaries.timed(frames.frame_of(series), inicio, every), period)
    out.print(frame_text(table.head(filas)) if len(table) else "ninguna medida")
    if len(table) > filas:
        out.print(f"… y {len(table) - filas} más (usa --filas para verlos)")
    out.print(f"{len(table)} periodos · {len(series)} medidas")
    if errors:
        raise typer.Exit(1)
```

- `parsed` es lo que `informe`, `estadisticas` y `filtrar` repiten, con una diferencia: el error lleva el **nombre del archivo**. Con `--contra` lees dos, y necesitas saber de cuál es cada línea mala. Los comandos de antes no cambian: sus tests esperan `error: línea 10`.
- `--contra` es opcional: sin él, el resumen; con él, la comparación. Los errores de los dos archivos se suman y cualquiera da código 1.
- `changes['change'].count()` cuenta los cambios que no son NaN: las etiquetas con media en los dos archivos.
- `--inicio` no tiene valor por defecto: es obligatorio, y Typer lo dice si falta. Con el tipo `datetime`, Typer lee y valida la fecha (teoría 05, sección 4).
- `--cada` y `--periodo` llegan como texto, y `duration` los convierte **antes** de leer el archivo: con un `--cada 0h` no tiene sentido leer nada.
- `--filas`, como en `filtrar`: 100 000 medidas cada 5 minutos son 348 días.

Actualiza también el docstring del módulo: ahora son catorce comandos, con `resumir` y `evolucion` detrás de `filtrar`.

```bash
uv run pytest -q
```

```
1 failed, 878 passed
```

### 9. Probarlo y medirlo

```bash
uv run observatorio resumir medidas.txt
printf 'Norte;14\nSur;8\nSur;10\nEste;3\n' > otras.txt
uv run observatorio resumir medidas.txt --contra otras.txt
uv run observatorio evolucion medidas.txt --inicio 2026-11-01T08:00:00 --periodo 3h
uv run observatorio evolucion medidas.txt --inicio 2026-11-01T08:00:00
```

La primera y la tercera dan la salida de "Qué construyes". La segunda compara:

```
error: medidas.txt: línea 10: 'Sur 9,5'
             antes  después   cambio
etiqueta
Centro    sin dato sin dato sin dato
Este      sin dato      3.0 sin dato
Norte         30.7     14.0    -16.7
Occidente     61.0 sin dato sin dato
Oriente       55.1 sin dato sin dato
Sur            8.8      9.0      0.2
2 de 6 etiquetas en los dos archivos
```

El Sur pasa de 8,75 a 9: `float_format` escribe 8,8 y un cambio de 0,2. Las etiquetas salen por orden alfabético: es un `outer`. La cuarta, con el periodo por defecto de un día, da una sola fila: las siete medidas caben en el 1 de noviembre.

```
etiqueta     Centro  Norte  Occidente  Oriente  Sur
periodo
2026-11-01 sin dato   30.7       61.0     55.1  8.8
1 periodos · 7 medidas
```

Ahora con el archivo grande de la semana 22:

```bash
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
time uv run observatorio resumir perfil/grande.txt
uv run observatorio evolucion perfil/grande.txt --inicio 2026-01-01 --cada 5min 2> /dev/null | tail -3
```

```
          medidas  faltan  media   mínimo  máximo
etiqueta
Sur         19206     975   39.9     0.0    80.0
Este        18862    1003   40.0     0.0    80.0
Centro      18938    1025   39.9     0.0    80.0
Oeste       19136     978   40.0     0.0    80.0
Norte       18898     979   40.3     0.0    80.0
5 etiquetas · 100000 medidas
real	0m1.250s
```

```
2026-01-20    37.4  41.1   43.9   37.0 43.3
… y 328 más (usa --filas para verlos)
348 periodos · 100000 medidas
```

Las cifras exactas dependen de tu `generar_medidas.py`. Mide cada pieza con `timeit` en un `uv run python`, como en las semanas 23 y 24. En la máquina del bootcamp, con 100 000 medidas:

| Operación | Python puro | pandas |
|---|---|---|
| Media por etiqueta | 9,6 ms (`series.means()`) | 9,2 ms (`summary`, cinco estadísticas) |
| Comparar dos archivos ya leídos | 12,9 ms (dos `means()` y un diccionario) | 1,3 ms (`compare` de dos resúmenes) |
| Poner tiempo | — | 0,1 ms (`timed`) |
| Media por etiqueta y día | — | 18,8 ms (`evolution`, 348 días) |

El comando tarda más de un segundo, y casi todo es analizar el texto (teoría 05, sección 5). Apunta tus números: van al *pull request*.

### 10. La versión

En `pyproject.toml`, `version = "0.25.0"`, y:

```bash
uv lock
uv run pytest -q
uv run observatorio --version
```

```
879 passed
observatorio 0.25.0
```

### 11. Calidad, cobertura y Docker

```bash
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
docker images local/observatorio
uv run python -c "import sys, observatorio.cli; print('pandas' in sys.modules)"
```

`coverage report` debe dar 100 % en `summaries.py` y en `cli.py`. `alembic check` sigue en `No new upgrade operations detected.`. La comprobación de `sys.modules` escribe `False`.

En `docker images`, `week-24` y `week-25` miden lo mismo, 508 MB: no hay dependencias nuevas.

Prueba lo que dice la teoría 05 sobre mypy: cambia el `groupby` de `summary` por `frame.groupby("label", sort=False)["value"].agg(count="count", size="size", mean="mean", minimum="min", maximum="max")`. Los tests pasan, pero `uv run mypy` da `Incompatible return value type (got "Series[Any]", expected "DataFrame")`. Deshazlo.

### 12. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `summaries.py` | `groupby("label", sort=False)` por `groupby("label")` | |
| `summaries.py` | `size=("value", "size")` por `size=("value", "count")` | |
| `summaries.py` | quita `validate="one_to_one",` | |
| `summaries.py` | `how="outer"` por `how="inner"` | |
| `summaries.py` | `joined["after"] - joined["before"]` por `joined["before"] - joined["after"]` | |
| `summaries.py` | `value <= pd.Timedelta(0)` por `value < pd.Timedelta(0)` | |
| `summaries.py` | quita `pd.isna(value) or ` | |
| `summaries.py` | `.resample(period)` por `.resample(period, origin="start")` | |
| `summaries.py` | `.mean()` por `.median()` en `evolution` | |
| `cli.py` | quita `errors += other_errors` | |

Los diez mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- ¿Por qué `test_evolution_known_values` y los tests de `evolucion` no matan el noveno, y quién lo mata? Fíjate en cuántos valores tiene cada etiqueta en cada periodo de esos tests, y en qué dan la media y la mediana de dos números.
- Sin `pd.isna(value) or`, ¿qué devuelve `duration("")`? Pruébalo en `uv run python` y explica por qué `NaT <= pd.Timedelta(0)` no basta para rechazarlo.

Un test con datos tan simples que la media y la mediana coinciden no distingue una de otra.

### 13. Tus tests

En `tests/test_my_summaries.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con los valores de tu dominio y las funciones de `test_summaries.py` (`summary_table`, `means_table`, `data_rows`, `write`). Ideas:

- el resumen de un archivo de tu dominio, con una etiqueta sin ningún valor;
- que `summary` después de `frames.select` por una etiqueta dé una sola fila (con Hypothesis);
- `compare` entre dos archivos tuyos, con una etiqueta que aparece y otra que desaparece;
- `evolution` con tu frecuencia real (cada 15 minutos, cada día) y un periodo que tenga sentido en tu dominio;
- que la suma de `count` en `summary` sea el número de valores de `frames.select(frame, low=-inf)`;
- que `evolucion` con `--cada` y `--periodo` iguales dé una fila por medida.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1006 tests en verde.

### 14. README y pull request

En el `README.md` de tu repositorio, añade una sección "Resumir y evolución": qué escriben `resumir` y `evolucion`, sus opciones, que `--contra` compara las medias de dos archivos, y que `evolucion` supone una medida cada `--cada` desde `--inicio` porque tus archivos no traen la hora.

Commits sugeridos, en este orden:

1. `test: add summary tests`
2. `feat: add summaries module`
3. `refactor: translate table names with one dictionary`
4. `feat: add resumir and evolucion commands`
5. `chore: bump version to 0.25.0`
6. `test: add my summary tests`

```bash
git push -u origin week-25
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-25` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. `resumir` con un archivo de tu dominio, `resumir --contra` con dos, y `evolucion` con un periodo que tenga sentido para ti.
3. Tu tabla de tiempos del paso 9.
4. La tabla de mutantes del paso 12 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'observatorio.core.summaries'` | Falta el paso 4, o el archivo no está en `src/observatorio/core/` |
| `test_summary_has_one_row_per_label_in_order_of_appearance` falla en el orden | Falta `sort=False` en el `groupby` |
| `test_summary_of_an_empty_frame_keeps_the_columns_and_types` falla | Creas `missing` de otra forma: `size - count` entre columnas `int64` da `int64` |
| mypy: `Incompatible return value type (got "Series[Any]", expected "DataFrame")` | Usas `["value"].agg(...)`: escribe la agregación con tuplas sobre la tabla (paso 4) |
| mypy: `Argument "index" to "rename_axis" ... has incompatible type "dict[str, str]"` | Anota `NAMES: dict[str \| int, str]` |
| `test_compare_rejects_a_repeated_label` falla | Falta `validate="one_to_one"` |
| `test_evolution_known_values` falla en el índice | Los periodos tienen que empezar a medianoche: no pases `origin` a `resample` |
| `test_evolution_known_values` falla en `freq` | Construyes el índice de otra forma: `date_range` con `freq=every` en `timed` |
| `test_resumir_reports_invalid_lines_with_the_file_and_exits_1` falla | El error de `parsed` lleva el nombre: `f"error: {ruta.name}: {error}"` |
| `test_resumir_has_the_columns_in_spanish` falla: sale `posición` encima de las etiquetas | Te quedaste con `rename_axis("posición")`: usa `rename_axis(index=NAMES, columns=NAMES)` |
| `error: no es una duración mayor que cero: '1M'` | Un mes no es una duración fija: usa días (`30D`) |
| `test_importing_the_cli_does_not_load_pandas` falla | `from observatorio.core import frames, summaries` está fuera de los comandos |

## Entrega

1. Rama `week-25` con `core/summaries.py`, los comandos `resumir` y `evolucion`, las imágenes `week-25`, la versión `0.25.0` y al menos 6 tests tuyos en `test_my_summaries.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Resumir y evolución".
4. *Pull request* `week-25` → `main` con lo que pide el paso 14.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Series de tiempo](../2-practicas/ejercicio-04-series-de-tiempo/README.md) | **Proyecto · Resumir medidas por grupos y por periodos** | [Rúbrica de la semana 25](../rubrica-evaluacion.md) |
