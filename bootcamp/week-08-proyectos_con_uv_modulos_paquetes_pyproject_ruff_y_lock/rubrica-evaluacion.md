# Rúbrica de Evaluación — Semana 08: Proyectos con uv: módulos, paquetes, `pyproject.toml`, ruff y lock

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 7 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | `units.py` tiene un `print` fuera de las funciones. Si tres archivos de un programa hacen `import units`, ¿cuántas veces sale el `print`? ¿Por qué? | 10 |
| 2 | ¿Qué vale `__name__` en un archivo que ejecutas y en uno que importas? ¿Para qué sirve `if __name__ == "__main__":`? | 10 |
| 3 | Creas un archivo `csv.py` en tu proyecto y otro módulo hace `import csv; csv.reader(...)`. ¿Qué pasa y por qué? | 10 |
| 4 | ¿Qué gana quien usa tu paquete si `core/__init__.py` reexporta `median`? ¿Qué hace `__all__` y qué **no** hace? | 10 |
| 5 | ¿Por qué el proyecto pone el paquete dentro de `src/` en lugar de en la raíz? | 10 |
| 6 | ¿Qué diferencia hay entre `dependencies` y `[dependency-groups]`? ¿Dónde va pytest y dónde iría `httpx` si tu programa lo importa al ejecutarse? | 10 |
| 7 | ¿Por qué la versión se escribe solo en `pyproject.toml` y se lee con `importlib.metadata.version`? ¿Qué número subes si añades `--version` sin romper nada, partiendo de `0.8.0`? | 10 |
| 8 | En `pyproject.toml` pone `ruff>=0.17,<0.18`. ¿Qué versión se instala en tu máquina y en la de una compañera que clona tu repositorio dentro de un mes? ¿Qué papel tiene `uv.lock`? | 10 |
| 9 | Editas `pyproject.toml` a mano y construyes la imagen Docker. ¿Qué pasa con `uv sync --locked` y por qué es lo que quieres? | 10 |
| 10 | ¿Qué diferencia hay entre `ruff check` y `ruff format`? ¿Por qué `--fix` no arregla `B006` en `def f(x, items=[])`, y qué bug es? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Una vez. El primer `import` busca el archivo, lo ejecuta y guarda el módulo en `sys.modules`; los siguientes encuentran el módulo ahí y lo reutilizan sin ejecutar nada.
2. `"__main__"` en el que ejecutas y el nombre del módulo (`"units"`) en el importado. El bloque `if __name__ == "__main__":` solo se ejecuta cuando lanzas el archivo, nunca al importarlo: un módulo puede llevar una prueba rápida o ser a la vez programa, como el `__main__.py` del Observatorio, que los tests importan sin ejecutar `main`.
3. `import csv` encuentra **tu** `csv.py` antes que el de la biblioteca estándar, porque la carpeta del script va primero en `sys.path`. Tu archivo no tiene `reader` y sale `AttributeError: module 'csv' has no attribute 'reader'`, con la pista de Python 3.14 de renombrarlo. Se arregla cambiando el nombre de tu archivo.
4. Puede escribir `from observatorio.core import median` sin saber que vive en `trends.py`, y tú puedes mover `median` de módulo cambiando solo el `__init__.py`. `__all__` dice qué nombres son la API pública y qué trae `from observatorio.core import *`; no esconde nada: `observatorio.core.trends.jumps` sigue accesible.
5. Para que la única forma de importar `observatorio` sea instalarlo. Sin `src/`, los tests importarían la carpeta suelta de la raíz y podrían pasar con un paquete construido roto. Con `src/`, prueban lo mismo que se instala; `uv sync` lo instala en modo editable, así que los cambios se ven al momento.
6. `dependencies` son las que el programa necesita para funcionar, y viajan con el paquete. `[dependency-groups]` son solo para desarrollar, y quien instala el *wheel* no las recibe. pytest va en el grupo `dev`; `httpx` iría en `dependencies`.
7. Para que haya un solo sitio donde cambiarla: si también se escribiera en el código, tarde o temprano dirían cosas distintas. `importlib.metadata.version` la lee de los metadatos del paquete instalado, que salen de `pyproject.toml`. Añadir algo sin romper sube el MENOR: `0.9.0`.
8. La misma en las dos máquinas: la que quedó apuntada en `uv.lock` cuando se resolvió (por ejemplo 0.17.4), aunque salga una 0.17.5. El rango dice qué se admite; el lock, qué se usa. Solo cambia si alguien ejecuta `uv lock --upgrade` (o `--upgrade-package ruff`) y sube el lock nuevo.
9. Falla con "The lockfile at `uv.lock` needs to be updated, but `--locked` was provided" y la imagen no se construye. Es lo que quieres: una imagen nunca se construye con dependencias distintas de las que probaste. Se arregla con `uv lock` y un commit de los dos archivos.
10. `ruff check` busca errores probables y malas prácticas; `ruff format` solo cambia la forma y nunca lo que hace el código. El arreglo de `B006` es inseguro, porque cambia el comportamiento: el `[]` por defecto se crea una sola vez, al definir la función, y todas las llamadas comparten la misma lista, así que cada una ve lo que añadieron las anteriores. Se arregla con `items: list[int] | None = None` y creando la lista dentro.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-08` muestra un commit por paso (dependencias, mover, API, versión, configuración, arreglos, formato, tests), sin cambiar los tests del bootcamp | 8 |
| Historial conservado | Los módulos se movieron con `git mv`: `git log --follow src/observatorio/core/record.py` llega hasta la semana 1 | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy`, `uv lock --check` y `--version`, en su máquina y en Docker | 8 |
| Rompe y explica | Desincroniza el lock a mano y explica el error de `uv lock --check`; deja un import con el camino viejo y explica el `ModuleNotFoundError` | 10 |
| Explica sus decisiones | Explica qué encontró ruff en su código, por qué el commit de formato va separado y por qué sus tests de `test_my_core.py` importan solo de `observatorio.core` | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 7

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Paquete y API | Los siete módulos en `observatorio.core`, con `__init__.py` y `__all__`; pasan los 36 tests de `test_package.py` y `test_main.py`, y los de las semanas anteriores siguen en verde | 30 |
| Versión | `version = "0.8.0"` solo en `pyproject.toml`, leída con `importlib.metadata`; `--version` y `-V` funcionan | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_core.py` con datos del dominio, que importan solo de `observatorio.core` (paso 11) | 20 |
| Herramientas | ruff y mypy fijados en el grupo `dev` y en `uv.lock`; `[tool.ruff]` y `[tool.mypy]` configurados; `ruff check`, `ruff format --check` y `mypy` sin avisos | 10 |
| Lock y Docker | `uv lock --check` en verde; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-08` en `python-<nombre>-<apellido>`, README con los comandos nuevos y el árbol del paquete | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, el árbol del paquete y lo que encontró ruff | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 09](../week-09-clases_y_dataclasses/README.md) |
