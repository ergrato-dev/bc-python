# Proyecto — Observatorio, capa 25: exportar a Parquet y preguntar con SQL

⏱️ 6 h 30 min · Capa 25 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Cada comando de tu Observatorio vuelve a leer el texto de tus archivos, y con 100 000 medidas eso es más de un segundo. Tampoco puedes hacerle una pregunta que no esté ya escrita como comando. Esta semana guardas las medidas en **Parquet** con Polars, una vez, y les preguntas lo que quieras con **SQL** gracias a DuckDB:

```
$ uv run observatorio exportar medidas.txt medidas.parquet
error: medidas.txt: línea 10: 'Sur 9,5'
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ etiqueta  ┃ medidas ┃ faltan ┃ media    ┃ mínimo   ┃ máximo   ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ Norte     │ 2       │ 0      │ 30.7     │ 12.5     │ 48.9     │
│ Sur       │ 2       │ 0      │ 8.8      │ 8.0      │ 9.5      │
│ Centro    │ 0       │ 1      │ sin dato │ sin dato │ sin dato │
│ Oriente   │ 1       │ 0      │ 55.1     │ 55.1     │ 55.1     │
│ Occidente │ 1       │ 0      │ 61.0     │ 61.0     │ 61.0     │
└───────────┴─────────┴────────┴──────────┴──────────┴──────────┘
7 medidas en medidas.parquet · 937 bytes

$ uv run observatorio sql medidas.parquet "SELECT * FROM medidas WHERE value > 50"
┏━━━━━━━━━━━┳━━━━━━━┓
┃ etiqueta  ┃ valor ┃
┡━━━━━━━━━━━╇━━━━━━━┩
│ Oriente   │ 55.1  │
│ Occidente │ 61.0  │
└───────────┴───────┘
2 filas
```

| Pieza | Qué hace |
|---|---|
| `core/columnar.py` | Pasar la serie a una tabla de Polars (`frame_of`), resumirla en perezoso (`summary`) y preguntarle a un Parquet con SQL (`query`), sin acceso a ningún otro archivo |
| `exportar RUTA PARQUET` | Guarda las medidas en Parquet y resume el archivo que acaba de escribir |
| `sql PARQUET CONSULTA [-n FILAS]` | Ejecuta tu SQL sobre el Parquet, que se llama `medidas` |
| `rows_table` y `cell_text` | Una tabla de Rich para cualquier resultado de Polars o DuckDB, con los nombres de `NAMES` |

Dos dependencias nuevas:

| Paquete | Para qué |
|---|---|
| `polars==2.1.0` | Las tablas, el resumen perezoso y escribir Parquet. Trae `polars-runtime-32`, su motor compilado |
| `duckdb==2.0.0` | SQL sobre el Parquet, dentro de tu proceso |

```
src/observatorio/
├── cli.py                  # modificado: rows_table, exportar y sql
└── core/
    └── columnar.py         # nuevo: Polars y DuckDB, sin reexportar en core/__init__.py
tests/
├── test_columnar.py        # nuevo: los tests del bootcamp
├── test_my_columnar.py     # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes de la semana 26
└── test_package.py         # modificado: columnar en core, polars, duckdb y 0.26.0
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-26`. El `starter/` trae la capa 24 resuelta: `core/summaries.py` y los comandos `resumir` y `evolucion`. **Tú** escribes `columnar.py` y los dos comandos.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-25` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-26
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-26-polars_parquet_y_duckdb/3-proyecto/starter
cp $STARTER/tests/test_columnar.py $STARTER/tests/test_my_columnar.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `tests/test_columnar.py`, con 46 tests, y `tests/test_my_columnar.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` (las imágenes se llaman `week-26`) y `test_package.py` (`columnar` es un módulo de `core`, `duckdb==2.0.0` y `polars==2.1.0` están en las dependencias y la versión es `0.26.0`).

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'duckdb'
E   ModuleNotFoundError: No module named 'observatorio.core.columnar'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Faltan las dos bibliotecas y tu módulo. Antes de seguir, lee `tests/test_columnar.py` entero. Fíjate en:

- `same_rows`, que compara `float` con tolerancia: pandas, Polars y DuckDB suman en distinto orden (teoría 05, sección 3);
- `test_summary_agrees_with_the_pandas_summary`, que compara tu resumen de Polars con el de `summaries.summary` de la semana pasada, con `None` donde pandas pone `NaN`;
- `test_query_cannot_touch_other_files`, que intenta leer y escribir otros archivos desde el SQL;
- `test_importing_the_cli_does_not_load_polars_or_duckdb`, el de la semana 24 para las dos bibliotecas nuevas.

### 4. Las dependencias

```bash
uv add polars==2.1.0 duckdb==2.0.0
uv run pytest -q
```

```
 + duckdb==2.0.0
 + polars==2.1.0
 + polars-runtime-32==2.1.0
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Ahora los dos errores son `No module named 'observatorio.core.columnar'`. Las dos versiones están revisadas en `docs/stack-versions.md` del bootcamp: publicadas hace más de dos semanas y sin avisos de seguridad. No hace falta ningún paquete de tipos: Polars trae los suyos y DuckDB, sus *stubs*.

