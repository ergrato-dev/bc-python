# Proyecto — Observatorio, capa 16: medidas en directo

⏱️ 6 h 30 min · Capa 16 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Hasta ahora, tus archivos están completos antes de leerlos. Una estación de verdad no funciona así: manda una medida cada pocos segundos, y quieres verla **en cuanto llega**, de todas las estaciones a la vez. Esta semana añades el comando `vigilar`, que reproduce varios archivos como si sus medidas llegaran en directo, con una pausa entre una y otra. Al final, escribe la misma tabla que `lote`:

```
$ uv run observatorio vigilar -i 0.2 medidas.csv medidas.txt falta.csv
medidas.csv · Norte: 12.5 unidad medio
medidas.txt · Norte: 12.5 unidad medio
medidas.csv · Sur: 8.0 unidad bajo
medidas.txt · Sur: 8.0 unidad bajo
medidas.csv · Centro: sin dato
medidas.txt · Centro: sin dato
...
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
| `--intervalo S`, `-i S` | Segundos entre dos medidas de un mismo archivo; por defecto, `INTERVAL = 0.5` |
| `--limite N`, `-l N` | Cuántos archivos se vigilan a la vez; por defecto, `WORKERS = 4` |
| `--tiempo SEGUNDOS` | Para a los SEGUNDOS indicados con `tiempo agotado` y código 1 |

Todo pasa en **un solo hilo**, con `asyncio`. Mientras un archivo espera su próxima medida, los demás avanzan. Las medidas de un mismo archivo salen en orden; las de archivos distintos, intercaladas.

La lógica va en un módulo nuevo de `core/`, que solo tiene corrutinas: no arranca el bucle ni escribe en la terminal.

```
src/observatorio/
├── cli.py          # + INTERVAL, show_reports, show_reading y el comando vigilar
└── core/
    ├── __init__.py # + replay, watch_file y watch_files
    ├── batch.py    # + FileReport.from_series
    └── live.py     # nuevo: replay, watch_file y watch_files
tests/
├── test_live.py       # nuevo: los tests del bootcamp
├── test_my_live.py    # nuevo: los tuyos
└── test_package.py    # modificado: el módulo live, la API y la versión 0.17.0
```

La semana 18 cambiará los archivos por peticiones HTTP a estaciones de verdad. El código asíncrono que escribes ahora es el que hará falta entonces.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-17`. El `starter/` trae la capa 15 resuelta. **Tú** escribes `core/live.py` y el comando `vigilar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-16` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-17
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-17-asyncio_corrutinas_tareas_y_colas/3-proyecto/starter
cp $STARTER/tests/test_live.py $STARTER/tests/test_my_live.py $STARTER/tests/test_package.py tests/
sed -i 's/week-16/week-17/' compose.yaml
git status --short
```

Copias estos archivos:

- **Nuevos:**
  - `tests/test_live.py`, con 37 tests de `live.py`, de `FileReport.from_series` y del comando `vigilar`;
  - `tests/test_my_live.py`, con un ejemplo.
- **Modificado:** `test_package.py`, que espera el módulo `live`, sus tres nombres en la API de `core` y la versión `0.17.0`.

No hay dependencias nuevas: `asyncio` es parte de Python.

### 3. Tests en rojo

```bash
uv run pytest
```

```
E   ImportError: cannot import name 'live' from 'observatorio.core' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Lee `tests/test_live.py` antes de escribir nada. Fíjate en tres cosas (teoría 05):

- cada test es una función **normal** que arranca el bucle con `asyncio.run`: pytest no ejecuta funciones `async def` sin un plugin;
- las tareas falsas ceden el turno con `asyncio.sleep(0)` o se esperan con una `asyncio.Barrier`. Ningún test mide cuánto se tarda, salvo el de `--tiempo`, que da 0,1 s a un trabajo de varios segundos;
- `monkeypatch.setattr(live, "watch_file", ...)` cambia la función que llama `watch_files`. Funciona porque `watch_files` la busca por su nombre en el módulo cada vez que la llama.

### 4. El esqueleto: `live.py` y la API

Crea `src/observatorio/core/live.py` con un *docstring* de módulo (qué, para qué, impacto) y:

