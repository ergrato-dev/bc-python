# Proyecto — Observatorio, capa 15: muchos archivos a la vez

⏱️ 6 h 30 min · Capa 15 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Hasta ahora, `informe` lee **un** archivo. Tus datos llegan en muchos: un archivo por estación, por día o por sensor. Esta semana añades el comando `lote`, que resume varios archivos **a la vez**, con hilos o con procesos, y escribe una fila por archivo:

```
$ uv run observatorio lote medidas.csv medidas.txt falta.csv
error: no existe el archivo falta.csv
                     Archivos
┏━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Archivo     ┃ Medidas ┃ Con valor ┃       Media ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ medidas.csv │       7 │         6 │ 32.5 unidad │
│ medidas.txt │       7 │         6 │ 32.5 unidad │
└─────────────┴─────────┴───────────┴─────────────┘
archivos: 3 · con error: 1
```

| Opción | Qué hace |
|---|---|
| `ARCHIVOS...` | Uno o más `.txt` o `.csv`, en el orden en que salen en la tabla |
| `--trabajadores N`, `-t N` | Cuántos archivos se leen a la vez; por defecto, `WORKERS = 4` |
| `--procesos` | Reparte los archivos entre procesos en lugar de hilos |

Un archivo que no se puede leer **no** para el lote: su error va a stderr, el resto sale en la tabla, y el código de salida es `1`. Las líneas inválidas de un archivo no se informan una a una, como en `informe`: `lote` solo cuenta las medidas que sí entiende.

La lógica va en un módulo nuevo de `core/`, sin nada de Typer ni de Rich:

```
src/observatorio/
├── cli.py          # + WORKERS, files_table y el comando lote
└── core/
    ├── __init__.py # + FileReport, report_file y report_files
    └── batch.py    # nuevo: FileReport, report_file y report_files
tests/
├── test_batch.py      # nuevo: los tests del bootcamp
├── test_my_batch.py   # nuevo: los tuyos
└── test_package.py    # modificado: el módulo batch, la API y la versión 0.16.0
```

Al final, mides. Vas a descubrir que, con tus archivos, los procesos van **más lentos** que los hilos, y entenderás por qué.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-16`. El `starter/` trae la capa 14 resuelta. **Tú** escribes `core/batch.py` y el comando `lote`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-15` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-16
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-16-concurrencia_hilos_procesos_gil_y_free_threading/3-proyecto/starter
cp $STARTER/tests/test_batch.py $STARTER/tests/test_my_batch.py $STARTER/tests/test_package.py tests/
sed -i 's/week-15/week-16/' compose.yaml
grep -q '^.venv-ft/$' .dockerignore || echo '.venv-ft/' >> .dockerignore
git status --short
```

Copias estos archivos:

- **Nuevos:**
  - `tests/test_batch.py`, con 31 tests de `batch.py` y del comando `lote`;
  - `tests/test_my_batch.py`, con un ejemplo.
- **Modificado:** `test_package.py`, que espera el módulo `batch`, sus tres nombres en la API de `core` y la versión `0.16.0`.

`.venv-ft/` es el entorno que crearás en el paso 12 con el Python sin GIL. `.dockerignore` lo deja fuera de la imagen, como `.venv/`. En Git no hace falta: uv escribe un `.gitignore` dentro de cada entorno que crea.

### 3. Tests en rojo

```bash
uv run pytest
```

```
E   ImportError: cannot import name 'FileReport' from 'observatorio.core' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Lee `tests/test_batch.py` antes de escribir nada. Fíjate en cómo prueba código concurrente **sin depender de la suerte** (teoría 05):

- las tareas falsas duermen tiempos distintos para que terminen en otro orden, y el test comprueba que `report_files` devuelve el orden de entrada;
- una `Barrier` de tres solo se abre si tres tareas corren **a la vez**: si fueran una detrás de otra, el test fallaría por *timeout*;
- un contador protegido con un `Lock` mide cuántas tareas hubo a la vez como máximo, y debe ser igual a `workers`.

