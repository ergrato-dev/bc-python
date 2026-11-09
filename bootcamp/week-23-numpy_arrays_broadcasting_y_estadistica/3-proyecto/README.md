# Proyecto — Observatorio, capa 22: estadística con NumPy

⏱️ 6 h 30 min · Capa 22 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

En la semana 22 decidiste con números no usar NumPy en `informe`: importarlo costaba más de lo que ahorraba. Esta semana entra en el proyecto, pero donde compensa y sin que lo paguen los demás comandos: un comando nuevo, `estadisticas`, que resume los valores de un archivo con NumPy.

```
$ uv run observatorio estadisticas medidas.txt
error: línea 10: 'Sur 9,5'
Estadísticas
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Medida     ┃       Valor ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ con valor  │           6 │
│ sin dato   │           1 │
│ media      │ 32.5 unidad │
│ desviación │ 22.8 unidad │
│ mínimo     │  8.0 unidad │
│ Q1         │ 10.2 unidad │
│ mediana    │ 30.7 unidad │
│ Q3         │ 53.5 unidad │
│ máximo     │ 61.0 unidad │
└────────────┴─────────────┘
histograma (5 intervalos):
   8.0 –   18.6  ██████████████████████████████ 3
  18.6 –   29.2                                 0
  29.2 –   39.8                                 0
  39.8 –   50.4  ██████████                     1
  50.4 –   61.0  ████████████████████           2
atípicas (|z| > 2): ninguna
media por etiqueta: Norte 30.7, Occidente 61.0, Oriente 55.1, Sur 8.8
```

| Pieza | Qué hace |
|---|---|
| `numpy==2.5.4` | Nueva dependencia de producción: la imagen `runtime` la necesita |
| `core/arrays.py` | La serie como array de `float64` con NaN, y sobre él el resumen, las puntuaciones z, los atípicos, el histograma y la media por etiqueta |
| `estadisticas RUTA [-u UMBRAL] [-i INTERVALOS]` | El comando nuevo, que importa NumPy **solo** cuando se ejecuta |

```
src/observatorio/
├── cli.py                  # modificado: estadisticas, stats_table, histogram_lines
└── core/
    └── arrays.py           # nuevo: NumPy, sin reexportar en core/__init__.py
tests/
├── test_arrays.py          # nuevo: los tests del bootcamp
├── test_my_arrays.py       # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes de la semana 23
└── test_package.py         # modificado: arrays en core, numpy y 0.23.0
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-23`. El `starter/` trae la capa 21 resuelta: `informe --filas`, `Series.parse` y `py-spy`. **Tú** escribes `arrays.py` y el comando.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-22` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-23
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-23-numpy_arrays_broadcasting_y_estadistica/3-proyecto/starter
cp $STARTER/tests/test_arrays.py $STARTER/tests/test_my_arrays.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `tests/test_arrays.py`, con 40 tests, y `tests/test_my_arrays.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` (las imágenes se llaman `week-23`) y `test_package.py` (`arrays` es un módulo de `core`, `numpy==2.5.4` está en las dependencias y la versión es `0.23.0`).

### 3. Tests en rojo y la dependencia nueva

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'numpy'
...
ERROR tests/test_arrays.py
ERROR tests/test_my_arrays.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Los dos archivos nuevos importan NumPy y pytest ni siquiera puede leerlos. Añádelo, con la versión fijada (`docs/stack-versions.md`):

```bash
uv add numpy==2.5.4
```

```
 + numpy==2.5.4
```

Esta vez **no** es `--dev`: `estadisticas` lo necesita para funcionar, también en la imagen `runtime`. NumPy no tiene dependencias propias; `uv.lock` solo gana una entrada, con las ruedas (`.whl`) compiladas para cada sistema.

```bash
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.arrays'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Ahora falta tu módulo. Antes de escribirlo, lee `tests/test_arrays.py` entero. Fíjate en:

- `floats(1, math.nan, 3)`, que crea arrays de prueba, y `np.testing.assert_array_equal` y `assert_allclose`, que comparan arrays con NaN y con tolerancia (teoría 05, sección 3);
- los cuatro tests con `@given`; dos comparan lo nuevo con lo que ya tenías, `trends.median` y `Series.means`;
- `test_zscores_without_spread_are_nan_and_do_not_warn`, que convierte los avisos en errores;
- el último, `test_importing_does_not_load_numpy`, que en otro proceso comprueba que ni `observatorio.core` ni `observatorio.cli` cargan NumPy al importarse.

### 4. La serie como array

Crea `src/observatorio/core/arrays.py`:

```python
"""Las medidas como arrays de NumPy: la estadística de la serie entera, sin bucles.

Qué: convierte una Series en un array de float64 (NaN donde falta el dato) y calcula
sobre él el resumen, las puntuaciones z, las medidas atípicas, el histograma y la
media de cada etiqueta.
Para qué: cada operación recorre el array en C, de una vez; con 100 000 medidas es
mucho más rápido que el bucle equivalente en Python, y se escribe en una línea.
Impacto: importar NumPy cuesta alrededor de 0,1 s. Este módulo no se reexporta en
`observatorio.core`, y la CLI lo importa solo en `estadisticas`: `informe` no lo paga.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from observatorio.core.model import Series

# Un array de números de coma flotante de 64 bits, el tipo de casi todo lo que sigue.
Floats = NDArray[np.float64]
# Un array de enteros del tamaño de un índice: conteos y posiciones.
Counts = NDArray[np.intp]


def values_array(series: Series) -> Floats:
    """Los valores de la serie en un array, en orden; NaN donde falta el dato.

    Un array tiene un solo tipo: None no cabe en float64, NaN sí. Así la posición i del
    array sigue siendo la medida i de la serie.
    """
    return np.fromiter(
        (np.nan if measurement.value is None else measurement.value for measurement in series),
        dtype=np.float64,
        count=len(series),
    )


def labels_array(series: Series) -> NDArray[np.str_]:
    """Las etiquetas de la serie en un array de texto, en el mismo orden que values_array."""
    return np.array([measurement.label for measurement in series], dtype=np.str_)
```

- `np.fromiter` llena el array desde un generador, sin crear una lista intermedia. `count` le dice cuántos elementos vienen, para que reserve la memoria de una vez (teoría 01, sección 2).
- Las medidas sin valor se quedan **en su sitio**, como NaN. Si las quitaras aquí, la posición 7 del array ya no sería la medida 7 de la serie, y no sabrías qué etiqueta tiene un atípico.
- `dtype=np.str_` en `labels_array` importa con una serie vacía: `np.array([])` daría `float64`, y `test_labels_array_is_text_even_when_empty` lo comprueba.

`arrays.py` **no** se añade a `core/__init__.py`. Si lo hicieras, cualquier `from observatorio.core import ...` cargaría NumPy. `test_every_module_lives_in_core` comprueba que el archivo existe en `core/`; el último test de `test_arrays.py`, que nadie lo importa sin querer.

### 5. El resumen

Debajo de los alias, el resumen como *dataclass* inmutable (semana 9), con tipos de Python:

```python
@dataclass(frozen=True)
class Stats:
    """El resumen de los valores presentes de una serie, los que no son NaN."""

    count: int
    missing: int
    mean: float
    std: float
    minimum: float
    q1: float
    median: float
    q3: float
    maximum: float
```

Y la función que lo calcula, al final del archivo:

```python
def stats_of(values: Floats) -> Stats | None:
    """El resumen de los valores que no son NaN, o None si no hay ninguno.

    La desviación es la de la población (ddof=0), la misma que np.std por defecto.
    """
    present = values[~np.isnan(values)]
    if present.size == 0:
        return None
    q1, median, q3 = np.percentile(present, [25, 50, 75])
    return Stats(
        count=int(present.size),
        missing=int(values.size - present.size),
        mean=float(present.mean()),
        std=float(present.std()),
        minimum=float(present.min()),
        q1=float(q1),
        median=float(median),
        q3=float(q3),
        maximum=float(present.max()),
    )
```