```python
# Lo que recibe cada medida en cuanto llega: el archivo y la medida.
OnReading = Callable[[Path, Measurement], None]


async def replay(lines: Iterable[str], *, interval: float = 0.0) -> AsyncIterator[Measurement]:
    """Da las medidas válidas de `lines`, esperando `interval` segundos antes de cada una."""
    raise NotImplementedError
    yield  # Nunca se ejecuta, pero hace de replay un generador asíncrono.


async def watch_file(
    path: Path, *, interval: float = 0.0, on_reading: OnReading | None = None
) -> FileReport:
    """Lee un archivo, reproduce sus medidas y lo resume. Un DataFileError queda en `error`."""
    raise NotImplementedError


async def watch_files(
    paths: Iterable[Path],
    *,
    interval: float = 0.0,
    limit: int = 4,
    on_reading: OnReading | None = None,
) -> list[FileReport]:
    """Vigila los archivos a la vez, como mucho `limit` cada vez, en el orden de `paths`."""
    raise NotImplementedError
```

`OnReading` es un **alias de tipo** (semana 4): una función que recibe la ruta y la medida, y no devuelve nada. `watch_file` la llama con cada medida en cuanto llega. Así `core` avisa de cada medida sin saber qué se hace con ella: la CLI la escribirá, y la API de la semana 20 podría enviarla a un navegador.

El `yield` que nunca se ejecuta parece raro, pero importa: una función `async def` con un `yield` es un **generador asíncrono**, y sin él sería una corrutina normal. Lo borrarás en el paso 6.

En `core/__init__.py`, importa los tres nombres de `observatorio.core.live` y añádelos a `__all__`. `uv run ruff check --fix` los ordena.

```
30 failed, 429 passed
```

### 5. Un refactor: `FileReport.from_series`

`watch_file` tiene que resumir una serie igual que `report_file`. En lugar de copiar las tres líneas, sácalas a un método de clase de `FileReport` en `batch.py`:

```python
    @classmethod
    def from_series(cls, path: Path, series: Series) -> FileReport:
        """El resumen de una serie ya leída: lo comparten `report_file` y `watch_file`."""
```

`measurements`, `with_value` y `mean` se calculan como en la semana 16. Después, `report_file` termina en una línea:

```python
    return FileReport.from_series(path, Series.from_lines(lines))
```

Los 31 tests de `test_batch.py` siguen en verde: has cambiado cómo está escrito, no qué hace.

```
28 failed, 431 passed
```

### 6. `replay`, un generador asíncrono

Recorre las medidas con `iter_measurements(lines)` (semana 11), que ya se salta la cabecera, las líneas vacías y las inválidas. Antes de cada medida, `await asyncio.sleep(interval)`, y después, `yield measurement`.

```bash
uv run pytest
```

```
24 failed, 435 passed
```

La espera va **antes** de cada medida, no después: así la primera también se hace esperar, como si llegara de lejos. Y es `asyncio.sleep`, no `time.sleep`. `test_replay_lets_other_tasks_run` lo comprueba: dos reproducciones a la vez se tienen que turnar, `A1, B1, A2, B2...`. Con `time.sleep`, la primera iría entera antes que la segunda (ejercicio 01, paso 6). Incluso con `interval=0`, `asyncio.sleep(0)` cede el turno.

### 7. `watch_file`

Cuatro partes:

1. Lee las líneas **en otro hilo**: `lines = await asyncio.to_thread(open_file(path).lines)`. Fíjate en que pasas el método `lines` sin llamarlo, sin paréntesis: `to_thread` lo llamará en el hilo (ejercicio 01, paso 7).
2. Un `DataFileError` al leer: devuelve `FileReport(path, error=str(problem))`, sin lanzar nada.
3. Recorre `replay(lines, interval=interval)` con `async for`: añade cada medida a una `Series()` vacía con `series.add`, y, si `on_reading` no es `None`, llámala con `(path, measurement)`.
4. Devuelve `FileReport.from_series(path, series)`.

¿Por qué `to_thread`, si leer un archivo pequeño es tan rápido? Porque mientras el disco responde, el bucle entero se para: ninguna otra estación avanza. Con un archivo local de siete líneas no se nota; con uno en un disco de red, sí. `test_watch_file_reads_the_disk_in_another_thread` lo comprueba con un espía.

```
17 failed, 442 passed
```

### 8. `watch_files` con `TaskGroup` y `Semaphore`

```python
    semaphore = asyncio.Semaphore(limit)

    async def guarded(path: Path) -> FileReport:
        async with semaphore:
            return await watch_file(path, interval=interval, on_reading=on_reading)

    # TaskGroup espera a todas las tareas al salir del bloque; si una falla, cancela el resto.
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(guarded(path)) for path in paths]
    return [task.result() for task in tasks]
```

Tres decisiones:

- **Una tarea por archivo, un semáforo para todas**: las tareas se crean todas a la vez, pero solo `limit` pasan del `async with semaphore:`. El resto espera su turno sin bloquear nada (ejercicio 03, paso 1).
- **`TaskGroup`, no `gather`**: si `watch_file` tiene un bug y lanza otra excepción, el grupo cancela las demás tareas y la relanza como `ExceptionGroup` (ejercicio 02, paso 2). Un archivo que falta no es un bug: `watch_file` ya lo convirtió en un `FileReport` con `error`.
- **`task.result()` en el orden de la lista**: la tabla sale en el orden de los argumentos, aunque un archivo corto termine antes.

`guarded` es una función anidada, y aquí no hay problema: con `asyncio` nada viaja a otro proceso, así que no hace falta `pickle` (semana 16).

```
9 failed, 450 passed
```

### 9. El comando `vigilar`

Primero, un refactor en `cli.py`: los pasos 2 a 5 del cuerpo de `lote` (errores, tabla, total y código 1) van a una función, porque `vigilar` hará lo mismo:

```python
def show_reports(reports: list[FileReport]) -> None:
    """Los errores a stderr, la tabla de los archivos leídos y el total; código 1 si falló alguno."""
```

`lote` queda en una línea: `show_reports(report_files(archivos, workers=trabajadores, processes=procesos))`. Los tests de `lote` siguen en verde.

Después, la función que escribe cada medida en cuanto llega:

```python
def show_reading(path: Path, measurement: Measurement) -> None:
    """Una línea por medida en cuanto llega: archivo, etiqueta, valor y nivel con su color."""
```

Construye un `Text(f"{path} · {measurement.label}: ")` de Rich y añádele con `append`:

- `sin dato`, si la medida no tiene valor;
- si lo tiene, `f"{measurement.value:.1f} {UNIT} "` y el nivel `SCALE.level(...)` con su estilo de `STYLES`.

Escríbelo con `out.print(line)`. `show_reading` encaja en `OnReading`: recibe una ruta y una medida.

Y el comando, de momento con el argumento y `--intervalo`:

```python
# Segundos entre dos medidas de un mismo archivo en `vigilar`, si no se dice con --intervalo.
INTERVAL = 0.5
```

- `archivos: list[Path]`, igual que en `lote`, con `help="Los .txt o .csv que se vigilan."`;
- `intervalo: float`, con `typer.Option("--intervalo", "-i", min=0, help=...)` y valor por defecto `INTERVAL`.

El cuerpo arranca el bucle y le pasa la corrutina:

```python
    reports = asyncio.run(watch_files(archivos, interval=intervalo, on_reading=show_reading))
    show_reports(reports)
```

`vigilar` es una función **normal**, no `async def`: Typer llama a sus comandos como funciones normales. `asyncio.run` es la frontera entre los dos mundos, y está **aquí**, en la CLI, no en `core`. `test_live_does_not_start_the_loop_nor_touch_the_terminal` lo comprueba.

```bash
uv run observatorio vigilar -i 0.2 medidas.csv medidas.txt falta.csv; echo $?
uv run pytest
```

```
...
archivos: 3 · con error: 1
1
...
3 failed, 456 passed
```

### 10. `--limite` y `--tiempo`

Dos opciones más:

- `limite: int`, con `typer.Option("--limite", "-l", min=1, help=...)` y valor por defecto `WORKERS`, que pasas como `limit=limite`;
- `tiempo: float | None`, con `typer.Option("--tiempo", min=0, metavar="SEGUNDOS", help=...)` y valor por defecto `None`.

Para el tiempo, el bucle necesita una corrutina que envuelva la espera en un `asyncio.timeout` (ejercicio 02, paso 4):

```python
    async def watch() -> list[FileReport]:
        # timeout(None) no pone límite: la misma línea sirve con y sin --tiempo.
        async with asyncio.timeout(tiempo):
            return await watch_files(
                archivos, interval=intervalo, limit=limite, on_reading=show_reading
            )

    try:
        reports = asyncio.run(watch())
    except TimeoutError:
        raise fail(f"tiempo agotado a los {tiempo:g} s", 1) from None
    show_reports(reports)
```

Cuando se acaba el tiempo, `timeout` cancela `watch_files`. El `TaskGroup` cancela a su vez cada tarea, y `asyncio.run` termina con un `TimeoutError`. Las medidas que ya salieron, ahí siguen; la tabla no sale, porque ningún archivo terminó. `from None` evita que el error de Typer arrastre la traza del `TimeoutError`.