### 4. El esqueleto: `FileReport` y la API

Crea `src/observatorio/core/batch.py` con un *docstring* de módulo (qué, para qué, impacto) y:

```python
@dataclass(frozen=True, slots=True)
class FileReport:
    """El resumen de un archivo: cuántas medidas tiene, cuántas con valor y su media.

    Si el archivo no se pudo leer, `error` dice por qué y los números quedan a cero.
    """

    path: Path
    measurements: int = 0
    with_value: int = 0
    mean: float | None = None
    error: str | None = None


def report_file(path: Path) -> FileReport:
    """Lee un archivo .txt o .csv y lo resume. Un DataFileError queda en `error`."""
    raise NotImplementedError


def report_files(
    paths: Iterable[Path], *, workers: int = 4, processes: bool = False
) -> list[FileReport]:
    """Resume los archivos con `workers` trabajadores a la vez, en el orden de `paths`."""
    raise NotImplementedError
```

`FileReport` es **inmutable** (`frozen=True`). Cada tarea crea el suyo y lo devuelve: ningún hilo modifica nada que otro esté usando, así que no hace falta ningún `Lock`. Y como es una *dataclass* normal, puede viajar con `pickle` a otro proceso y volver.

En `core/__init__.py`, importa los tres nombres de `observatorio.core.batch` y añádelos a `__all__`. `uv run ruff check --fix` los ordena.

```
30 failed, 391 passed
```

### 5. `report_file`

Lee el archivo con `open_file(path).lines()` (semana 10) y construye la serie con `Series.from_lines(lines)` (semana 9):

- **`measurements`**: cuántas medidas tiene la serie, `len(series)`;
- **`with_value`**: cuántas tienen valor, `len(series.values())`;
- **`mean`**: `statistics.fmean(values)` si hay valores, o `None`;
- **un `DataFileError`** al leer: devuelve `FileReport(path, error=str(problem))`, sin lanzar nada.

```bash
uv run pytest
```

```
23 failed, 398 passed
```

### 6. `report_files` con hilos

```python
    pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="observatorio")
    # with espera a que terminen todas las tareas y cierra el pool, también si hay error.
    # map devuelve los resultados en el orden de las entradas, no en el que terminan.
    with pool:
        return list(pool.map(report_file, paths))
```

Tres decisiones:

- **`map`, no `as_completed`**: la tabla sale en el orden de los argumentos, aunque el segundo archivo termine antes que el primero.
- **`list(...)` dentro del `with`**: `map` devuelve un iterador perezoso; `list` recoge todos los resultados antes de cerrar el *pool*.
- **`thread_name_prefix`**: los hilos se llaman `observatorio_0`, `observatorio_1`... y se reconocen en un registro o en un depurador.

Solo se captura `DataFileError`, en `report_file`. Cualquier otra excepción dentro de una tarea es un bug, y `map` la vuelve a lanzar aquí (ejercicio 04, paso 3). `test_unexpected_errors_reach_the_caller` lo comprueba.

```
13 failed, 408 passed
```

### 7. `report_files` con procesos

Con `processes=True`, el *pool* es un `ProcessPoolExecutor(max_workers=workers)`. El resto no cambia: los dos tienen la misma interfaz, `Executor`.

```python
    pool: Executor
    if processes:
        pool = ProcessPoolExecutor(max_workers=workers)
    else:
        pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="observatorio")
```

`pool: Executor` le dice a mypy que la variable puede tener cualquiera de los dos. Sin esa anotación, mypy deduciría `ProcessPoolExecutor` de la primera asignación y rechazaría la segunda.

`report_file` puede ir a otro proceso porque está definida a nivel de módulo, y `Path` y `FileReport` pueden viajar con `pickle` (ejercicio 02, paso 5).

```
12 failed, 409 passed
```

