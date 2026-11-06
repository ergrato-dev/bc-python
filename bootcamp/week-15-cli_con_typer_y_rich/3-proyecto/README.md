# Proyecto — Observatorio, capa 14: la CLI con Typer y Rich

⏱️ 6 h 30 min · Capa 14 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana y cierre de la fase 2.**

## Qué construyes

Desde la semana 3, tu `main` lee `sys.argv` con un `match` que ha ido creciendo: `-h`, `-V`, `-f`, `-j`, `-v`... Esta semana lo sustituyes por una aplicación **Typer** con dos comandos, y el informe pasa a ser una tabla de **Rich**:

```
$ uv run observatorio informe -f medidas.csv -e escala.json
error: línea 7: 'Sur 9,5'
               Medidas
┏━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Etiqueta  ┃       Valor ┃ Nivel    ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Norte     │ 12.5 unidad │ medio    │
│ Sur       │  8.0 unidad │ bajo     │
│ Centro    │    sin dato │ sin dato │
│ Oriente   │ 55.1 unidad │ alto     │
│ Occidente │ 61.0 unidad │ alto     │
│ Norte     │ 48.9 unidad │ medio    │
│ Sur       │  9.5 unidad │ bajo     │
└───────────┴─────────────┴──────────┘
registros: 7 | bajo: 2 | medio: 2 | alto: 2 | sin dato: 1
racha más larga en alto: 2
en alto: 28.6 %
etiquetas distintas: 5
medias más altas: Occidente 61.0, Oriente 55.1, Norte 30.7
más frecuentes: Norte 2, Sur 2, Centro 1
mediana: 30.7 unidad
media móvil (3): 25.2 · 41.4 · 55.0 · 39.8
mayor salto: +47.1 unidad
```

En tu terminal, los niveles salen en color: `bajo` en cian, `medio` en verde y `alto` en rojo.

| Antes (`__main__.py`) | Ahora (`cli.py`) |
|---|---|
| `observatorio "Norte;12,5"` | `observatorio informe "Norte;12,5"` |
| `observatorio < medidas.txt` | `observatorio informe < medidas.txt` |
| `observatorio -f medidas.csv -j resumen.json` | `observatorio informe -f medidas.csv -j resumen.json`, y también al revés |
| — | `observatorio informe -f medidas.csv -e escala.json`: la escala de un JSON, con `read_scale` (semana 13) |
| — | `observatorio validar medidas.json`: valida con Pydantic, con `read_measurements` (semana 13) |
| `observatorio -v ...`, `observatorio --version` | Igual: opciones del callback |
| `observatorio -h`, `USAGE` | `observatorio --help`, generado por Typer |

Los códigos de salida no cambian: `0` si todo va bien, `1` si hay líneas con errores, `2` si la llamada está mal o un archivo no se puede leer. `read_scale` y `read_measurements` existían desde la semana 13, pero ningún comando los usaba.

```
src/observatorio/
├── __main__.py   # tres líneas: python -m observatorio llama a cli.app
├── cli.py        # nuevo: la aplicación Typer, las consolas de Rich y las constantes de tu dominio
└── core/         # sin cambios
tests/
├── test_cli.py      # nuevo: los tests del bootcamp, con CliRunner
├── test_my_cli.py   # nuevo: los tuyos
└── test_main.py     # se borra: probaba la CLI vieja
```

`core/` no cambia. Es la prueba de que la separación de las semanas 3 y 8 funcionaba: cambia toda la interfaz, y la lógica ni se entera.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-15`. El `starter/` trae la capa 13 resuelta. **Tú** añades las dependencias, escribes `cli.py` comando a comando y adaptas `__main__.py`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-14` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-15
```

### 2. Copia los archivos nuevos y borra el viejo

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-15-cli_con_typer_y_rich/3-proyecto/starter
cp $STARTER/tests/test_cli.py $STARTER/tests/test_my_cli.py tests/
cp $STARTER/tests/test_package.py $STARTER/tests/test_quality.py tests/
cp $STARTER/tests/test_sources.py $STARTER/tests/test_model.py tests/
sed -i 's/week-14/week-15/' compose.yaml
git rm -q tests/test_main.py
git status --short
```

