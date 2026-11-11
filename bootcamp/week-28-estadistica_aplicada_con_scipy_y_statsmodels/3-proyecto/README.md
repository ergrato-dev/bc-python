# Proyecto — Observatorio, capa 27: comparar dos etiquetas

⏱️ 6 h 30 min · Capa 27 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

`resumir` escribe la media de cada etiqueta, y es tentador leerla así: "el Norte mide más que el Sur". Esta semana tu Observatorio responde a la pregunta de verdad: **¿esa diferencia es real, o puede ser azar?**

```
$ uv run observatorio comparar medidas.txt Norte Sur
error: medidas.txt: línea 10: 'Sur 9,5'
Norte: 2 medidas, media 30.70, desviación 25.74
Sur: 2 medidas, media 8.75, desviación 1.06
diferencia Norte - Sur: 21.95, IC 95 %: [-207.66, 251.56]
tamaño del efecto (d de Cohen): 1.21
p (Welch): 0.44 · p (Mann-Whitney): 0.333
```

El Norte sale 22 °C por encima, pero con dos medidas de cada etiqueta la diferencia de verdad puede estar en cualquier sitio entre −208 y 252. `comparar` no da un veredicto: da los números que lo deciden (teoría 03, sección 9).

| Pieza | Qué hace |
|---|---|
| `core/inference.py` | `sample` saca los valores de una etiqueta; `difference` compara dos muestras con Welch y Mann-Whitney, y devuelve un `Comparison` con la diferencia, su intervalo, la d de Cohen y los p-valores |
| `comparar RUTA ETIQUETA OTRA [--confianza]` | Lee el archivo, compara las dos etiquetas y escribe el informe |

Dos dependencias nuevas:

| Paquete | Grupo | Para qué |
|---|---|---|
| `scipy==1.18.1` | Proyecto | Las pruebas y los intervalos de `scipy.stats` |
| `scipy-stubs==1.18.1.1` | `dev` | Los tipos de SciPy para mypy. Trae `optype` |

```
src/observatorio/
├── cli.py                  # modificado: comparar
└── core/
    └── inference.py        # nuevo: SciPy, sin reexportar en core/__init__.py
tests/
├── test_inference.py       # nuevo: los tests del bootcamp
├── test_my_inference.py    # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes de la semana 28
└── test_package.py         # modificado: inference en core, scipy, scipy-stubs y 0.28.0
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-28`. El `starter/` trae la capa 26 resuelta: `core/charts.py` y el comando `graficar`. **Tú** escribes `inference.py` y `comparar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-27` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-28
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-28-estadistica_aplicada_con_scipy_y_statsmodels/3-proyecto/starter
cp $STARTER/tests/test_inference.py $STARTER/tests/test_my_inference.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `tests/test_inference.py`, con 40 tests, tres de ellos con Hypothesis, y `tests/test_my_inference.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` (las imágenes se llaman `week-28`) y `test_package.py` (`inference` es un módulo de `core`, `scipy==1.18.1` está en las dependencias, `scipy-stubs` en las de desarrollo, y la versión es `0.28.0`).

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.inference'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `tests/test_inference.py` entero. Fíjate en:

- `LOW` y `HIGH`, y el comentario que dice cómo calcular a mano su error estándar, su t y sus grados de libertad: los tests comparan con números que puedes comprobar con papel y lápiz (teoría 05, sección 4);
- `NARROW` y `WIDE`, con dispersiones muy distintas: solo con ellas se distingue Welch de Student;
- `test_difference_p_ranks_is_exact_mann_whitney` y `test_difference_p_ranks_cannot_go_below_one_tenth_with_three_and_three`;
- `TENTHS` y `SAMPLES`, los datos que genera Hypothesis, y las tres propiedades que comprueba;
- los tests de `comparar`, que comparan las líneas **enteras** de la salida;
- `test_importing_the_cli_does_not_load_scipy`, en otro proceso.

### 4. Las dependencias

```bash
uv add scipy==1.18.1
uv add --dev scipy-stubs==1.18.1.1
uv run pytest -q
```

