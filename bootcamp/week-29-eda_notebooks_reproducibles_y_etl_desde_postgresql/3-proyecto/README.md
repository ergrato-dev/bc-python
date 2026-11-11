# Proyecto — Observatorio, capa 28: extraer y explorar

⏱️ 6 h 30 min · Capa 28 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Tus medidas viven en PostgreSQL desde la semana 19, y desde entonces las has resumido con comandos. Esta semana las **exploras**: un ETL las saca de la base a una instantánea con su huella, y un notebook reproducible las analiza y escribe lo que encuentra.

```
$ uv run observatorio extraer notebooks/instantanea.csv --carga 1
instantanea.csv: 2000 medidas · cargas: 1
sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
```

| Pieza | Qué hace |
|---|---|
| `core/etl.py` | `extract` lee las medidas de PostgreSQL en su orden; `transform` añade el nivel y pone las columnas en español; `write_snapshot` escribe el CSV y devuelve su huella SHA-256 |
| `extraer SALIDA [--carga N]` | Ejecuta el ETL contra la base de `OBSERVATORIO_DATABASE_URL` |
| `notebooks/eda.ipynb` | Tu análisis exploratorio: preguntas, tablas, gráficos y conclusiones, sobre `notebooks/instantanea.csv` |
| Etapa `notebook` y servicio `notebook` | JupyterLab en Docker, solo para tu máquina y con token |
| Gancho `notebook-outputs` | Quita salidas, contadores y horas antes de cada commit |

Una dependencia nueva, en un grupo propio que `uv sync` no instala:

| Paquete | Grupo | Para qué |
|---|---|---|
| `jupyterlab==4.6.4` | `notebook` | JupyterLab, el kernel y `nbconvert`. Trae 77 paquetes más |

```
src/observatorio/
├── cli.py                  # modificado: extraer
└── core/
    └── etl.py              # nuevo: pandas, sin reexportar en core/__init__.py
notebooks/
├── eda.ipynb               # nuevo: tu análisis
└── instantanea.csv         # nuevo: los datos del análisis
tests/
├── test_etl.py             # nuevo: los tests del bootcamp
├── test_notebook.py        # nuevo: el notebook, JupyterLab, Docker y el gancho
├── test_my_etl.py          # nuevo: los tuyos
├── db_fixtures.py          # modificado: db_env vacía las tablas también al terminar
├── test_delivery.py        # modificado: la etapa notebook, el gancho y las imágenes week-29
└── test_package.py         # modificado: etl en core y la versión 0.29.0
Dockerfile                  # modificado: la etapa notebook
compose.yaml                # modificado: el servicio notebook y las imágenes week-29
.pre-commit-config.yaml     # modificado: el gancho notebook-outputs
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-29`. El `starter/` trae la capa 27 resuelta: `core/inference.py` y el comando `comparar`. **Tú** escribes `etl.py`, `extraer` y tu notebook.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-28` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-29
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/3-proyecto/starter
cp $STARTER/tests/test_etl.py $STARTER/tests/test_notebook.py $STARTER/tests/test_my_etl.py tests/
cp $STARTER/tests/db_fixtures.py $STARTER/tests/test_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `test_etl.py`, con 22 tests (uno con Hypothesis); `test_notebook.py`, con 21; y `test_my_etl.py`, con un ejemplo.
- **Modificados:**
  - `db_fixtures.py`: `db_env` vacía las tablas también al **terminar** cada test. `extraer` lee lo que guardó `guardar`, que confirma de verdad; sin esa limpieza, las cargas de un test de la CLI llegarían a los tests de `session` que vienen después, que esperan las tablas vacías.
  - `test_delivery.py`: la etapa `notebook` entre `test` y `runtime`, el gancho `notebook-outputs` y las imágenes `week-29`.
  - `test_package.py`: `etl` es un módulo de `core`, y la versión es `0.29.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.etl'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `tests/test_etl.py` y `tests/test_notebook.py` enteros. Fíjate en:

- `SNAPSHOT`, la instantánea de dos medidas **byte a byte**, con la celda vacía del "sin dato";
- `test_extract_orders_even_after_an_update`, y el comentario que explica por qué un `UPDATE` cambia el orden (teoría 04, sección 5);
- `test_extract_a_load_without_values_keeps_float`: una carga sin ningún valor;
- `test_snapshot_reads_back_the_same`: con cualquier etiqueta, también "NA" o una con comas y comillas, la instantánea se lee igual, si se lee como el notebook;
- `test_notebook_runs_top_to_bottom`, que ejecuta tu notebook sin Jupyter (teoría 05, sección 5);
- `test_colab_cell_installs_the_pinned_versions`, que compara la celda de Colab con tu `pyproject.toml`.

### 4. El módulo `etl.py`

Crea `src/observatorio/core/etl.py`:

```python
"""Extraer de PostgreSQL, transformar con pandas y guardar una instantánea para analizar.

Qué: `extract` lee las medidas guardadas con una consulta de SQLAlchemy, `transform` añade
el nivel y pone los nombres de columna en español, y `write_snapshot` escribe un CSV y
devuelve su huella SHA-256.
Para qué: la base de datos cambia cada vez que alguien guarda o borra una carga; un análisis
que la lee directamente da otro resultado cada día. El notebook lee la instantánea, y la
huella demuestra que es la misma que se analizó.
Impacto: importa pandas, como frames.py: core/__init__.py no lo reexporta.
"""

import hashlib
from pathlib import Path

import pandas as pd
from sqlalchemy import Connection, select

from observatorio.core.database import Reading
from observatorio.core.frames import with_levels
from observatorio.core.model import Scale

# El tipo de cada columna, fijado: sin él, pandas lo deduce de las filas que lleguen, y una
# carga sin ningún valor tendría la columna `value` de tipo object en lugar de float64.
TYPES = {"load_id": "int64", "position": "int64", "label": "str", "value": "float64"}
# Los nombres de la instantánea, en el idioma del dominio, como los de medidas.csv.
SNAPSHOT_COLUMNS = {
    "load_id": "carga",
    "position": "posicion",
    "label": "etiqueta",
    "value": "valor",
    "level": "nivel",
}


def extract(connection: Connection, load_id: int | None = None) -> pd.DataFrame:
    """Las medidas de una carga, o de todas, en el orden en que se guardaron."""
    query = select(Reading.load_id, Reading.position, Reading.label, Reading.value).order_by(
        Reading.load_id, Reading.position
    )
    if load_id is not None:
        # El filtro va en el WHERE: PostgreSQL envía solo esas filas, no la tabla entera.
        query = query.where(Reading.load_id == load_id)
    return pd.read_sql(query, connection, dtype=TYPES)


def transform(frame: pd.DataFrame, scale: Scale) -> pd.DataFrame:
    """Una copia con el nivel de cada medida y las columnas en español."""
    return with_levels(frame, scale).rename(columns=SNAPSHOT_COLUMNS)


def write_snapshot(frame: pd.DataFrame, path: Path) -> str:
    """Escribe la tabla en CSV y devuelve la huella SHA-256 de los bytes escritos."""
    # lineterminator="\n": los mismos bytes en Linux, macOS y Windows, y la misma huella.
    data = frame.to_csv(index=False, lineterminator="\n").encode()
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()
```

Tres funciones, una por letra del ETL (teoría 04):

- `extract` recibe una **conexión**, no una sesión ni una URL: quien la abre decide la transacción. `ORDER BY` por carga y posición, y el `WHERE` solo si hay carga. `dtype=TYPES` fija los tipos aunque no llegue ninguna fila, o ningún valor.
- `transform` reutiliza `with_levels` de la semana 24: los mismos niveles que `informe`, sin escribirlos dos veces.
- `write_snapshot` construye los bytes **una vez**, los escribe y calcula su huella sobre esos mismos bytes: la huella es la del archivo, no la de otra conversión.

