# Proyecto — Observatorio, capa 26: dibujar la evolución

⏱️ 6 h 30 min · Capa 26 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

`evolucion` escribe la media de cada etiqueta en cada periodo: una tabla que hay que leer número a número. Esta semana tu Observatorio la **dibuja**, con matplotlib, en un PNG, un SVG o un PDF:

```
$ uv run observatorio graficar medidas.txt evolucion.png --inicio 2026-11-01T08:00:00 --periodo 2h
error: medidas.txt: línea 10: 'Sur 9,5'
5 etiquetas y 4 periodos de 7 medidas en evolucion.png · 24437 bytes
```

Abre `evolucion.png`: una línea por etiqueta, con un punto en cada periodo que tiene dato, cortada donde falta, y una leyenda con las cinco etiquetas. Con `--periodo 2h` y estas siete medidas, casi todo son puntos sueltos: por eso cada valor lleva su marcador.

| Pieza | Qué hace |
|---|---|
| `core/charts.py` | `evolution_figure` dibuja la tabla de `summaries.evolution` con una `Figure`, sin `pyplot`; `save` la guarda en el formato de la extensión, igual byte a byte con los mismos datos |
| `evolution_of` | Lee el archivo y calcula la tabla de la evolución, para `evolucion` y para `graficar` |
| `graficar RUTA SALIDA --inicio ... [--cada] [--periodo]` | Dibuja la evolución y dice qué dibujó |

Una dependencia nueva:

| Paquete | Para qué |
|---|---|
| `matplotlib==3.11.2` | Los gráficos. Trae `pillow`, `fonttools`, `kiwisolver`, `contourpy`, `cycler` y `pyparsing` |

```
src/observatorio/
├── cli.py                  # modificado: evolution_of, evolucion y graficar
└── core/
    └── charts.py           # nuevo: matplotlib, sin pyplot y sin reexportar en core/__init__.py
tests/
├── test_charts.py          # nuevo: los tests del bootcamp
├── test_my_charts.py       # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes de la semana 27 y MPLCONFIGDIR
└── test_package.py         # modificado: charts en core, matplotlib y 0.27.0
Dockerfile                  # modificado: MPLCONFIGDIR en runtime
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-27`. El `starter/` trae la capa 25 resuelta: `core/columnar.py` y los comandos `exportar` y `sql`. **Tú** escribes `charts.py`, `evolution_of` y `graficar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-26` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-27
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-27-visualizacion_con_matplotlib_seaborn_y_plotly/3-proyecto/starter
cp $STARTER/tests/test_charts.py $STARTER/tests/test_my_charts.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `tests/test_charts.py`, con 43 tests, y `tests/test_my_charts.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` (las imágenes se llaman `week-27`, y la etapa `runtime` define `MPLCONFIGDIR`) y `test_package.py` (`charts` es un módulo de `core`, `matplotlib==3.11.2` está en las dependencias y la versión es `0.27.0`).

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'matplotlib'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Falta la biblioteca. Antes de seguir, lee `tests/test_charts.py` entero. Fíjate en:

- `xs`, `ys` y `legend_of`: los tests miran **dentro** de la figura (los datos de cada línea, la leyenda), no los píxeles (teoría 05, sección 3);
- `test_evolution_figure_keeps_nan_so_the_line_breaks` y `test_evolution_figure_marks_every_point`, que dicen qué hacer con lo que falta;
- `test_evolution_figure_legend_keeps_labels_that_start_with_underscore`, una trampa de `legend()` (teoría 01, sección 4);
- `test_save_is_reproducible` y `test_save_does_not_change_the_global_settings`;
- `test_charts_does_not_use_pyplot` y `test_importing_the_cli_does_not_load_matplotlib`, en otro proceso.

### 4. La dependencia

```bash
uv add matplotlib==3.11.2
uv run pytest -q
```

```
 + contourpy==1.4.0
 + cycler==0.12.1
 + fonttools==4.68.0
 + kiwisolver==1.5.1
 + matplotlib==3.11.2
 + pillow==13.0.0
 + pyparsing==3.3.3
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Ahora los dos errores son `No module named 'observatorio.core.charts'`. La versión está revisada en `docs/stack-versions.md` del bootcamp: publicada hace más de dos semanas y sin avisos de seguridad. matplotlib trae sus propios tipos: mypy no necesita nada más.

### 5. La figura y el archivo

Crea `src/observatorio/core/charts.py`:

```python
"""Los gráficos del Observatorio, con matplotlib y sin pyplot.

Qué: evolution_figure dibuja la tabla de summaries.evolution, una línea por etiqueta, y
save guarda una figura en el formato que diga la extensión del archivo.
Para qué: un gráfico deja ver de un vistazo lo que en la tabla de `evolucion` hay que leer
número a número: qué etiqueta sube, cuál baja y dónde faltan datos.
Impacto: usa Figure y no pyplot: sin estado global ni ventanas, funciona igual en tu
terminal, en un test y en Docker. No se reexporta en core: importar matplotlib cuesta.
"""