```
 + scipy==1.18.1
...
 + optype==0.19.0
 + scipy-stubs==1.18.1.1
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Las dos versiones están revisadas en `docs/stack-versions.md` del bootcamp: publicadas hace más de dos semanas y sin avisos de seguridad. SciPy no trae tipos; sin `scipy-stubs`, mypy vería `Any` en cada llamada a `stats`. Solo lo necesita mypy: por eso va en `dev` y no entra en la imagen.

### 5. El módulo, sin comprobaciones

Crea `src/observatorio/core/inference.py`. Primero **sin** las dos comprobaciones de `difference`, para ver qué hace SciPy cuando una prueba no tiene sentido:

```python
"""Estadística inferencial con SciPy: ¿la diferencia entre dos etiquetas es real o es azar?

Qué: sample saca de una serie los valores de una etiqueta, y difference compara dos
muestras: la diferencia de medias con su intervalo de confianza (Welch), el tamaño del
efecto (d de Cohen) y los p-valores de Welch y de Mann-Whitney.
Para qué: dos medias distintas no bastan para decir que una etiqueta mide más que otra;
con pocas medidas, o muy dispersas, la diferencia puede ser ruido. El intervalo dice
cuánto puede valer la diferencia de verdad, y el p-valor, qué raro sería verla si no la hubiera.
Impacto: importar scipy.stats cuesta unos 0,4 s. No se reexporta en core, y la CLI lo
importa solo en `comparar`.
"""

from dataclasses import dataclass

import numpy as np
from scipy import stats

from observatorio.core.arrays import Floats, labels_array, values_array
from observatorio.core.model import Series


@dataclass(frozen=True)
class Comparison:
    """Dos muestras comparadas; difference, low y high son de la primera menos la segunda."""

    sizes: tuple[int, int]
    means: tuple[float, float]
    stds: tuple[float, float]
    difference: float
    low: float
    high: float
    effect: float
    p_welch: float
    p_ranks: float


def sample(series: Series, label: str) -> Floats:
    """Los valores de label en la serie, en orden y sin los que faltan."""
    values = values_array(series)
    # Anotado: indexar con una máscara de booleanos devuelve Any para mypy.
    chosen: Floats = values[(labels_array(series) == label) & ~np.isnan(values)]
    return chosen


def difference(first: Floats, second: Floats, confidence: float = 0.95) -> Comparison:
    """Compara dos muestras. Lanza ValueError si alguna tiene menos de 2 valores o no varía:
    sin dispersión no hay con qué medir el azar."""
    # ddof=1: la desviación de la muestra, que estima la de todas las medidas posibles.
    stds = float(first.std(ddof=1)), float(second.std(ddof=1))
    # equal_var=False es Welch: no supone que las dos etiquetas tengan la misma dispersión.
    welch = stats.ttest_ind(first, second, equal_var=False)
    interval = welch.confidence_interval(confidence)
    diff = float(first.mean() - second.mean())
    return Comparison(
        sizes=(int(first.size), int(second.size)),
        means=(float(first.mean()), float(second.mean())),
        stds=stds,
        difference=diff,
        low=float(interval.low),
        high=float(interval.high),
        # La diferencia medida en desviaciones: 0,2 es pequeña, 0,8 grande, sea cual sea la unidad.
        effect=diff / float(np.sqrt((stds[0] ** 2 + stds[1] ** 2) / 2)),
        p_welch=float(welch.pvalue),
        # Mann-Whitney compara los rangos, no las medias: no supone una campana, y un valor
        # extremo pesa como cualquier otro.
        p_ranks=float(stats.mannwhitneyu(first, second).pvalue),
    )
```

- `sample` reutiliza `values_array` y `labels_array` de la semana 23: no necesita pandas.
- `equal_var=False` va explícito: el valor por defecto de SciPy es Student (teoría 03, sección 5).
- `confidence_interval` es el intervalo de la diferencia que corresponde a la prueba de Welch.
- La d de Cohen usa la media de las dos varianzas: comparable entre dominios y unidades.

```bash
uv run pytest -q
```

```
21 failed, 991 passed, 15 warnings
```

Mira los avisos (`warnings summary`): `SmallSampleWarning`, `Mean of empty slice`, `Precision loss occurred in moment calculation`... SciPy no falla con una muestra de un valor, una vacía o una que no varía: avisa, y devuelve `nan` o números sin sentido. Fallan los tests que esperan un `ValueError` y los de `comparar`, que aún no existe.

### 6. Las comprobaciones

Al principio de `difference`, antes de `stds = ...`:

```python
    if first.size < 2 or second.size < 2:
        raise ValueError(
            f"cada muestra necesita al menos 2 valores (tienen {first.size} y {second.size})"
        )
    # min == max y no std == 0: la std de [0.1, 0.1, 0.1] sale 1,4e-17 por el redondeo.
    if first.min() == first.max() or second.min() == second.max():
        raise ValueError("las dos muestras tienen que variar: una tiene todos sus valores iguales")