### 5. La tabla de Polars y su resumen

Crea `src/observatorio/core/columnar.py`:

```python
"""Las medidas en formato columnar: Polars para la tabla, Parquet para el archivo y DuckDB
para preguntarle con SQL.

Como frames y summaries, importa bibliotecas que tardan en cargarse: core/__init__.py no lo
reexporta, y la CLI lo importa solo dentro de los comandos que lo usan.
"""

from pathlib import Path

import duckdb
import polars as pl

from observatorio.core.model import Series

# El nombre de la tabla que ve el SQL de `query`.
TABLE = "medidas"


def frame_of(series: Series) -> pl.DataFrame:
    """Una fila por medida, con label (String) y value (Float64, null si falta)."""
    # El esquema explícito: sin él, una serie vacía, o sin ningún valor, no tendría tipos.
    return pl.DataFrame(
        {"label": [m.label for m in series], "value": [m.value for m in series]},
        schema={"label": pl.String, "value": pl.Float64},
    )


def summary(frame: pl.LazyFrame) -> pl.LazyFrame:
    """Una fila por etiqueta, en el orden en que aparece: count, missing, mean, minimum, maximum.

    Es el mismo resumen que summaries.summary, con null donde pandas pone NaN. Devuelve un
    plan: no calcula nada hasta collect().
    """
    value = pl.col("value")
    # maintain_order: sin él, Polars reparte los grupos entre hilos y el orden cambia.
    return frame.group_by("label", maintain_order=True).agg(
        count=value.count(),
        missing=value.null_count(),
        mean=value.mean(),
        minimum=value.min(),
        maximum=value.max(),
    )
```

- `frame_of` es el de `frames.py` en Polars, sin índice: la posición es el número de fila. Un `None` de tu `Measurement` es `null`, no `NaN` (teoría 01, sección 3).
- El `schema` fija los tipos aunque no haya ninguna fila. Sin él, Polars los deduce de los datos, y de una lista vacía no hay nada que deducir.
- `summary` recibe y devuelve un `LazyFrame`: el plan se puede construir sobre una tabla en memoria (`frame.lazy()`) o sobre un archivo (`pl.scan_parquet`), y solo se ejecuta con `collect()` (teoría 02).
- `count()`, `null_count()`, `mean()`, `min()` y `max()` ignoran los `null`. Por eso Centro tiene `count` 0, `missing` 1 y `null` en las tres medias.

### 6. Preguntar con SQL

Al final del archivo:

```python
def query(path: Path, sql: str) -> tuple[list[str], list[tuple[object, ...]]]:
    """Las columnas y las filas de sql sobre el Parquet de path, que se llama medidas.

    Lanza duckdb.Error si el archivo no se lee o el SQL falla. El SQL no puede leer ni
    escribir ningún otro archivo.
    """
    with duckdb.connect() as connection:
        connection.execute(f"CREATE TABLE {TABLE} AS SELECT * FROM read_parquet(?)", [str(path)])
        # Desde aquí, sin archivos ni red: el SQL lo escribe quien usa la CLI, y solo tiene que
        # ver la tabla. DuckDB no deja volver a activarlos con la conexión abierta.
        connection.execute("SET enable_external_access = false")
        cursor = connection.execute(sql)
        return [column[0] for column in cursor.description], cursor.fetchall()
```

