# Rúbrica de Evaluación — Semana 01: Entorno, uv, Docker y tipos

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 0 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué diferencia hay entre Python y CPython? | 10 |
| 2 | Nombra las tres fases que sigue CPython para ejecutar `main.py`. ¿En cuál salta un `SyntaxError` y en cuál un `NameError`? | 10 |
| 3 | ¿Qué contiene `uv.lock` que no contiene `pyproject.toml`? ¿Cuál de los dos, junto con `.venv/`, va al repositorio? | 10 |
| 4 | ¿Qué hace `uv sync --locked` si `pyproject.toml` cambió y `uv.lock` no? ¿Por qué lo queremos así en Docker? | 10 |
| 5 | En el `Dockerfile` del curso, ¿por qué se copian `pyproject.toml` y `uv.lock` antes que el resto del código? | 10 |
| 6 | ¿Qué riesgo hay en que un contenedor corra como root, y con qué dos líneas lo evitas? | 10 |
| 7 | ¿Por qué `0.1 + 0.2 == 0.3` es `False`, y cómo comparas dos `float`? | 10 |
| 8 | ¿Qué dan `int("4.5")`, `int(4.99)` y `bool("False")`? | 10 |
| 9 | ¿Por qué un dato faltante debe guardarse como `None` y no como `0`? ¿Cómo preguntas si falta? | 10 |
| 10 | `def f(text: str) -> int: return int(text)` y llamas `f(42)`. ¿Python da error por el tipo? ¿Qué herramienta lo detectaría? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Python es el lenguaje (las reglas); CPython es el programa oficial, escrito en C, que lee y ejecuta código Python.
2. Analizar, compilar a bytecode y ejecutar en la PVM. `SyntaxError` salta al analizar, antes de ejecutar nada; `NameError` salta durante la ejecución, al llegar a la línea.
3. `uv.lock` tiene la versión exacta y el hash de **todas** las dependencias, transitivas incluidas; `pyproject.toml` solo declara las directas. Al repositorio van `pyproject.toml` y `uv.lock`; `.venv/` no, porque se regenera desde el lock.
4. Falla con `The lockfile at uv.lock needs to be updated, but --locked was provided`. En Docker queremos instalar exactamente lo que se probó; si el lock no está al día, es mejor parar que instalar otra cosa sin avisar.
5. Por la caché de capas: las dependencias cambian poco y el código mucho. Así, un cambio en el código no obliga a reinstalar las bibliotecas.
6. Si alguien explota un fallo del programa, tiene todos los permisos dentro del contenedor. Se evita con `RUN useradd --create-home --uid 10001 app` y `USER app`.
7. Los `float` se guardan en binario y `0.1` no tiene representación binaria exacta, así que la suma arrastra un error de redondeo (`0.30000000000000004`). Se comparan con `math.isclose(a, b)`.
8. `ValueError` (no adivina cómo redondear), `4` (de `float` a `int` trunca) y `True` (cualquier texto no vacío es verdadero).
9. `0` es un valor real y falsea los cálculos: un promedio baja sin dar error. `None` significa "no hay dato". Se pregunta con `value is None`, no con `not value`, porque `not 0` también es `True`.
10. No: Python no comprueba las anotaciones al ejecutar, y `int(42)` funciona. Lo detectaría un comprobador de tipos como mypy (semana 13), o el editor.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor. Los ejercicios guiados no se evalúan.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Rojo antes que verde | El historial muestra el starter con tests en rojo y después los commits que los ponen en verde | 8 |
| Commits con sentido | Commits pequeños, con Conventional Commits, sin `.venv/` ni `__pycache__/` | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `uv run observatorio` y `docker compose run --build --rm app` desde un clon limpio | 10 |
| Explica su código | Responde qué hace cada línea de `parse_value` y por qué `is_valid` comprueba `None` primero | 8 |
| Explica su entorno | Dice qué guardan `pyproject.toml`, `uv.lock` y `.venv/`, y por qué la imagen no corre como root | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 0

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones | `parse_value`, `describe_record` e `is_valid` pasan los 12 tests de `tests/test_record.py` | 30 |
| Tests propios | Al menos 5 tests con valores del dominio calculados a mano, que cubren los 5 casos del paso 9 | 30 |
| Dominio | `__main__.py` con 3 registros reales del dominio (uno faltante, uno con coma) y `README.md` completado | 15 |
| Docker | `docker compose run --build --rm app` en verde | 10 |
| Git | Repositorio `python-<nombre>-<apellido>`, rama `week-01`, commits con Conventional Commits, sin `.venv/` en el repositorio | 10 |
| Pull request | Descripción con dominio, versiones y salidas pedidas en el paso 11 | 5 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 02 (próximamente) |
