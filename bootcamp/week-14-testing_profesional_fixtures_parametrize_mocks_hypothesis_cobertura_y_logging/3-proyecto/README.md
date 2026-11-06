# Proyecto — Observatorio, capa 13: tests que buscan bugs

⏱️ 6 h 30 min · Capa 13 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Tu Observatorio tiene más de 300 tests, y todos pasan. Todos prueban los casos que se te ocurrieron a ti. Esta semana cambias de pregunta: no "¿funciona con mis ejemplos?", sino "¿qué dato lo rompe?". Los tests nuevos del bootcamp usan las herramientas de la semana y destapan **tres bugs reales** de las capas anteriores:

| Bug | Desde | Lo encuentra |
|---|---|---|
| `uv run observatorio "Norte;abc"` termina con un `ValueError` y una traza, en vez de un `error: línea 1` | Semana 2 | Hypothesis, con texto al azar |
| `"nan"` e `"inf"` pasan por medidas: `nan` sale como `alto` y la mediana es `nan` | Semana 1 | Hypothesis, con `float` al azar |
| Un archivo sin permiso de lectura escapa como `PermissionError` y no como `DataFileError` | Semana 7 | Un mock: sin él no se puede provocar en todos los equipos |

Además:

| Nombre | Qué hace | Herramienta de la semana |
|---|---|---|
| `tests/conftest.py` | Las fixtures `scale`, `lines`, `series` y `write_file`, compartidas por los tests | Fixtures |
| `logger` en `storage.py` y `groups.py` | `read_lines` registra cuántas líneas leyó y `records_of`, cada línea que descarta, en DEBUG | `logging` |
| `observatorio -v ...` | Muestra los mensajes DEBUG del paquete en stderr | `logging.basicConfig` |
| `[tool.coverage]` | Mide líneas y ramas del paquete y falla por debajo del 95 % | coverage |

La versión sube a `0.14.0`, y `hypothesis==6.170.8` y `coverage==7.17.0` entran en el grupo `dev`. Sin `-v`, el informe es **idéntico** al de la semana 13 para cualquier entrada válida.

```
src/observatorio/
├── __main__.py        # + la opción -v
└── core/
    ├── record.py      # parse_value rechaza nan e inf
    ├── groups.py      # parse_record no deja escapar ValueError; records_of registra
    ├── rules.py       # parse_line, construida sobre parse_record
    ├── schemas.py     # MeasurementIn rechaza NaN e Infinity
    ├── storage.py     # read_lines: PermissionError y registro
    ├── streams.py     # iter_lines: PermissionError
    └── ...            # los demás módulos, sin cambios
tests/
├── conftest.py        # nuevo: tus fixtures
├── test_quality.py    # nuevo: los tests del bootcamp de esta semana
└── test_my_quality.py # nuevo: los tuyos
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-14`. El `starter/` trae la capa 12 resuelta. **Tú** añades las dependencias, escribes `conftest.py`, arreglas los tres bugs, añades el registro y la opción `-v` y configuras coverage.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-13` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-14
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/3-proyecto/starter
cp $STARTER/tests/test_quality.py $STARTER/tests/test_my_quality.py tests/
cp $STARTER/tests/test_package.py $STARTER/tests/test_main.py tests/
cp $STARTER/Dockerfile $STARTER/.dockerignore .
sed -i 's/week-13/week-14/' compose.yaml
git status --short
```

Copias estos archivos:

- **Nuevos:**
  - `tests/test_quality.py`, con 47 tests;
  - `tests/test_my_quality.py`, con un ejemplo.
- **Modificados:**
  - `test_package.py`, que ahora espera la versión `0.14.0`, Hypothesis y coverage en `dev`, y la configuración de coverage;
  - `test_main.py`, que solo cambia la versión esperada;
  - `Dockerfile` y `.dockerignore`, que ahora tienen en cuenta Hypothesis y coverage (paso 16);
  - `compose.yaml`.

### 3. Tests en rojo

```bash
uv run pytest
```

