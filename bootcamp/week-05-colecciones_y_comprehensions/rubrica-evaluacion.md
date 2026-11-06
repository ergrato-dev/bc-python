# Rúbrica de Evaluación — Semana 05: Colecciones y comprehensions

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 4 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué valen `readings` y `result` después de `readings = [3, 1, 2]` y `result = readings.sort()`? ¿Y con `result = sorted(readings)`? | 10 |
| 2 | Después de `a = [1, 2]`, `b = a` y `c = a.copy()`, se ejecuta `b.append(3)`. ¿Qué valen `a`, `b` y `c`? ¿Qué dan `a is b`, `a is c` y `a == c` antes del `append`? | 10 |
| 3 | ¿Por qué `grid = [[0] * 3] * 3` seguido de `grid[0][0] = 9` cambia tres casillas? ¿Cómo se escribe bien? | 10 |
| 4 | ¿Cuándo usarías una tupla en lugar de una lista? Escribe una tupla de un solo elemento. | 10 |
| 5 | ¿Qué diferencia hay entre `units["luz"]` y `units.get("luz")` cuando la clave no existe? ¿Cuándo prefieres cada uno? | 10 |
| 6 | Explica qué hace `groups.setdefault(label, []).append(value)` cuando `label` es nueva y cuando ya existe. | 10 |
| 7 | ¿Por qué `{["Norte", "lunes"]: 12.5}` da error y `{("Norte", "lunes"): 12.5}` no? | 10 |
| 8 | Con `monday = {"Norte", "Sur"}` y `tuesday = {"Sur", "Este"}`, ¿qué dan `monday & tuesday`, `monday \| tuesday` y `monday - tuesday`? ¿Por qué no se puede hacer `monday[0]`? | 10 |
| 9 | ¿Qué devuelven `[v for v in [12, 60, 70] if v >= 50]` y `["alto" if v >= 50 else "normal" for v in [12, 60, 70]]`? ¿Por qué tienen distinta longitud? | 10 |
| 10 | ¿Qué imprime `gen = (n for n in range(3))`, luego `print(sum(gen))` y `print(sum(gen))`? ¿Qué tiene que ver con `list(sys.stdin)` en tu `main`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Con `sort`: `readings` queda `[1, 2, 3]` y `result` es `None`, porque `sort` cambia la lista y no la devuelve. Con `sorted`: `readings` sigue `[3, 1, 2]` y `result` es la lista nueva `[1, 2, 3]`.
2. `a` y `b` valen `[1, 2, 3]` (son la misma lista) y `c` vale `[1, 2]`. Antes del `append`: `a is b` es `True`, `a is c` es `False` y `a == c` es `True`: mismo contenido, objetos distintos.
3. `* 3` repite la referencia a la misma lista interior: las tres filas son un solo objeto, y cambiar una casilla se ve en las tres. Bien: `[[0] * 3 for _ in range(3)]`, que crea una lista nueva en cada vuelta.
4. Para un registro con pocas partes fijas, a menudo de tipos distintos, que no debe cambiar: `("Norte", 12.5)`. También cuando necesitas una clave de diccionario o un elemento de un set. De un elemento: `(5,)`, con la coma.
5. `units["luz"]` lanza `KeyError: 'luz'`; `units.get("luz")` devuelve `None` (o el valor por defecto que le pases). `[clave]` cuando la clave tiene que estar y su falta es un error; `.get` cuando puede faltar y hay un valor razonable para ese caso.
6. Si `label` es nueva, guarda una lista vacía con esa clave y la devuelve, y el `append` añade el primer valor. Si ya existe, devuelve la lista que había y el `append` añade a ella. En los dos casos la lista vive dentro del diccionario.
7. Las claves tienen que ser hashables: el diccionario las guarda según su hash y, si cambiaran, no las encontraría. Una lista puede cambiar y no es hashable (`TypeError: cannot use 'list' as a dict key`); una tupla de textos no cambia y sí lo es.
8. `{'Sur'}`, `{'Norte', 'Sur', 'Este'}` (en cualquier orden) y `{'Norte'}`. Un set no guarda orden ni posiciones: `TypeError: 'set' object is not subscriptable`.
9. `[60, 70]` y `['normal', 'alto', 'alto']`. El `if` del final filtra y quita los que no cumplen; el `if ... else` del principio elige el valor de cada elemento y no quita ninguno.
10. `3` y después `0`: el generador se agotó en la primera suma. `sys.stdin` se comporta igual: si `main` lo recorre con `process_lines`, `records_of` no recibe nada. `list(sys.stdin)` lo lee una vez y lo guarda para recorrerlo las veces que haga falta.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Rojo, verde, refactorizar | El historial de `week-05` muestra los tests en rojo, un commit por función en verde y el commit de refactorización de `count_level` sin cambiar los tests | 8 |
| Commits con sentido | Commits pequeños, con Conventional Commits (`feat`, `refactor`, `test`), sin `.venv/` ni `__pycache__/` | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `mypy` y el informe en Docker con `-T` | 8 |
| Explica sus colecciones | Por qué un registro es una tupla, por qué los grupos son un diccionario de listas y por qué las etiquetas distintas son un set | 10 |
| Explica una trampa | Muestra en el REPL un alias o una copia superficial que cambia "sola", y cómo lo evita su código | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 4

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones | Las siete funciones de `groups.py` y `main` pasan los 35 tests de `test_groups.py` y `test_main.py`, y los de las semanas anteriores siguen en verde | 30 |
| Comprehensions con criterio | `records_of`, `label_means` y `distinct_labels` usan comprehensions legibles; los bucles quedan donde hay estado o efectos | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_groups.py` con datos del dominio (paso 13) | 20 |
| Tipos | `mypy src tests` sin errores | 10 |
| Datos y Docker | `medidas.txt` con al menos 10 líneas y 3 etiquetas repetidas; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-05` en `python-<nombre>-<apellido>` y README con el informe nuevo | 10 |
| Pull request | Descripción con tests, `mypy`, informe y la explicación de `list(sys.stdin)` | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 06 (próximamente) |
