# Rúbrica de Evaluación — Semana 06: Algoritmos y Big-O con `collections` e `itertools`

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 5 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Cuál es el orden de una función que recorre una lista con un `for` y, dentro, hace `if x in otra_lista`? ¿Cómo la bajarías a O(n)? | 10 |
| 2 | Un programa tarda 2 s con 10 000 datos y 8 s con 20 000. ¿Qué orden sugiere? ¿Cuánto esperas que tarde con 40 000? | 10 |
| 3 | ¿Por qué una sola medida con `perf_counter` no basta para comparar dos algoritmos? ¿Qué hace `timeit` para mejorarlo? | 10 |
| 4 | ¿Por qué la búsqueda binaria es O(log n)? ¿Qué pasa si la lista no está ordenada? ¿Cuántas miradas necesita, como mucho, con un millón de elementos? | 10 |
| 5 | Con `ordered = [8, 12, 30, 30, 61]`, ¿qué dan `bisect_left(ordered, 30)` y `bisect_right(ordered, 30)`? ¿Qué cuenta cada uno? | 10 |
| 6 | ¿Por qué `median` usa `sorted(values)` y no `values.sort()`? ¿Cuál es su orden, y por qué la mediana resiste mejor que la media un valor extremo? | 10 |
| 7 | Después de `groups = defaultdict(list)` y `print(groups["Sur"])`, ¿qué vale `"Sur" in groups`? ¿Por qué `values_by_label` devuelve `dict(groups)`? | 10 |
| 8 | Explica por qué tu `moving_average` es O(n) y la versión que hace `sum(window)` en cada paso es O(n · k). ¿Por qué hay que restar `recent[0]` antes del `append`? | 10 |
| 9 | ¿Qué devuelve `[(k, len(list(g))) for k, g in groupby(["a", "a", "b", "a"])]`? ¿Por qué `groupby` sirve para rachas y no para agrupar por clave? | 10 |
| 10 | Con `jumps = [5.0, -8.0, 3.0]`, ¿qué dan `max(jumps)`, `max(jumps, key=abs)` y `max([], default=0.0)`? ¿Qué pasa con `max([])`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. O(n · m): por cada uno de los `n` elementos, `in` recorre la otra lista de `m`. Si las dos crecen igual, O(n²). Se baja construyendo una vez `allowed = set(otra_lista)` (O(m)) y preguntando `x in allowed`, que es O(1): en total O(n + m).
2. Al doblar los datos, el tiempo se multiplica por 4: sugiere O(n²). Con 40 000, otra vez por 4: unos 32 s.
3. El sistema hace otras cosas a la vez y una medida suelta tiene ruido; además, operaciones muy rápidas tardan menos de lo que el reloj distingue bien. `timeit` repite la instrucción muchas veces (`number`) y devuelve el total; con `-m timeit` repite la tanda varias veces y se queda con la mejor.
4. Porque cada mirada descarta la mitad de lo que queda: el número de miradas es cuántas veces se puede partir `n` por la mitad, `log₂ n`. Si la lista no está ordenada, descarta mitades equivocadas y da una respuesta falsa sin avisar. Con un millón, unas 20 miradas.
5. `2` y `4`. `bisect_left` cuenta los elementos **menores** que 30 (8 y 12); `bisect_right`, los **menores o iguales** (8, 12, 30, 30).
6. Porque `.sort()` cambia la lista de quien llama, y una función no debe tocar sus argumentos; `sorted` crea una copia. Es O(n log n), por ordenar. La mediana es el valor del centro: un valor enorme solo ocupa una posición en un extremo y no la mueve, mientras que en la media suma todo su tamaño.
7. `True`: leer una clave que no está en un `defaultdict` la crea con una lista vacía. Por eso `values_by_label` devuelve `dict(groups)`: quien pregunte por una etiqueta que no existe debe ver un `KeyError`, no crear una lista vacía sin querer.
8. La mía hace dos operaciones por valor (restar el que sale y sumar el que entra), sea cual sea la ventana: `n` valores, O(n). La otra suma los `k` valores de la ventana en cada uno de los `n` pasos: O(n · k). Con `maxlen`, el `append` sobre una ventana llena expulsa el más antiguo; si no lo resto antes, `recent[0]` ya es otro y el total queda mal.
9. `[('a', 2), ('b', 1), ('a', 1)]`. `groupby` junta solo los elementos seguidos con la misma clave: `a` sale dos veces. Eso es justo una racha; para un grupo por clave hay que ordenar antes o usar un diccionario.
10. `5.0`, `-8.0` (el de mayor valor absoluto, con su signo) y `0.0`. `max([])` lanza `ValueError: max() iterable argument is empty`.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Rojo, verde, refactorizar | El historial de `week-06` muestra los tests en rojo, un commit por función en verde y un commit `refactor` por cada refactorización, sin cambiar los tests | 8 |
| Commits con sentido | Commits pequeños, con Conventional Commits (`feat`, `refactor`, `test`), sin `.venv/` ni `__pycache__/` | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest --durations=3`, `mypy` y el informe en Docker con `-T` | 8 |
| Explica sus órdenes | Dice el orden de cada función de `trends.py` y por qué, y señala en su código un O(n²) evitado o uno que existiría con otra colección | 10 |
| Mide | Muestra con `timeit` o `--durations` la diferencia entre su media móvil y la versión con `sum` en cada paso, o entre `in` en lista y en set | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 5

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones | Las seis funciones de `trends.py` y `main` pasan los 39 tests de `test_trends.py` y `test_main.py`, y los de las semanas anteriores siguen en verde | 30 |
| Eficiencia y herramientas | `moving_average` es O(n) con `deque`; `most_common_labels` usa `Counter`, `jumps` usa `pairwise`; las dos refactorizaciones usan `defaultdict` y `groupby` | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_trends.py` con datos del dominio (paso 12) | 20 |
| Tipos | `mypy src tests` sin errores | 10 |
| Datos y Docker | `medidas.txt` con al menos 12 líneas en orden; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-06` en `python-<nombre>-<apellido>` y README con el informe nuevo y la tabla de órdenes | 10 |
| Pull request | Descripción con tests, `mypy`, informe y la explicación de la media móvil en O(n) | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 07 (próximamente) |