```
E   ModuleNotFoundError: No module named 'hypothesis'
...
ERROR tests/test_quality.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

Lee `tests/test_quality.py` entero antes de escribir nada: es la especificación. Tiene cinco bloques, uno por herramienta de la semana. Fíjate en los nombres de los parámetros de los primeros tests: `scale`, `lines`, `series` y `write_file` no se importan de ningún sitio. Son las fixtures que escribirás en el paso 5.

### 4. Las dependencias

```bash
uv add --dev hypothesis==6.170.8 coverage==7.17.0
```

Las dos van en el grupo `dev`, como pytest: se usan para probar, y quien instale tu Observatorio no las necesita. Hypothesis trae una dependencia, `sortedcontainers`. Míralo con `uv tree --depth 2`.

Hypothesis guarda sus contraejemplos en `.hypothesis/` y coverage, sus datos en `.coverage`. Ninguno de los dos va a Git. Añádelos a tu `.gitignore`:

```bash
printf '.hypothesis/\n.coverage\n' >> .gitignore
```

Ejecuta `uv run pytest`:

```
E       fixture 'scale' not found
...
27 failed, 345 passed, 11 errors
```

Los 11 `errors` no son fallos: pytest no puede ni empezar esos tests, porque piden fixtures que no existen.

### 5. Las fixtures: `tests/conftest.py`

Crea `tests/conftest.py`. Estas son las cuatro fixtures que esperan los tests:

| Fixture | Devuelve |
|---|---|
| `scale` | `Scale("unidad", 10.0, 50.0)` |
| `lines` | `["# medidas", "Norte;12,5", "Sur;NA", "malo", "Este;55,1"]` |
| `series` | `Series.from_lines(lines)`: pide la fixture `lines` |
| `write_file` | Una **función** `write(name, text) -> Path` que crea el archivo en `tmp_path` y devuelve su ruta |

Las tres primeras son como las del ejercicio 01. La cuarta es una **fábrica**: la fixture no devuelve un archivo, sino una función para crear los que el test necesite:

```python
@pytest.fixture
def write_file(tmp_path: Path) -> Callable[[str, str], Path]:
    """Una fábrica: write_file(nombre, texto) crea el archivo en tmp_path y da su ruta."""

    def write(name: str, text: str) -> Path:
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        return path

    return write
```

Escribe las otras tres, con su docstring y su tipo de vuelta (`strict` también revisa `conftest.py`). Importa `Callable` de `collections.abc`, `Path`, `pytest` y, de `observatorio.core`, `Scale` y `Series`.

```
31 failed, 352 passed
```

Los errores han desaparecido. Algunos se han convertido en fallos: ahora el test empieza, pero el código no hace lo que pide.

### 6. Hypothesis encuentra el primer bug

Antes de arreglar nada, mira qué encontró Hypothesis:

```bash
uv run pytest tests/test_quality.py -k never_crashes
```

```
E       ValueError: could not convert string to float: ':'
E       Failing test case: test_process_lines_never_crashes_and_counts_every_data_line(
E           lines=['0;:'],
E       )
```

Tu contraejemplo puede ser otro, como `['0;a']`: cualquier línea con un `;` y un valor que no es un número. La propiedad dice que `process_lines` nunca lanza una excepción y que cada línea de datos acaba en una fila o en un error. Pruébalo en tu programa:

```bash
uv run observatorio "Norte;abc"
```

```
...
    return float(text.replace(",", "."))
ValueError: could not convert string to float: 'abc'
```

El docstring de `parse_line` lo avisaba desde la semana 2: *"Un valor no numérico ("abc") lanza ValueError: lo manejarás en la semana 7"*. Ningún test lo comprobaba, y se quedó así. Tus tests probaban `"Norte;12,5"`, `"Sur;NA"` y `"malo"`: líneas sin `;`, no con un valor roto.

### 7. Arréglalo una vez: `parse_record`

El bug está en **dos** sitios, porque la regla está copiada en dos: `parse_record` (`groups.py`) y `parse_line` (`rules.py`) parten la línea por su cuenta. Se arregla en la raíz.

En `parse_record`, un valor que no es un número da `None`, como una línea mal formada:

```python
        case [label, text] if label.strip():
            try:
                return label.strip(), parse_value(text)
            except ValueError:
                return None
```

Y `parse_line` deja de repetir la regla: usa `parse_record`.

```python
def parse_line(line: str, unit: str, low: float, high: float) -> str | None:
    """Convierte "etiqueta;valor" en la fila de format_row, con su nivel.

    Las reglas son las de parse_record: devuelve None si la línea no tiene exactamente
    un ";", si la etiqueta queda vacía o si el valor no es un número finito ("abc", "nan").
    """
    record = parse_record(line)
    if record is None:
        return None
    label, value = record
    return format_row(label, value, unit, classify(value, low, high))