```bash
uv run pytest -q
```

```
31 failed, 1025 passed
```

Los de `extract`, `transform` y `write_snapshot` ya pasan. Fallan los de `extraer`, los del notebook y los de Docker.

### 5. El comando `extraer`

En `src/observatorio/cli.py`, después de `consultar`:

```python
@app.command()
def extraer(
    salida: Annotated[Path, typer.Argument(metavar="SALIDA", help="El CSV que escribe.")],
    carga: Annotated[
        int | None, typer.Option("--carga", "-c", help="Solo las medidas de esta carga.")
    ] = None,
) -> None:
    """Extrae de PostgreSQL las medidas guardadas y escribe una instantánea CSV con su nivel.

    Lee OBSERVATORIO_DATABASE_URL del entorno o de .env.
    """
    # Importar aquí, como en `filtrar`: pandas tarda en cargarse.
    from observatorio.core import etl

    with database() as session:
        if carga is not None and session.get(Load, carga) is None:
            raise fail(f"no existe la carga {carga}", 1)
        frame = etl.extract(session.connection(), carga)
    if frame.empty:
        raise fail("no hay medidas que extraer: guarda una carga con `observatorio guardar`", 1)
    snapshot = etl.transform(frame, SCALE)
    try:
        digest = etl.write_snapshot(snapshot, salida)
    except OSError as problem:
        raise fail(f"no se puede escribir {salida}: {problem}", 2) from problem
    loads = snapshot["carga"].nunique()
    out.print(f"{salida.name}: {len(snapshot)} medidas · cargas: {loads}")
    out.print(f"sha256: {digest}")
```

- Como `consultar`, comprueba que la carga existe **antes** de extraer: una carga que no existe sale con código 1 y no escribe nada. Sin carga y sin medidas, también código 1.
- `session.connection()`: la conexión de la sesión que abre `database()`, con sus errores de conexión ya traducidos a mensajes (semana 19).
- Importa `etl` dentro: pandas solo se carga al extraer.

Actualiza el docstring del módulo: "diecinueve comandos", con `extraer` entre `consultar` y `borrar`.

```bash
uv run pytest -q
uv run observatorio extraer /tmp/todo.csv
uv run observatorio extraer /tmp/x.csv --carga 999; echo $?
```

```
25 failed, 1031 passed
```

El primer `extraer` escribe todas tus cargas (las que guardaste en la semana 19); el segundo, `error: no existe la carga 999` y `1`.

### 6. Versión e imágenes

En `pyproject.toml`, `version = "0.29.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-29-test` y `local/observatorio:week-29`.

```bash
uv run pytest -q
```

```
22 failed, 1034 passed
```

### 7. La instantánea

Guarda una carga con datos de **tu dominio**, con al menos unos cientos de medidas, y extráela a `notebooks/`. Si todavía no tienes datos tuyos tan grandes, usa el generador de la semana 22 con las etiquetas de tu dominio en `LABELS`:

```bash
uv run python scripts/generar_medidas.py 2000 perfil/eda.txt
uv run observatorio guardar perfil/eda.txt
uv run observatorio cargas
mkdir -p notebooks
uv run observatorio extraer notebooks/instantanea.csv --carga <número>
```

```
carga 3: perfil/eda.txt, 2000 medidas
...
instantanea.csv: 2000 medidas · cargas: 1
sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
```

Tu número de carga y tu huella serán otros. **Copia la huella**: la necesitas en el paso 9. Ejecuta `extraer` otra vez: misma huella, porque los mismos datos dan los mismos bytes.

Solo datos sintéticos o anonimizados: este archivo va a Git y quizá a Colab. Con unos cientos de KB basta; el gancho `check-added-large-files` para el commit por encima de 500 KB.

```bash
uv run pytest -q
```

