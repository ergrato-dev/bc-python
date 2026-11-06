# Rúbrica de Evaluación — Semana 12: Closures, decoradores y functools

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 11 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué diferencia hay entre `serie.where(above(50.0))` y `serie.where(above)`? ¿Por qué la segunda no lanza ningún error al ejecutarse y qué hace? | 10 |
| 2 | Explica la regla LEGB con este código: `limit = 50.0` en el módulo y `def make_threshold(limit): def is_above(v): return v > limit`. ¿Qué `limit` usa `is_above` y por qué? | 10 |
| 3 | Dentro de una función anidada, `total += 1` lanza `UnboundLocalError: cannot access local variable 'total' where it is not associated with a value`, aunque `total` existe fuera. ¿Por qué? Da dos formas de arreglarlo y di cuál prefieres. | 10 |
| 4 | ¿Qué es una closure? ¿Qué guarda exactamente: el valor de la variable o la variable? Usa la trampa de `[lambda v: v > limit for limit in (10, 30, 50)]` para responder. | 10 |
| 5 | Escribe sin `@` lo que hace `@skip_missing` encima de `def to_fahrenheit(...)`. ¿Cuándo se ejecuta `skip_missing` y cuándo su `wrapper`? | 10 |
| 6 | Sin `functools.wraps`, ¿qué devuelven `to_fahrenheit.__name__` y `to_fahrenheit.__doc__` después de decorarla? ¿Qué más añade `wraps` y para qué sirve en los tests? | 10 |
| 7 | ¿Por qué `rounded` tiene tres funciones anidadas y `skip_missing` solo dos? ¿Qué pasa si escribes `@rounded` sin paréntesis? | 10 |
| 8 | ¿Qué ganas al anotar un decorador con `[**P, R]` y `Callable[P, R]` en lugar de `Callable[..., Any]`? Pon un ejemplo de error que mypy detecta solo con la primera. | 10 |
| 9 | Da tres condiciones para que `@functools.cache` sea seguro. ¿Por qué tu `Series` no usa `cache` ni `cached_property`? | 10 |
| 10 | ¿Qué hace `singledispatch` y qué ventaja tiene frente a una cadena de `if isinstance(...)`? ¿Por qué `describe(3)` no usa la versión registrada para `float`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `above(50.0)` **llama** a la fábrica y devuelve la función `is_above`, que recibe una medida y devuelve un `bool`: es lo que espera `where`. `above`, sin llamar, es la fábrica misma: `where` la llama con cada medida (`above(medida)`), que devuelve una función, y una función es verdadera en un `if`. No hay error en ejecución: la serie se queda con **todas** las medidas. mypy sí lo detecta: `Argument 1 to "where" of "Series" has incompatible type "Callable[[float], Callable[[Measurement], bool]]"; expected "Callable[[Measurement], bool]"`.
2. Python busca en Local, Enclosing, Global y Built-in, en ese orden, y usa el primero. `is_above` no tiene `limit` local; lo encuentra en `make_threshold` (E), su parámetro, y no llega al `limit = 50.0` del módulo (G). `make_threshold(10.0)` crea un `is_above` que compara con `10.0`.
3. Porque `total += 1` es `total = total + 1`: asigna, y una asignación hace que `total` sea local en **toda** la función, decidido al compilar. Al leerla para sumar, la local aún no tiene valor. Arreglos: `nonlocal total` (o `global total` si es del módulo), o no cambiar la variable de fuera y devolver el nuevo valor. Mejor la segunda casi siempre; `nonlocal` para estado dentro de una closure, como un contador o un decorador.
4. Una función que lleva consigo las variables de la función que la rodeaba, aunque esta ya haya terminado. Guarda la **variable** (una celda), no su valor en ese momento. Por eso las tres `lambda` del bucle comparten la celda `limit`, la miran al llamarse, cuando ya vale `50`, y `check(20)` da `False` las tres veces. Arreglos: `lambda v, limit=limit: ...` (el valor por defecto se calcula al crearla) o una fábrica, `make_threshold(limit)`, que crea una celda por llamada.
5. `to_fahrenheit = skip_missing(to_fahrenheit)`, justo después del `def`. `skip_missing` se ejecuta **una vez**, al definir la función (al importar el módulo); su `wrapper` se ejecuta en **cada** llamada a `to_fahrenheit`.
6. `'wrapper'` y `None` (o el *docstring* del `wrapper`, si tuviera): el nombre `to_fahrenheit` apunta al `wrapper`. `wraps` copia también `__module__`, `__qualname__` y el `__dict__`, y añade `__wrapped__`, la función original. En los tests, `__wrapped__` deja probar la original sin el decorador, y un nombre correcto hace legibles las trazas y los informes de pytest.
7. `skip_missing` recibe la función directamente: decorador (recibe `func`) y `wrapper` (recibe cada llamada). `rounded` necesita antes un nivel que reciba `digits`: `rounded(1)` devuelve el decorador. Sin paréntesis, Python hace `f = rounded(f)`: `digits` recibe la función y `f` pasa a ser `decorator`; al llamar a `f(10.0)`, `decorator` trata `10.0` como la función que decorar. mypy lo detecta: `Argument 1 to "rounded" has incompatible type ...; expected "int"`.
8. Con `ParamSpec`, mypy sabe que la función decorada tiene **la misma firma** que la original y sigue comprobando cada llamada. Con `Callable[..., Any]` acepta cualquier argumento y no sabe qué devuelve. Ejemplo: `third("10")` con `@rounded(1) def third(value: float)`: `Argument 1 to "third" has incompatible type "str"; expected "float"`.
9. Argumentos *hashables* (son claves de un diccionario: con una lista, `TypeError: unhashable type: 'list'`); función pura (el mismo argumento da siempre el mismo resultado, sin leer archivos ni la hora); y no en métodos (`lru_cache` guarda `self` y mantiene vivos los objetos: ruff `B019`). `Series` es mutable (`add`): un resultado guardado quedaría viejo. Y tiene `slots=True`, sin `__dict__`, así que `cached_property` lanza `TypeError: No '__dict__' attribute on 'Series' instance to cache ...`. Además, sus cálculos son rápidos: no hay nada que ganar.
10. Convierte una función en una versión por defecto a la que se registran versiones por tipo (`@describe.register`, según la anotación del primer parámetro); al llamarla, elige la del tipo del primer argumento, siguiendo la jerarquía de clases. Frente a los `isinstance`, añadir un tipo es registrar una función nueva, sin tocar las demás ni la original, incluso desde otro módulo. `describe(3)`: `int` no es subclase de `float` (aunque mypy acepte un `int` donde pides `float`), así que va a la versión por defecto. Se arregla registrando `int | float`.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-12` muestra un commit por paso (esqueleto, `where`, `above`, `skip_missing`, `wraps`, `rounded`, `describe` y sus versiones, versión, tests), sin cambiar los tests del bootcamp | 8 |
| Reutiliza sin reescribir | `describe` usa `len(serie)` y `serie.labels()`; `git diff main -- src/observatorio` solo muestra `model.py` ampliado, `functional.py` nuevo y `core/__init__.py` ampliado; `__main__.py` sin cambios | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy` y `--version`, en su máquina y en Docker | 6 |
| Rompe y explica | Quita `@wraps` y explica los dos fallos; escribe `serie.where(above)` y explica por qué no falla en ejecución y qué dice mypy; invierte `skip_missing` y `rounded` y explica el `TypeError` con un `None` | 10 |
| Explica sus decisiones | Explica por qué `above` es una closure y no una clase, por qué `functional` importa `model` y no al revés, y por qué el núcleo no usa `cache` | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 11

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones como argumento y closure | `Series.where` y `above`, como en la tabla del proyecto; pasan sus tests de `test_functional.py` | 15 |
| Decoradores y `singledispatch` | `skip_missing` y `rounded` con `functools.wraps` y `rounded` con `[**P]`; `describe` con versiones para `Measurement`, `Series` y `Scale`; pasan sus tests y los de las semanas anteriores siguen en verde | 15 |
| API y versión | Los cuatro nombres en `observatorio.core.__all__`; versión `0.12.0`; pasan `test_package.py` y `test_main.py`; el informe es idéntico al de la semana 11 | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_functional.py` con datos del dominio, que importan solo de `observatorio.core` (paso 14) | 20 |
| Calidad | `ruff check`, `ruff format --check` y `mypy` sin avisos; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-12` en `python-<nombre>-<apellido>`, README con `functional.py` en el árbol del paquete | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, los dos fallos del paso 7 y las preguntas del paso 16 | 20 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 13 (próximamente) |