```

En `rules.py`, importa `parse_record` de `observatorio.core.groups` en lugar de `parse_value`. `groups` no importa `rules`, así que no hay ciclo. Actualiza también el docstring de `parse_record`.

```
24 failed, 359 passed
```

Ahora `uv run observatorio "Norte;abc"` escribe `error: línea 1: 'Norte;abc'` y devuelve 1, como cualquier línea inválida.

### 8. `nan` e `inf`

`float("nan")` y `float("inf")` son números válidos para Python, y tu programa los acepta:

```bash
uv run observatorio "Norte;nan" "Sur;12"
```

```
Norte               nan unidad | alto
Sur                12.0 unidad | medio
...
mediana: nan unidad
```

`nan` no es mayor ni menor que nada, así que `classify` acaba en `alto`, y un solo `nan` convierte la mediana en `nan`. Ningún sensor mide "infinito". En `record.py`, importa `math` y añade la comprobación al final de `parse_value`:

```python
    value = float(text.replace(",", "."))
    if not math.isfinite(value):
        raise ValueError(f"valor no finito: {text!r}")
    return value
```

Añade al docstring que lanza `ValueError` si el valor no es finito. Como `parse_record` ya convierte el `ValueError` en `None`, `"Norte;nan"` pasa a ser una línea inválida en todo el programa.

La frontera de JSON tiene el mismo agujero por otro lado. Un texto `"nan"` ya lo rechaza `parse_text`, que usa `parse_value`. Pero el `json` de Python acepta los literales `NaN` e `Infinity`, y Pydantic también, salvo que se lo prohíbas. En `schemas.py`:

```python
    # allow_inf_nan=False: rechaza el NaN y el Infinity que el JSON de Python acepta.
    value: Annotated[float | None, Field(strict=True, allow_inf_nan=False)]
```

```
12 failed, 371 passed
```

### 9. El registro del paquete

Una línea inválida aparece como `error:` en el informe, pero `Series.from_lines`, a través de `records_of`, la descarta sin decir nada. Esta capa deja un rastro en el **registro**, con nivel DEBUG, que nadie ve salvo que lo pida.

En `storage.py`, importa `logging` y crea el logger del módulo, debajo de los imports:

```python
# Un logger por módulo, con el nombre del módulo: "observatorio.core.storage".
# El paquete solo escribe en él; quien decide si se ve y dónde es main.
logger = logging.getLogger(__name__)
```

En `read_lines`, guarda las líneas en una variable, registra cuántas son **después** del `try` (si el archivo falla, no hay nada que contar) y devuélvelas:

```python
    try:
        with path.open(encoding="utf-8") as file:
            lines = file.read().splitlines()
    except FileNotFoundError as error:
        ...
    logger.debug("%d líneas leídas de %s", len(lines), path)
    return lines
```

En `groups.py`, crea también su `logger`. Después, escribe `records_of` como un bucle, para registrar cada línea que descarta:

```python
    records: list[Record] = []
    for line in lines:
        if not is_data_line(line):
            continue
        record = parse_record(line.strip())
        if record is None:
            logger.debug("línea ignorada: %r", line)
        else:
            records.append(record)
    return records
```

`logger.debug("... %r", line)` y no `logger.debug(f"... {line!r}")`: con `%`, el texto solo se compone si alguien va a ver el mensaje.

```
9 failed, 374 passed
```

`uv run mypy` ya no da errores: los tests encuentran los `logger` que buscaban.

### 10. La opción `-v`

El paquete escribe en sus loggers, pero nadie los ha configurado: los DEBUG no salen. La configuración es cosa del **programa**. En `__main__.py`, importa `logging` y, justo después de calcular `args`:

```python
    if args[:1] in (["-v"], ["--verbose"]):
        # Solo main configura el registro: el paquete se limita a escribir en sus loggers.
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")
        args = args[1:]
```

`args[:1]` es una lista con el primer argumento, o vacía si no hay ninguno: no falla con `args` vacía. Detrás de `-v` va cualquier otra forma del programa: `-v -f medidas.csv`, `-v --version`, `-v "Norte;12,5"`. Añade `[-v] ` a `USAGE`, detrás de `observatorio`, y una línea al docstring de `main`.

```
7 failed, 376 passed
```

### 11. Un mock: el archivo sin permiso

`read_lines` convierte en `DataFileError` un archivo que no existe, una carpeta y un texto que no es UTF-8. ¿Y un archivo sin permiso de lectura? Provocarlo de verdad en un test no es fiable: `chmod 000` no impide leer a `root`, que es como se ejecutan muchos contenedores y CI, y en Windows funciona de otra manera. Los tests usan un **mock**:

```python
    with (
        mock.patch.object(Path, "open", side_effect=denied),
        pytest.raises(DataFileError, match="sin permiso para leer") as caught,
    ):
        read_lines(tmp_path / "medidas.txt")