```

```bash
uv run pytest -q
```

```
15 failed, 997 passed
```

Sin avisos. Un `ValueError` con el motivo es mejor que un `nan` que llega a la pantalla (teoría 05, sección 3).

### 7. El comando `comparar`

En `cli.py`, debajo de `graficar`:

```python
@app.command()
def comparar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    etiqueta: Annotated[str, typer.Argument(metavar="ETIQUETA", help="La primera etiqueta.")],
    otra: Annotated[str, typer.Argument(metavar="OTRA", help="La etiqueta con la que compara.")],
    confianza: Annotated[
        float, typer.Option(min=0.5, max=0.999, help="Nivel del intervalo: 0.9, 0.95, 0.99...")
    ] = 0.95,
) -> None:
    """Contrasta con SciPy si las medias de dos etiquetas son distintas, o si puede ser azar."""
    # Importar aquí, como en `graficar`: scipy.stats tarda en cargarse.
    from observatorio.core import inference

    series, errors = parsed(ruta)
    first, second = inference.sample(series, etiqueta), inference.sample(series, otra)
    try:
        result = inference.difference(first, second, confianza)
    except ValueError as problem:
        raise fail(f"no se puede comparar {etiqueta} con {otra}: {problem}", 2) from problem
    for label, size, mean, std in zip(
        (etiqueta, otra), result.sizes, result.means, result.stds, strict=True
    ):
        out.print(f"{label}: {size} medidas, media {mean:.2f}, desviación {std:.2f}")
    out.print(
        f"diferencia {etiqueta} - {otra}: {result.difference:.2f},"
        f" IC {confianza * 100:g} %: [{result.low:.2f}, {result.high:.2f}]"
    )
    out.print(f"tamaño del efecto (d de Cohen): {result.effect:.2f}")
    out.print(f"p (Welch): {result.p_welch:.3g} · p (Mann-Whitney): {result.p_ranks:.3g}")
    if errors:
        raise typer.Exit(1)
