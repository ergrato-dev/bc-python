# Proyecto — Observatorio, capa 21: rendimiento

⏱️ 6 h 30 min · Capa 21 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Tu Observatorio pasa la CI, se entrega en una imagen segura y tiene más de 800 tests. Pero nunca lo has probado con un archivo grande. Con 100 000 medidas:

```
$ time uv run observatorio informe -f perfil/grande.txt > /dev/null
real	0m21.335s
```

Más de 20 segundos y 330 MB de memoria para un archivo de 1 MB. Esta semana lo **mides**, encuentras con cProfile y py-spy dónde se va el tiempo, lo arreglas cambiando una cosa cada vez, y compruebas con tests que el resultado no cambia y que el trabajo no vuelve a crecer:

```
$ time uv run observatorio informe -f perfil/grande.txt > /dev/null
real	0m1.052s
```

| Pieza | Qué cambia |
|---|---|
| `informe --filas N` (`-n`) | La tabla pinta las 20 primeras medidas (o N) y dice cuántas hay; la media móvil, las 20 últimas |
| `Series.parse` y `records_with_errors` | Las medidas y los errores en **una** pasada: cada línea se analiza una vez, no dos |
| `py-spy==0.4.2` | Nueva dependencia de desarrollo: el perfilador por muestreo |
| `scripts/generar_medidas.py` | Viene hecho: genera el archivo grande, siempre igual |
| `.gitignore` y `.dockerignore` | Dejan fuera la carpeta `perfil/`, con los datos y los perfiles |

```
scripts/
└── generar_medidas.py      # nuevo, viene hecho
src/observatorio/
├── cli.py                  # modificado: --filas, Series.parse, sin process_lines
└── core/
    ├── groups.py           # modificado: records_with_errors
    └── model.py            # modificado: Series.parse
tests/
├── test_performance.py     # nuevo: los tests del bootcamp, que cuentan trabajo
├── test_my_performance.py  # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes de la semana 22
└── test_package.py         # modificado: py-spy y 0.22.0
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-22`. El `starter/` trae la capa 20 resuelta. **Tú** mides, perfilas y escribes los cambios.

Los tiempos de este README son de un portátil con WSL2. Los tuyos serán otros: lo que debe coincidir son las proporciones y qué domina cada perfil.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-21` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-22
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/3-proyecto/starter
cp $STARTER/tests/test_performance.py $STARTER/tests/test_my_performance.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
mkdir -p scripts && cp $STARTER/scripts/generar_medidas.py scripts/
git status --short
```

- **Nuevos:**
  - `tests/test_performance.py`, con 24 tests;
  - `tests/test_my_performance.py`, con un ejemplo;
  - `scripts/generar_medidas.py`.
- **Modificados:** `test_delivery.py` (las imágenes se llaman `week-22`) y `test_package.py` (`py-spy` en `dev` y la versión `0.22.0`).

