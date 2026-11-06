# Semana 08 — Proyectos con uv: módulos, paquetes, `pyproject.toml`, ruff y lock

> Tu Observatorio ya calcula, lee archivos y falla bien. Esta semana no aprende nada nuevo sobre tus datos: se ordena por dentro y gana las herramientas de un proyecto profesional. Los módulos pasan a un paquete `core` con una API pública, la versión vive en un solo sitio, ruff y mypy quedan fijados en el lock, y `uv build` produce un paquete que se instala en cualquier máquina. Es el cierre de la fase 1: lo que construyas en la fase 2 se apoya en esta estructura.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Explicar** qué hace un `import`, dónde busca Python los módulos y por qué un módulo se ejecuta una sola vez
- **Organizar** módulos en paquetes y **definir** una API pública con `__init__.py` y `__all__`
- **Leer** y **escribir** `pyproject.toml`: metadatos, comandos, grupos de dependencias y configuración de herramientas
- **Gestionar** dependencias con `uv add`, `uv remove` y `uv.lock`, y **explicar** por qué el lock hace el proyecto reproducible
- **Revisar** y **formatear** código con ruff, y **configurarlo** en `pyproject.toml`
- **Construir** un *wheel* con `uv build` y **versionar** el proyecto con SemVer

---

## 📋 Prerrequisitos

- [Semana 07](../week-07-pathlib_json_csv_excepciones_y_context_managers/README.md): `pathlib`, JSON, CSV, excepciones y context managers.
- El *pull request* `week-07` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 7 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Módulos e imports](1-teoria/01-modulos-e-imports.md) | Qué hace `import`, `sys.modules`, formas de importar, `__name__`, `sys.path`, imports circulares | 50 min |
| [02 · Paquetes](1-teoria/02-paquetes.md) | Paquetes y subpaquetes, `__init__.py`, reexportar, `__all__`, imports relativos, `python -m`, estructura `src/` | 45 min |
| [03 · `pyproject.toml`](1-teoria/03-pyproject-toml.md) | TOML, cada tabla y quién la lee, `[project.scripts]`, SemVer, `importlib.metadata`, `requires-python` | 50 min |
| [04 · Dependencias y lock](1-teoria/04-dependencias-y-lock.md) | Especificadores, `uv add`/`remove`/`tree`, `uv.lock`, `--locked` y `--check`, actualizar, `uvx` | 45 min |
| [05 · ruff](1-teoria/05-ruff.md) | *Linter* y *formatter*, familias de reglas, arreglos seguros e inseguros, `# noqa`, configuración | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Módulos e imports](2-practicas/ejercicio-01-modulos-e-imports/README.md) | El caché de módulos, `from` y `as`, `__name__`, `sys.path` y un archivo que tapa la biblioteca estándar | 1 h 30 min |
| [02 · Paquetes](2-practicas/ejercicio-02-paquetes/README.md) | Módulos de un paquete, reexportar en `__init__.py`, `__all__`, un import relativo y `python -m` | 1 h 30 min |
| [03 · `pyproject.toml` y dependencias](2-practicas/ejercicio-03-pyproject-y-dependencias/README.md) | `uv init`, leer `pyproject.toml` y `uv.lock` con `tomllib`, rango frente a lock, `uv build` y el *wheel* por dentro | 1 h 30 min |
| [04 · ruff](2-practicas/ejercicio-04-ruff/README.md) | Avisos, `ruff rule`, `--fix` y arreglos a mano, un bug que encuentra ruff, `ruff format` y más reglas | 1 h |

### Proyecto

El Observatorio pasa a ser un paquete de verdad: los siete módulos se mudan a `observatorio.core`, que expone su API pública con `__all__`; la versión `0.8.0` se lee de `pyproject.toml` y sale con `--version`; ruff y mypy entran en el grupo `dev`, configurados en `pyproject.toml`. El informe no cambia ni un carácter. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Ver dónde está un módulo | `uv run python -c "import statistics; print(statistics.__file__)"` |
| Ver dónde busca Python | `uv run python -c "import sys; print(*sys.path, sep='\n')"` |
| Encontrar imports con un camino viejo | `grep -rnE "from observatorio\.(analysis\|groups\|record\|report\|rules\|storage\|trends) import" src tests` |
| Ver qué versiones tienen actualización | `uv tree --outdated --depth 1` |
| Comprobar que el lock está al día | `uv lock --check` |
| Lint, formato y tipos de una vez | `uv run ruff check && uv run ruff format --check && uv run mypy` |
| Saber qué significa un aviso de ruff | `uv run ruff rule F401` |
| Mover un archivo sin perder su historial | `git mv viejo.py carpeta/` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-08` de `python-<nombre>-<apellido>` con el paquete `observatorio.core`, la versión `0.8.0` y `--version`, ruff y mypy en el grupo `dev` del lock, su configuración en `pyproject.toml` y al menos 6 tests propios en `tests/test_my_core.py`, todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check` y `mypy` sin avisos
2. ✅ `README.md` del repositorio con los comandos nuevos y el árbol del paquete
3. ✅ Pull request `week-08` → `main` con tests, `mypy`, `ruff`, el árbol del paquete y lo que encontró ruff

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv lock --check
uv run observatorio --version
docker compose run --build --rm app
```

Los tests terminan en `passed` sin `failed`, ruff dice `All checks passed!` y `N files already formatted`, `mypy` dice `Success: no issues found`, `uv lock --check` termina sin error y `--version` escribe `observatorio 0.8.0`. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 07](../week-07-pathlib_json_csv_excepciones_y_context_managers/README.md) | **Semana 08** | [Semana 09](../week-09-clases_y_dataclasses/README.md) |

← [Volver al índice de semanas](../README.md)