```
21 failed, 1035 passed
```

### 8. JupyterLab

```bash
uv add --group notebook jupyterlab==4.6.4
uv run pytest -q
```

```
 + jupyterlab==4.6.4
...
20 failed, 1036 passed
```

Mira en `pyproject.toml` el grupo nuevo, `notebook`, y añade encima un comentario que diga por qué no va en `dependencies` (teoría 05, sección 2). La versión está revisada en `docs/stack-versions.md` del bootcamp. JupyterLab trae 77 paquetes más; `uv` resuelve los suyos al día de hoy, así que pueden ser algo más nuevos que los del bootcamp.

Añade a tu `.gitignore` la carpeta en la que JupyterLab guarda copias de seguridad:

```bash
echo ".ipynb_checkpoints/" >> .gitignore
```

Y ábrelo:

```bash
uv run --group notebook jupyter lab notebooks/
```

### 9. Tu notebook

En JupyterLab, *File → New → Notebook*, kernel *Python 3 (ipykernel)*, y guárdalo como `notebooks/eda.ipynb`. Su estructura, la que comprueba `test_notebook.py`:

**Celda 1, Markdown:** el título, el botón de Colab, tus preguntas y de dónde salen los datos.

```markdown
# Análisis exploratorio de las medidas

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ana-perez/python-ana-perez/blob/main/notebooks/eda.ipynb)

**Preguntas**: ¿cuántas medidas faltan, y en qué etiquetas? ¿Cómo se reparten los valores de cada etiqueta? ¿Hay medidas fuera de lo normal? ¿Difieren las etiquetas entre sí?

**Datos**: `instantanea.csv`, escrita por `observatorio extraer instantanea.csv --carga 1` desde PostgreSQL. El notebook no lee la base de datos: lee esta instantánea y comprueba su huella, así da lo mismo hoy que dentro de un año.

**Para repetirlo**: *Kernel → Restart Kernel and Run All Cells*. En Colab, sube antes `instantanea.csv` con el panel de archivos.
```

Cambia `ana-perez/python-ana-perez` por tu usuario de GitHub y tu repositorio.

**Celda 2, código:** las versiones de tu `pyproject.toml`, solo en Colab (teoría 03, sección 5).

```python
import sys

# Solo en Colab: instala las versiones de uv.lock. En tu máquina y en Docker ya las tienes.
if "google.colab" in sys.modules:
    import subprocess

    subprocess.run(
        ["uv", "pip", "install", "--system", "pandas==3.1.0", "matplotlib==3.11.2", "scipy==1.18.1"],
        check=True,
    )
```

**Celda 3, código:** cargar la instantánea, comprobando su huella. Pon la tuya en `EXPECTED`.

```python
import hashlib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

SNAPSHOT = Path("instantanea.csv")
# La huella que escribió `observatorio extraer`. Si el archivo cambia, el notebook se para.
EXPECTED = "3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65"
assert hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest() == EXPECTED, "no es la instantánea analizada"

# keep_default_na=False: una etiqueta "NA" o "null" sigue siendo texto; solo un valor vacío falta.
frame = pd.read_csv(SNAPSHOT, keep_default_na=False, na_values={"valor": [""]})
frame.shape
```

`keep_default_na=False` y `na_values`: una etiqueta "NA" sigue siendo una etiqueta; solo una celda vacía de `valor` es un hueco (teoría 01, sección 4).

**Después**, tu análisis exploratorio, con el recorrido de la teoría 01: una sección por pregunta, código y un hallazgo en Markdown. Como referencia, el notebook de ejemplo del bootcamp tiene estas secciones, con datos generados al azar:

| Sección | Código |
|---|---|
| 1. Forma y tipos | `frame.dtypes`, `frame.head()` |
| 2. Lo que falta | `frame["valor"].isna().groupby(frame["etiqueta"]).agg(["sum", "mean"])` |
| 3. Cómo se reparten | `frame.groupby("etiqueta")["valor"].describe()` y un histograma por etiqueta |
| 4. Fuera de lo normal | La regla de Tukey |
| 5. Niveles por etiqueta | `pd.crosstab(frame["etiqueta"], frame["nivel"], margins=True)` |
| 6. ¿Difieren las etiquetas? | `stats.f_oneway`, de la semana 28 |

Con tus datos tendrás otras preguntas y otros hallazgos: no copies estas secciones si no las responden.

**Última celda, Markdown:** `## Conclusiones`, con lo que responde el análisis, los problemas que encontraste y lo que **no** puede responder.

Tres reglas, que comprueba el test:

- **Python normal**: ni `%magias`, ni `!órdenes`, ni `display(...)`.
- **Rutas relativas**: `Path("instantanea.csv")`, nunca la ruta completa de tu máquina.
- **De arriba abajo**: antes de guardar, *Kernel → Restart Kernel and Run All Cells*.

```bash
uv run pytest -q
```

```
12 failed, 1044 passed
```

Fallan nueve tests de Docker y del gancho, que vienen ahora, y tres que te sorprenderán:

```
FAILED tests/test_notebook.py::test_notebook_has_no_outputs
FAILED tests/test_notebook.py::test_notebook_has_no_execution_counts
FAILED tests/test_notebook.py::test_notebook_has_no_execution_times
```

JupyterLab guardó tu notebook **con** sus salidas, sus contadores y la hora de cada celda. Ábrelo con un editor de texto y búscalos. El paso 10 los quita.

### 10. Docker y el gancho

En el `Dockerfile`, una etapa nueva **entre** `test` y `runtime` (`runtime` tiene que seguir siendo la última). Cambia también el comentario del principio: ahora son cinco etapas.

```dockerfile
# Etapa 4: JupyterLab, para explorar con los mismos paquetes y versiones que el proyecto.
# Solo con `docker compose --profile notebook up notebook`: nunca va a producción.
FROM builder AS notebook

ENV PATH="/opt/venv/bin:$PATH"

# --group notebook: JupyterLab y sus dependencias, encima de las del proyecto.
RUN uv sync --locked --no-dev --no-editable --group notebook

# UID 1000, el de tu usuario en casi cualquier Linux o WSL: los notebooks se guardan en tu
# carpeta notebooks/ (un volumen), y con otro UID no podría escribir en ella.
RUN useradd --create-home --uid 1000 analyst
USER 1000:1000
WORKDIR /app/notebooks

EXPOSE 8888

# 0.0.0.0 dentro del contenedor; compose.yaml solo abre el puerto a tu máquina. Sin
# --IdentityProvider.token, Jupyter crea un token al azar y lo escribe en el registro.
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--no-browser"]
```

En `compose.yaml`, un servicio nuevo después de `api`, y el comentario del principio con cuatro servicios:

```yaml
  notebook:
    build:
      context: .
      target: notebook
    image: local/observatorio:week-29-notebook
    # Con un perfil, `docker compose up` no lo arranca: hace falta `--profile notebook`.
    profiles:
      - notebook
    # Tu carpeta notebooks/ dentro del contenedor: lo que guardas en JupyterLab queda en
    # tu repositorio, y sobrevive a `docker compose down`.
    volumes:
      - ./notebooks:/app/notebooks
    ports:
      - "127.0.0.1:8888:8888"
```

Si `id -u` no te da 1000, pon tu número en `useradd --uid` y en `USER` (teoría 05, sección 3).

```bash
uv run pytest -q
docker compose --profile notebook build notebook
docker compose --profile notebook up -d notebook
docker compose logs notebook | grep 127.0.0.1
```

```
6 failed, 1050 passed
...
notebook-1  |         http://127.0.0.1:8888/lab?token=c2c8dead1c442d0dfdbee66100b1cbdcdce9e08870ab620e
```