### 3. Tests en rojo y la dependencia nueva

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
27 failed, ... passed
```

Lee `tests/test_performance.py` antes de escribir nada. Ningún test mide segundos (teoría 01, sección 9). En su lugar:

- `profiled_informe` ejecuta `informe` dentro de cProfile;
- `calls_of(profiler, función)` cuenta cuántas veces se llamó una función, con la clave `(archivo, línea, nombre)` de su código (teoría 02, sección 6);
- `table_rows` cuenta las filas de datos de la tabla: las líneas que empiezan por `│`;
- `test_parse_agrees_with_process_lines_and_from_lines` comprueba con Hypothesis que lo nuevo da lo mismo que lo viejo, con cualquier lista de líneas.

Añade py-spy, con la versión fijada (`docs/stack-versions.md`):

```bash
uv add --dev py-spy==0.4.2
uv run py-spy --version
```

```
py-spy 0.4.2
```

`py-spy 0.4.3` salió hace menos de una semana; la 0.4.2 es la primera que entiende Python 3.14 y lleva seis meses publicada. Es un binario de Rust dentro de un paquete de Python, sin dependencias: `uv.lock` solo gana una entrada.

Un test menos en rojo: `test_dev_tools_are_pinned`.

### 4. Los datos y la carpeta `perfil/`

```bash
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
head -3 perfil/grande.txt
wc -l perfil/grande.txt
```

```
Sur;49,0
Este;9,6
Centro;6,4
100000 perfil/grande.txt
```

La semilla es fija: el archivo es el mismo cada vez, y tus medidas de antes y de después comparan lo mismo. Cambia `LABELS` del script por las etiquetas de tu dominio si quieres, pero hazlo **antes** de medir.

`perfil/` va a guardar datos y perfiles que no son código. Que no entren en Git ni en la imagen:

```bash
echo "perfil/" >> .gitignore
echo "perfil/" >> .dockerignore
```

Sin la línea de `.gitignore`, el gancho `check-added-large-files` de la semana 21 te para el commit: `perfil/grande.txt (1014 KB) exceeds 500 KB`. Sin la de `.dockerignore`, la etapa `test` (`COPY . .`) mete el megabyte en la imagen; `test_profiles_stay_out_of_the_image` lo comprueba.

Cambia también `week-21` por `week-22` en las dos imágenes de `compose.yaml` (`local/observatorio:week-22-test` y `local/observatorio:week-22`). Quedan 23 en rojo.

### 5. Medir el punto de partida

```bash
time uv run observatorio informe -f perfil/grande.txt > /dev/null
time uv run observatorio informe -f perfil/grande.txt > /dev/null
time uv run observatorio informe -f perfil/grande.txt > /dev/null
uv run observatorio informe -f perfil/grande.txt | wc -c
```

```
real	0m21.335s
user	0m18.314s
sys	0m0.531s
...
5360179
```

Tres veces: te quedas con el mínimo (teoría 01). `user + sys` es casi todo `real`: el programa **calcula**, no espera. Y escribe 5,4 MB de texto. En Linux y WSL, mide también la memoria máxima:

```bash
/usr/bin/time -f "%e s %M KB" uv run observatorio informe -f perfil/grande.txt > /dev/null
```

```
21.02 s 330048 KB
```

Apunta los tres números (segundos, MB, bytes de salida) en la primera fila de una tabla. Antes de seguir, escribe en una línea **dónde crees** que se va el tiempo. Lo comprobarás en el paso siguiente.

### 6. Perfilar con cProfile

```bash
uv run python -m cProfile -o perfil/w21.prof -m observatorio informe -f perfil/grande.txt > /dev/null
uv run python -m pstats perfil/w21.prof
```

```
perfil/w21.prof% strip
perfil/w21.prof% sort cumulative
perfil/w21.prof% stats informe|print|table_of|process_lines|from_lines|median
```

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.081    0.081   51.801   51.801 cli.py:145(informe)
        2    0.000    0.000   49.374   24.687 console.py:1652(print)
        1    0.173    0.173    0.950    0.950 cli.py:132(table_of)
        1    0.097    0.097    0.622    0.622 analysis.py:17(process_lines)
        1    0.033    0.033    0.443    0.443 model.py:102(from_lines)
        1    0.000    0.000    0.008    0.008 trends.py:31(median)
```

Con cProfile tarda 51 s en lugar de 21: el coste por llamada (teoría 02, sección 7). Las proporciones sí valen:

- `Console.print` se lleva 49,4 de 51,8 s: **pintar** la tabla de 100 000 filas;
- **construirla** (`table_of`) cuesta menos de un segundo;
- analizar las líneas, `process_lines` y `from_lines`, 1 s entre las dos;
- la mediana, que ordena, 8 ms.

Prueba también `sort tottime` y `stats 6`: el tiempo está repartido entre funciones de Rich, ninguna pasa de 2,5 s. No hay nada que arreglar **en** Rich: lo caro es pedirle 1,4 millones de celdas. ¿Acertaste en el paso 5?

### 7. Perfilar con py-spy

```bash
uv run py-spy record --nonblocking -o perfil/antes.svg -- python -m observatorio informe -f perfil/grande.txt > /dev/null
```