- `values[~np.isnan(values)]` se queda con los presentes, una vez; todo lo demás se calcula sobre `present` (teoría 04, sección 2).
- Sin valores, `None`: la media de nada no existe, y sin el `if` NumPy avisaría con `Mean of empty slice` y devolvería `nan`.
- `np.percentile` calcula los tres cuartiles en una llamada.
- `float(...)` e `int(...)` convierten los escalares de NumPy en tipos de Python: lo que sale del módulo no es NumPy (teoría 05, sección 2).

### 6. Puntuaciones z, atípicos e histograma

```python
def zscores(values: Floats) -> Floats:
    """A cuántas desviaciones de la media está cada valor: (valor - media) / desviación.

    NaN donde falta el dato. Si no hay valores o todos son iguales (desviación 0), todo
    NaN: ningún valor se aleja de la media, y dividir por 0 daría inf o NaN con un aviso.
    """
    present = values[~np.isnan(values)]
    std = present.std() if present.size else 0.0
    if std == 0:
        return np.full_like(values, np.nan)
    return (values - present.mean()) / std


def outliers(values: Floats, threshold: float) -> Counts:
    """Las posiciones de los valores con |z| > threshold, en orden.

    Una comparación con NaN da False: los datos que faltan nunca son atípicos.
    """
    return np.flatnonzero(np.abs(zscores(values)) > threshold)


def histogram(values: Floats, bins: int) -> tuple[Counts, Floats]:
    """Cuántos valores caen en cada uno de `bins` intervalos iguales, y sus bordes.

    Sin los NaN. Devuelve bins conteos y bins + 1 bordes; el último intervalo incluye
    su borde derecho, así que el máximo también cuenta.
    """
    counts, edges = np.histogram(values[~np.isnan(values)], bins=bins)
    return counts, edges
```

- `zscores` resta y divide el array **entero**, NaN incluidos: un NaN da NaN en su posición, y el resultado tiene la misma forma que la entrada. La media y la desviación, en cambio, se calculan sobre los presentes.
- `np.full_like(values, np.nan)` crea un array de la misma forma y tipo, todo NaN. Comprobar `std == 0` **antes** de dividir es la forma de no avisar (teoría 04, sección 3).
- En `outliers`, `np.abs(z) > threshold` es una máscara y `np.flatnonzero` da sus posiciones. NaN comparado con lo que sea es `False`: no hace falta quitarlos.
- `np.histogram` no acepta NaN: se los quitas antes.

### 7. La media de cada etiqueta, sin bucles

El último, y el más interesante. Tu `Series.means()` agrupa con un diccionario (semana 5). Con arrays, se agrupa así:

```python
def group_means(labels: NDArray[np.str_], values: Floats) -> dict[str, float]:
    """La media de cada etiqueta, sin bucles: {"Norte": 30.7, "Sur": 8.75}.

    Mismo resultado que Series.means(): sin los NaN, y una etiqueta sin ningún valor no
    aparece. Las etiquetas salen ordenadas, porque np.unique las ordena.
    """
    present = ~np.isnan(values)
    names, codes = np.unique(labels[present], return_inverse=True)
    sums = np.bincount(codes, weights=values[present])
    counts = np.bincount(codes)
    return dict(zip(names.tolist(), (sums / counts).tolist(), strict=True))
```

Con `labels = ["Norte", "Sur", "Norte"]` y `values = [12.5, 8.0, 48.9]`:

| Paso | Resultado |
|---|---|
| `np.unique(labels, return_inverse=True)` | `names = ['Norte' 'Sur']`, `codes = [0 1 0]`: cada etiqueta, cambiada por su número |
| `np.bincount(codes, weights=values)` | `[61.4  8. ]`: suma los valores de cada número |
| `np.bincount(codes)` | `[2 1]`: cuántos hay de cada número |
| `sums / counts` | `[30.7  8. ]`: la media de cada etiqueta |

