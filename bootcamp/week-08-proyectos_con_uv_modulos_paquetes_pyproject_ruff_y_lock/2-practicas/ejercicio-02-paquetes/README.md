# Ejercicio 02 — Paquetes

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-paquetes.md)

## Objetivo

Importar módulos de un paquete, decidir qué sube al `__init__.py`, controlar lo que exporta con `__all__`, usar un import relativo y ejecutar un paquete con `python -m`. Es el paquete `observatorio.core` del proyecto en pequeño. Ejercicio **guiado**: descomentas cada paso de `packages_lab.py` y de `meteo/__init__.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/2-practicas/ejercicio-02-paquetes/starter
uv run python packages_lab.py
```

```
Ejercicio 02 · Paquetes
```

El paquete es la carpeta `meteo/`:

```
meteo/
├── __init__.py    # se ejecuta al importar el paquete
├── __main__.py    # lo que ejecuta `python -m meteo`
├── convert.py     # c_to_f y una ayuda interna, _round1
└── stats.py       # mean y mean_f, que usan convert
```

## Pasos

### 1. Importar módulos de un paquete

Descomenta el **PASO 1** de `packages_lab.py` y ejecuta:

```
  [cargando el paquete meteo]
30 °C: 86.0 °F
Media: 20.5
Nombre completo: meteo.convert
¿meteo es un paquete? True
```

El camino a un módulo de un paquete va con puntos, `paquete.módulo`, igual que en el disco va con `/`. Antes de cargar `meteo.convert`, Python carga el paquete `meteo`, es decir, ejecuta su `__init__.py`: por eso la primera línea. Solo una vez, aunque luego se importe `meteo.stats`. El nombre completo del módulo es `meteo.convert`, y un paquete se distingue de un módulo porque tiene `__path__`, la carpeta donde buscar sus módulos.

### 2. Lo que reexporta el `__init__.py`

Descomenta solo el **PASO 2** de `packages_lab.py` y ejecuta:

```
ImportError: cannot import name 'c_to_f' from 'meteo' (.../meteo/__init__.py)
```

`c_to_f` vive en `meteo.convert`, no en `meteo`. Ahora descomenta también el **PASO 2** de `meteo/__init__.py` y ejecuta:

```
Desde el paquete: 212.0
¿La misma función? True
```

El `__init__.py` importa los nombres importantes de sus módulos, y con eso pasan a ser nombres del paquete: `from meteo import c_to_f`. Quien usa el paquete no necesita saber en qué módulo vive cada función, y tú puedes moverla de módulo sin romperle nada. Es la misma función, no una copia.

### 3. `__all__`

Antes de tocar nada, prueba qué trae un `import *`:

```bash
uv run python -c "from meteo import *; print(sorted(n for n in dir() if not n.startswith('_')))"
```

```
  [cargando el paquete meteo]
['c_to_f', 'convert', 'mean', 'stats']
```

Sin `__all__`, `*` trae todo lo que no empieza por `_`, también los **módulos** `convert` y `stats`, que quedaron como nombres del paquete al importarlos. Descomenta el **PASO 3** de `meteo/__init__.py`, después el de `packages_lab.py`, y ejecuta los dos comandos:

```bash
uv run python packages_lab.py
uv run python -c "from meteo import *; print(sorted(n for n in dir() if not n.startswith('_')))"
```

```
Nombres públicos de meteo: ['c_to_f', 'convert', 'mean', 'stats']
Su __all__: ['c_to_f', 'mean']
```

```
  [cargando el paquete meteo]
['c_to_f', 'mean']
```

`__all__` no esconde nada: `meteo.convert` sigue ahí. Dice qué nombres son la API pública del paquete, y es lo que trae `from meteo import *`. En tu código no escribirás `import *` (no se sabe qué nombres llegan), pero `__all__` sirve igual de lista oficial. En el proyecto, un test comprueba que cada nombre de la lista existe.

### 4. Un import relativo

Abre `meteo/stats.py`: empieza con `from .convert import _round1, c_to_f`. El punto significa "el paquete en el que estoy". Ejecuta el módulo como un archivo suelto:

```bash
uv run python meteo/stats.py
```

```
ImportError: attempted relative import with no known parent package
```

Ejecutado así, `stats.py` es el archivo principal, sin paquete: el `.` no apunta a ningún sitio. Ejecútalo como módulo **del paquete**, con `-m` y el camino con puntos:

```bash
uv run python -m meteo.stats
```

```
  [cargando el paquete meteo]
Prueba rápida de stats: 20.5
```

Con `-m`, Python carga primero el paquete `meteo` y después `meteo.stats` como `"__main__"`. Por eso en el proyecto se usan imports absolutos (`from observatorio.core.record import ...`): funcionan igual se ejecute como se ejecute.

### 5. Un paquete que se ejecuta

```bash
uv run python -m meteo
```

```
  [cargando el paquete meteo]
meteo como programa: media de 20, 22,5 y 19 = 20.5
```

`python -m paquete` ejecuta el `__main__.py` del paquete. Es lo que hace el `__main__.py` de tu Observatorio: `uv run python -m observatorio` funciona igual que `uv run observatorio`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'meteo'` | Ejecutas desde otra carpeta: `cd` a `starter/` |
| `ImportError: cannot import name 'c_to_f' from 'meteo'` | Falta descomentar el PASO 2 de `meteo/__init__.py`: es lo que muestra el paso 2 |
| `AttributeError: module 'meteo' has no attribute '__all__'` | Falta descomentar el PASO 3 de `meteo/__init__.py` |
| `ImportError: attempted relative import with no known parent package` | Ejecutaste un módulo del paquete como archivo: usa `python -m meteo.stats` |
| `No module named meteo.__main__; 'meteo' is a package and cannot be directly executed` | Falta `meteo/__main__.py`, o lo renombraste |
| `[cargando el paquete meteo]` no sale | Has borrado el `print` del `__init__.py`: no pasa nada, solo era una señal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Módulos e imports](../ejercicio-01-modulos-e-imports/README.md) | **Ejercicio 02 · Paquetes** | [Ejercicio 03 · `pyproject.toml` y dependencias](../ejercicio-03-pyproject-y-dependencias/README.md) |