Copias estos archivos:

- **Nuevos:**
  - `tests/test_cli.py`, con 28 tests de la CLI nueva;
  - `tests/test_my_cli.py`, con un ejemplo.
- **Modificados:** los tests que llamaban a la CLI vieja ahora usan `CliRunner` con la nueva:
  - `test_quality.py`: 5 tests;
  - `test_sources.py`: 1 test;
  - `test_package.py`: la versión `0.15.0`, las tres dependencias y `[project.scripts]`;
  - `test_model.py`: pierde el test de `SCALE` en `__main__`, que pasa a `test_cli.py`.

`test_main.py` se borra con `git rm`: probaba `main(argv)`, que desaparece. Sus casos siguen en `test_cli.py`, escritos para los comandos nuevos.

Si **tus** tests de semanas anteriores (`test_my_*.py`) llaman a `main` de `__main__.py`, apúntalos: los pasarás a `CliRunner` en el paso 14.

### 3. Tests en rojo

```bash
uv run pytest
```

```
E   ModuleNotFoundError: No module named 'typer'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Lee `tests/test_cli.py` antes de escribir nada: es la especificación de la CLI. Cada test dice qué comando se ejecuta, con qué argumentos, y qué esperar en `stdout`, en `stderr` y en `exit_code`.

### 4. Las dependencias

```bash
uv add typer==0.27.3 rich==15.0.0
```

Van en `dependencies`, no en `dev`: el programa las necesita para funcionar. Typer ya depende de Rich, pero tu código importa Rich directamente, así que la fijas tú. Si mañana Typer dejara de traerla, tu programa seguiría funcionando. Mira el árbol con `uv tree --depth 2`.

```
E   ImportError: cannot import name 'cli' from 'observatorio' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

### 5. El esqueleto: `cli.py`, `[project.scripts]` y `__main__.py`

Crea `src/observatorio/cli.py` con:

- un *docstring* de módulo: qué, para qué, impacto;
- tus constantes **de `__main__.py`**: `UNIT`, `LOW`, `HIGH`, `SCALE`, `TOP` y `WINDOW`. Muévelas tal cual, con tu unidad y tus umbrales;
- la aplicación y las consolas;
- `show_version` y el callback, por ahora solo con `--version`.

```python
app = typer.Typer(
    help="Observatorio de datos de mi dominio.",
    no_args_is_help=True,
    add_completion=False,
)
# Dos consolas: el resultado va a stdout y los errores a stderr, como en la semana 3.
out = Console()
err = Console(stderr=True)


def show_version(value: bool) -> None:
    """Con --version, escribe la versión y termina antes de mirar nada más."""
    if value:
        out.print(f"observatorio {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version", "-V", callback=show_version, is_eager=True,
            help="Muestra la versión y termina.",
        ),
    ] = False,
) -> None:
    """Observatorio de datos de mi dominio."""
```

En `pyproject.toml`, apunta el comando a la aplicación:

```toml
[project.scripts]
# `uv run observatorio` ejecuta la aplicación Typer `app` de src/observatorio/cli.py.
observatorio = "observatorio.cli:app"
```

Y sustituye **todo** `__main__.py` por:

```python
"""`python -m observatorio ...` hace lo mismo que el comando `observatorio ...`."""

from observatorio.cli import app

if __name__ == "__main__":
    app(prog_name="observatorio")
```

Antes de borrarlo, guarda una copia de tu `main` viejo (`git show main:src/observatorio/__main__.py`): los pasos siguientes trasladan su lógica a los comandos.

```bash
uv sync
uv run observatorio --version
uv run pytest
```

```
observatorio 0.14.0
...
30 failed, 359 passed
```

`uv sync` vuelve a generar el ejecutable `observatorio` con la tabla nueva.

### 6. El comando `informe`, con líneas