from pathlib import Path

import matplotlib
import pandas as pd
from matplotlib.figure import Figure


def evolution_figure(table: pd.DataFrame, title: str) -> Figure:
    """Una línea por columna de table, con un punto por periodo; un NaN corta la línea."""
    figure = Figure(figsize=(8, 4.5), layout="constrained")
    axes = figure.add_subplot()
    # El marcador hace visible un periodo con valor entre dos sin él: una línea de un solo
    # punto no se ve.
    lines = [axes.plot(table.index, table[label], marker="o")[0] for label in table.columns]
    axes.set(title=title, xlabel="periodo", ylabel="media")
    # Los nombres van explícitos: si no, legend se salta las etiquetas que empiezan por "_".
    axes.legend(lines, list(table.columns), title="etiqueta")
    return figure


def save(figure: Figure, path: Path) -> None:
    """Guarda la figura en el formato de la extensión de path: .png, .svg, .pdf...

    Sin fecha y con una sal fija para los identificadores del SVG: los mismos datos dan el
    mismo PNG y el mismo SVG, byte a byte. En el SVG, el texto sigue siendo texto.
    """
    with matplotlib.rc_context({"svg.hashsalt": "observatorio", "svg.fonttype": "none"}):
        figure.savefig(path, metadata={"Date": None})
```

- `Figure` en lugar de `pyplot`: ninguna figura queda en una lista global, nada abre ventanas, y funciona igual en un test y en Docker (teoría 05, sección 2).
- `table[label]` lleva sus `NaN`: la línea se corta donde no hay dato, en lugar de unir dos periodos lejanos. Por eso `marker="o"`: un periodo con dato entre dos sin él sería invisible.
- Las columnas de la tabla salen en orden alfabético (`pivot`, semana 25), y el ciclo de colores de matplotlib da a cada una el suyo.
- `axes.legend(lines, nombres)`: con `legend()` a secas, una etiqueta como `_interna` desaparecería de la leyenda sin avisar.
- `save` deja que matplotlib elija el formato por la extensión. `metadata={"Date": None}` y `svg.hashsalt` hacen que el SVG salga igual dos veces; `svg.fonttype: "none"` deja el texto como texto. Todo dentro de `rc_context`, para no cambiar los gráficos del resto del programa (teoría 05, sección 4).
- No atrapa nada: una extensión desconocida (`ValueError`) o una carpeta que no existe (`FileNotFoundError`) suben a quien llama, que sabe qué decirle al usuario.

```bash
uv run pytest -q
```

```
16 failed, 955 passed
```

Fallan los tests de `graficar`, que aún no existe, y los de la versión y Docker.

### 6. El comando `graficar`

`graficar` necesita lo mismo que `evolucion`: comprobar `--cada` y `--periodo`, leer el archivo y calcular la tabla. Sácalo a una función, **encima** de `evolucion`:

```python
def evolution_of(
    ruta: Path, inicio: datetime, cada: str, periodo: str
) -> tuple[pd.DataFrame, Series, list[str]]:
    """La tabla de summaries.evolution de un archivo, su serie y sus errores, para `evolucion` y
    `graficar`; código 2 si cada o periodo no son duraciones."""
    from observatorio.core import frames, summaries

    try:
        every, period = summaries.duration(cada), summaries.duration(periodo)
    except ValueError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = parsed(ruta)
    table = summaries.evolution(summaries.timed(frames.frame_of(series), inicio, every), period)
    return table, series, errors
```

En `evolucion`, sustituye esas mismas líneas (desde el `from observatorio.core import ...` hasta `table = ...`) por:

```python
    table, series, errors = evolution_of(ruta, inicio, cada, periodo)