```

- `typer.Option(min=0.5, max=0.999)`: Typer rechaza un nivel fuera de rango con código 2, antes de leer nada. Un intervalo del 100 % sería infinito.
- Una etiqueta que no está, o con un solo valor, o que no varía: código 2 y un mensaje con las dos etiquetas y el motivo.
- Las líneas malas se escriben en stderr, se compara con las buenas y el código es 1, como en `graficar`.
- `confianza * 100:g` escribe `95` y `99`, y `99.9` si hace falta.

Actualiza también el docstring del módulo: ahora son dieciocho comandos, con `comparar` detrás de `graficar`.

```bash
uv run pytest -q
```

```
3 failed, 1009 passed
```

### 8. Probarlo y medirlo

```bash
uv run observatorio comparar medidas.txt Norte Sur
uv run observatorio comparar medidas.txt Norte Sur --confianza 0.99
uv run observatorio comparar medidas.txt Norte Centro
uv run observatorio comparar medidas.txt Norte Sur --confianza 1
```

La primera da la salida de "Qué construyes". La segunda, el mismo informe con un intervalo mucho más ancho:

```
diferencia Norte - Sur: 21.95, IC 99 %: [-1122.15, 1166.05]
```

Con un grado de libertad (dos medidas por etiqueta), el valor crítico de t para el 99 % es enorme. La tercera y la cuarta terminan con código 2:

```
error: no se puede comparar Norte con Centro: cada muestra necesita al menos 2 valores (tienen 2 y 0)
```

```
│ Invalid value for '--confianza': 1.0 is not in the range 0.5<=x<=0.999.      │
```

`Centro` tiene una medida, pero es `NA`: `sample` la deja fuera.

Ahora con el archivo grande de la semana 22:

```bash
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
time uv run observatorio resumir perfil/grande.txt 2> /dev/null | tail -1
time uv run observatorio comparar perfil/grande.txt Norte Sur 2> /dev/null
uv run python -X importtime -c "import scipy.stats" 2>&1 | tail -1
```

En la máquina del bootcamp:

| Comando | Tiempo |
|---|---|
| `resumir` | 0,95 s |
| `comparar ... Norte Sur` | 1,3-1,5 s |
| `import scipy.stats` | unos 0,4 s |

```
Norte: 18898 medidas, media 40.26, desviación 23.25
Sur: 19206 medidas, media 39.95, desviación 23.08
diferencia Norte - Sur: 0.32, IC 95 %: [-0.15, 0.78]
tamaño del efecto (d de Cohen): 0.01
p (Welch): 0.184 · p (Mann-Whitney): 0.184
```

`generar_medidas.py` saca todas las etiquetas de la misma distribución: no hay diferencia, y `comparar` no la inventa. Con casi 19 000 medidas por etiqueta, el intervalo es estrecho (±0,47) y contiene el 0.

Ahora con **tus** datos: elige dos etiquetas de tu dominio que creas distintas y dos que creas iguales. ¿Qué dice `comparar`? ¿Coinciden Welch y Mann-Whitney? Si no, busca el valor extremo. Apunta tus números y tus respuestas: van al *pull request*.

### 9. Versión, Docker y calidad

En `pyproject.toml`, `version = "0.28.0"`, y:

```bash
uv lock
uv run pytest -q
uv run observatorio --version
```

```
2 failed, 1010 passed
observatorio 0.28.0
```

En `compose.yaml`, las imágenes pasan a llamarse `local/observatorio:week-28-test` y `local/observatorio:week-28`. A diferencia de matplotlib, SciPy no necesita nada en el `Dockerfile`: no escribe cachés ni busca fuentes.

```bash
uv run pytest -q
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
docker images local/observatorio
uv run python -c "import sys, observatorio.cli; print('scipy' in sys.modules)"
```

`pytest` da `1012 passed`. `coverage report` debe dar 100 % en `inference.py` y en `cli.py`. `alembic check` sigue en `No new upgrade operations detected.`. La comprobación de `sys.modules` escribe `False`.

En `docker images`, la imagen `week-28` mide unos 1,18 GB, frente a los 986 MB de `week-27`. Mira de dónde salen:

```bash
docker run --rm --entrypoint sh local/observatorio:week-28 -c 'cd /opt/venv/lib/python3.14/site-packages && du -sh scipy scipy.libs && ls scipy.libs'
```

```
110M	scipy
30M	scipy.libs
libgfortran-040039e1-0352e75f.so.5.0.0
libgfortran-83c28eba.so.5.0.0
libquadmath-2284e583.so.0.0.0
libquadmath-96973f99-934c22de.so.0.0.0
libscipy_openblas-5f890258.so
```

SciPy trae su propio OpenBLAS (el álgebra lineal) y las bibliotecas de Fortran con las que se compila parte de su código. La teoría 05, sección 6, explica por qué el proyecto no añade además statsmodels.

### 10. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `inference.py` | `equal_var=False` por `equal_var=True` en `ttest_ind` | |
| `inference.py` | `first.std(ddof=1)` por `first.std()` | |
| `inference.py` | `first.mean() - second.mean()` por `second.mean() - first.mean()` en `diff` | |
| `inference.py` | `welch.confidence_interval(confidence)` por `welch.confidence_interval()` | |
| `inference.py` | `first.size < 2 or second.size < 2` por `first.size < 1 or second.size < 1` | |
| `inference.py` | en la segunda comprobación, `or` por `and` | |
| `inference.py` | `np.sqrt((stds[0] ** 2 + stds[1] ** 2) / 2)` por `np.sqrt(stds[0] * stds[1])` | |
| `inference.py` | `stats.mannwhitneyu(first, second)` por `stats.mannwhitneyu(first, second, method="asymptotic")` | |
| `inference.py` | quita ` & ~np.isnan(values)` en `sample` | |
| `cli.py` | en `comparar`, `inference.difference(first, second, confianza)` por `inference.difference(first, second)` | |

Los diez mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el primero, ¿qué test falla? ¿Por qué **no** falla `test_difference_p_value_is_welch`, que también mira el p-valor de Welch? Pista: calcula a mano los grados de libertad de Welch y de Student con `LOW` y `HIGH`.
- Con el octavo, ¿qué test falla, y qué diferencia hay entre el p-valor exacto y el asintótico? ¿Cuál usa SciPy con las 19 000 medidas por etiqueta del paso 8? Pista: lee la documentación de `method` en `mannwhitneyu`.

### 11. Tus tests

En `tests/test_my_inference.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con los valores de tu dominio y las funciones de `test_inference.py` (`floats`, `write`, `comparar`). Ideas:

- que dos etiquetas de tu dominio que deberían ser distintas den un intervalo que no contiene el 0;
- que el mismo valor repetido en tu dominio (un sensor atascado) haga terminar `comparar` con código 2;
- que con pocas medidas de tu dominio el intervalo sea muy ancho, y con cuatro veces más se estreche más o menos a la mitad (teoría 02, sección 5);
- que una medida extrema mueva mucho el p-valor de Welch y poco el de Mann-Whitney (ejercicio 03, paso 3);
- que `--confianza 0.99` dé un intervalo más ancho que el de por defecto, con tus datos;
- que la d de Cohen no cambie si pasas tus medidas a otra unidad (°C a °F, euros a céntimos), y explica por qué en un comentario.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1154 tests en verde.

### 12. README y pull request

En el `README.md` de tu repositorio, añade una sección "Comparar etiquetas": qué hace `comparar`, qué significa cada línea de su salida, y un ejemplo con tus datos y lo que concluyes de él (y lo que **no** puedes concluir).

Commits sugeridos, en este orden:

1. `test: add inference tests`
2. `build: add scipy and scipy-stubs`
3. `feat: add inference module`
4. `feat: reject samples that cannot be compared`
5. `feat: add comparar command`
6. `chore: bump version to 0.28.0`
7. `build: rename images to week-28`
8. `test: add my inference tests`

```bash
git push -u origin week-28
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-28` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. Dos salidas de `comparar` con tus datos (una pareja que creas distinta y otra que creas igual), con lo que concluyes de cada una.
3. Tu tabla de tiempos del paso 8 y el tamaño de tu imagen.
4. La tabla de mutantes del paso 10 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'observatorio.core.inference'` | Falta el paso 5, o el archivo no está en `src/observatorio/core/` |
| `ModuleNotFoundError: No module named 'scipy'` | Falta el paso 4: `uv add scipy==1.18.1` |
| mypy: `Returning Any from function declared to return "ndarray[...]"` en `sample` | Falta la anotación `chosen: Floats = ...` |
| mypy: `Library stubs not installed for "scipy"  [import-untyped]` | Falta `uv add --dev scipy-stubs==1.18.1.1`. Ignora la pista que da mypy para instalarlo: en este proyecto, siempre `uv` |
| `test_difference_does_not_assume_equal_spreads` falla | `ttest_ind` sin `equal_var=False`: es Student |
| `test_difference_sizes_means_and_sample_stds` falla con 1,414 | `std()` sin `ddof=1` |
| `test_difference_needs_both_samples_to_vary[first2-second2]` falla | Compruebas `std() == 0`: con `[0.1, 0.1, 0.1]` sale 1,4e-17. Usa `min() == max()` |
| `test_difference_p_ranks_is_exact_mann_whitney` falla | Pasas `method=` a `mannwhitneyu`: deja que SciPy elija el exacto con pocos datos |
| `p (Welch): nan` en la salida de `comparar` | Falta el paso 6 |
| `test_importing_the_cli_does_not_load_scipy` falla | `inference` se importa fuera de `comparar` |
| Hypothesis encuentra un fallo con valores como `1e-300` | Cambiaste `TENTHS`: con esos valores SciPy pierde precisión (teoría 05, sección 4) |

## Entrega

1. Rama `week-28` con `core/inference.py`, el comando `comparar`, `scipy` y `scipy-stubs` fijados, las imágenes `week-28`, la versión `0.28.0` y al menos 6 tests tuyos en `test_my_inference.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Comparar etiquetas".
4. *Pull request* `week-28` → `main` con lo que pide el paso 12.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Regresión con statsmodels](../2-practicas/ejercicio-04-regresion-con-statsmodels/README.md) | **Proyecto · Comparar dos etiquetas** | [Rúbrica de la semana 28](../rubrica-evaluacion.md) |