Escribe `table_of(series, scale) -> Table` y el comando `informe`, de momento solo con el argumento `lineas` (`list[str] | None`, `metavar="LINEAS"`).

**`table_of`** devuelve una tabla de título `Medidas` con tres columnas (`Etiqueta`, `Valor` alineada a la derecha y `Nivel`) y una fila por medida de la serie:

- el valor, `f"{value:.1f} {scale.unit}"`, o `sin dato`;
- el nivel, `scale.level(value)`, como `Text(level, style=STYLES.get(level, ""))`, con `STYLES = {"bajo": "cyan", "medio": "green", "alto": "bold red"}`.

**`informe`** hace lo que hacía tu `main` con las líneas, en este orden:

1. `process_lines(lines, scale.unit, scale.low, scale.high)` y cada error con `err.print(f"error: {error}")`;
2. `out.print(table_of(series, scale))`;
3. el resumen como texto, en `out`. Fíjate en las dos líneas que cambian de formato:

```
medias más altas: Occidente 61.0, Oriente 55.1, Norte 30.7
más frecuentes: Norte 2, Sur 2, Centro 1
```

4. si hubo errores, `raise typer.Exit(1)`.

Usa una variable `scale = SCALE` dentro del comando, y no `SCALE` directamente: en el paso 9 vendrá de `--escala`.

```bash
uv run observatorio informe "Norte;12,5" "Oriente;55,1" "malo"
uv run pytest
```

```
22 failed, 367 passed
```

### 7. stdin, `--archivo` y los errores de archivo

Añade `archivo: Path | None`, con `typer.Option("--archivo", "-f", help=...)`, y elige la fuente como en la teoría 03: el archivo con `open_file`, las líneas con `LinesSource`, o `sys.stdin`.

Tres errores:

- **Líneas y archivo a la vez**: `raise typer.BadParameter("usa líneas o --archivo, no los dos", param_hint="LINEAS")`. Código 2, y Typer añade `Usage:`.
- **`DataFileError` al leer**: escribe `error: <mensaje>` en `err` y termina con código 2. Escribe una función `fail(message, code) -> typer.Exit` que haga las dos cosas y **devuelva** la excepción, y en el comando: `raise fail(str(problem), 2) from problem`.
- **Líneas inválidas**: como en el paso 6, código 1.

```bash
uv run observatorio informe -f medidas.csv
uv run observatorio informe < medidas.txt
uv run observatorio informe -f no-existe.csv; echo $?
uv run pytest
```

```
error: no existe el archivo no-existe.csv
2
...
16 failed, 373 passed
```

### 8. `--json`

Añade `json_path: Path | None` con `typer.Option("--json", "-j", ...)`. Al final del comando, como hacía `main`: `write_json(summary_data(series.records), json_path)`, `resumen guardado en <ruta>` en `out`, y un `DataFileError` al escribir da código 2 con `fail`.

Ahora `-j` ya no tiene que ir detrás de `-f`: Typer acepta las opciones en cualquier orden, y también con líneas o con stdin.

```
14 failed, 375 passed
```

### 9. `--escala`

Añade `escala: Path | None` con `typer.Option("--escala", "-e", ...)`. Si llega, `scale = read_scale(escala)`. Ponlo **dentro** del mismo `try` que lee las líneas: una escala imposible (`low` mayor que `high`) ya da un `DataFileError` desde la semana 13.

```bash
uv run observatorio informe -f medidas.csv -e escala.json
```

```
11 failed, 378 passed
```

### 10. El comando `validar`

```python
@app.command()
def validar(
    ruta: Annotated[Path, typer.Argument(help="Un JSON con una lista de medidas.")],
) -> None:
    """Comprueba un JSON de medidas con Pydantic sin escribir el informe."""
```

Lee con `read_measurements(ruta)` y escribe `<ruta>: <n> medidas válidas`. Un `DataFileError` da código 2 con `fail`.

```bash
uv run observatorio validar medidas.json
uv run observatorio --help
```

```
medidas.json: 7 medidas válidas
```

La ayuda enumera ya los dos comandos con la primera línea de su *docstring*.

