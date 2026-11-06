# Glosario — Semana 08

| Término | Definición |
|---|---|
| **`__all__`** | Lista de textos con los nombres públicos de un módulo o paquete; decide qué trae `from paquete import *` y documenta la API |
| **API pública** | Lo que un paquete promete que funciona: los nombres que exporta. Lo de dentro se puede reorganizar sin avisar |
| **Arreglo inseguro** (*unsafe fix*) | Corrección que ruff sabe hacer pero que podría cambiar el comportamiento; no se aplica con `--fix` a secas |
| **Build backend** | Programa que convierte el código en un paquete instalable; en tu proyecto, `uv_build`, declarado en `[build-system]` |
| **Dependencia directa** | La que pides tú en `pyproject.toml` |
| **Dependencia transitiva** | La que trae una de tus dependencias; también queda fijada en `uv.lock` |
| **`dependency-groups`** | Tabla de `pyproject.toml` con dependencias solo para desarrollar (tests, lint, tipos); no viajan con el paquete |
| **Entorno virtual** (`.venv`) | Carpeta con un Python y los paquetes de un proyecto, aislados del resto; se rehace con `uv sync` y nunca va a Git |
| ***Formatter*** | Herramienta que reescribe la forma del código (espacios, comillas, saltos de línea) sin cambiar lo que hace: `ruff format` |
| **Import absoluto** | Import con el camino completo desde el paquete de arriba: `from observatorio.core.record import parse_value` |
| **Import circular** | Dos módulos que se importan entre sí; uno pide un nombre al otro cuando este todavía está a medio cargar |
| **Import relativo** | Import con puntos que parte del paquete actual: `from .record import parse_value` |
| **`importlib.metadata`** | Módulo estándar que lee los metadatos de los paquetes instalados, como `version("observatorio")` |
| **`__init__.py`** | Archivo que convierte una carpeta en paquete; se ejecuta al importarlo y suele reexportar los nombres importantes |
| ***Linter*** | Herramienta que busca errores probables y malas prácticas sin ejecutar el código: `ruff check` |
| **Lock** (`uv.lock`) | Archivo con la versión exacta, el origen y el *hash* de cada dependencia; garantiza el mismo entorno en todas las máquinas |
| **`__main__.py`** | Archivo de un paquete que ejecuta `python -m paquete` |
| **Módulo** | Un archivo `.py`; su nombre sin extensión es el nombre con el que se importa |
| **`# noqa`** | Comentario que silencia un aviso de ruff en una línea; siempre con el código: `# noqa: F401` |
| **Paquete** | Carpeta de módulos con un `__init__.py`; puede contener subpaquetes |
| **`pyproject.toml`** | Archivo de configuración del proyecto: metadatos, dependencias, cómo se construye y la configuración de cada herramienta |
| **Reexportar** | Importar en el `__init__.py` nombres de los módulos de dentro para que el paquete los ofrezca directamente |
| **Reproducible** | Que da el mismo resultado en cualquier máquina y en cualquier momento; se consigue fijando versiones y con el lock |
| **`requires-python`** | Rango de versiones de Python con las que funciona el proyecto; distinto de `.python-version`, el Python exacto que usas tú |
| **Ruff** | *Linter* y *formatter* de Python escrito en Rust; sustituye a flake8, isort, pyupgrade y black |
| **SemVer** | Versionado semántico, `MAYOR.MENOR.PARCHE`: qué número sube según rompas, añadas o arregles |
| **src layout** | Estructura con el paquete dentro de `src/`: obliga a instalarlo para importarlo, y los tests prueban lo que se instala |
| **`sys.modules`** | Diccionario con los módulos ya cargados; un segundo `import` reutiliza el módulo de aquí |
| **`sys.path`** | Lista de carpetas donde `import` busca módulos, en orden: la del script, la biblioteca estándar y `site-packages` |
| **TOML** | Formato de configuración legible, con tablas `[...]`, claves y valores; es el de `pyproject.toml` y `uv.lock` |
| **`tomllib`** | Módulo estándar que lee TOML; abre el archivo en binario (`"rb"`) |
| **Wheel** (`.whl`) | Paquete listo para instalar: un zip con el código y una carpeta `.dist-info` con los metadatos |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