`test_processes_give_the_same_reports_as_threads` ya pasaba en el paso 6, porque con hilos el resultado es el mismo. El que falta es `test_processes_uses_a_process_pool`, que sustituye `ProcessPoolExecutor` por un espía que apunta cómo se creó.

### 8. El comando `lote`

En `cli.py`, una función que construye la tabla:

```python
def files_table(reports: list[FileReport]) -> Table:
    """Una fila por archivo leído: ruta, medidas, medidas con valor y media."""
```

Con título `Archivos` y cuatro columnas: `Archivo`, y `Medidas`, `Con valor` y `Media` alineadas a la derecha. La media, `f"{report.mean:.1f} {UNIT}"`, o `sin dato`.

Y el comando, de momento solo con el argumento:

```python
@app.command()
def lote(
    archivos: Annotated[
        list[Path], typer.Argument(metavar="ARCHIVOS", help="Los .txt o .csv que se resumen.")
    ],
) -> None:
    """Resume varios archivos a la vez: una fila por archivo."""
```

`list[Path]` sin `| None` ni valor por defecto: Typer exige al menos un archivo. El cuerpo:

1. `reports = report_files(archivos)`;
2. cada informe con error, a `err` como `error: <mensaje>`;
3. la tabla de los informes **sin** error, a `out`;
4. `archivos: <total> · con error: <fallidos>`, a `out`;
5. si alguno falló, `raise typer.Exit(1)`.

```bash
uv run observatorio lote medidas.csv medidas.txt falta.csv; echo $?
uv run pytest
```

```
...
archivos: 3 · con error: 1
1
...
6 failed, 415 passed
```

### 9. `--trabajadores` y `--procesos`

Una constante en `cli.py`, junto a `TOP` y `WINDOW`:

```python
# Cuántos archivos lee `lote` a la vez si no se dice otra cosa con --trabajadores.
WORKERS = 4
```

Y dos opciones en `lote`:

- `trabajadores: int`, con `typer.Option("--trabajadores", "-t", min=1, help=...)` y valor por defecto `WORKERS`. `min=1` hace que Typer rechace `-t 0` con un error de uso (código 2) antes de llamar a tu función;
- `procesos: bool`, con `typer.Option("--procesos", help=...)` y valor por defecto `False`.

Pásalas a `report_files(archivos, workers=trabajadores, processes=procesos)`.

```bash
uv run observatorio lote --help
uv run observatorio lote -t 2 --procesos medidas.csv medidas.txt
```

```
1 failed, 420 passed
```

### 10. La versión

```bash
uv version --bump minor
uv run observatorio --version
uv run pytest
```

```
observatorio 0.16.0
...
421 passed
```

### 11. Medir

¿Cuánto ganas leyendo a la vez? No lo adivines: **mídelo**. Crea 500 copias de tu archivo en una carpeta temporal:

```bash
mkdir -p /tmp/lote
for i in $(seq 500); do cp medidas.csv /tmp/lote/m$i.csv; done
time uv run observatorio lote -t 1 /tmp/lote/*.csv > /dev/null
time uv run observatorio lote -t 8 /tmp/lote/*.csv > /dev/null
time uv run observatorio lote --procesos /tmp/lote/*.csv > /dev/null
time uv run observatorio lote --procesos -t 8 /tmp/lote/*.csv > /dev/null
```

Apunta el tiempo **real** (`real` o `total`) de cada uno. En la máquina del bootcamp:

| Orden | Tiempo |
|---|---|
| `-t 1` | 0,77 s |
| `-t 8` | 0,67 s |
| `--procesos` | 1,10 s |
| `--procesos -t 8` | 1,15 s |

Casi nada que ganar con hilos, y los procesos **pierden**. ¿Por qué?

- **Hilos**: un archivo local pequeño se lee en microsegundos, y además el sistema operativo lo tiene ya en memoria. Casi no hay espera que solapar. El resto del tiempo es Python interpretando líneas, y con el GIL eso lo hace un hilo cada vez.
- **Procesos**: arrancar cada proceso y enviar cada ruta y cada `FileReport` con `pickle` cuesta más que resumir un archivo de siete líneas (ejercicio 02, paso 7).
- Una parte fija del tiempo es arrancar Python y cargar Typer, Rich y Pydantic, igual en las cuatro órdenes.