```
9 failed, 380 passed
```

### 11. `-v`

Añade al callback la opción `verbose`, `typer.Option("--verbose", "-v", help=...)`, y lleva a su cuerpo el `logging.basicConfig` de tu `main` de la semana 14. Es el principio del programa, el único sitio que configura el registro.

```bash
uv run observatorio -v informe -f medidas.csv > /dev/null
```

```
DEBUG observatorio.core.storage: 9 líneas leídas de medidas.csv
error: línea 7: 'Sur 9,5'
DEBUG observatorio.core.groups: línea ignorada: 'Sur 9,5'
```

`-v` va **antes** del comando: es del callback.

```
6 failed, 383 passed
```

### 12. Los corchetes y el ancho

Quedan 5 fallos que no son de lógica, sino de Rich:

```bash
uv run pytest -x tests/test_cli.py -k brackets
```

```
E       AssertionError: assert 'Sala [b]' in '             Medidas ...más frecuentes: Sala  1\nmediana: 12.0 unidad...'
```

Una estación llamada `Sala [b]` pierde su `[b]`: Rich lo toma por "negrita" (teoría 04). Los otros cuatro fallos son mensajes con rutas largas que Rich **corta** en dos líneas, porque sin terminal el ancho es 80.

Las dos consolas, con tres opciones:

```python
# markup=False: Rich no interpreta los corchetes de los datos ("Sala [b]") como estilos.
# highlight=False: no colorea por su cuenta los números y las rutas.
# soft_wrap=True: no corta las líneas largas al ancho de la terminal (80 sin terminal).
out = Console(markup=False, highlight=False, soft_wrap=True)
err = Console(stderr=True, markup=False, highlight=False, soft_wrap=True)
```

```
1 failed, 388 passed
```

### 13. La versión

```bash
uv version --bump minor
uv run observatorio --version
uv run pytest
```

```
observatorio 0.15.0
...
389 passed
```

### 14. Calidad, cobertura y una prueba de mutación

```bash
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
```

mypy estricto comprueba también tus comandos: los `Annotated` son tipos normales para él. En `coverage report`, `__main__.py` y la línea de `basicConfig` salen sin cubrir aunque haya tests que los ejecutan, porque esos tests lanzan otro proceso (teoría 05).

Ahora pregúntate si tus tests detectarían un bug. Haz estos cambios en `cli.py`, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshaz el cambio con `git checkout src/observatorio/cli.py`:

| Mutante | ¿Lo detectan? |
|---|---|
| `raise typer.Exit(1)` por `raise typer.Exit(0)` | |
| `err.print(f"error: {error}")` por `out.print(...)` | |
| En `table_of`, `scale.level(...)` por `SCALE.level(...)` | |
| `"alto": "bold red"` por `"alto": "green"` | |
| `TOP = 3` por `TOP = 2` | |

Apunta el resultado: lo pide el *pull request*. Los cinco deberían morir. El tercero y el cuarto sobrevivían con una versión anterior de `test_cli.py`, con la misma cobertura (teoría 05).

### 15. Tus tests

En `tests/test_my_cli.py`, sustituye el ejemplo por **al menos 6 tests** con `CliRunner` y datos de **tu dominio**:

- un `informe` con éxito, que compare las filas de la tabla, no solo que aparezca una palabra;
- un `informe` con una línea inválida: código 1 y el error en `stderr`;
- un archivo que no existe: código 2;
- stdin con `input=`;
- `--json` con `tmp_path`, leyendo después el JSON;
- `validar` con un JSON de tu dominio, válido o no.

Al menos uno debe matar un mutante que **sobreviva** a los tests del bootcamp: busca uno en tus umbrales (`LOW` y `HIGH` exactos) o en tu unidad.

Si tus tests de semanas anteriores llamaban a `main` (paso 2), pásalos a `CliRunner`. Al final, al menos 466 tests en verde.

### 16. Contenedor, README y pull request

```bash
docker compose run --build --rm app
docker compose run --rm app observatorio --version
docker compose run --rm app observatorio informe -f medidas.csv
```

