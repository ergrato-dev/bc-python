# Proyecto — Observatorio, capa 7: un paquete de verdad

⏱️ 6 h 30 min · Capa 7 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Esta semana el Observatorio no aprende a calcular nada nuevo: se ordena por dentro. Siete módulos sueltos junto a `__main__.py` funcionaban con siete; con los que llegan en la fase 2 (modelos, CLI, base de datos) serían un cajón desordenado. Al terminar, tu proyecto queda así:

```
src/observatorio/
├── __init__.py          # __version__, leída de pyproject.toml
├── __main__.py          # main: la única parte que toca la terminal
└── core/                # el núcleo: lógica pura y archivos
    ├── __init__.py      # la API pública: imports y __all__
    ├── analysis.py
    ├── groups.py
    ├── record.py
    ├── report.py
    ├── rules.py
    ├── storage.py
    └── trends.py
```

Y el proyecto gana las herramientas de un equipo profesional, fijadas en `pyproject.toml` y en `uv.lock`:

| Qué | Cómo queda |
|---|---|
| Paquete `core` | `from observatorio.core import median, read_data` funciona sin saber en qué módulo vive cada función |
| Versión | `version = "0.8.0"` en `pyproject.toml`, `observatorio.__version__` y `uv run observatorio --version` |
| Herramientas de desarrollo | `ruff` y `mypy` en el grupo `dev`, con versión exacta: `uv run mypy` en lugar de `uv run --with mypy==2.4.1 ...` |
| Estilo | `uv run ruff check` y `uv run ruff format --check` sin avisos |
| Configuración | `[tool.ruff]` y `[tool.mypy]` en `pyproject.toml`: los comandos van sin argumentos |
| Distribución | `uv build` crea un *wheel* que funciona en cualquier máquina con Python 3.14 |

El informe de `uv run observatorio -f medidas.csv` es **idéntico** al de la semana 7: una reorganización que cambia lo que calcula el programa no es una reorganización, es un bug. Los 185 tests del bootcamp vigilan que así sea.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-08`. El `starter/` trae las capas 0 a 6 resueltas y sin mover; **tú mueves las tuyas**. No copias `__main__.py`: lo amplías tú.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-07` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-08
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/3-proyecto/starter
for name in analysis groups main record report rules storage trends package; do
  cp $STARTER/tests/test_$name.py tests/
done
cp $STARTER/tests/test_my_core.py tests/
cp $STARTER/.dockerignore .
sed -i 's/week-07/week-08/' compose.yaml
git status --short
```

Modificados: los ocho archivos de tests del bootcamp (solo cambian sus `import`), `.dockerignore` (tres carpetas más que no deben entrar en la imagen) y `compose.yaml`. Nuevos: `tests/test_package.py` y `tests/test_my_core.py`. Tus `test_my_*.py` de semanas anteriores no se tocan: los arreglas tú en el paso 5.

### 3. Tests en rojo

```bash
uv run pytest
```

Salida esperada:

```
E   ModuleNotFoundError: No module named 'observatorio.core'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 10 errors during collection !!!!!!!!!!!!!!!!!!!
```

Es otro tipo de rojo. Hasta ahora fallaban tests sueltos (`failed`); ahora pytest ni siquiera puede **importar** diez archivos de tests (`errors during collection`), porque piden `observatorio.core`, que todavía no existe. Cuando un import falla al cargar el archivo, pytest no llega a ejecutar ningún test y se detiene.

Abre `tests/test_package.py`: son tests de la **forma** del proyecto, no de lo que calcula. Fíjate en `importlib.util.find_spec`, que busca un módulo sin importarlo, y en `tomllib`, que lee tu `pyproject.toml` (teoría 03).

### 4. Las herramientas, dentro del proyecto

Hasta ahora `mypy` llegaba con `uv run --with mypy==2.4.1`, cada vez, y ruff no estaba. Añádelos al grupo de desarrollo, con versión exacta (teoría 04):

```bash
uv add --dev ruff==0.17.3 mypy==2.4.1
git diff pyproject.toml
uv tree
```

`uv add` hace tres cosas: escribe las dos dependencias en `[dependency-groups]`, resuelve y apunta en `uv.lock` las versiones exactas de todo lo que necesitan, y las instala en tu `.venv`. En `git diff` verás el grupo `dev` con tres herramientas en orden alfabético. `uv tree` enseña quién trae a quién:

```
observatorio v0.1.0
├── mypy v2.4.1 (group: dev)
│   ├── ast-serialize v0.13.1
│   ├── librt v0.16.0
│   ├── mypy-extensions v1.2.0
│   ├── pathspec v1.1.1
│   └── typing-extensions v4.16.0
├── pytest v9.2.0 (group: dev)
│   ├── iniconfig v2.3.1
│   ├── packaging v26.3
│   ├── pluggy v1.7.0
│   └── pygments v2.21.0
└── ruff v0.17.3 (group: dev)
```

Pediste dos herramientas y entraron siete paquetes: las cinco dependencias de mypy también quedan fijadas en `uv.lock`. Haz commit de `pyproject.toml` y `uv.lock` juntos: son una pareja.

### 5. El paquete `core`

Crea la carpeta y mueve los siete módulos con `git mv`, que conserva su historial (teoría 02):

```bash
mkdir src/observatorio/core
touch src/observatorio/core/__init__.py
cd src/observatorio
git mv analysis.py groups.py record.py report.py rules.py storage.py trends.py core/
cd ../..
uv run observatorio "Sur;8"
```

El programa ya no arranca:

```
  File ".../src/observatorio/__main__.py", line 13, in <module>
    from observatorio.analysis import count_level, process_lines, share