Los hilos ganarían de verdad con archivos en un disco de red o descargados por HTTP (semana 18). Los procesos, con archivos de millones de líneas. El código ya está listo para los dos casos: solo cambia una opción.

### 12. Sin GIL

Ejecuta la suite entera con el Python *free-threaded* (ejercicio 03), en un entorno aparte para no tocar tu `.venv`:

```bash
UV_PROJECT_ENVIRONMENT=.venv-ft uv run --python 3.14.10t pytest -q
UV_PROJECT_ENVIRONMENT=.venv-ft uv run --python 3.14.10t python -c "import sys; print(sys._is_gil_enabled())"
```

```
421 passed
False
```

`UV_PROJECT_ENVIRONMENT=.venv-ft` hace que uv cree e instale el entorno en `.venv-ft/` en lugar de `.venv/`. Las dependencias salen del mismo `uv.lock`: Pydantic publica una versión compilada para el Python sin GIL, y Rich y Typer son Python puro. `False`: ninguna biblioteca obligó a encender el GIL.

Repite la medida del paso 11 con `-t 1` y `-t 8` en el entorno sin GIL. Apunta los cuatro números en el *pull request*. ¿Cambia algo? ¿Por qué tan poco?

### 13. Calidad, cobertura y una prueba de mutación

```bash
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
```

`batch.py` debe salir al 100 %. La prueba de `lote --procesos` desde otra terminal (`test_lote_runs_processes_from_the_terminal`) ejecuta `report_file` en procesos hijos, y `coverage` no los mide sin configuración extra. Los otros tests cubren esas líneas con hilos.

Ahora la prueba de mutación, como en la semana 15. Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `batch.py` | `ThreadPoolExecutor(max_workers=workers, ...)` por `max_workers=4` | |
| `batch.py` | `if processes:` por `if not processes:` | |
| `batch.py` | `FileReport(path, error=str(problem))` por `FileReport(path)` | |
| `batch.py` | `list(pool.map(report_file, paths))` por `sorted(pool.map(report_file, paths), key=lambda r: str(r.path))` | |
| `batch.py` | `if values else None` por `if values else 0.0` | |
| `cli.py` | `workers=trabajadores` por `workers=WORKERS` | |
| `cli.py` | `err.print(f"error: {report.error}")` por `out.print(...)` | |
| `cli.py` | `files_table([... if report.error is None])` por `files_table(reports)` | |

Los ocho deberían morir. Si alguno sobrevive, busca qué test debería matarlo y por qué no lo hace.

### 14. Tus tests

En `tests/test_my_batch.py`, sustituye el ejemplo por **al menos 6 tests** con archivos de **tu dominio** en `tmp_path`:

- `report_file` de un archivo válido: medidas, con valor y media exactas;
- `report_file` de un archivo que falta o con la cabecera mala;
- `report_files` con varios archivos: el orden de entrada;
- `report_files` con `processes=True`: el mismo resultado que con hilos;
- `lote` con `CliRunner`, comparando las filas de la tabla (`table_rows`, como en `test_batch.py`);
- `lote` con un archivo que falta: código 1, el error en `stderr` y la línea del total.

Al menos uno debe matar un mutante que **sobreviva** a los tests del bootcamp. Una pista: `UNIT` en la media, con tu unidad.

Para la tabla, cambia de carpeta con `monkeypatch.chdir(tmp_path)` y pasa nombres cortos. Sin terminal, Rich tiene 80 columnas, y una ruta larga de `tmp_path` partiría la celda en dos líneas. Al final, al menos 503 tests en verde.

### 15. Contenedor, README y pull request

```bash
docker compose run --build --rm app
docker compose run --rm app observatorio lote medidas.csv medidas.txt
docker compose run --rm app observatorio lote --procesos medidas.csv medidas.txt
```