- `duckdb.connect()` sin ruta abre una base de datos **en memoria**: desaparece al salir del `with`.
- La ruta viaja como parámetro `?`, no pegada en el texto: una ruta con una comilla no rompe la consulta (teoría 04, sección 4). El nombre de la tabla sí va en la *f-string*: es una constante tuya, y SQL no admite parámetros para nombres.
- `CREATE TABLE ... AS SELECT` **copia** el Parquet a memoria. Después, `enable_external_access = false` cierra el disco y la red: el SQL que llega desde la terminal puede leer `medidas` y nada más. Sin la copia, la tabla no se podría leer (teoría 05, sección 4).
- `description` tiene una tupla por columna, con el nombre primero. `fetchall()` da las filas como tuplas, con `None` donde SQL tiene `NULL`.

```bash
uv run pytest -q
```

```
19 failed, 907 passed
```

Todos los tests de `columnar.py` pasan. Fallan los de los comandos, que aún no existen, el de la versión y los dos de las imágenes de `compose.yaml`.

### 7. Una tabla para cualquier resultado

Cambia `week-25` por `week-26` en las dos imágenes de `compose.yaml`. Quedan 17.

`frame_text` escribe tablas de pandas. Los resultados de Polars (`rows()`) y de DuckDB (`fetchall()`) son listas de tuplas, con `None` donde falta un dato. En `src/observatorio/cli.py`, después de `evolucion`:

```python
def cell_text(value: object) -> str:
    """Un valor de Polars o de DuckDB como texto: "sin dato" si falta y un decimal si es float."""
    if value is None:
        return "sin dato"
    return f"{value:.1f}" if isinstance(value, float) else str(value)


def rows_table(columns: list[str], rows: list[tuple[object, ...]]) -> Table:
    """Una tabla de Rich, una fila por tupla, con las columnas que están en NAMES en español."""
    table = Table()
    for column in columns:
        table.add_column(NAMES.get(column, column))
    for row in rows:
        table.add_row(*(cell_text(value) for value in row))
    return table
```

- `NAMES.get(column, column)`: las columnas conocidas salen en español; las que invente tu SQL (`AS n`), tal cual.
- Una consulta que llama `mean` a una columna (`avg(value) AS mean`) la verá escrita como `media`: el diccionario de la semana 25 sirve también aquí.
- `cell_text` no recibe nunca un `NaN`: Polars y DuckDB usan `None`. Lo comprueba `test_frame_of_a_missing_value_is_null_not_nan`.

### 8. Los comandos `exportar` y `sql`

Debajo de `rows_table`:

```python
@app.command()
def exportar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    salida: Annotated[
        Path, typer.Argument(metavar="PARQUET", help="El archivo Parquet que escribe.")
    ],
) -> None:
    """Guarda las medidas en Parquet con Polars, y resume lo que guardó."""
    # Importar aquí, como en `filtrar`: Polars y DuckDB tardan en cargarse.
    import polars as pl

    from observatorio.core import columnar

    series, errors = parsed(ruta)
    try:
        columnar.frame_of(series).write_parquet(salida)
    except OSError as problem:
        raise fail(f"no se puede escribir {salida}: {problem}", 2) from problem
    # Resume el archivo, no la tabla en memoria: así se ve lo que de verdad quedó guardado.
    table = columnar.summary(pl.scan_parquet(salida)).collect()
    out.print(rows_table(table.columns, table.rows()) if len(table) else "ninguna medida")
    out.print(f"{len(series)} medidas en {salida.name} · {salida.stat().st_size} bytes")
    if errors:
        raise typer.Exit(1)


@app.command()
def sql(
    parquet: Annotated[
        Path, typer.Argument(metavar="PARQUET", help="Un archivo escrito por `exportar`.")
    ],
    consulta: Annotated[
        str, typer.Argument(metavar="CONSULTA", help="SQL sobre la tabla medidas (label, value).")
    ],
    filas: Annotated[
        int, typer.Option("--filas", "-n", min=1, help="Cuántas filas escribe, como mucho.")
    ] = ROWS,
) -> None:
    """Pregunta con SQL (DuckDB) a un archivo Parquet, que se llama medidas."""
    import duckdb

    from observatorio.core import columnar

    try:
        columns, rows = columnar.query(parquet, consulta)
    except duckdb.Error as problem:
        raise fail(str(problem), 2) from problem
    out.print(rows_table(columns, rows[:filas]))
    if len(rows) > filas:
        out.print(f"… y {len(rows) - filas} más (usa --filas para verlas)")
    out.print(f"{len(rows)} filas")
```