`present` se aplica a las etiquetas y a los valores **a la vez**, para que sigan emparejados. `.tolist()` convierte nombres y medias en `str` y `float` de Python. Es un *group by* sin bucles: lo que hace pandas por debajo con `df.groupby("etiqueta")["valor"].mean()` (semana 25).

```bash
uv run pytest -q
```

```
14 failed, ... passed
```

Los tests de `arrays.py` pasan, incluidos los de Hypothesis. Si alguno falla con un ejemplo raro, léelo: Hypothesis te da el caso más pequeño que lo rompe.

### 8. El comando `estadisticas`

Cambia `week-22` por `week-23` en las dos imágenes de `compose.yaml` (`local/observatorio:week-23-test` y `local/observatorio:week-23`). Quedan 12.

En `src/observatorio/cli.py`, primero los tipos **solo para mypy**. Cambia el import de `typing` y añade el bloque debajo de los imports:

```python
from typing import TYPE_CHECKING, Annotated
```

```python
if TYPE_CHECKING:
    # Solo para mypy: en ejecución no se importa NumPy al cargar la CLI. Desde Python
    # 3.14 las anotaciones se evalúan cuando alguien las pide, así que `Stats` y
    # `Floats` pueden aparecer en las firmas sin estar importados de verdad.
    from observatorio.core.arrays import Counts, Floats, Stats
```

Junto a `TOP`, `WINDOW` y `ROWS`, los valores por defecto:

```python
# A partir de cuántas desviaciones de la media es atípica una medida en `estadisticas`,
# y en cuántos intervalos reparte su histograma, si no se dice con --umbral e --intervalos.
THRESHOLD = 2.0
BINS = 5
# Cuántos caracteres mide la barra del intervalo con más medidas en el histograma.
BAR = 30
```

Dos funciones que escriben, antes de `files_table`:

```python
def stats_table(stats: Stats, unit: str) -> Table:
    """Una fila por número del resumen: cuántas, media, desviación y cuartiles."""
    table = Table(title="Estadísticas")
    table.add_column("Medida")
    table.add_column("Valor", justify="right")
    table.add_row("con valor", str(stats.count))
    table.add_row("sin dato", str(stats.missing))
    for name, value in [
        ("media", stats.mean),
        ("desviación", stats.std),
        ("mínimo", stats.minimum),
        ("Q1", stats.q1),
        ("mediana", stats.median),
        ("Q3", stats.q3),
        ("máximo", stats.maximum),
    ]:
        table.add_row(name, f"{value:.1f} {unit}")
    return table


def histogram_lines(counts: Counts, edges: Floats) -> list[str]:
    """Una línea por intervalo: sus bordes, una barra proporcional y cuántas medidas caen."""
    longest = counts.max()
    return [
        f"{low:6.1f} – {high:6.1f}  {'█' * round(count / longest * BAR):<{BAR}} {count}"
        for low, high, count in zip(edges[:-1], edges[1:], counts, strict=True)
    ]
```

`edges[:-1]` y `edges[1:]` son los bordes izquierdo y derecho de cada intervalo: dos cortes desplazados, como `pairwise` (semana 6). `{...:<{BAR}}` rellena la barra con espacios hasta 30 caracteres, para que los conteos queden alineados. `counts.max()` nunca es 0: solo se llama si hay algún valor.

Y el comando, detrás de `informe`:

```python
@app.command()
def estadisticas(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    umbral: Annotated[
        float,
        typer.Option("--umbral", "-u", min=0, help="Desviaciones a partir de las que es atípica."),
    ] = THRESHOLD,
    intervalos: Annotated[
        int, typer.Option("--intervalos", "-i", min=1, help="Intervalos del histograma.")
    ] = BINS,
) -> None:
    """Resume los valores con NumPy: estadísticas, histograma, atípicas y medias."""
    # Importar aquí: NumPy tarda alrededor de 0,1 s en cargarse, y solo lo usa este comando.
    from observatorio.core import arrays

    try:
        lines = open_file(ruta).lines()
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {error}")
    values = arrays.values_array(series)
    stats = arrays.stats_of(values)
    if stats is None:
        out.print("ninguna medida con valor")
    else:
        out.print(stats_table(stats, UNIT))
        counts, edges = arrays.histogram(values, intervalos)
        out.print(
            "\n".join([f"histograma ({intervalos} intervalos):", *histogram_lines(counts, edges)])
        )
        z = arrays.zscores(values)
        found = arrays.outliers(values, umbral)
        atypical = (
            ", ".join(f"{series[i].label} {values[i]:.1f} (z {z[i]:+.1f})" for i in found)
            or "ninguna"
        )
        means = arrays.group_means(arrays.labels_array(series), values)
        out.print(f"atípicas (|z| > {umbral:g}): {atypical}")
        out.print(
            "media por etiqueta: "
            + ", ".join(f"{label} {mean:.1f}" for label, mean in means.items())
        )
    if errors:
        raise typer.Exit(1)
```

- El `import` va **dentro** del comando, como el de uvicorn en `servir` (teoría 05, sección 4). Si lo subes al principio del archivo, `test_importing_does_not_load_numpy[observatorio.cli]` falla.
- `Series.parse` (semana 22) da la serie y los errores en una pasada; los errores van a stderr y el código de salida es 1, como en `informe`.
- `found` son posiciones en el array, y como `values_array` no movió nada, también lo son en la serie: `series[i].label` es la etiqueta del atípico.
- `{umbral:g}` escribe `2` en lugar de `2.0`, y `0.5` tal cual.
- `min=0` y `min=1`: Typer rechaza `-u -1` e `-i 0` con un error de uso (código 2), en vez de que `np.histogram` falle con `ValueError`.

Actualiza también el docstring del módulo: ahora son once comandos, con `estadisticas` (y `servir`, que faltaba en la lista).

```bash
uv run pytest -q
```

```
1 failed, ... passed
```

### 9. Probarlo y medirlo

```bash
uv run observatorio estadisticas medidas.txt
uv run observatorio estadisticas -u 1 medidas.txt
```

La primera da la salida de "Qué construyes". Con `-u 1`, las atípicas cambian:

```
atípicas (|z| > 1): Sur 8.0 (z -1.1), Occidente 61.0 (z +1.2), Sur 9.5 (z -1.0)
```

Con seis valores, ninguno se aleja dos desviaciones: con tan pocos datos, la propia muestra define qué es "normal". Prueba con tus datos y busca un umbral que tenga sentido en tu dominio.

Ahora, con el archivo grande de la semana 22:

```bash
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
time uv run observatorio estadisticas perfil/grande.txt > /dev/null
uv run observatorio estadisticas perfil/grande.txt | tail -9
```

```
real	0m0.840s
```

```
histograma (5 intervalos):
   0.0 –   16.0  ██████████████████████████████ 19088
  16.0 –   32.0  █████████████████████████████  18762
  32.0 –   48.0  ██████████████████████████████ 18994
  48.0 –   64.0  ██████████████████████████████ 19062
  64.0 –   80.0  ██████████████████████████████ 19134
atípicas (|z| > 2): ninguna
media por etiqueta: Centro 39.9, Este 40.0, Norte 40.3, Oeste 40.0, Sur 39.9
```

El generador reparte los valores **por igual** entre 0 y 80 (`rng.uniform`), y el histograma lo muestra: cinco barras iguales, no una campana. Con una distribución uniforme, ningún valor puede alejarse más de 1,73 desviaciones de la media, así que nunca hay atípicas con `-u 2`. No es un fallo: es lo que dicen los datos.