```
py-spy> Wrote flamegraph data to 'perfil/antes.svg'. Samples: 743 Errors: 889
```

`--nonblocking` porque, en modo normal, las pilas profundas de Rich hacen que la pausa en cada muestra multiplique el tiempo (teoría 03, sección 5). A cambio, con pilas tan profundas muchas lecturas salen rotas (`Errors`): las que quedan siguen dando las proporciones.

Abre `perfil/antes.svg` en el navegador y busca (`Ctrl+F`) `cli.py:182`: `informe (observatorio/cli.py:182)` tiene en torno al 80 % de las muestras, y la línea 182 es `out.print(table_of(series, scale))`. Dos perfiladores distintos dicen lo mismo.

### 8. No pintar lo que nadie lee

El arreglo no es pintar más deprisa, es pintar **menos** (teoría 04, sección 2). En `src/observatorio/cli.py`, junto a `TOP` y `WINDOW`:

```python
# Cuántas filas de la tabla y cuántas medias móviles escribe `informe` si no se dice
# otra cosa con --filas. Pintar 100 000 filas con Rich tarda más de 20 segundos.
ROWS = 20
```

`table_of` recibe cuántas filas pintar, con `ROWS` por defecto para que sus llamadas de antes sigan valiendo:

```python
def table_of(series: Series, scale: Scale, rows: int = ROWS) -> Table:
    """Una fila por medida, solo las `rows` primeras: etiqueta, valor y nivel, con su color.

    Si hay más medidas que filas, el pie de la tabla dice cuántas se muestran.
    """
    shown = series.measurements[:rows]
    caption = f"{len(shown)} de {len(series)} medidas" if len(shown) < len(series) else None
    table = Table(title="Medidas", caption=caption)
    table.add_column("Etiqueta")
    table.add_column("Valor", justify="right")
    table.add_column("Nivel")
    for measurement in shown:
        ...
```

En `informe`, la opción, detrás de `escala`:

```python
    filas: Annotated[
        int,
        typer.Option(
            "--filas", "-n", min=0, help="Cuántas filas de la tabla y medias móviles escribe."
        ),
    ] = ROWS,
```

`min=0`: Typer rechaza `-n -1` con un error de uso (código 2), en vez de que `[:−1]` pinte todas menos una. Pásala a la tabla:

```python
    out.print(table_of(series, scale, filas))
```

La media móvil tenía el mismo problema: 100 000 medias en una línea. Escribe solo las **últimas** `filas`, las más recientes:

```python
        # Las últimas: son las más recientes. [-0:] daría todas, por eso el `if`.
        recent = moving_average(values, WINDOW)[-filas:] if filas else []
        averages = " · ".join(f"{average:.1f}" for average in recent)
```

`lista[-0:]` es `lista[0:]`: la lista entera. Con `-n 0`, sin el `if`, saldrían todas. `test_moving_average_with_zero_rows_is_empty` lo comprueba.

```bash
uv run pytest -q
```

```
10 failed, ... passed
```

Mide igual que en el paso 5, con `time`, `/usr/bin/time` y `wc -c`, y quédate con el mínimo:

```
real	0m1.062s
1.06 s 119568 KB
1806
```

De 21,3 s a 1,1 s, de 330 a 119 MB, de 5,4 MB de salida a 1,8 KB. Segunda fila de la tabla.

### 9. Perfilar otra vez: el trabajo repetido

```bash
uv run python -m cProfile -o perfil/filas.prof -m observatorio informe -f perfil/grande.txt > /dev/null
uv run python -m pstats perfil/filas.prof
```

```
perfil/filas.prof% strip
perfil/filas.prof% sort tottime
perfil/filas.prof% stats 6
```

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.112    0.112    0.337    0.337 groups.py:46(records_of)
   200000    0.108    0.000    0.313    0.000 groups.py:27(parse_record)
   200000    0.100    0.000    0.149    0.000 record.py:15(parse_value)
      578    0.089    0.000    0.089    0.000 {built-in method marshal.loads}
  1003556    0.082    0.000    0.082    0.000 {method 'strip' of 'str' objects}
        1    0.053    0.053    0.366    0.366 analysis.py:17(process_lines)