- `exportar` usa `parsed` de la semana 25: los errores llevan el nombre del archivo, y las líneas buenas se guardan igual. Con alguna mala, el Parquet se escribe y el código es 1.
- Después de escribir, **vuelve a leer** el archivo con `scan_parquet` y lo resume. Si algo se perdiera al guardar (un tipo, los `null`), lo verías en la tabla.
- `sql` atrapa `duckdb.Error`, la clase madre de todos los errores de DuckDB: un archivo que no existe (`IOException`), un SQL mal escrito (`ParserException`), una columna que no existe (`BinderException`) o un archivo prohibido (`PermissionException`). Todos son código 2: el comando no pudo hacer lo que le pediste.
- El mensaje de DuckDB es bueno: dice qué columna no existe, sugiere otra y señala dónde. Se escribe entero.
- `--filas`, como en `filtrar`: un `SELECT * FROM medidas` de 100 000 filas no cabe en una terminal.

Actualiza también el docstring del módulo: ahora son dieciséis comandos, con `exportar` y `sql` detrás de `evolucion`.

```bash
uv run pytest -q
```

```
1 failed, 925 passed
```

### 9. Probarlo y medirlo

```bash
uv run observatorio exportar medidas.txt medidas.parquet
uv run observatorio sql medidas.parquet "SELECT label, count(value) AS count, avg(value) AS mean FROM medidas GROUP BY label ORDER BY mean DESC NULLS LAST"
uv run observatorio sql medidas.parquet "SELECT * FROM 'medidas.csv'"
uv run observatorio sql medidas.parquet "SELECT etiqueta FROM medidas"
```

La primera da la salida de "Qué construyes". La segunda, la media de cada etiqueta, con los nombres de `NAMES`:

```
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
┃ etiqueta  ┃ medidas ┃ media    ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
│ Occidente │ 1       │ 61.0     │
│ Oriente   │ 1       │ 55.1     │
│ Norte     │ 2       │ 30.7     │
│ Sur       │ 2       │ 8.8      │
│ Centro    │ 0       │ sin dato │
└───────────┴─────────┴──────────┘
5 filas
```

La tercera intenta leer otro archivo, y la cuarta usa el nombre en español de la columna. Las dos terminan con código 2:

```
error: Permission Error: Cannot access file "medidas.csv" - file system operations are disabled by configuration
error: Binder Error: Referenced column "etiqueta" not found in FROM clause!
Candidate bindings: "value"

LINE 1: SELECT etiqueta FROM medidas
               ^^^^^^^^
```

Ahora con el archivo grande de la semana 22:

```bash
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
uv run observatorio filtrar perfil/grande.txt -o perfil/grande.csv > /dev/null 2>&1
time uv run observatorio exportar perfil/grande.txt perfil/grande.parquet 2> /dev/null
ls -l perfil/
time uv run observatorio sql perfil/grande.parquet "SELECT label, avg(value) AS mean FROM medidas GROUP BY label ORDER BY label"
```

```
100000 medidas en grande.parquet · 252313 bytes
real	0m1.111s
```

```
1037872 grande.csv
252313 grande.parquet
1037857 grande.txt
```