Abre esa dirección, abre `eda.ipynb` y ejecútalo entero: es tu carpeta `notebooks/`, dentro del contenedor. Comprueba también que sin token no se entra:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8888/api/contents
docker compose --profile notebook stop notebook
```

```
403
```

Ahora el gancho. En `.pre-commit-config.yaml`, al final de los ganchos locales:

```yaml
      # Quita de cada notebook las salidas, los contadores y los metadatos de cada celda
      # (la hora a la que se ejecutó), y deja el kernel: en Git queda solo el código. Si
      # cambia algo, el commit se para: vuelve a añadir el notebook.
      - id: notebook-outputs
        name: notebooks sin salidas
        entry: >-
          uv run --locked --group notebook jupyter nbconvert --clear-output --inplace
          --ClearMetadataPreprocessor.enabled=True
          --ClearMetadataPreprocessor.preserve_nb_metadata_mask=kernelspec
        language: unsupported
        files: \.ipynb$
```

```bash
git add -A
uv run pre-commit run notebook-outputs --all-files
git add -A
uv run pytest -q
```

```
notebooks sin salidas....................................................Failed
- hook id: notebook-outputs
- files were modified by this hook
...
1056 passed
```

La primera vez, `uv` instala el grupo `notebook` y el gancho reescribe tu notebook: por eso dice `Failed`. Ejecútalo otra vez y dirá `Passed`. A partir de ahora lo hace solo en cada `git commit`.

Y la calidad de siempre:

```bash
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
docker compose build app api && docker compose run --rm app
docker images local/observatorio
uv run python -c "import sys, observatorio.cli; print('pandas' in sys.modules)"
```

`coverage report` debe dar 100 % en `etl.py` y en `cli.py`. `alembic check`: `No new upgrade operations detected.` (`etl.py` no crea tablas). La comprobación de `sys.modules` escribe `False`. En `docker images`, `week-29` mide lo mismo que `week-28` (1,18 GB): JupyterLab no entra en `runtime`. `week-29-notebook`, unos 2,5 GB.

Mide cuánto tarda cada forma de ejecutar el notebook:

```bash
uv run pytest -q --durations=1 tests/test_notebook.py
time uv run --group notebook jupyter execute notebooks/eda.ipynb
```

En la máquina del bootcamp, 0,7 s el test y 3,8 s `jupyter execute`: la diferencia es arrancar un kernel. `jupyter execute` no guarda nada: tu notebook sigue limpio.

### 11. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_etl.py tests/test_my_etl.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `etl.py` | quita el `.order_by(...)` de `extract` | |
| `etl.py` | `query = query.where(...)` por `pass` | |
| `etl.py` | `pd.read_sql(query, connection, dtype=TYPES)` por `pd.read_sql(query, connection)` | |
| `etl.py` | `"level": "nivel"` por `"level": "level"` | |
| `etl.py` | `with_levels(frame, scale).rename` por `frame.rename` | |
| `etl.py` | quita `index=False` de `to_csv` | |
| `etl.py` | `lineterminator="\n"` por `lineterminator="\r\n"` | |
| `etl.py` | `hashlib.sha256(data)` por `hashlib.md5(data)` | |
| `cli.py` | en `extraer`, quita la comprobación de que la carga existe | |
| `cli.py` | `if frame.empty:` por `if False:` | |

Los diez mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el primero, ¿qué test falla? ¿Por qué **no** falla `test_extract_keeps_the_saved_order`, que también comprueba el orden? Pista: lee el comentario del test que sí falla, y piensa en qué orden están guardadas las filas en disco.
- Con el tercero, ¿qué test falla? ¿Qué tipo tendría la columna `value` de una carga de tu dominio en la que el sensor no midió nada, y qué pasaría al calcular su media en el notebook?

Después, en `tests/test_my_etl.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las etiquetas y los valores de tu dominio y las funciones de `test_etl.py` (`save`, `values`, `snapshot_of`). Ideas:

- una carga de tu dominio extraída en su orden, con un "sin dato" en medio;
- el nivel de una medida en cada borde de tu escala;
- una etiqueta de tu dominio con coma o comillas, escrita y leída de vuelta;
- que la huella cambie al cambiar un solo valor, y no cambie al escribir dos veces;
- `extraer --carga` con dos cargas de tu dominio, y solo las líneas de una en el archivo;
- que tu notebook lea una etiqueta "NA" como texto (lee la instantánea con las mismas opciones que la celda 3).

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1203 tests en verde.

### 12. README y pull request

En el `README.md` de tu repositorio, añade una sección "Explorar los datos": cómo generar la instantánea, cómo abrir el notebook (con `uv`, con Docker y en Colab) y tres hallazgos de tu análisis.

Commits sugeridos, en este orden:

1. `test: add etl and notebook tests`
2. `feat: add etl module`
3. `feat: add extraer command`
4. `chore: bump version to 0.29.0`
5. `data: add snapshot for the exploratory analysis`
6. `build: add jupyterlab notebook group`
7. `docs: add exploratory analysis notebook`
8. `build: serve jupyterlab from docker`
9. `ci: clear notebook outputs before each commit`
10. `test: add my etl tests`

```bash
git push -u origin week-29
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-29` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `extraer`, con tu huella, y el enlace a `notebooks/eda.ipynb` en tu rama: GitHub lo muestra sin salidas.
3. Tus conclusiones, copiadas del notebook.
4. El tamaño de tus imágenes y tus dos tiempos del paso 10.
5. La tabla de mutantes del paso 11 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'observatorio.core.etl'` | Falta el paso 4, o el archivo no está en `src/observatorio/core/` |
| `test_extract_orders_even_after_an_update` falla | Falta el `ORDER BY`, o solo ordenas por carga |
| `test_write_snapshot_writes_csv` falla con `\r\n` | Falta `lineterminator="\n"` |
| Tests de `session` fallan con cargas que no son suyas | No copiaste el `db_fixtures.py` nuevo |
| `test_notebook_runs_top_to_bottom` falla con `NameError` en `celda N` | Una celda usa algo de una celda borrada o posterior: *Restart Kernel and Run All Cells* y arréglalo |
| `test_notebook_runs_top_to_bottom` falla con `AssertionError: no es la instantánea analizada` | Regeneraste `instantanea.csv` con otros datos: pon la huella nueva en `EXPECTED` y revisa tus hallazgos |
| `test_notebook_is_plain_python` falla | Quita `%`, `!` y `display(` del notebook |
| `test_colab_cell_installs_the_pinned_versions` falla | Una versión de la celda de Colab no es la de tu `pyproject.toml` |
| `test_notebook_has_no_outputs` falla tras un commit | El gancho no está instalado: `uv run pre-commit install` |
| JupyterLab en Docker: `Permission denied` al guardar | El UID de la etapa no es el tuyo: mira `id -u` |
| `Bind for 127.0.0.1:8888 failed: port is already allocated` | Tienes otro JupyterLab abierto (quizá con `uv run`): ciérralo |
| `[IPKernelApp] WARNING \| Kernel is running over TCP without encryption` | Normal: el kernel escucha en tu propia máquina o en el contenedor |

## Entrega

1. Rama `week-29` con `core/etl.py`, el comando `extraer`, `notebooks/eda.ipynb` y `notebooks/instantanea.csv` de tu dominio, el grupo `notebook`, la etapa y el servicio `notebook`, el gancho, las imágenes `week-29`, la versión `0.29.0` y al menos 6 tests tuyos en `test_my_etl.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Explorar los datos".
4. *Pull request* `week-29` → `main` con lo que pide el paso 12.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Reproducible o no](../2-practicas/ejercicio-04-reproducible-o-no/README.md) | **Proyecto · Extraer y explorar** | [Webgrafía](../4-recursos/webgrafia/README.md) |