```

Mientras dura el `with`, `Path.open` lanza `PermissionError`, como lo haría el sistema operativo. Añade el caso a `read_lines`, junto a los otros:

```python
    except PermissionError as error:
        raise DataFileError(f"sin permiso para leer {path}") from error
```

`iter_lines` (`streams.py`) promete los mismos errores que `read_lines`: añádelo allí también. Actualiza los dos docstrings.

```
4 failed, 379 passed
```

### 12. La cobertura

En `pyproject.toml`, debajo de `[tool.pytest.ini_options]`:

```toml
[tool.coverage.run]
# Mide tu paquete, no los tests ni las bibliotecas, y cuenta también las ramas:
# un if cuyo else nunca se ejecutó no está cubierto aunque su línea sí.
source_pkgs = ["observatorio"]
branch = true

[tool.coverage.report]
# `coverage report` falla por debajo del 95 % y dice qué líneas no ejecutó ningún test.
fail_under = 95
show_missing = true
# El arranque desde la terminal se prueba ejecutando el programa, no con pytest.
exclude_also = ['if __name__ == "__main__":']
```

Mide:

```bash
uv run coverage run -m pytest -q
uv run coverage report
```

```
Name                                  Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------------------
...
src/observatorio/core/storage.py         57      0      8      0   100%
src/observatorio/core/streams.py         29      2     10      0    95%   35-36
src/observatorio/core/trends.py          33      0     12      0   100%
---------------------------------------------------------------------------------
TOTAL                                    ...                          99%
```

Tus cifras pueden ser algo distintas: tu código y tus tests no son los de la solución. `streams.py`, líneas 35-36: ningún test lee con `iter_lines` un archivo que no es UTF-8. Los de la semana 11 probaron el archivo que no existe y la carpeta, pero no ese caso. Lo cubrirás en el paso 15. Si tu informe enseña otras líneas, apúntalas: también son para el paso 15.

```
3 failed, 380 passed
```

### 13. La versión

```bash
uv version --bump minor
```

```
observatorio 0.13.0 => 0.14.0
```

```
383 passed
```

### 14. Todo junto

```bash
uv run observatorio -v -f medidas.csv > /dev/null
```

```
DEBUG observatorio.core.storage: 9 líneas leídas de medidas.csv
error: línea 7: 'Sur 9,5'
DEBUG observatorio.core.groups: línea ignorada: 'Sur 9,5'
```

Con tu `medidas.csv`, las cifras y las líneas serán otras. `> /dev/null` tira el informe, que va a stdout: queda solo stderr, con el error de siempre y los dos mensajes de registro. Cada mensaje dice su nivel y qué módulo lo escribió. Sin `-v`, los DEBUG no salen.

```bash
uv run observatorio "Norte;abc" "Sur;nan" "Este;12"
echo $?
```

```
error: línea 1: 'Norte;abc'
error: línea 2: 'Sur;nan'
Este               12.0 unidad | medio
...
1
```

Ni traza ni `nan`: dos líneas inválidas, como cualquier otra.

### 15. Tus tests

En `tests/test_my_quality.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con datos de tu dominio, importando solo de `observatorio.core` (y `pytest`, `hypothesis` o `unittest.mock` si lo necesitas). Usa al menos una vez cada herramienta de la semana:

| Qué pruebas | Ejemplo (calidad del aire) |
|---|---|
| Una propiedad con la estrategia de **tu** dominio | Para cualquier valor entre 0 y 500 µg/m³, `parse_value(str(v).replace(".", ","))` da `v` |
| Valores imposibles de tu dominio, con `parametrize` | `"sin calibrar"`, `"inf"` y `"1e999"` hacen que `parse_record("Norte;...")` dé `None` |
| Una fixture de `conftest.py` con tus datos | Una fixture `my_lines` con tus estaciones, y un test que la usa con `Series.from_lines` |
| Lo que se registra, con `caplog` | `records_of` con una línea mal escrita de tu dominio registra `línea ignorada` |
| Un fallo que solo se provoca con un mock | `write_json` con `Path.open` lanzando `PermissionError` lanza `DataFileError` |
| Las líneas que el paso 12 dejó sin cubrir | `next(iter_lines(path))` con un archivo en Latin-1 (`write_bytes("ñ".encode("latin-1"))`) lanza `DataFileError` |

```bash
uv run pytest
uv run ruff check && uv run ruff format --check && uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
```