```
5 filas
real	0m0.676s
```

El Parquet ocupa la cuarta parte que el texto. `exportar` tarda lo mismo que `resumir`, porque lee el texto; `sql` no lo lee, y le pregunta lo que quieras en dos tercios de segundo, casi todo arrancar Python e importar.

Mide cada pieza con `timeit` en un `uv run python`, como en las semanas anteriores. En la máquina del bootcamp, con 100 000 medidas:

| Operación | pandas | Polars | DuckDB |
|---|---|---|---|
| De `Series` a tabla | 8,9 ms (`frames.frame_of`) | 6,6 ms (`columnar.frame_of`) | — |
| Resumen por etiqueta, en memoria | 7,9 ms (`summaries.summary`) | 2,1 ms (`summary(...).collect()`) | — |
| Resumen leyendo el Parquet | — | 3,7 ms (`summary(scan_parquet(...))`) | 30,7 ms (`query`) |
| Escribir el archivo | 69 ms (`write_frame`, CSV) | 3,9 ms (`write_parquet`) | — |

`query` tarda más que Polars porque abre una base de datos y copia el archivo antes de preguntar: unos 14 ms en conectar y 8 ms en copiar. Es el precio de cerrar el disco al SQL de fuera (teoría 05, sección 4). Apunta tus números: van al *pull request*.

### 10. La versión

En `pyproject.toml`, `version = "0.26.0"`, y:

```bash
uv lock
uv run pytest -q
uv run observatorio --version
```

```
926 passed
observatorio 0.26.0
```

### 11. Calidad, cobertura y Docker

```bash
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
docker images local/observatorio
uv run python -c "import sys, observatorio.cli; print('polars' in sys.modules, 'duckdb' in sys.modules)"
```

`coverage report` debe dar 100 % en `columnar.py` y en `cli.py`. `alembic check` sigue en `No new upgrade operations detected.`. La comprobación de `sys.modules` escribe `False False`.

En `docker images`, la imagen `week-26` mide unos 850 MB, frente a los 508 MB de `week-25`: 342 MB más. Mira de dónde salen:

```bash
docker run --rm --entrypoint sh local/observatorio:week-26 -c 'du -sh /opt/venv/lib/python3.14/site-packages/* | sort -h | tail -5'
```

```
29M	/opt/venv/lib/python3.14/site-packages/sqlalchemy
43M	/opt/venv/lib/python3.14/site-packages/numpy
65M	/opt/venv/lib/python3.14/site-packages/_duckdb.abi3.so
83M	/opt/venv/lib/python3.14/site-packages/pandas
170M	/opt/venv/lib/python3.14/site-packages/_polars_runtime_32
```

El motor de Polars es lo más grande de la imagen: más que pandas y NumPy juntos. La teoría 05, sección 6, explica cuándo compensa.

### 12. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `columnar.py` | `group_by("label", maintain_order=True)` por `group_by("label")` | |
| `columnar.py` | `missing=value.null_count()` por `missing=value.is_nan().sum()` | |
| `columnar.py` | `count=value.count()` por `count=value.len()` | |
| `columnar.py` | `mean=value.mean()` por `mean=value.median()` | |
| `columnar.py` | quita la línea `schema={"label": pl.String, "value": pl.Float64},` | |
| `columnar.py` | quita `connection.execute("SET enable_external_access = false")` | |
| `cli.py` | `rows_table(columns, rows[:filas])` por `rows_table(columns, rows)` | |
| `cli.py` | quita `if value is None:` y su `return "sin dato"` | |
| `cli.py` | `except duckdb.Error` por `except duckdb.ProgrammingError` | |
| `cli.py` | en `exportar`, quita ` if len(table) else "ninguna medida"` | |

Los diez mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el segundo mutante, ¿qué da `value.is_nan()` para una medida sin valor, y qué suma entonces `missing`? Pruébalo en `uv run python` con `pl.Series([1.0, None]).is_nan()`. ¿Qué te dice eso de `null` y `NaN`?
- Con el noveno, ¿qué test falla primero, y qué excepción lanza DuckDB en él? Mira de qué clases hereda con `duckdb.IOException.__mro__` y `duckdb.PermissionException.__mro__`, y explica por qué el comando atrapa `duckdb.Error`.