```

Ejecuta `uv run pytest -q tests/test_summaries.py`: los tests de `evolucion` de la semana 25 siguen en verde. Has cambiado código que funcionaba sin cambiar lo que hace, y los tests lo confirman.

Debajo de `evolucion`:

```python
@app.command()
def graficar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    salida: Annotated[
        Path, typer.Argument(metavar="SALIDA", help="El gráfico: un .png, un .svg o un .pdf.")
    ],
    inicio: Annotated[
        datetime,
        typer.Option(help="Cuándo se tomó la primera medida, como 2026-11-01T08:00:00."),
    ],
    cada: Annotated[str, typer.Option(help="Tiempo entre dos medidas: 1h, 15min, 1D...")] = EVERY,
    periodo: Annotated[str, typer.Option(help="Tamaño de cada periodo: 3h, 1D, 7D...")] = PERIOD,
) -> None:
    """Dibuja con matplotlib la media de cada etiqueta por periodos, como `evolucion`."""
    # Importar aquí, como en `exportar`: matplotlib tarda en cargarse.
    from observatorio.core import charts

    table, series, errors = evolution_of(ruta, inicio, cada, periodo)
    figure = charts.evolution_figure(table, f"{ruta.name}: media cada {periodo}")
    try:
        charts.save(figure, salida)
    except (OSError, ValueError) as problem:
        # ValueError: una extensión que matplotlib no sabe escribir, como .txt.
        raise fail(f"no se puede escribir {salida}: {problem}", 2) from problem
    out.print(
        f"{len(table.columns)} etiquetas y {len(table)} periodos de {len(series)} medidas"
        f" en {salida.name} · {salida.stat().st_size} bytes"
    )
    if errors:
        raise typer.Exit(1)
```

- Las opciones son las de `evolucion`, con los mismos valores por defecto: el mismo archivo da la misma tabla, dibujada. `test_graficar_draws_the_same_table_as_evolucion` lo comprueba comparando los bytes del SVG.
- Un `--cada` o `--periodo` que no es una duración termina con código 2 **antes** de dibujar nada.
- Las líneas malas se escriben en stderr, el gráfico se dibuja con las buenas y el código es 1, como en `exportar`.
- Un archivo sin medidas da un gráfico vacío y `0 etiquetas y 0 periodos`: no es un error.
- La última línea dice qué se dibujó y cuánto pesa, para ver de un vistazo si salió lo que esperabas.

Actualiza también el docstring del módulo: ahora son diecisiete comandos, con `graficar` detrás de `evolucion`.

```bash
uv run pytest -q
```

```
4 failed, 967 passed
```

### 7. Probarlo y medirlo

```bash
uv run observatorio graficar medidas.txt evolucion.png --inicio 2026-11-01T08:00:00 --periodo 2h
uv run observatorio graficar medidas.txt evolucion.svg --inicio 2026-11-01T08:00:00 --periodo 2h
uv run observatorio graficar medidas.txt evolucion.txt --inicio 2026-11-01T08:00:00
uv run observatorio graficar medidas.txt evolucion.png --inicio 2026-11-01T08:00:00 --periodo 0h
```

La primera da la salida de "Qué construyes". La segunda, el mismo gráfico en SVG:

```
5 etiquetas y 4 periodos de 7 medidas en evolucion.svg · 18787 bytes
```

Ábrelo con el navegador y busca "Norte" con Ctrl+F: el texto es texto. Ejecútala otra vez y compara con `sha256sum evolucion.svg` antes y después: el mismo archivo.

La tercera y la cuarta terminan con código 2:

```
error: no se puede escribir evolucion.txt: Format 'txt' is not supported (supported formats: avif, eps, gif, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp)
error: no es una duración mayor que cero: '0h'
```

Ahora con el archivo grande de la semana 22:

```bash
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
time uv run observatorio evolucion perfil/grande.txt --inicio 2026-11-01T00:00:00 --cada 1min 2> /dev/null | tail -1
for formato in png svg pdf; do
  time uv run observatorio graficar perfil/grande.txt perfil/grande.$formato --inicio 2026-11-01T00:00:00 --cada 1min 2> /dev/null