Esperado: todo en verde, al menos `455 passed`, y `coverage report` sin `Coverage failure`. Son los 372 tests del bootcamp (los 324 de la semana 13, los 47 de `test_quality.py` y uno nuevo en `test_package.py`) más los 83 tuyos como mínimo (5 + 6 × 13, de las semanas 1 a 14).

### 16. Contenedor, README y pull request

El `Dockerfile` que copiaste en el paso 2 tiene una línea nueva:

```dockerfile
# HYPOTHESIS_STORAGE_DIRECTORY: Hypothesis guarda sus ejemplos en /tmp, por lo mismo.
    HYPOTHESIS_STORAGE_DIRECTORY=/tmp/hypothesis
```

En el contenedor, `/app` no se puede escribir (el usuario es `app`, no `root`). Sin esa línea, Hypothesis no podría crear `.hypothesis/` allí y llenaría la salida de `HypothesisWarning`. `.dockerignore` deja fuera `.hypothesis/` y `.coverage`.

```bash
docker compose run --build --rm app
docker compose run --rm app observatorio --version
```

Los tests en verde, sin avisos, y `observatorio 0.14.0`.

En el `README.md` de tu repositorio, añade la opción `-v` a la lista de comandos y, en la de tests, `uv run coverage run -m pytest && uv run coverage report`.

Commits sugeridos, en este orden:

1. `build: add hypothesis and coverage`
2. `test: add shared fixtures in conftest`
3. `fix: treat non-numeric values as invalid lines`
4. `fix: reject non-finite values`
5. `feat: log read and ignored lines`
6. `feat: add verbose option`
7. `fix: map PermissionError to DataFileError`
8. `build: configure coverage`
9. `chore: bump version to 0.14.0`
10. `test: add quality tests`

Al final:

```bash
git push -u origin week-14
```

En GitHub, abre un *pull request* de `week-14` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy`, `uv run ruff check` y `uv run coverage report`.
2. El contraejemplo que te dio Hypothesis en el paso 6 y por qué ningún test de antes lo encontró.
3. Por qué el bug de `"abc"` estaba en dos sitios y por qué el permiso se prueba con un mock.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'hypothesis'` | Falta el paso 4: `uv add --dev hypothesis==6.170.8 coverage==7.17.0` |
| `fixture 'series' not found` | `conftest.py` no está en `tests/`, o la fixture tiene otro nombre (paso 5) |
| `ImportError: ... partially initialized module` | Importaste algo de `rules` en `groups`: es un ciclo. Solo `rules` importa a `groups` |
| `test_parse_value_rejects_non_finite_values` dice `DID NOT RAISE` | Falta el `math.isfinite` en `parse_value` (paso 8) |
| `test_measurement_in_rejects_non_finite_values[json-nan]` dice `DID NOT RAISE` | Falta `allow_inf_nan=False` en `Field` (paso 8) |
| `caplog.messages` vacío en los tests de registro | El nombre del logger no es `__name__`, o registras con `logger.info` en vez de `logger.debug` |
| Los mensajes DEBUG salen sin `-v` | Tienes un `logging.basicConfig` fuera de `main`: el paquete no configura el registro |
| `test_verbose_shows_debug_messages_on_stderr` falla | El formato de `basicConfig` debe ser exactamente `"%(levelname)s %(name)s: %(message)s"` |
| `Coverage failure: total of ... is less than fail-under=95` | Mira `Missing` en `coverage report` y escribe los tests que faltan (paso 15) |
| `HypothesisWarning: The database setting is not configured` en Docker | Falta `HYPOTHESIS_STORAGE_DIRECTORY` en el `Dockerfile` (paso 16) |

## Entrega

- Rama `week-14` de `python-<nombre>-<apellido>` con:
  - `hypothesis==6.170.8` y `coverage==7.17.0` en el grupo `dev`, y `[tool.coverage]` con ramas y `fail_under = 95`;
  - `tests/conftest.py` con `scale`, `lines`, `series` y `write_file`;
  - los tres bugs arreglados: `parse_record` y `parse_line`, `parse_value` y `MeasurementIn`, `read_lines` e `iter_lines`;
  - los loggers de `storage.py` y `groups.py`, y la opción `-v`;
  - la versión `0.14.0` y al menos 6 tests propios en `tests/test_my_quality.py`.

  Todo en verde, también en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
- `README.md` del repositorio con `-v` y el comando de cobertura.
- *Pull request* `week-14` → `main` con la descripción del paso 16.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Cobertura y logging](../2-practicas/ejercicio-04-cobertura-y-logging/README.md) | **Proyecto · Observatorio, capa 13** | [Webgrafía](../4-recursos/webgrafia/README.md) |