```

El tiempo ya no tiene un culpable claro, pero mira `ncalls`: **200 000** llamadas a `parse_record` para 100 000 líneas. ¿Quién la llama?

```
perfil/filas.prof% callers parse_record
```

```
groups.py:27(parse_record)  <-  100000    0.058    0.163  groups.py:46(records_of)
                                100000    0.050    0.150  rules.py:42(parse_line)
```

`informe` analiza cada línea dos veces: una en `process_lines` (vía `parse_line`), para las filas de texto y los errores, y otra en `Series.from_lines` (vía `records_of`), para las medidas. Y `marshal.loads`, que carga los `.pyc` al importar, ya aparece entre los primeros: el arranque empieza a pesar (paso 12).

### 10. Analizar cada línea una vez

En `src/observatorio/core/groups.py`, una función que da los registros **y** los errores en una pasada, con las reglas de `process_lines` (numerar desde 1 contando las que se saltan) y el mensaje `DEBUG` de `records_of`:

```python
def records_with_errors(lines: Iterable[str]) -> tuple[list[Record], list[str]]:
    """Los registros de las líneas válidas y un error por cada inválida, en una pasada.

    Mismas reglas que records_of y que process_lines: numera desde 1 contando las que se
    saltan, y cada inválida da "línea <n>: '<línea>'" y un mensaje DEBUG.
    """
    records: list[Record] = []
    errors: list[str] = []
    for number, line in enumerate(lines, start=1):
        if not is_data_line(line):
            continue
        line = line.strip()
        record = parse_record(line)
        if record is None:
            logger.debug("línea ignorada: %r", line)
            errors.append(f"línea {number}: {line!r}")
        else:
            records.append(record)
    return records, errors
```

Y `records_of` pasa a usarla, para que las reglas vivan en un solo sitio:

```python
    records, _ = records_with_errors(lines)
    return records
```

El mensaje `DEBUG` va **aquí**, en `groups.py`: `test_verbose_shows_debug_messages_on_stderr`, de la semana 14, espera `DEBUG observatorio.core.groups: línea ignorada: 'malo'`. Si lo olvidas o lo mueves a otro módulo, ese test te lo dice. Optimizar no puede cambiar lo que el programa escribe.

En `src/observatorio/core/model.py`, importa `records_with_errors` y añade a `Series`, debajo de `from_lines`:

```python
    @classmethod
    def parse(cls, lines: Iterable[str]) -> tuple[Series, list[str]]:
        """La serie de las líneas válidas y los errores de las inválidas, leyendo cada una una vez.

        Mismas reglas que process_lines: numera desde 1 contando las que se saltan, quita
        los espacios de los lados, salta las que no son de datos y da un error
        "línea <n>: '<línea>'" por cada inválida. Con from_lines y process_lines a la vez,
        `informe` analizaba cada línea dos veces.
        """
        records, errors = records_with_errors(lines)
        return cls([Measurement(label, value) for label, value in records]), errors
```

```bash
uv run pytest -q
```

```
3 failed, ... passed
```

Los tests de `Series.parse` ya pasan; el de Hypothesis compara con `process_lines` cientos de listas de líneas raras. Falta usarla.

### 11. `informe` con `Series.parse`

En `informe`, cambia las dos lecturas por una:

```python
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {error}")
    rows = [scale.row(measurement) for measurement in series]
