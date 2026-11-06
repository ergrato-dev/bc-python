# Rúbrica de Evaluación — Semana 04: Funciones, scope, type hints y pytest

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 3 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué diferencia hay entre parámetro y argumento? ¿Y entre `f` y `f()`? | 10 |
| 2 | Una función hace `print(resultado)` en lugar de `return resultado`. ¿Qué devuelve y qué problema tiene para un test? | 10 |
| 3 | Con `def money(amount, decimals=2, *, sign="$")`, ¿cuáles de estas llamadas fallan: `money(5)`, `money(5, 0)`, `money(5, 0, "€")`, `money(5, sign="€")`, `money(sign="€", 5)`? | 10 |
| 4 | ¿Por qué `visits += 1` dentro de una función, con `visits` global, da `UnboundLocalError`? ¿Cómo lo arreglas sin `global`? | 10 |
| 5 | ¿Qué imprime `def f(x, acc=[]): acc.append(x); return acc` llamada como `f(1)` y luego `f(2)`? ¿Cómo se corrige? | 10 |
| 6 | ¿Qué hace `sorted(["12,5", "8", "55,1"], key=lambda t: float(t.replace(",", ".")))` y por qué hace falta `key`? | 10 |
| 7 | Una función tiene la anotación `-> int` y devuelve un `str`. ¿Qué pasa al ejecutarla? ¿Quién lo detecta? | 10 |
| 8 | `parse_value` devuelve `float \| None`. ¿Qué te dice `mypy` si haces `parse_value(t) * 2` y cómo lo arreglas? | 10 |
| 9 | ¿Por qué `assert ratio(2, 7) == 0.2857142857` falla y qué usas en su lugar? ¿Cómo compruebas que `ratio(5, 4)` lanza `ValueError`? | 10 |
| 10 | Para `classify` con umbrales 10 y 50, ¿qué cinco valores pondrías en un `parametrize` y por qué? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. El parámetro es el nombre en la definición (`def f(x)`); el argumento, el valor en la llamada (`f(3)`). `f` es la función misma, que se puede pasar a otra; `f()` la llama y es su resultado.
2. Devuelve `None`. El test no puede comparar el resultado (`assert f(x) == ...` compara con `None`); tendría que capturar la salida con `capsys`. Las funciones de lógica devuelven y solo `main` imprime.
3. Falla `money(5, 0, "€")` (`sign` va después de `*` y solo se pasa por nombre: `TypeError`) y `money(sign="€", 5)` (`SyntaxError`: un argumento por posición después de uno por nombre). Las otras tres funcionan.
4. Al ver una asignación a `visits` dentro de la función, Python la trata como local en toda ella, y `+=` intenta leerla antes de que tenga valor. Arreglo: `def add_visit(visits: int) -> int: return visits + 1` y `visits = add_visit(visits)`.
5. `[1]` y después `[1, 2]`: el `[]` por defecto se crea una sola vez, al definir la función, y se comparte. Se corrige con `acc=None` y `if acc is None: acc = []` dentro.
6. Devuelve `['8', '12,5', '55,1']`: los textos ordenados por su valor numérico. Sin `key` se comparan como texto, carácter a carácter, y `"8"` iría al final porque `"8" > "5"`.
7. Se ejecuta sin error: Python no comprueba las anotaciones. Lo detecta `mypy` (`Incompatible return value type`), sin ejecutar el código, y VS Code lo subraya.
8. `Unsupported operand types for * ("None" and "int")`. Se arregla guardando el valor y comprobando `if value is None:` (con `return` o un valor alternativo) antes de multiplicar; después, `mypy` sabe que es `float`.
9. `2 / 7` es `0.2857142857142857`, que no es igual a `0.2857142857`: los decimales calculados no se comparan con `==`. Se usa `pytest.approx(0.2857142857)`. El error se comprueba con `with pytest.raises(ValueError): ratio(5, 4)`.
10. Por ejemplo `9.9` (justo antes de 10, `bajo`), `10.0` (justo en el umbral, `medio`), `49.9` (`medio`), `50.0` (`alto`) y `None` (`sin dato`). Los errores de `<` frente a `<=` solo aparecen justo en los umbrales.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Rojo, verde, refactorizar | El historial de `week-04` muestra los tests en rojo, un commit por función en verde y al menos un commit de refactorización (tipos o nombres) sin cambiar los tests | 8 |
| Commits con sentido | Commits pequeños, con Conventional Commits (`feat`, `refactor`, `test`), sin `.venv/` ni `__pycache__/` | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `uv run --with mypy==2.4.1 mypy src tests` y el informe en Docker | 8 |
| Explica su código | Por qué `process_lines` no imprime, qué pasa si `ratio` recibe `part > total` y por qué `decimals` va después de `*` | 10 |
| Explica sus tests | Por qué eligió esos límites en su `parametrize` y qué fallo detectaría cada uno | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 3

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones | `process_lines`, `count_level`, `ratio`, `share` y `main` pasan los 28 tests de `test_analysis.py` y `test_main.py`, y los de las semanas anteriores siguen en verde | 30 |
| Tests propios | Al menos 6 tests en `tests/test_my_analysis.py` con datos del dominio, que usan `parametrize`, `approx` y `raises` (paso 10) | 25 |
| Tipos | `mypy src tests` sin errores | 15 |
| Docker | `docker compose run --build --rm app` en verde y el informe con `-T` en el contenedor | 10 |
| Git y README | Rama `week-04` en `python-<nombre>-<apellido>` y README con la organización del código y el informe nuevo | 10 |
| Pull request | Descripción con tests, `mypy`, informe y un límite del dominio justificado | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 05](../week-05-colecciones_y_comprehensions/README.md) |