ModuleNotFoundError: No module named 'observatorio.analysis'
```

Cada `import` dice el camino completo del módulo, y el camino cambió: `observatorio.analysis` ahora es `observatorio.core.analysis`. Busca todos los imports viejos:

```bash
grep -rnE "from observatorio\.(analysis|groups|record|report|rules|storage|trends) import" src tests
```

Cámbialos uno a uno, en tus módulos de `core/`, en `__main__.py` y en tus `tests/test_my_*.py`: `from observatorio.record import parse_value` pasa a `from observatorio.core.record import parse_value`. Si prefieres hacerlo de una vez:

```bash
sed -i -E 's/^from observatorio\.(analysis|groups|record|report|rules|storage|trends) import/from observatorio.core.\1 import/' src/observatorio/*.py src/observatorio/core/*.py tests/test_my_*.py
```

```bash
uv run pytest
```

Esperado: `Interrupted: 2 errors during collection`, en `test_main.py` y `test_my_core.py`. Los otros ocho ya se importan, porque piden módulos concretos (`observatorio.core.record`). Estos dos piden nombres directamente a `observatorio.core` (`from observatorio.core import median`), y tu `core/__init__.py` está vacío.

### 6. La API pública

Escribe `core/__init__.py`: un docstring, un `from observatorio.core.<módulo> import ...` por módulo con **todos** sus nombres públicos (funciones, constantes, `Record` y `DataFileError`) y, al final, `__all__` con esos mismos nombres como textos (teoría 02):

```python
"""El núcleo del Observatorio: modelo de registros, análisis y archivos."""

from observatorio.core.analysis import count_level, process_lines, ratio, share
from observatorio.core.groups import LEVELS, Record, distinct_labels, ...
...

__all__ = [
    "LEVELS",
    "Record",
    "count_level",
    ...
]
```

Después, en `__main__.py`, cambia los seis imports de `core` por uno solo, `from observatorio.core import (...)`, con los nombres que usa `main` entre paréntesis, uno por línea.

```bash
uv run pytest
```

Esperado: `7 failed`. Cinco son de la versión (los dos `test_version_*` de `test_package.py`, los dos `test_main_version[...]` y `test_usage_mentions_version`) y dos de la configuración, con `KeyError: 'ruff'` y `KeyError: 'mypy'`. Si además falla `test_dev_tools_are_pinned`, te saltaste el paso 4. Si falla `test_every_name_in_core_all_exists`, escribiste en `__all__` un nombre que no importaste.

### 7. La versión

La versión se escribe en **un solo sitio**, `pyproject.toml`, y el resto la lee (teoría 03):

1. En `pyproject.toml`, `version = "0.8.0"`: la semana 8 de un proyecto que todavía no ha llegado a su 1.0.
2. En `src/observatorio/__init__.py`, debajo del docstring:

   ```python
   from importlib.metadata import version

   __version__ = version("observatorio")
   ```

3. En `__main__.py`, `from observatorio import __version__`, un `case ["-V" | "--version"]:` justo debajo del de ayuda que escriba `observatorio 0.8.0` y devuelva `0`, `  o  observatorio --version` al final de `USAGE` y una línea en el docstring de `main`.

```bash
uv run observatorio --version
uv run pytest
```

Esperado: `observatorio 0.8.0` y `2 failed`, los de configuración. `version("observatorio")` lee los metadatos del paquete **instalado** en tu `.venv`; `uv run` lo reinstala solo cuando cambia `pyproject.toml`, por eso no hizo falta nada más.

### 8. Configura ruff y mypy

Añade al final de `pyproject.toml`:

```toml
[tool.ruff]
# Líneas de hasta 100 caracteres (por defecto, 88). Las reglas del linter son las
# recomendadas de ruff: no hace falta elegirlas.
line-length = 100

[tool.mypy]
# `uv run mypy` sin argumentos revisa estas carpetas.
files = ["src", "tests"]
```

```bash
uv run pytest
uv run mypy
```

Esperado: todo en verde, `190 passed`, y `Success: no issues found in 24 source files`. Desde hoy `mypy` va sin argumentos: la configuración vive en el proyecto, no en tu memoria.

### 9. ruff: lint y formato

```bash
uv run ruff check
```

Si tu `analysis.py` es como el del starter, ruff encuentra algo que llevaba ahí desde la semana 6:

```
F401 [*] `observatorio.core.report.level_of` imported but unused
  --> src/observatorio/core/analysis.py:13:52
...
Found 1 error.
[*] 1 fixable with `--fix`.
```

Cuando en la semana 6 `count_level` pasó a usar `level_counts`, `level_of` se quedó importado sin uso. Los tests no lo vieron, porque no cambia ningún resultado; ruff sí. Lee cada aviso antes de arreglarlo: el código (`F401`) se busca con `uv run ruff rule F401`. Los que llevan `[*]` se arreglan solos:

```bash
uv run ruff check --fix
uv run ruff format
git diff --stat
uv run ruff check && uv run ruff format --check
uv run pytest
```

`ruff format` reescribe la forma (comillas, espacios, saltos de línea), nunca lo que hace el código: los tests siguen en `190 passed`. Haz commit del formato **solo**, separado de cualquier cambio de lógica, con `style: format with ruff`: quien revise sabrá que no hay nada que leer línea a línea. La última línea de comandos es la que pasará el CI de la semana 21: los dos sin avisos.

### 10. Rompe el lock a propósito

Cambia **a mano** en `pyproject.toml` `ruff==0.17.3` por `ruff==0.17.4`, sin pasar por `uv`, y comprueba si el lock sigue al día:

```bash
uv lock --check; echo "código: $?"
```

```
error: The lockfile at `uv.lock` needs to be updated, but `--check` was provided.

hint: To update the lockfile, run `uv lock`.
código: 1
```

`pyproject.toml` pide una versión que `uv.lock` no tiene: están desincronizados. Tu `Dockerfile` instala con `uv sync --locked`, que da el mismo error y para la construcción de la imagen. Es lo que quieres: una imagen nunca se construye con dependencias distintas de las que probaste. Deshaz el cambio:

```bash
git restore pyproject.toml
uv lock --check; echo "código: $?"
```

Esperado: `código: 0`. Para subir una versión de verdad, `uv add --dev ruff==0.17.4` cambia los dos archivos a la vez (teoría 04). Esta semana te quedas en 0.17.3.

### 11. Tus tests

En `tests/test_my_core.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con datos de tu dominio. La condición: importan **solo** de `observatorio.core`, nunca de un módulo de dentro. Así prueban la API pública, la que no debe romperse aunque reorganices `core` otra vez. Cada test cruza al menos dos funciones:

| Qué pruebas | Ejemplo (calidad del aire) |
|---|---|
| De CSV a resumen | Un CSV de tres estaciones en `tmp_path` da el `summary_data` calculado a mano |
| De líneas a niveles | `process_lines` con tus umbrales y `level_counts` de las filas |
| Ida y vuelta | `write_json(summary_data(...))` y `read_json` devuelven lo mismo |
| Errores de la API | Un CSV sin cabecera da `DataFileError`, importada de `observatorio.core` |
| Tendencias | `largest_jump(values_of(records_of(lineas)))` con tus lecturas |
| La API completa | Cada función que usa tu `main` está en `observatorio.core.__all__` |

```bash
uv run pytest
uv run ruff check && uv run ruff format --check && uv run mypy
```

Esperado: todo en verde, al menos `232 passed`: los 185 del bootcamp (12 + 17 + 19 + 20 + 26 + 27 + 28 + 24 + 12) y los 47 tuyos como mínimo (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 de las semanas 1 a 8). Pasa `ruff format` también a tus tests nuevos.

### 12. Construye el paquete y pruébalo en el contenedor

```bash
uv build
uvx --from dist/observatorio-0.8.0-py3-none-any.whl observatorio --version
docker compose run --build --rm app
docker compose run --rm app observatorio -f medidas.csv
```

`uv build` crea en `dist/` dos archivos: el *wheel* (`.whl`, el paquete listo para instalar) y el `.tar.gz` (el código fuente). `uvx --from` instala el *wheel* en un entorno temporal, fuera de tu proyecto, y ejecuta `observatorio`: escribe `observatorio 0.8.0`, la prueba de que tu paquete funciona instalado, no solo en tu carpeta. `dist/` ya trae su propio `.gitignore`: no se sube. En el contenedor, los tests en verde y el mismo informe que en tu máquina.

### 13. README, commit y pull request

En el `README.md` de tu repositorio:

1. Los comandos nuevos: `--version`, `ruff check`, `ruff format` y `mypy` sin argumentos.
2. Un árbol del paquete como el de arriba, con una línea por carpeta que diga qué va en ella.

Commits sugeridos, en este orden: `chore: add ruff and mypy as dev dependencies`, `refactor: move modules into core package`, `feat: expose core public API`, `feat: add --version`, `chore: configure ruff and mypy`, `fix: remove unused import`, `style: format with ruff` y `test: add core tests`. Al final:

```bash
git push -u origin week-08
```

En GitHub, abre un *pull request* de `week-08` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy` y `uv run ruff check`.
2. El árbol de `src/observatorio`.
3. Qué encontró ruff en tu código y por qué el commit de formato va separado.

Con este *pull request* cierras la **fase 1**: un proyecto `uv` con paquete, tests, tipos, lint, lock e imagen Docker. En la fase 2 los registros dejan de ser tuplas y pasan a ser clases.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'observatorio.analysis'` | Queda un import con el camino viejo: `grep -rnE "from observatorio\.(analysis\|groups\|record\|report\|rules\|storage\|trends) import" src tests` |
| `ImportError: cannot import name 'median' from 'observatorio.core'` | Falta ese nombre en los imports de `core/__init__.py` |
| `test_every_name_in_core_all_exists` falla | Hay un nombre en `__all__` que no importaste, o mal escrito |
| `test_no_module_is_left_outside_core` falla | Quedó una copia de un módulo en `src/observatorio/`: bórrala |
| `PackageNotFoundError: No package metadata was found for observatorio` | Ejecutaste con `python` fuera del entorno: usa `uv run` |
| `--version` sigue diciendo `0.1.0` | No guardaste `pyproject.toml`, o escribiste la versión a mano en `__init__.py` en lugar de `version("observatorio")` |
| `error: Failed to spawn: ruff` | No hiciste el paso 4: `uv add --dev ruff==0.17.3 mypy==2.4.1` |
| `The lockfile at uv.lock needs to be updated` | `pyproject.toml` cambió sin `uv`: `uv lock`, o `git restore pyproject.toml` si fue sin querer |
| `ruff format` cambia muchos archivos | Es normal la primera vez. Haz un commit solo con eso |
| `RUF022 __all__ is not sorted` | `uv run ruff check --fix` lo ordena: primero las CONSTANTES, después las Clases y luego el resto |
| Docker: `uv sync --locked` falla al construir | Lo mismo que el paso 10: `uv lock`, commit, y vuelve a construir |

## Entrega

- Rama `week-08` de `python-<nombre>-<apellido>` con el paquete `core`, la versión `0.8.0` y `--version`, `ruff` y `mypy` en el grupo `dev`, la configuración en `pyproject.toml` y al menos 6 tests propios en `tests/test_my_core.py`. Todo en verde (también en Docker), con `ruff check`, `ruff format --check` y `mypy` sin avisos.
- `README.md` del repositorio con los comandos nuevos y el árbol del paquete.
- *Pull request* `week-08` → `main` con la descripción del paso 13.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · ruff](../2-practicas/ejercicio-04-ruff/README.md) | **Proyecto · Observatorio, capa 7** | [Webgrafía](../4-recursos/webgrafia/README.md) |
