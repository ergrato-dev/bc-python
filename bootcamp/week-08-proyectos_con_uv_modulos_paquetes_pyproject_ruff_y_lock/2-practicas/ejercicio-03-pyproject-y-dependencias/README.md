# Ejercicio 03 — `pyproject.toml` y dependencias

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-pyproject-toml.md) y [04](../../1-teoria/04-dependencias-y-lock.md)

## Objetivo

Crear un proyecto `uv` desde cero, leer su `pyproject.toml` y su `uv.lock` desde Python, ver la diferencia entre un rango de versiones y una versión fijada, y construir un *wheel* para mirar qué lleva dentro. Es lo mismo que harás con el Observatorio en los pasos 4, 7 y 12 del proyecto. Ejercicio **guiado**: ejecutas los comandos de `uv`, descomentas cada paso de `inspect_project.py` y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/2-practicas/ejercicio-03-pyproject-y-dependencias/starter
uv run python inspect_project.py
```

```
Ejercicio 03 · pyproject.toml y dependencias
```

`inspect_project.py` lee los archivos del proyecto `sondeo`, que todavía no existe: lo creas en el paso 1, dentro de `starter/`. El `.gitignore` del starter ya lo deja fuera de Git.

## Pasos

### 1. Un proyecto nuevo con `uv init`

```bash
uv init --package --no-workspace sondeo
```

```
Initialized project `sondeo` at `.../starter/sondeo`
```

`--package` crea un proyecto **instalable**, con `src/`, como tu Observatorio. `--no-workspace` evita que uv lo una al proyecto de `starter/`, que está en la carpeta de arriba. Mira lo que creó:

```
sondeo/
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── sondeo/
        └── __init__.py
```

Ejecuta su comando:

```bash
cd sondeo
uv run sondeo
cd ..
```

```
Hello from sondeo!
```

El primer `uv run` creó `sondeo/.venv`, instaló el paquete en él y escribió `sondeo/uv.lock`. `sondeo` es un comando porque `pyproject.toml` lo declara en `[project.scripts]`, apuntando a la función `main` de `src/sondeo/__init__.py`.

### 2. Leer `pyproject.toml`

Descomenta el **PASO 2** de `inspect_project.py` y ejecuta:

```
Nombre: sondeo | versión: 0.1.0
Python: >=3.14.10
Dependencias: []
Comandos: {'sondeo': 'sondeo:main'}
Se construye con: uv_build
Grupos: ninguno
```

`tomllib.load` convierte el TOML en diccionarios y listas de Python: cada `[tabla]` es un diccionario. Abre `sondeo/pyproject.toml` al lado y compara línea a línea. `requires-python` lo escribió `uv init` a partir de tu Python. En tu Observatorio es `>=3.14,<3.15`, que admite cualquier 3.14 y ninguna 3.15. En `[build-system]`, `uv_build` es el programa que convierte tu código en un paquete instalable.

### 3. Una dependencia de desarrollo y el lock

```bash
cd sondeo
uv add --dev pytest==9.2.0
uv tree
cd ..
uv run python inspect_project.py
```

`uv tree` dibuja quién necesita a quién:

```
sondeo v0.1.0
└── pytest v9.2.0 (group: dev)
    ├── iniconfig v2.3.1
    ├── packaging v26.3
    ├── pluggy v1.7.0
    └── pygments v2.21.0
```

Y el script, al final:

```
Grupos: {'dev': ['pytest==9.2.0']}
Paquetes en el lock: 7
  colorama==0.4.6
  iniconfig==2.3.1
  packaging==26.3
  pluggy==1.7.0
  pygments==2.21.0
  pytest==9.2.0
  sondeo==0.1.0
```

Pediste un paquete; el lock fija siete, cada uno con su versión exacta: pytest, sus cuatro dependencias, el propio `sondeo` y `colorama`. `colorama` no aparece en `uv tree` ni se instaló, porque pytest solo lo necesita **en Windows**. El lock es **universal**: vale para Linux, macOS y Windows a la vez, y cada máquina instala la parte que le toca. Abre `sondeo/uv.lock`: es un TOML largo, que escribe uv y nunca tú.

### 4. Un rango en `pyproject.toml`, una versión en el lock

```bash
cd sondeo
uv add --dev "ruff>=0.17,<0.18"
grep ruff pyproject.toml
grep -A1 'name = "ruff"' uv.lock
```

```
    "ruff>=0.17,<0.18",