Los tests en verde y `observatorio 0.15.0`. `docker compose run` da al contenedor una terminal, y el informe sale con colores. Con `docker compose run --rm -T app observatorio informe -f medidas.csv` (`-T`: sin terminal) sale en texto plano, como en el CI.

En el `README.md` de tu repositorio, actualiza la lista de comandos: `informe`, `validar`, `--escala` y `--help`.

Commits sugeridos, en este orden:

1. `test: replace main tests with cli tests`
2. `build: add typer and rich`
3. `feat: add typer app skeleton with version`
4. `feat: add informe command`
5. `feat: read stdin and files in informe`
6. `feat: save the summary with --json`
7. `feat: read the scale with --escala`
8. `feat: add validar command`
9. `feat: move verbose option to the callback`
10. `fix: print user data without rich markup`
11. `chore: bump version to 0.15.0`
12. `test: add my cli tests`

Al final:

```bash
git push -u origin week-15
```

En GitHub, abre un *pull request* de `week-15` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy`, `uv run ruff check` y `uv run coverage report`.
2. La tabla de mutantes del paso 14, con el resultado de cada uno, y el mutante que mata tu test del paso 15.
3. Por qué `core/` no cambió y por qué la CLI usa `Console(markup=False)`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'typer'` | Falta el paso 4: `uv add typer==0.27.3 rich==15.0.0` |
| `ImportError: cannot import name 'cli' from 'observatorio'` | Falta `src/observatorio/cli.py`, o no se llama así |
| `ImportError: cannot import name 'main' from 'observatorio.__main__'` al ejecutar `observatorio` | `[project.scripts]` apunta aún a `__main__:main`: cámbialo a `observatorio.cli:app` y ejecuta `uv sync` |
| `Got unexpected extra argument(s) (informe)` | Tu aplicación no tiene callback y solo un comando: Typer no espera su nombre. Escribe el `@app.callback()` del paso 5 |
| `No such option: -v` | `-v` va antes del comando: `observatorio -v informe ...` |
| Una traza con `DataFileError` y código 1 | La excepción escapó del comando: captúrala y usa `raise fail(str(problem), 2) from problem` |
| `test_informe_writes_the_summary` falla en la línea de medias o de frecuentes | El formato cambió: `medias más altas: A 61.0, B 55.1` en una línea, sin `describe_record` |
| `test_informe_reads_the_scale` falla en la tabla | `table_of` recibe `SCALE` y no la escala leída |
| `test_table_colors_each_level` falla | El nivel no va en un `Text` con el estilo de `STYLES`, o los colores no son `cyan`, `green` y `bold red` |
| Un mensaje de error largo sale partido en dos líneas | Falta `soft_wrap=True` en la consola |
| `test_verbose_shows_debug_messages_on_stderr` falla | Los tests de `-v` ejecutan `python -m observatorio -v informe -f ...`: revisa `__main__.py` y el formato de `basicConfig` |
| Los colores salen como `^[[32m` en un archivo | Tienes `FORCE_COLOR` definida: quítala al redirigir |

## Entrega

- Rama `week-15` de `python-<nombre>-<apellido>` con:
  - `typer==0.27.3` y `rich==15.0.0` en `dependencies`, y `[project.scripts]` apuntando a `observatorio.cli:app`;
  - `cli.py` con el callback (`--version`, `-v`), los comandos `informe` (líneas, stdin, `-f`, `-j`, `-e`) y `validar`, y la tabla de Rich;
  - `__main__.py` reducido a llamar a `app`, y `tests/test_main.py` borrado;
  - la versión `0.15.0` y al menos 6 tests propios en `tests/test_my_cli.py`.

  Todo en verde, también en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
- `README.md` del repositorio con los comandos nuevos.
- *Pull request* `week-15` → `main` con la descripción del paso 16.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Probar la CLI](../2-practicas/ejercicio-04-probar-la-cli/README.md) | **Proyecto · Observatorio, capa 14** | [Webgrafía](../4-recursos/webgrafia/README.md) |