```bash
uv run observatorio vigilar --help
uv run observatorio vigilar -i 1 --tiempo 2.5 medidas.csv; echo $?
```

```
medidas.csv · Norte: 12.5 unidad medio
medidas.csv · Sur: 8.0 unidad bajo
error: tiempo agotado a los 2.5 s
1
```

```
1 failed, 458 passed
```

Y con Ctrl+C a medio vigilar: `asyncio.run` cancela las tareas, cierra el bucle y vuelve a lanzar el `KeyboardInterrupt`. El programa termina sin traza, con código 130 (`echo $?`), el código de "interrumpido por el usuario". Pruébalo.

### 11. La versión

```bash
uv version --bump minor
uv run observatorio --version
uv run pytest
```

```
observatorio 0.17.0
...
459 passed
```

### 12. Medir

¿Cuánto ganas vigilando a la vez? Cada copia de `medidas.csv` tiene 7 medidas: con `-i 0.2`, un archivo tarda 1,4 s. Crea seis copias y mide:

```bash
mkdir -p /tmp/vigilar
for i in $(seq 6); do cp medidas.csv /tmp/vigilar/m$i.csv; done
time uv run observatorio informe -f medidas.csv > /dev/null
time uv run observatorio vigilar -i 0.2 -l 1 /tmp/vigilar/m{1,2,3}.csv > /dev/null
time uv run observatorio vigilar -i 0.2 /tmp/vigilar/m{1,2,3}.csv > /dev/null
time uv run observatorio vigilar -i 0.2 -l 2 /tmp/vigilar/m*.csv > /dev/null
time uv run observatorio vigilar -i 0.2 -l 6 /tmp/vigilar/m*.csv > /dev/null
```

Apunta el tiempo **real** de cada uno. En la máquina del bootcamp:

| Orden | Tiempo | Cuentas |
|---|---|---|
| `informe` (arrancar Python y la CLI) | 0,9 s | |
| 3 archivos, `-l 1` | 4,9 s | 0,8 + 3 × 1,4 |
| 3 archivos, `-l 4` | 2,1 s | 0,8 + 1,4 |
| 6 archivos, `-l 2` | 4,9 s | 0,8 + 3 tandas × 1,4 |
| 6 archivos, `-l 6` | 2,1 s | 0,8 + 1,4 |

Esta vez los números salen **exactos**: el programa casi no calcula, todo es espera, y las esperas se solapan perfectamente. Con `-l 6`, seis archivos tardan lo mismo que uno, y en **un solo hilo**. La semana 16 necesitaba un hilo por archivo para conseguirlo; aquí cada estación es una tarea, que ocupa unos pocos kilobytes. Podrías vigilar mil.

Compara con la semana 16: allí, con archivos que no hacían esperar, la concurrencia casi no ganaba nada. Aquí la espera es lo único que hay. `asyncio` brilla exactamente en este caso: muchas cosas que esperan.

### 13. Calidad, cobertura y una prueba de mutación

```bash
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
```

`live.py` debe salir al 100 %.

Ahora la prueba de mutación. Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `live.py` | `await asyncio.sleep(interval)` por `time.sleep(interval)` (con `import time`) | |
| `live.py` | `await asyncio.to_thread(open_file(path).lines)` por `open_file(path).lines()` | |
| `live.py` | `asyncio.Semaphore(limit)` por `asyncio.Semaphore(4)` | |
| `live.py` | `replay(lines, interval=interval)` por `replay(lines)` | |
| `live.py` | el `TaskGroup` por `return [await guarded(path) for path in paths]` | |
| `live.py` | el `TaskGroup` por `asyncio.gather(..., return_exceptions=True)` | |
| `cli.py` | `asyncio.timeout(tiempo)` por `asyncio.timeout(None)` | |
| `cli.py` | `line.append(level, style=STYLES.get(level, ""))` por `line.append(level)` | |

Siete mueren. Uno **sobrevive**: ¿cuál, y por qué ningún test del bootcamp lo ve? Lo vas a matar en el paso siguiente.

### 14. Tus tests

En `tests/test_my_live.py`, sustituye el ejemplo por **al menos 6 tests** con archivos de **tu dominio** en `tmp_path`, cada uno con su `asyncio.run`:

- `replay` con líneas de tu dominio: las medidas válidas, en orden;
- `watch_file` de un archivo válido: el mismo `FileReport` que `report_file`;
- `watch_file` de un archivo que falta o con la cabecera mala;
- `watch_files` con varios archivos: el orden de entrada;
- `vigilar` con `CliRunner` y `-i 0`: una línea por medida y las filas de la tabla;
- el mutante que sobrevivió en el paso 13.