Los tests en verde, y la misma tabla con hilos y con procesos. Los procesos funcionan igual dentro del contenedor.

En el `README.md` de tu repositorio, añade `lote` a la lista de comandos, con `-t` y `--procesos`.

Commits sugeridos, en este orden:

1. `test: add batch tests`
2. `feat: add FileReport and the batch api skeleton`
3. `feat: summarize one file with report_file`
4. `feat: summarize files with a thread pool`
5. `feat: summarize files with a process pool`
6. `feat: add lote command`
7. `feat: add --trabajadores and --procesos to lote`
8. `chore: bump version to 0.16.0`
9. `test: add my batch tests`

Al final:

```bash
git push -u origin week-16
```

En GitHub, abre un *pull request* de `week-16` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy`, `uv run ruff check` y `uv run coverage report`.
2. La tabla de tiempos del paso 11, los dos tiempos sin GIL del paso 12, y tu explicación de los resultados.
3. La tabla de mutantes del paso 13, y el mutante que mata tu test del paso 14.
4. Por qué `report_files` no necesita ningún `Lock`, y por qué usa `map` y no `as_completed`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'FileReport' from 'observatorio.core'` | Falta `core/batch.py`, o no importas sus nombres en `core/__init__.py` |
| `ImportError: cannot import name 'batch' from 'observatorio.core'` | Lo mismo: el módulo se tiene que llamar `batch.py` y vivir en `core/` |
| `test_report_file_turns_a_missing_file_into_an_error` falla con una traza de `DataFileError` | `report_file` deja escapar la excepción: captúrala y devuelve `FileReport(path, error=str(problem))` |
| `test_report_files_keeps_the_order_of_the_paths` falla | Usas `as_completed`, o recoges los resultados en el orden en que terminan: usa `pool.map` |
| `test_report_files_runs_the_tasks_at_the_same_time` falla con `BrokenBarrierError` | Las tareas no corren a la vez: ¿pasas `max_workers=workers` al *pool*? ¿Recoges cada resultado antes de enviar la siguiente tarea? |
| `test_workers_limit_the_tasks_at_the_same_time` falla con `assert 4 == 1` | El *pool* ignora `workers`: revisa `max_workers` |
| mypy: `Incompatible types in assignment (expression has type "ThreadPoolExecutor", variable has type "ProcessPoolExecutor")` | Anota la variable: `pool: Executor` antes del `if` |
| `PicklingError` con `--procesos` | La función que envías al *pool* no está a nivel de módulo: tiene que ser `report_file`, no una `lambda` ni una función anidada |
| `Missing argument 'ARCHIVOS'.` | `lote` necesita al menos un archivo |
| La tabla de tus tests sale con celdas partidas | Las rutas son demasiado largas para 80 columnas: `monkeypatch.chdir(tmp_path)` y nombres cortos |
| `uv run --python 3.14.10t` reinstala tu `.venv` | Te falta `UV_PROJECT_ENVIRONMENT=.venv-ft` delante: sin él, uv cambia el Python de tu entorno principal. Vuelve con `uv sync` |

## Entrega

- Rama `week-16` de `python-<nombre>-<apellido>` con:
  - `core/batch.py` con `FileReport`, `report_file` y `report_files` (hilos y procesos), exportados desde `core`;
  - el comando `lote` con `--trabajadores` y `--procesos`, y la constante `WORKERS`;
  - la versión `0.16.0` y al menos 6 tests propios en `tests/test_my_batch.py`.

  Todo en verde, también en Docker y con el Python sin GIL, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
- `README.md` del repositorio con el comando `lote`.
- *Pull request* `week-16` → `main` con la descripción del paso 15.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · concurrent.futures](../2-practicas/ejercicio-04-concurrent-futures/README.md) | **Proyecto · Observatorio, capa 15** | [Webgrafía](../4-recursos/webgrafia/README.md) |