name = "ruff"
version = "0.17.4"
```

En `pyproject.toml` escribiste un **rango**: cualquier ruff de la serie 0.17. En `uv.lock`, uv apuntó **una** versión, la más reciente que cabía en el rango cuando lo ejecutaste (0.17.4 cuando se escribió este ejercicio: la tuya puede ser otra). Desde ahora, `uv sync` instala esa versión exacta en cualquier máquina, hasta que alguien ejecute `uv lock --upgrade`. El rango dice qué admites; el lock, qué usas. En el bootcamp se fija con `==` también en `pyproject.toml`, para que lo que lees en el README sea lo que instalas.

Quita ruff:

```bash
uv remove --dev ruff
cd ..
```

`uv remove` lo borra de `pyproject.toml`, de `uv.lock` y de `.venv`. Ejecuta `uv run python inspect_project.py`: vuelven a ser 7 paquetes.

### 5. La versión y el *wheel*

```bash
cd sondeo
uv version --bump minor
uv build
cd ..
```

```
sondeo 0.1.0 => 0.2.0
...
Successfully built dist/sondeo-0.2.0.tar.gz
Successfully built dist/sondeo-0.2.0-py3-none-any.whl
```

`uv version --bump minor` sube el número del medio en `pyproject.toml`, en el único sitio donde vive la versión. `uv build` crea en `dist/` el código fuente (`.tar.gz`) y el *wheel* (`.whl`). El nombre del *wheel* dice qué es: `sondeo`, versión `0.2.0`, para cualquier Python 3 (`py3`), sin código compilado (`none`) y para cualquier sistema (`any`).

Descomenta el **PASO 4**:

```
Wheel: sondeo-0.2.0-py3-none-any.whl
   sondeo/
   sondeo/__init__.py
   sondeo-0.2.0.dist-info/
   sondeo-0.2.0.dist-info/WHEEL
   sondeo-0.2.0.dist-info/entry_points.txt
   sondeo-0.2.0.dist-info/METADATA
   sondeo-0.2.0.dist-info/RECORD
   Name: sondeo
   Version: 0.2.0
   Requires-Python: >=3.14.10
```

Un *wheel* es un zip: tu paquete tal cual, sin `src/`, y una carpeta `.dist-info` con los metadatos. `METADATA` lleva lo que escribiste en `[project]`; `entry_points.txt`, los comandos de `[project.scripts]`. No viajan los tests, ni `.venv`, ni `uv.lock`. Es lo que `importlib.metadata.version("observatorio")` lee en el proyecto: los metadatos del paquete instalado.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `FileNotFoundError: ... sondeo/pyproject.toml` | No hiciste el paso 1, o creaste `sondeo` en otra carpeta: tiene que estar dentro de `starter/` |
| `Adding sondeo as member of workspace` | Faltó `--no-workspace`: borra `sondeo/` y la tabla `[tool.uv.workspace]` que se añadió al final del `pyproject.toml` de `starter/` |
| `error: Cannot initialize a project in .../sondeo because pyproject.toml already exists` | Ya existe `sondeo/`: bórrala con `rm -rf sondeo` si quieres empezar de nuevo |
| `StopIteration` en el paso 4 | No hay *wheel*: ejecuta `uv build` dentro de `sondeo/` |
| `uv add` dentro de `starter/` en lugar de `sondeo/` | Cambiaste el ejercicio y no `sondeo`: `uv remove --dev pytest` en `starter/`, después `cd sondeo` |
| Otra versión de `ruff` en el paso 4 | Es lo esperado: el rango admite la más reciente de la serie 0.17 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Paquetes](../ejercicio-02-paquetes/README.md) | **Ejercicio 03 · `pyproject.toml` y dependencias** | [Ejercicio 04 · ruff](../ejercicio-04-ruff/README.md) |
