# Webgrafía — Semana 08

| Recurso | Para qué |
|---|---|
| [Módulos — tutorial](https://docs.python.org/es/3.14/tutorial/modules.html) (en español) | Módulos, `__name__`, `sys.path` y paquetes con `__init__.py` y `__all__`: la teoría 01 y la 02 en la documentación oficial |
| [El sistema de importación](https://docs.python.org/es/3.14/reference/import.html) (en español) | Para quien quiera el detalle: `sys.modules`, cómo se buscan y cargan los módulos, imports relativos |
| [Módulo `tomllib`](https://docs.python.org/es/3.14/library/tomllib.html) (en español) | `load` y `loads`, y la tabla de conversión de tipos TOML a Python |
| [Módulo `importlib.metadata`](https://docs.python.org/es/3.14/library/importlib.metadata.html) (en español) | `version` y el resto de metadatos de un paquete instalado: dependencias, comandos, archivos |
| [Escribir tu `pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) (en inglés) | Cada clave de `[project]` explicada, de la guía oficial de empaquetado |
| [src layout frente a flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) (en inglés) | Por qué tu proyecto tiene `src/`, en una página |
| [uv: estructura de un proyecto](https://docs.astral.sh/uv/concepts/projects/layout/) (en inglés) | `pyproject.toml`, `.venv` y `uv.lock`, y qué va a Git |
| [uv: dependencias](https://docs.astral.sh/uv/concepts/projects/dependencies/) (en inglés) | `uv add` y `uv remove`, `dependencies` y `dependency-groups`, especificadores de versión |
| [uv: lock y sync](https://docs.astral.sh/uv/concepts/projects/sync/) (en inglés) | Cuándo uv actualiza el lock, `--locked`, `--frozen` y cómo subir versiones |
| [uv: construir paquetes](https://docs.astral.sh/uv/concepts/projects/build/) (en inglés) | `uv build`, *wheels* y distribuciones de código fuente |
| [Ruff: el *linter*](https://docs.astral.sh/ruff/linter/) (en inglés) | `ruff check`, arreglos seguros e inseguros, `# noqa` y la selección de reglas |
| [Ruff: el *formatter*](https://docs.astral.sh/ruff/formatter/) (en inglés) | `ruff format`, `--check` y `--diff`, y en qué se parece a black |
| [Ruff: reglas](https://docs.astral.sh/ruff/rules/) (en inglés) | El catálogo completo, por familias: busca aquí cualquier código que te salga |
| [Ruff: configuración](https://docs.astral.sh/ruff/configuration/) (en inglés) | `[tool.ruff]` y `[tool.ruff.lint]` con ejemplos |
| [Especificación de TOML 1.0](https://toml.io/en/v1.0.0) (en inglés) | El formato entero en una página: tablas, listas de tablas, tipos |
| [Versionado semántico](https://semver.org/lang/es/) (en español) | Qué significa cada número de `0.8.0` y cuándo subir cada uno |
| [PEP 8](https://peps.python.org/pep-0008/) (en inglés) | La sección "Imports": orden, absolutos frente a relativos y por qué no `import *` |
| [PEP 735 — Grupos de dependencias](https://peps.python.org/pep-0735/) (en inglés) | La propuesta que añadió `[dependency-groups]` a `pyproject.toml` |
| [Extensión Ruff para VS Code](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) (en inglés) | Avisos mientras escribes y formato al guardar, con la configuración de tu `pyproject.toml` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto · Observatorio, capa 7](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