done
```

En la máquina del bootcamp:

| Comando | Tiempo | Archivo |
|---|---|---|
| `evolucion` | 1,0 s | — |
| `graficar ... grande.png` | 1,6 s | 165 905 bytes |
| `graficar ... grande.svg` | 1,4 s | 62 251 bytes |
| `graficar ... grande.pdf` | 1,4 s | 23 399 bytes |

Casi todo el tiempo es leer el texto, como en `evolucion`; importar matplotlib añade unos 0,3 s. Mídelo:

```bash
uv run python -X importtime -c "import matplotlib.figure" 2>&1 | tail -1
```

Abre `perfil/grande.png`: cinco líneas que se cruzan sin parar, porque `generar_medidas.py` da valores al azar alrededor de 40. Con los datos de tu dominio, ¿se lee mejor? ¿Qué cambiarías según la teoría 02? Apunta tus números y tu respuesta: van al *pull request*.

### 8. La versión

En `pyproject.toml`, `version = "0.27.0"`, y:

```bash
uv lock
uv run pytest -q
uv run observatorio --version
```

```
3 failed, 968 passed
observatorio 0.27.0
```

### 9. Docker, calidad y cobertura

En `compose.yaml`, las imágenes pasan a llamarse `local/observatorio:week-27-test` y `local/observatorio:week-27`:

```bash
uv run pytest -q
```

```
1 failed, 970 passed
```

Falla `test_runtime_gives_matplotlib_a_folder_it_can_write`. El usuario `app` de la imagen `runtime` no tiene carpeta personal, y matplotlib necesita una para su caché de fuentes. Pruébalo **antes** de arreglarlo:

```bash
docker compose build api
docker run --rm -v "$PWD:/data:ro" local/observatorio:week-27 observatorio graficar /data/medidas.csv /tmp/g.png --inicio 2026-11-01T08:00:00
```

```
mkdir -p failed for path /home/app/.config/matplotlib: [Errno 13] Permission denied: '/home/app'
Matplotlib created a temporary cache directory at /tmp/matplotlib-... because there was an issue with the default path (/home/app/.config/matplotlib); it is highly recommended to set the MPLCONFIGDIR environment variable to a writable directory, in particular to speed up the import of Matplotlib and to better support multiprocessing.
error: medidas.csv: línea 7: 'Sur 9,5'
5 etiquetas y 1 periodos de 7 medidas en g.png · 27789 bytes
```

Funciona, pero con un aviso en cada comando. En el `Dockerfile`, en la etapa `runtime`, cambia el `ENV`:

```dockerfile
# MPLCONFIGDIR: el usuario app no tiene carpeta personal, y matplotlib necesita una
# carpeta en la que pueda escribir su caché de fuentes. Sin ella, avisa en cada comando.
ENV PATH="/opt/venv/bin:$PATH" \
    MPLCONFIGDIR=/tmp/matplotlib
```

Vuelve a construir y a ejecutar: sin aviso, y el PNG pesa **lo mismo** que en tu máquina, byte a byte. Después:

```bash
uv run pytest -q
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
docker images local/observatorio
uv run python -c "import sys, observatorio.cli; print('matplotlib' in sys.modules)"
```

`pytest` da `971 passed`. `coverage report` debe dar 100 % en `charts.py` y en `cli.py`. `alembic check` sigue en `No new upgrade operations detected.`. La comprobación de `sys.modules` escribe `False`.

En `docker images`, la imagen `week-27` mide unos 986 MB, frente a los 850 MB de `week-26`. Mira de dónde salen:

```bash
docker run --rm --entrypoint sh local/observatorio:week-27 -c 'cd /opt/venv/lib/python3.14/site-packages && du -sh matplotlib fontTools PIL pillow.libs kiwisolver contourpy'
```

```
37M	matplotlib
29M	fontTools
7.4M	PIL
15M	pillow.libs
5.6M	kiwisolver
1.4M	contourpy
```

La teoría 05, sección 6, explica por qué el proyecto no añade además seaborn ni plotly.

### 10. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `charts.py` | quita `, marker="o"` | |
| `charts.py` | `axes.legend(lines, list(table.columns), title="etiqueta")` por `axes.legend(title="etiqueta")` | |
| `charts.py` | `table[label]` por `table[label].dropna()` | |
| `charts.py` | `table[label]` por `table[label].interpolate()` | |
| `charts.py` | quita `"svg.hashsalt": "observatorio", ` | |
| `charts.py` | `"svg.fonttype": "none"` por `"svg.fonttype": "path"` | |
| `charts.py` | `figure.savefig(path, metadata={"Date": None})` por `figure.savefig(path)` | |
| `charts.py` | cambia el `with matplotlib.rc_context(...)` por `matplotlib.rcParams.update(...)` y guarda fuera del `with` | |
| `charts.py` | añade `from matplotlib import pyplot` | |
| `cli.py` | en `graficar`, `except (OSError, ValueError)` por `except OSError` | |

Los diez mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el segundo mutante, ¿qué test falla, y qué escribe la leyenda? Pruébalo en `uv run python`: dibuja una línea con `label="_interna"` y otra con `label="Norte"`, llama a `axes.legend()` y mira `axes.get_legend().get_texts()`. ¿Por qué hace eso matplotlib, y qué pasaría si una etiqueta de tu dominio empezara por `_`?
- Con el octavo, ¿qué test falla, y por qué ese test pone sus propios valores con `rc_context` **antes** de llamar a `save`, en lugar de copiar `rcParams` y compararlo después? Pista: piensa en qué orden se ejecutan los tests.

### 11. Tus tests

En `tests/test_my_charts.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con los valores de tu dominio y las funciones de `test_charts.py` (`table_of`, `legend_of`, `xs`, `ys`, `saved`, `write`). Ideas:

- que la leyenda de tus medidas tenga tus etiquetas en orden alfabético;
- que un periodo sin datos de una etiqueta de tu dominio sea `NaN` en su línea, y que la línea tenga tantos puntos como periodos;
- que `graficar` con un archivo de tu dominio y tu `--periodo` dibuje las etiquetas y los periodos que esperas;
- que el SVG de tus medidas tenga el título con el nombre de tu archivo;
- que el mismo PDF guardado dos veces **no** sea siempre igual, y explica por qué en un comentario (teoría 05, sección 4);
- que `graficar` con `.jpg` termine con código 2 y `metadata not supported for format 'jpeg'`, y explica en un comentario por qué (mira `save`).

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1108 tests en verde.

### 12. README y pull request

En el `README.md` de tu repositorio, añade una sección "Gráficos": qué dibuja `graficar`, qué formatos acepta, un ejemplo con tus datos y una imagen del gráfico. Para la imagen, guarda un PNG en `docs/evolucion.png` y enlázalo desde el README con la sintaxis de imagen de Markdown (un `!` delante de un enlace normal).

Commits sugeridos, en este orden:

1. `test: add charts tests`
2. `build: add matplotlib`
3. `feat: add charts module`
4. `refactor: extract evolution_of`
5. `feat: add graficar command`
6. `chore: bump version to 0.27.0`
7. `fix: give matplotlib a writable config dir in docker`
8. `test: add my charts tests`

```bash
git push -u origin week-27
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-27` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. Un gráfico de `graficar` con tus datos, pegado como imagen.
3. Tu tabla de tiempos del paso 7, tu respuesta sobre el gráfico grande y el tamaño de tu imagen.
4. La tabla de mutantes del paso 10 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'matplotlib'` | Falta el paso 4: `uv add matplotlib==3.11.2` |
| `ModuleNotFoundError: No module named 'observatorio.core.charts'` | Falta el paso 5, o el archivo no está en `src/observatorio/core/` |
| `test_charts_does_not_use_pyplot` falla | Algún `import matplotlib.pyplot` en `charts.py`: usa `from matplotlib.figure import Figure` |
| `test_evolution_figure_marks_every_point` falla | Falta `marker="o"` en `plot` |
| `test_evolution_figure_legend_keeps_labels_that_start_with_underscore` falla | Llamas a `axes.legend()` sin las líneas y los nombres |
| `test_save_is_reproducible[.svg]` falla | Falta `svg.hashsalt` o `metadata={"Date": None}` |
| `test_save_svg_keeps_the_text_as_text` falla | Falta `"svg.fonttype": "none"` |
| `test_graficar_cannot_write_exits_2[evolucion.txt]` falla con una traza | Atrapas solo `OSError`: una extensión desconocida es `ValueError` |
| Los tests de `evolucion` fallan tras el paso 6 | Al sustituir las líneas por `evolution_of`, quitaste o dejaste alguna de más |
| `test_importing_the_cli_does_not_load_matplotlib` falla | `charts` se importa fuera de `graficar` |
| En Docker sale `Matplotlib created a temporary cache directory` | Falta `MPLCONFIGDIR=/tmp/matplotlib` en el `ENV` de la etapa `runtime` |
| mypy: `Argument 1 to "list" has incompatible type "Buffer \| ..."` en tus tests | `get_xdata()` y `get_ydata()` devuelven `ArrayLike`: usa `xs` e `ys` de `test_charts.py` |

## Entrega

1. Rama `week-27` con `core/charts.py`, `evolution_of`, el comando `graficar`, `matplotlib` fijado, las imágenes `week-27`, `MPLCONFIGDIR` en el `Dockerfile`, la versión `0.27.0` y al menos 6 tests tuyos en `test_my_charts.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Gráficos" y una imagen.
4. *Pull request* `week-27` → `main` con lo que pide el paso 12.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · plotly, y tres bibliotecas](../2-practicas/ejercicio-04-plotly-y-tres-bibliotecas/README.md) | **Proyecto · Dibujar la evolución** | [Rúbrica de la semana 27](../rubrica-evaluacion.md) |
