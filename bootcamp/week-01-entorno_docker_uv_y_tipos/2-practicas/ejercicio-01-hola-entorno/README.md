# Ejercicio 01 — Hola, entorno

⏱️ 2 h · Teoría previa: [02](../../1-teoria/02-del-codigo-a-la-ejecucion.md), [03](../../1-teoria/03-uv-proyectos-y-entornos.md) y [05](../../1-teoria/05-variables-y-tipos.md)

## Objetivo

Comprobar que uv usa Python 3.14.10, ejecutar tu primer programa, usar el REPL y provocar a propósito los dos tipos de error. Es un ejercicio **guiado**: el código ya está escrito en `main.py`, comentado por pasos; tú lo descomentas, lo ejecutas y compruebas la salida. No se entrega.

## Antes de empezar

Abre una terminal (en Windows, la de Ubuntu en WSL2) y entra en el starter. Todos los comandos de este ejercicio se escriben **dentro de `starter/`**:

```bash
cd bootcamp/week-01-entorno_docker_uv_y_tipos/2-practicas/ejercicio-01-hola-entorno/starter
ls -A
```

Debes ver: `.python-version  main.py  pyproject.toml  uv.lock`.

**Cómo se descomenta**: en VS Code (`code .`), selecciona las líneas del paso y pulsa `Ctrl+K Ctrl+U` (en macOS `Cmd+K Cmd+U`). Quita solo el `# ` del principio de cada línea; la sangría que queda debe ser la del código (4 espacios dentro de una función).

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

La primera vez, uv descarga Python 3.14.10 si no lo tenías y crea `.venv/` dentro del starter; antes de la versión muestra líneas como `Creating virtual environment at: .venv`. Comprueba que existe con `ls -A`.

### 2. Mira el proyecto con los ojos de uv

```bash
uv sync --locked
uv tree
```

Salida esperada (los tiempos varían):

```
Resolved 1 package in 1ms
Checked in 0.01ms
Resolved 1 package in 1ms
hola-entorno v0.1.0
```

El único "paquete" es el propio ejercicio: no tiene dependencias. Abre `pyproject.toml` y `uv.lock` y relaciona cada línea con la teoría 03. En el proyecto de la semana aparece la primera dependencia (`pytest`) y verás cómo crece el lock.

### 3. Una función que saluda

Ejecuta el programa tal como viene:

```bash
uv run python main.py
```

```
Ejercicio 01 · Hola, entorno
```

Descomenta el bloque del **PASO 3** y ejecuta de nuevo:

```
Ejercicio 01 · Hola, entorno
Hola, Ana
Hola, mundo
```

Lee la función línea a línea:

1. `name.strip()` quita los espacios de los lados; el resultado se guarda otra vez en `name`.
2. Si el nombre quedó vacío, devuelve `"Hola, mundo"` y la función termina ahí.
3. Si no, devuelve el saludo con el nombre (una f-string, teoría 05).

Cambia `"Ana"` por tu nombre con espacios alrededor (`"  Luis  "`) y comprueba que el saludo sale limpio.

### 4. La versión del intérprete

Prueba antes en el REPL:

```bash
uv run python
```

```python
>>> import platform
>>> platform.python_version()
'3.14.10'
>>> exit
```

Descomenta el **PASO 4** y ejecuta:

```
Ejercicio 01 · Hola, entorno
Hola, Ana
Hola, mundo
Python 3.14.10
```

### 5. Mira el bytecode

```bash
uv run python -m dis main.py
```

Busca el bloque `Disassembly of <code object greet ...>` y, dentro, la instrucción `COMPARE_OP`: es el `name == ""` del `if`. Así ve tu código la máquina virtual de Python (teoría 02).

### 6. Provoca los dos tipos de error

**a) Error de sintaxis.** Al final de `main.py` añade la línea `print("adiós"` (sin cerrar el paréntesis) y ejecuta `uv run python main.py`. La última línea dice `SyntaxError: '(' was never closed` y **no se imprime nada**: Python compila el archivo entero antes de ejecutar la primera línea.

**b) Error en ejecución.** Cambia esa línea por `print(adios)` (sin comillas) y ejecuta otra vez. Ahora sí se imprimen las líneas anteriores y al final aparece `NameError: name 'adios' is not defined`: el archivo compiló bien y el error llegó al ejecutar esa línea.

Borra la línea y comprueba que el programa vuelve a dar la salida del paso 4.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `uv: command not found` | Instala uv según [`docs/setup.md`](../../../../docs/setup.md) y abre una terminal nueva |
| `uv --version` muestra otra versión | `uv self update 0.13.7` |
| `error: No 'project' table found` | No estás dentro de `starter/`: `cd` hasta la carpeta que tiene `pyproject.toml` |
| `IndentationError: unexpected indent` | Quitaste el `#` pero quedó un espacio de más al principio de la línea |
| `IndentationError: expected an indented block` | Quitaste también la sangría del cuerpo de la función: deben quedar 4 espacios |
| `NameError: name 'greet' is not defined` | Descomentaste el `print` pero no el `def` |
| La versión no es `3.14.10` | Borra `.venv/` (`rm -rf .venv`) y repite `uv sync --locked` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Variables y tipos](../../1-teoria/05-variables-y-tipos.md) | **Ejercicio 01 · Hola, entorno** | [Ejercicio 02 · Python en Docker](../ejercicio-02-python-en-docker/README.md) |