```

`scale.row` (semana 9) da la misma fila de texto que `parse_line`, a partir de la medida ya analizada. Quita `process_lines` de los imports de `cli.py`: ruff te lo pide. `process_lines` sigue en `core` porque es parte de su API y tiene sus tests.

```bash
uv run pytest -q
```

```
1 failed, ... passed
```

`test_informe_reads_each_line_once` cuenta con cProfile que `parse_record` se llama una vez por línea de datos. Si alguien vuelve a añadir un `Series.from_lines(lines)` en `informe`, falla.

Mide otra vez, alternando con la versión del paso 8 si puedes (teoría 01, sección 4). En la máquina del bootcamp, el mínimo bajó de 1,06 a 1,05 s: la diferencia está **dentro del ruido**. Analizar las líneas costaba unos 0,3 s y te has ahorrado la mitad de una parte que ya era pequeña (Amdahl). Apunta la tercera fila tal cual: medir también es descubrir que un arreglo no se nota. Lo dejas porque `informe` queda más simple, con una lectura en vez de dos, y el test impide que el trabajo vuelva a doblarse con archivos más grandes.

### 12. Lo que queda: el arranque y NumPy

```bash
uv run py-spy record --nonblocking -o perfil/despues.svg -- python -m observatorio informe -f perfil/grande.txt > /dev/null
```

En `perfil/despues.svg`, busca `_find_and_load`: casi la mitad de las muestras están **importando** módulos. Mídelo:

```bash
uv run python -X importtime -c "import observatorio.cli" 2>&1 | tail -1
```

```
import time:      3623 |     451584 | observatorio.cli
```

0,45 s de 1,05 en importar SQLAlchemy, Pydantic, FastAPI, httpx y Rich, aunque `informe` no use la base de datos ni la red. Es el siguiente cuello de botella, y el arreglo (importar cada cosa solo donde se usa, como `servir` desde la semana 20) toca medio paquete. Para una CLI que tarda un segundo, no compensa esta semana: apúntalo en el *pull request* como trabajo pendiente, con el número.

¿Y vectorizar las tendencias con NumPy (teoría 05)? Pruébalo **sin** añadirlo al proyecto:

```bash
uv run --with numpy==2.5.4 python -X importtime -c "import numpy" 2>&1 | tail -1
```

Importar NumPy cuesta alrededor de 0,1 s; la mediana, la media móvil y el mayor salto suman unos 30 ms con 100 000 valores. Por Amdahl, `informe` iría **más lento**. Escribe en el *pull request* esa cuenta con tus números: decidir con datos que no es tan válido como un arreglo.

### 13. La versión

En `pyproject.toml`, `version = "0.22.0"`, y:

```bash
uv lock
uv run pytest -q
uv run observatorio --version
```

```
... passed
observatorio 0.22.0
```

### 14. Calidad y cobertura

```bash
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
```

`alembic check` sigue diciendo `No new upgrade operations detected.`: esta semana no cambia la base de datos. En Docker, la etapa `test` lleva py-spy (22 MB más); `runtime` no, porque es de desarrollo: sigue en 301 MB.

### 15. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `cli.py` | `series.measurements[:rows]` por `series.measurements` | |
| `cli.py` | `if len(shown) < len(series)` por `<=` | |
| `cli.py` | quita `min=0,` de `--filas` | |
| `cli.py` | `[-filas:] if filas else []` por `[-filas:]` | |
| `cli.py` | `[-filas:] if filas else []` por `[:filas]` | |
| `cli.py` | añade `Series.from_lines(lines)` debajo de `Series.parse(lines)` | |
| `cli.py` | `scale.row(measurement)` por `SCALE.row(measurement)` | |
| `groups.py` | `enumerate(lines, start=1)` por `enumerate(lines)` en `records_with_errors` | |
| `groups.py` | quita el `logger.debug` de `records_with_errors` | |
| `scripts/generar_medidas.py` | `"NA" if rng.random() < 0.05 else ` por nada | |

Nueve mueren. Uno **sobrevive**: ¿cuál, y por qué? Pista: el generador sigue siendo reproducible y sus líneas siguen siendo válidas, pero ¿qué parte de `informe` deja de recibir datos en tus medidas? Lo vas a matar en el paso siguiente.

Fíjate en el sexto: ningún test de salida lo ve (el informe es idéntico), solo `test_informe_reads_each_line_once`, que cuenta trabajo.

### 16. Tus tests

En `tests/test_my_performance.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las funciones de `test_performance.py` (`calls_of`, `profiled_informe`, `lines_of`, `table_rows`). Ideas:

- el mutante que sobrevivió: que el generador ponga algún `"NA"` (genera 200 líneas en `tmp_path`, como `test_the_generator_is_reproducible`);
- que `informe -n 5` llame a `Table.add_row` 5 veces;
- que `informe` analiza cada línea una vez también cuando hay muchas inválidas;
- que `Series.parse` da lo mismo que `process_lines` con **tus** líneas de ejemplo;
- que `--escala` sigue cambiando los niveles del resumen;
- que `table_of` sin `rows` pinta 20.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 845 tests en verde.

### 17. README y pull request

En el `README.md` de tu repositorio, añade una sección "Rendimiento": cómo generar el archivo grande, cómo medir (`time`, `/usr/bin/time`), cómo perfilar (`cProfile` y `py-spy`) y la opción `--filas`.

Commits sugeridos, en este orden:

1. `test: add performance tests`
2. `build: add py-spy`
3. `chore: ignore the profile folder`
4. `perf: show only the first rows of the table`
5. `perf: parse each line once`
6. `chore: bump version to 0.22.0`
7. `test: add my performance tests`

`perf:` es el tipo de Conventional Commits para un cambio que mejora el rendimiento sin cambiar lo que hace el programa. Sube la rama y abre el *pull request*:

```bash
git push -u origin week-22
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-22` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La tabla de medidas: una fila por vuelta (semana 21, `--filas`, `Series.parse`), con segundos, MB y bytes de salida.
3. Las capturas de `perfil/antes.svg` y `perfil/despues.svg` (arrastra las imágenes al *pull request*; los SVG no se suben al repositorio).
4. La tabla de mutantes del paso 15 y el test con el que mataste al superviviente.
5. Por qué no usas NumPy en `informe` y por qué dejas el arranque para más adelante, con tus números.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `test_dev_tools_are_pinned` falla | Falta el paso 3: `uv add --dev py-spy==0.4.2` |
| `check-added-large-files` para el commit con `perfil/grande.txt` | Falta `perfil/` en `.gitignore`; si ya lo añadiste a Git, `git rm -r --cached perfil` |
| `test_profiles_stay_out_of_the_image` falla | Falta `perfil/` en `.dockerignore`, en una línea sola |
| `test_table_colors_each_level` falla con `missing 1 required positional argument: 'rows'` | `table_of` necesita `rows: int = ROWS`, con valor por defecto |
| `test_verbose_shows_debug_messages_on_stderr` falla | Falta el `logger.debug` en `records_with_errors`, o está en otro módulo |
| `test_parse_agrees_with_process_lines_and_from_lines` falla con un ejemplo raro | Lee el ejemplo que imprime Hypothesis: suele ser el orden de `strip` y `is_data_line`, o la numeración |
| `test_informe_reads_each_line_once` da 104 en lugar de 52 | `informe` sigue llamando a `process_lines` o a `Series.from_lines` además de `Series.parse` |
| `informe` tarda lo mismo que antes | ¿Mides con `> /dev/null`? Sin él, tu terminal también tarda en dibujar. ¿Repetiste? Compara mínimos |
| py-spy dice `Permission Denied` | En macOS hace falta `sudo .venv/bin/py-spy ...`; en Linux, solo con `--pid` (teoría 03, sección 8) |
| `py-spy record` tarda muchísimo | Falta `--nonblocking`: la pausa en cada muestra con pilas profundas |
| `/usr/bin/time: No such file or directory` | En macOS: `brew install gnu-time` y `gtime`; o mide la memoria solo con `time` y apúntalo |

## Entrega

1. Rama `week-22` con `--filas`, `records_with_errors`, `Series.parse`, `informe` con una sola lectura, `py-spy==0.4.2` en `dev`, `perfil/` fuera de Git y de la imagen, la versión `0.22.0` y al menos 6 tests tuyos en `test_my_performance.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Rendimiento".
4. *Pull request* `week-22` → `main` con lo que pide el paso 17.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Vectorizar con NumPy](../2-practicas/ejercicio-04-vectorizar-con-numpy/README.md) | **Proyecto · Rendimiento del Observatorio** | [Rúbrica de la semana 22](../rubrica-evaluacion.md) |