### 13. Tus tests

En `tests/test_my_columnar.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con los valores de tu dominio y las funciones de `test_columnar.py` (`summary_rows`, `same_rows`, `parquet_of`, `cells`, `header`, `write`). Ideas:

- `exportar` con un archivo de tu dominio, y que el Parquet tenga tus etiquetas en el orden del archivo;
- una consulta SQL que tenga sentido en tu dominio (la etiqueta con la media más alta, las medidas por encima de un umbral tuyo) y su resultado exacto;
- que `summary` sobre `scan_parquet` con un filtro de `pl.col("label")` dé una sola fila (con Hypothesis);
- que la suma de `count` del resumen de Polars sea el `count(value)` de DuckDB;
- que `query` no pueda escribir un archivo con `COPY ... TO`, con una ruta de `tmp_path`;
- que `sql` con `-n 1` escriba una fila y el aviso de las que faltan.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1058 tests en verde.

### 14. README y pull request

En el `README.md` de tu repositorio, añade una sección "Parquet y SQL": qué escribe `exportar`, cómo se llama la tabla y sus columnas en `sql`, dos consultas de ejemplo de tu dominio, y que el SQL no puede leer ni escribir otros archivos.

Commits sugeridos, en este orden:

1. `test: add columnar tests`
2. `build: add polars and duckdb`
3. `feat: add columnar module`
4. `feat: add exportar and sql commands`
5. `chore: bump version to 0.26.0`
6. `test: add my columnar tests`

```bash
git push -u origin week-26
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-26` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. `exportar` con un archivo de tu dominio y dos consultas `sql` que tengan sentido para ti.
3. Tu tabla de tiempos del paso 9 y el tamaño de tu imagen.
4. La tabla de mutantes del paso 12 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'duckdb'` | Falta el paso 4: `uv add polars==2.1.0 duckdb==2.0.0` |
| `ModuleNotFoundError: No module named 'observatorio.core.columnar'` | Falta el paso 5, o el archivo no está en `src/observatorio/core/` |
| `test_dependencies_are_pinned` falla | Añadiste las versiones sin `==`, o a mano en otro orden: usa `uv add` con la versión exacta |
| `test_frame_of_an_empty_series_keeps_the_types` falla: `'value': Null` | Falta `schema=` en `frame_of` |
| Los tests de `summary` fallan en el orden de las etiquetas | Falta `maintain_order=True` en `group_by` |
| `missing` sale 0 en una etiqueta sin valor | Usaste `is_nan()`: lo que falta en Polars es `null`, y se cuenta con `null_count()` |
| `test_query_cannot_touch_other_files` falla | Falta `SET enable_external_access = false`, o va **antes** de `CREATE TABLE`, y entonces no se lee ni tu archivo |
| `Permission Error: Cannot access file "...medidas.parquet"` con tu propio archivo | Cerraste el disco antes de copiar: `CREATE TABLE` va primero |
| `test_exportar_cannot_write_exits_2` falla | Falta el `try` alrededor de `write_parquet`, o atrapas otra excepción: es `OSError` |
| `test_importing_the_cli_does_not_load_polars_or_duckdb` falla | Algún `import polars` o `import duckdb` está fuera de los comandos |

## Entrega

1. Rama `week-26` con `core/columnar.py`, los comandos `exportar` y `sql`, `polars` y `duckdb` fijados, las imágenes `week-26`, la versión `0.26.0` y al menos 6 tests tuyos en `test_my_columnar.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Parquet y SQL".
4. *Pull request* `week-26` → `main` con lo que pide el paso 14.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Una pregunta, tres herramientas](../2-practicas/ejercicio-04-una-pregunta-tres-herramientas/README.md) | **Proyecto · Exportar a Parquet y preguntar con SQL** | [Rúbrica de la semana 26](../rubrica-evaluacion.md) |