¿Dónde va el tiempo? Mide cada pieza con `timeit` en un `uv run python` (ejercicio 01 de la semana 22). En la máquina del bootcamp, con 100 000 medidas:

| Operación | Python puro | NumPy |
|---|---|---|
| Media, desviación y mediana | 52 ms (`statistics.fmean`, `statistics.pstdev`, `median`) | 1,6 ms (`stats_of`, con los cuartiles) |
| Puntuaciones z | 44 ms (comprensión) | 0,2 ms (`zscores`) |
| Media por etiqueta | **7,8 ms** (`series.means()`) | 11,2 ms (`group_means`) |
| Convertir la serie | — | 4,1 ms (`values_array`) y 8,8 ms (`labels_array`) |
| Analizar el texto | 71 ms (`Series.parse`) | — |

NumPy gana por 30 y por 200 con números, y **pierde** con las etiquetas: `np.unique` ordena 100 000 textos para agruparlos, y el diccionario lo hace en una pasada (teoría 05, sección 5). Y el total sigue dominado por arrancar, importar y analizar texto (Amdahl). Apunta tus números: van al *pull request*.

Por último, comprueba que los demás comandos no pagan:

```bash
uv run python -c "import sys, observatorio.cli; print('numpy' in sys.modules)"
time uv run observatorio informe -f perfil/grande.txt > /dev/null
```

```
False
real	0m0.990s
```

`informe` tarda lo mismo que en la semana 22.

### 10. La versión

En `pyproject.toml`, `version = "0.23.0"`, y:

```bash
uv lock
uv run pytest -q
uv run observatorio --version
```

```
774 passed
observatorio 0.23.0
```

### 11. Calidad, cobertura y Docker

```bash
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
docker images local/observatorio
```

`mypy` estricto pasa sin configurar nada: NumPy trae sus propios tipos. `coverage report` debe dar 100 % en `arrays.py` y en `cli.py`. `alembic check` sigue en `No new upgrade operations detected.`.

En `docker images`, compara `week-22` y `week-23`:

```
week-23        395MB
week-22        301MB
```

94 MB más: NumPy trae compilada su propia biblioteca de álgebra lineal (OpenBLAS). En la CI, el trabajo `image` pasa Trivy sobre la imagen nueva: `numpy==2.5.4` no tiene avisos de seguridad publicados (lo comprobaste en `docs/stack-versions.md`).

### 12. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `arrays.py` | `np.nan if measurement.value is None` por `0.0 if ...` | |
| `arrays.py` | quita `count=len(series),` en `values_array` | |
| `arrays.py` | `present = values[~np.isnan(values)]` por `present = values` en `stats_of` | |
| `arrays.py` | `missing=int(values.size - present.size)` por `missing=0` | |
| `arrays.py` | `present.std()` por `present.std(ddof=1)` en `stats_of` | |
| `arrays.py` | `if std == 0:` por `if present.size == 0:` | |
| `arrays.py` | `> threshold` por `>= threshold` | |
| `arrays.py` | `sums / counts` por `sums / counts.max()` | |
| `cli.py` | mueve `from observatorio.core import arrays` al principio del archivo | |
| `cli.py` | quita `min=0,` de `--umbral` | |

Nueve mueren. Uno **sobrevive**: ¿cuál, y por qué no hay test que pueda matarlo? Pista: compara el array que devuelve `values_array` con y sin el cambio. Un mutante que no cambia lo que hace el programa se llama **equivalente**: no delata un test que falta, sino una línea que solo cambia **cómo** se hace (aquí, cuánta memoria se reserva y cuándo). Explícalo en el *pull request*.

Fíjate en el sexto: con valores iguales, el resultado sigue siendo todo NaN. Solo lo mata el test que convierte los avisos en errores.

### 13. Tus tests

