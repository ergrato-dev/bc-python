# Ejercicio 01 — Hola, entorno

⏱️ 2 h · Teoría previa: [02](../../1-teoria/02-del-codigo-a-la-ejecucion.md), [03](../../1-teoria/03-uv-proyectos-y-entornos.md) y [05](../../1-teoria/05-variables-y-tipos.md)

## Objetivo

Comprobar que uv usa Python 3.14.10, pasar de 4 tests en rojo a 5 en verde, usar el REPL y provocar a propósito los dos tipos de error.

## Antes de empezar

Abre una terminal (en Windows, la de Ubuntu en WSL2) y entra en el starter. Todos los comandos de este ejercicio se escriben **dentro de `starter/`**:

```bash
cd bootcamp/week-01-entorno_docker_uv_y_tipos/2-practicas/ejercicio-01-hola-entorno/starter
ls -A
```

Debes ver: `.python-version  main.py  pyproject.toml  tests  uv.lock`.

## Pasos

### 1. Comprueba la toolchain

```bash
uv --version
uv run python --version
```

Salida esperada:

```
uv 0.13.7
Python 3.14.10
```

La primera vez, uv descarga Python 3.14.10 si no lo tenías y crea `.venv/` dentro del starter; antes de la versión muestra líneas como `Creating virtual environment at: .venv` e `Installed 5 packages`. Comprueba que existe con `ls -A`. Anota las dos líneas en `NOTAS.md` (créalo en `starter/`).

### 2. Mira qué se instaló y desde dónde

`uv run` del paso 1 ya creó el entorno e instaló las dependencias del lock. Compruébalo:

```bash
uv sync --locked
uv tree
```

Salida esperada:

```
Resolved 7 packages in ...
Checked 5 packages in ...
Resolved 7 packages in ...
hola-entorno v0.1.0
└── pytest v9.2.0 (group: dev)
    ├── iniconfig v2.3.1
    ├── packaging v26.3
    ├── pluggy v1.7.0
    └── pygments v2.21.0
```

`Checked 5 packages` significa que `.venv/` ya coincide con el lock y no hay nada que instalar. Abre `pyproject.toml`: solo pide `pytest==9.2.0`. Responde en `NOTAS.md`: ¿de dónde salen los otros cuatro paquetes y en qué archivo están fijadas sus versiones?

### 3. Mira el estado inicial: tests en rojo

```bash
uv run pytest
```

Al final verás:

```
4 failed, 1 passed in 0.03s
```

Los 4 fallos dicen `NotImplementedError`: las funciones aún no hacen nada. El que pasa (`test_python_is_the_pinned_version`) comprueba que uv usa la versión fijada. Así se ve un test en rojo: es el punto de partida de cada ejercicio del bootcamp.

### 4. Implementa `greet`

Abre `main.py` en VS Code (`code .`). Sustituye la línea `raise NotImplementedError("Paso 4: implementa greet")` por:

```python
    name = name.strip()
    if name == "":
        return "Hola, mundo"
    return f"Hola, {name}"
```

Fíjate en la sangría: 4 espacios, dentro de la función. Línea a línea:

1. `name.strip()` quita los espacios de los lados; el resultado se guarda otra vez en `name`.
2. Si el nombre quedó vacío, devuelve `"Hola, mundo"` y la función termina ahí.
3. Si no, devuelve el saludo con el nombre (una f-string, teoría 05).

Ejecuta solo los tests de `greet`, con `-k` (filtra por nombre):

```bash
uv run pytest -k greet
```

Salida esperada: `3 passed, 2 deselected`.

### 5. Implementa `python_summary`

La función debe devolver `"Python 3.14.10"`. El archivo ya importa el módulo `platform` (primera línea), que trae `platform.python_version()`. Pruébalo antes en el REPL:

```bash
uv run python
```

```python
>>> import platform
>>> platform.python_version()
'3.14.10'
>>> f"Python {platform.python_version()}"
'Python 3.14.10'
>>> exit
```

Ahora sustituye el `raise NotImplementedError(...)` de `python_summary` por un `return` con esa f-string. Ejecuta todo:

```bash
uv run pytest
```

Salida esperada: `5 passed`. Y ejecuta el programa:

```bash
uv run python main.py
```

```
Hola, mundo
Python 3.14.10
```

### 6. Mira el bytecode

```bash
uv run python -m dis main.py
```

Busca el bloque `Disassembly of <code object greet ...>`. Responde en `NOTAS.md`: ¿qué instrucción aparece para el `if name == "":`? (Pista: busca `COMPARE_OP`.)

### 7. Provoca los dos tipos de error

**a) Error de sintaxis.** Al final de `main.py` añade la línea `print("adiós"` (sin cerrar el paréntesis) y ejecuta `uv run python main.py`. Copia en `NOTAS.md` la última línea del error. ¿Se imprimió `Hola, mundo` antes del error? ¿Por qué?

**b) Error en ejecución.** Cambia esa línea por `print(adios)` (sin comillas) y ejecuta otra vez. Copia la última línea del error. ¿Ahora sí se imprimió `Hola, mundo`? ¿Por qué?

Borra la línea y comprueba que `uv run pytest` vuelve a dar `5 passed`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `uv: command not found` | Instala uv según [`docs/setup.md`](../../../../docs/setup.md) y abre una terminal nueva |
| `uv --version` muestra otra versión | `uv self update 0.13.7` |
| `error: No 'project' table found` | No estás dentro de `starter/`: `cd` hasta la carpeta que tiene `pyproject.toml` |
| `IndentationError: expected an indented block` | La línea nueva no tiene 4 espacios de sangría |
| `test_python_is_the_pinned_version` falla | Borra `.venv/` (`rm -rf .venv`) y repite `uv sync --locked` |
| `ModuleNotFoundError: No module named 'main'` | Ejecutaste `pytest` sin `uv run`, o desde otra carpeta |

## Entrega

`uv run pytest` con 5 de 5 en verde, y `NOTAS.md` con las respuestas de los pasos 1, 2, 6 y 7.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Variables y tipos](../../1-teoria/05-variables-y-tipos.md) | **Ejercicio 01 · Hola, entorno** | [Ejercicio 02 · Python en Docker](../ejercicio-02-python-en-docker/README.md) |
