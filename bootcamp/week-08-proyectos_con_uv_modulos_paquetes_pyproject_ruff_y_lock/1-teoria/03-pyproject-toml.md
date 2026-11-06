# 03 · `pyproject.toml`

⏱️ 50 min

## 🎯 Objetivos

- Leer y escribir TOML: tablas, claves, textos, listas y tablas en línea.
- Explicar cada tabla del `pyproject.toml` de tu Observatorio y qué herramienta la lee.
- Declarar comandos con `[project.scripts]`.
- Versionar el proyecto con un único número y leerlo con `importlib.metadata`.
- Leer un TOML desde Python con `tomllib`.

---

## 1. Un archivo para todo el proyecto

`pyproject.toml` es la ficha del proyecto: cómo se llama, qué versión es, qué Python necesita, de qué depende, cómo se construye y cómo se configuran sus herramientas. Lo definen varias PEP (518, 621, 735) y lo entienden uv, pip, pytest, ruff, mypy y casi cualquier herramienta moderna de Python. Antes, cada herramienta tenía su archivo (`setup.py`, `setup.cfg`, `requirements.txt`, `pytest.ini`, `mypy.ini`...). Hoy, uno.

## 2. TOML en cinco minutos

TOML (*Tom's Obvious Minimal Language*) es un formato de configuración pensado para leerse y escribirse a mano:

```toml
# Un comentario
name = "observatorio"              # clave = valor; los textos, entre comillas
version = "0.8.0"
line-length = 100                  # un número
package = false                    # un booleano: true o false, en minúscula
dev = ["pytest==9.2.0", "ruff==0.17.3"]   # una lista

[project]                          # una tabla: las claves de debajo son suyas
name = "observatorio"

[project.scripts]                  # una tabla dentro de otra: project → scripts
observatorio = "observatorio.__main__:main"

[[package]]                        # una lista de tablas: cada [[package]] añade una
name = "pytest"
```

Una tabla dura hasta la siguiente cabecera `[...]`. Por eso el orden importa: una clave escrita debajo de `[tool.ruff]` es de ruff, aunque quisieras otra cosa. Desde Python, una tabla es un diccionario:

```python
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as file:   # tomllib pide el archivo en binario
    pyproject = tomllib.load(file)

print(pyproject["project"]["version"])            # 0.8.0
print(pyproject["tool"]["ruff"]["line-length"])   # 100
```

`tomllib` está en la biblioteca estándar desde Python 3.11 y solo lee. Para escribir TOML no hay módulo estándar: a `pyproject.toml` lo escribes tú, o `uv add`.

## 3. El `pyproject.toml` del Observatorio, tabla a tabla

```toml
[project]
name = "observatorio"
version = "0.8.0"
description = "Observatorio de datos de mi dominio"
readme = "README.md"
requires-python = ">=3.14,<3.15"
dependencies = []

[project.scripts]
observatorio = "observatorio.__main__:main"

[dependency-groups]
dev = [
    "mypy==2.4.1",
    "pytest==9.2.0",
    "ruff==0.17.3",
]

[build-system]
requires = ["uv_build==0.13.7"]
build-backend = "uv_build"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100

[tool.mypy]
files = ["src", "tests"]
```

| Tabla | Qué dice | Quién la lee |
|---|---|---|
| `[project]` | Los metadatos: nombre, versión, Python, dependencias **del programa** | uv, al instalar; `uv_build`, al construir el paquete |
| `[project.scripts]` | Los comandos que crea la instalación | `uv_build`; uv los pone en `.venv/bin/` |
| `[dependency-groups]` | Dependencias **solo para desarrollar**: tests, lint, tipos | uv (`uv sync` instala el grupo `dev` por defecto) |
| `[build-system]` | Qué programa construye el paquete | uv, al instalar tu proyecto o al hacer `uv build` |
| `[tool.<herramienta>]` | La configuración de cada herramienta | Cada una lee la suya y no mira las demás |

`dependencies` frente a `dependency-groups`: si tu programa hace `import httpx` al ejecutarse (semana 18), `httpx` va en `dependencies`, porque sin él no funciona. pytest, ruff y mypy los usas tú mientras desarrollas; quien instala tu *wheel* no los necesita, y no se los lleva.

## 4. Comandos: `[project.scripts]`

```toml
[project.scripts]
observatorio = "observatorio.__main__:main"
```

A la izquierda, el nombre del comando. A la derecha, `módulo:función`: al instalar el paquete, se crea un pequeño programa `observatorio` en `.venv/bin/` que importa `observatorio.__main__` y llama a `main()`. Lo que devuelve `main` es el código de salida. Por eso `uv run observatorio` funciona, y por eso, en Docker, `observatorio` funciona sin `uv run`: `/opt/venv/bin` está en el `PATH`.

## 5. La versión

`version = "0.8.0"` sigue el **versionado semántico** (*SemVer*), `MAYOR.MENOR.PARCHE`:

| Sube | Cuándo | Ejemplo |
|---|---|---|
| PARCHE | Arreglas un bug sin cambiar la API | `0.8.0` → `0.8.1` |
| MENOR | Añades algo sin romper lo que había | `0.8.0` → `0.9.0` |
| MAYOR | Rompes algo: quien te usa tiene que cambiar su código | `1.4.2` → `2.0.0` |

Mientras el MAYOR es `0`, el proyecto avisa de que todavía no es estable y cualquier versión puede romper cosas. Tu Observatorio usa `0.<semana>.0` hasta el capstone.

La versión se escribe **en un solo sitio**. Si también la escribieras en `__init__.py`, tarde o temprano dirían cosas distintas. El paquete la lee de sus propios metadatos de instalación:

```python
from importlib.metadata import version

__version__ = version("observatorio")
```

`importlib.metadata.version` busca el paquete instalado en el entorno y lee su `METADATA`, que `uv_build` escribió a partir de `[project]`. Para cambiar la versión, editas `pyproject.toml` o ejecutas `uv version --bump minor`, y el siguiente `uv run` reinstala el paquete con los metadatos nuevos. Si el paquete no está instalado (ejecutas el código con `python` fuera del entorno), da `PackageNotFoundError: No package metadata was found for observatorio`.

## 6. `requires-python`

`requires-python = ">=3.14,<3.15"` dice con qué Python funciona tu proyecto. uv lo usa para elegir el intérprete y para resolver dependencias: solo acepta versiones de bibliotecas que funcionen en ese rango. Es distinto de `.python-version` (`3.14.10`), que dice qué Python exacto usas tú para desarrollar. El primero es una promesa para quien instala tu paquete; el segundo, tu elección en tu máquina.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TOML parse error at line N` | Falta una comilla, una coma en una lista o un `]` | Lee la línea que dice el mensaje |
| Una opción no hace efecto | Está debajo de otra tabla: el orden de las cabeceras manda | Muévela bajo su `[tool.xxx]` |
| `TypeError: File must be opened in binary mode` | `tomllib.load` con un archivo abierto en texto | `open("rb")` |
| `--version` dice una versión vieja | Escribiste la versión a mano en el código | `version("observatorio")` |
| `PackageNotFoundError` | El paquete no está instalado en el entorno que usas | Ejecuta con `uv run` |
| `error: Failed to spawn: observatorio` | El comando no está en `[project.scripts]` o el proyecto tiene `package = false` | Revisa la tabla y quita `package = false` |

---

## ✅ Qué debes saber al terminar

- [ ] Escribir tablas, listas y tablas anidadas en TOML, y leerlas con `tomllib`.
- [ ] Qué dice cada tabla del `pyproject.toml` del Observatorio y quién la lee.
- [ ] La diferencia entre `dependencies` y `dependency-groups`.
- [ ] Cómo se convierte `observatorio = "observatorio.__main__:main"` en un comando.
- [ ] Qué significa cada número de `0.8.0` y por qué la versión se escribe en un solo sitio.
- [ ] La diferencia entre `requires-python` y `.python-version`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Paquetes](02-paquetes.md) | **03 · `pyproject.toml`** | [04 · Dependencias y lock](04-dependencias-y-lock.md) |