En `tests/test_my_arrays.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con los valores de tu dominio y las funciones de `test_arrays.py` (`floats`, `stats_rows`, `write`). Ideas:

- un atípico de verdad en tus datos: un archivo con 20 valores normales y uno imposible, y `estadisticas` lo encuentra con su etiqueta;
- que los conteos de `histogram` sumen el `count` de `stats_of`, con cualquier número de intervalos (con Hypothesis);
- que `group_means` dé las mismas etiquetas que `Series.labels()` cuando todas tienen valor;
- que `zscores` de `[a, b]` sea siempre `[-1, 1]` si `a < b` (con Hypothesis);
- que `stats_of` dé la misma mediana que `trends.median` con **tus** datos de ejemplo;
- que `estadisticas` con un `.csv` dé lo mismo que con el `.txt` equivalente.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 779 tests en verde.

### 14. README y pull request

En el `README.md` de tu repositorio, añade una sección "Estadísticas": qué escribe `estadisticas`, sus opciones `--umbral` e `--intervalos`, y por qué NumPy solo se importa en ese comando.

Commits sugeridos, en este orden:

1. `test: add array statistics tests`
2. `build: add numpy`
3. `feat: add array statistics module`
4. `feat: add estadisticas command`
5. `chore: bump version to 0.23.0`
6. `test: add my array tests`

```bash
git push -u origin week-23
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-23` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `estadisticas` con tus datos, y un umbral que tenga sentido en tu dominio, con el porqué.
3. Tu tabla de tiempos del paso 9: dónde gana NumPy y dónde no.
4. El tamaño de la imagen antes y después.
5. La tabla de mutantes del paso 12 y por qué el superviviente es equivalente.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | Falta el paso 3: `uv add numpy==2.5.4` |
| `test_dependencies_are_pinned` falla | Lo añadiste con `--dev` o sin versión: `uv remove --dev numpy` y `uv add numpy==2.5.4` |
| `ModuleNotFoundError: No module named 'observatorio.core.arrays'` | El archivo tiene que llamarse `arrays.py` y vivir en `src/observatorio/core/` |
| `test_importing_does_not_load_numpy[observatorio.core]` falla | Has añadido `arrays` a `core/__init__.py`: quítalo |
| `test_importing_does_not_load_numpy[observatorio.cli]` falla | El `from observatorio.core import arrays` está fuera de `estadisticas`, o el bloque de tipos no está dentro de `if TYPE_CHECKING:` |
| `NameError: name 'Stats' is not defined` al ejecutar | Usas Python anterior a 3.14, o has puesto `Stats` en los parámetros de un comando de Typer: solo en las funciones auxiliares |
| `test_zscores_without_spread_are_nan_and_do_not_warn` falla con `RuntimeWarning` | Divides antes de comprobar que la desviación no es 0 |
| `test_group_means_agree_with_series_means` falla | Comprueba que aplicas `present` a las etiquetas **y** a los valores |
| mypy: `incompatible type ... signedinteger ...; expected ... float64` | Los conteos son `Counts` (`NDArray[np.intp]`), no `Floats` |
| `test_estadisticas_writes_the_summary` falla en una fila | Compara el nombre exacto de la fila (`"con valor"`, `"desviación"`...) y el formato `.1f` |
| La barra del histograma no queda alineada | Falta `:<{BAR}}` en el f-string: rellena con espacios hasta 30 |
| `docker compose run --rm app` falla con `No module named 'numpy'` | Reconstruye la imagen: `docker compose build app api` |

## Entrega

1. Rama `week-23` con `core/arrays.py`, el comando `estadisticas`, `numpy==2.5.4` en las dependencias, las imágenes `week-23`, la versión `0.23.0` y al menos 6 tests tuyos en `test_my_arrays.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Estadísticas".
4. *Pull request* `week-23` → `main` con lo que pide el paso 14.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · NaN, estadística y aleatoriedad](../2-practicas/ejercicio-04-nan-estadistica-y-aleatoriedad/README.md) | **Proyecto · Estadística con NumPy** | [Rúbrica de la semana 23](../rubrica-evaluacion.md) |