Para el último, mira cómo prueba `test_cli.py` los colores de la tabla (`test_table_colors_each_level`): una `Console` que finge ser una terminal y graba lo que escribe. Cambia `cli.out` por ella con `monkeypatch.setattr` y llama a `cli.show_reading` directamente.

Al final, al menos 546 tests en verde.

### 15. Contenedor, README y pull request

```bash
docker compose run --build --rm app
docker compose run --rm app observatorio vigilar -i 0.2 medidas.csv medidas.txt
```

`docker compose run` te da una terminal: las medidas salen con color, una a una, como en tu máquina.

En el `README.md` de tu repositorio, añade `vigilar` a la lista de comandos, con `-i`, `-l` y `--tiempo`.

Commits sugeridos, en este orden:

1. `test: add live tests`
2. `feat: add the live api skeleton`
3. `refactor: extract FileReport.from_series`
4. `feat: replay measurements with an async generator`
5. `feat: watch one file without blocking the loop`
6. `feat: watch files with a task group and a semaphore`
7. `feat: add vigilar command`
8. `feat: add --limite and --tiempo to vigilar`
9. `chore: bump version to 0.17.0`
10. `test: add my live tests`

Al final:

```bash
git push -u origin week-17
```

En GitHub, abre un *pull request* de `week-17` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy`, `uv run ruff check` y `uv run coverage report`.
2. La tabla de tiempos del paso 12, con tus cuentas.
3. La tabla de mutantes del paso 13, y el test con el que mataste al superviviente.
4. Por qué `asyncio.run` está en `cli.py` y no en `core`, y por qué `watch_files` usa `TaskGroup` y no `gather`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'live' from 'observatorio.core'` | Falta `core/live.py`, o no lo importas en `core/__init__.py` |
| `test_replay_is_an_async_generator` falla | Tu `replay` no tiene `yield`: sin él, es una corrutina normal |
| `TypeError: 'async for' requires an object with __aiter__ method, got coroutine` | Lo mismo: recorres con `async for` una función `async def` sin `yield` |
| `RuntimeWarning: coroutine 'watch_files' was never awaited` | Llamaste a `watch_files(...)` sin `asyncio.run` ni `await` |
| `test_replay_lets_other_tasks_run` da `['A1', 'A2', 'A3', 'B1', ...]` | Usas `time.sleep`, o no esperas nada en el bucle de `replay`: tiene que ser `await asyncio.sleep(interval)` |
| `test_watch_file_reads_the_disk_in_another_thread` da `assert 0 == 1` | Lees el archivo directamente: `await asyncio.to_thread(open_file(path).lines)` |
| `TypeError: 'list' object is not callable` en `to_thread` | Escribiste `open_file(path).lines()`, con paréntesis: `to_thread` necesita la función, no su resultado |
| `test_limit_caps_the_files_at_the_same_time` da `assert 6 == 1` | El `await watch_file(...)` está fuera del `async with semaphore:` |
| `test_watch_files_runs_the_files_at_the_same_time` falla con `TimeoutError` | Las tareas van una detrás de otra: créalas todas con `group.create_task` antes de esperar ninguna |
| Una prueba se queda colgada | Un `await` espera algo que nunca llega. Ctrl+C y ejecuta ese test solo con `-x -q` para ver dónde |
| `vigilar` tarda segundos en los tests | Te falta `-i 0`: sin él, cada medida espera `INTERVAL` |

## Entrega

- Rama `week-17` de `python-<nombre>-<apellido>` con:
  - `core/live.py` con `replay`, `watch_file` y `watch_files`, exportados desde `core`, y `FileReport.from_series` en `batch.py`;
  - el comando `vigilar` con `--intervalo`, `--limite` y `--tiempo`, la constante `INTERVAL` y `show_reports` compartido con `lote`;
  - la versión `0.17.0` y al menos 6 tests propios en `tests/test_my_live.py`.

  Todo en verde, también en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
- `README.md` del repositorio con el comando `vigilar`.
- *Pull request* `week-17` → `main` con la descripción del paso 15.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Iteradores y gestores asíncronos](../2-practicas/ejercicio-04-iteradores-y-gestores-asincronos/README.md) | **Proyecto · Observatorio, capa 16** | [Webgrafía](../4-recursos/webgrafia/README.md) |
