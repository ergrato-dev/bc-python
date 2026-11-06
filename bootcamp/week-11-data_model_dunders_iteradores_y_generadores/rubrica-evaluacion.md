# Rúbrica de Evaluación — Semana 11: Data model, dunders, iteradores y generadores

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 10 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué llama Python cuando escribes `len(serie)`, `serie[0]` y `if serie:`? ¿Por qué Python usa `len(x)` y no un método `x.len()`? | 10 |
| 2 | `Reading` tiene `__str__` pero no `__repr__`. ¿Qué muestran `print(lectura)` y `print([lectura])`? ¿Cuál escribirías si solo pudieras escribir uno? | 10 |
| 3 | Defines `__eq__` en `Station` y `{Station("N-01")}` lanza `TypeError: cannot use 'Station' as a set element (unhashable type: 'Station')`. ¿Por qué? ¿Cómo se arregla y cuándo **no** debes arreglarlo? | 10 |
| 4 | ¿Qué diferencia hay entre devolver `NotImplemented` y lanzar `NotImplementedError`? ¿Qué pasa con `serie + [medida]` si `__add__` no comprueba el tipo, y qué pasa si devuelve `NotImplemented`? | 10 |
| 5 | `sum([Distance(1.5), Distance(2.0)])` falla con `unsupported operand type(s) for +: 'int' and 'Distance'` aunque `Distance` tiene `__add__`. ¿Por qué? Da dos formas de arreglarlo. | 10 |
| 6 | ¿Qué diferencia hay entre un iterable y un iterador? Pon un ejemplo de cada uno y explica por qué `list(zip(a, b))` dos veces da la segunda vez `[]`. | 10 |
| 7 | Escribe con un `while` lo que hace `for value in values: print(value)`. ¿Quién lanza `StopIteration` y quién la captura? | 10 |
| 8 | Llamas a `running_mean([10.0, 20.0])` dentro de un `print` y sale `<generator object running_mean at 0x...>`. ¿Por qué no salen las medias? ¿Qué pasa en cada `next()`? | 10 |
| 9 | ¿Por qué `iter_lines(Path("no-existe.txt"))` no lanza `DataFileError` y `next(...)` sí? ¿Qué ventaja y qué riesgo tiene? | 10 |
| 10 | En tu proyecto, ¿por qué `Series.__iter__` usa `yield from` en lugar de devolver `self`? ¿Por qué `main` sigue trabajando con listas y no con generadores? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `type(serie).__len__(serie)`, `type(serie).__getitem__(serie, 0)` y `__bool__` o, si no existe, `__len__`, siendo `0` falso. Con `len(x)`, todas las colecciones se miden igual (listas, cadenas, diccionarios, tu `Series`), y lo que se apoya en `len` (`if`, `bool`, `Sized`) funciona con cualquier clase que escriba `__len__`, sin que cada una invente su nombre.
2. `print(lectura)` usa `__str__` y muestra el texto legible. `print([lectura])` muestra los elementos con `__repr__`, que no existe, así que sale `[<__main__.Reading object at 0x...>]`. Si solo escribes uno, escribe `__repr__`: `str()` lo usa cuando no hay `__str__`, y sirve en listas, consola y depurador.
3. Porque al definir `__eq__` Python pone `__hash__ = None`: dos objetos iguales deben tener el mismo *hash*, y el heredado de `object` usa la identidad. Se arregla con un `__hash__` que use los mismos datos que `__eq__` (`hash(self.code)`) o con `@dataclass(frozen=True)`. No lo arregles si el objeto es mutable: si cambiara el dato mientras está en un `set`, el `set` lo buscaría en el sitio equivocado.
4. `NotImplemented` es una constante que un operador **devuelve** para decir "no sé operar con eso, prueba al revés"; `NotImplementedError` es una excepción que se **lanza** (semana 10, un método que falta). Sin comprobación, `serie + [medida]` entra en `__add__` y falla dentro con `AttributeError: 'list' object has no attribute 'measurements'`. Con `NotImplemented`, Python prueba `[medida].__radd__(serie)`, que no existe, y lanza el `TypeError: unsupported operand type(s) for +: 'Series' and 'list'`, que dice exactamente qué pasa.
5. `sum` empieza por `0` y hace `0 + Distance(1.5)`: el `int` no sabe sumar distancias y `Distance` no tiene `__radd__` para la suma por la derecha. Arreglos: escribir `__radd__` que devuelva `self` cuando `other == 0`, o dar a `sum` el inicio: `sum(distancias, Distance(0))`.
6. Un iterable se puede recorrer y su `__iter__` da un iterador **nuevo** cada vez (lista, `str`, `dict`, tu `Series`); se recorre muchas veces. Un iterador es el cursor: tiene `__next__`, su `__iter__` devuelve `self` y avanza una sola vez (`iter(lista)`, `zip`, `map`, un archivo, un generador). `zip` devuelve un iterador: la primera `list` lo agota y la segunda no encuentra nada.
7. `cursor = iter(values)` y luego `while True:` con `try: value = next(cursor)` / `except StopIteration: break` y `print(value)`. La lanza el `__next__` del iterador cuando no quedan valores; la captura el `for` (en el `while`, el `except`).
8. Porque `running_mean` tiene `yield`: al llamarla devuelve un generador sin ejecutar ni una línea, y `print` muestra ese objeto. El primer `next()` ejecuta hasta el primer `yield` (`total = 10`, da `10.0`) y se pausa; el segundo sigue desde ahí (`total = 30`, da `15.0`); el tercero termina el `for` y el generador lanza `StopIteration`. Para ver las medias: `print(list(running_mean(...)))`.
9. Porque el cuerpo de un generador no se ejecuta hasta el primer `next()`: hasta entonces no se intenta abrir el archivo. Ventaja: crear el generador es gratis, y si nadie lo recorre no se abre nada. Riesgo: el error llega lejos de donde se escribió la ruta, quizá en otra función, y cuesta más saber de dónde viene.
10. Con `yield from`, cada `iter(serie)` crea un generador nuevo: la serie es un iterable y cada `for` empieza por la primera medida; dos bucles anidados no se estorban. Si devolviera `self`, la serie sería un iterador y se gastaría tras el primer `for`. `main` recorre los mismos datos muchas veces (filas, recuento, racha, medias, mediana, media móvil): necesita listas. Los generadores dan ventaja al leer y transformar de una pasada, no en un informe que vuelve sobre los datos.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-11` muestra un commit por paso (esqueleto, `__str__`, `__len__`, `__iter__`, `__getitem__`, `__add__`, los tres generadores, versión, tests), sin cambiar los tests del bootcamp | 8 |
| Reutiliza sin reescribir | `iter_measurements` usa `Measurement.from_line` e `is_data_line`; `git diff main -- src/observatorio` solo muestra `model.py` ampliado, `streams.py` nuevo y `core/__init__.py` ampliado; `__main__.py` sin cambios | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy` y `--version`, en su máquina y en Docker | 6 |
| Rompe y explica | Quita el `isinstance` de `__add__` y explica el `AttributeError`; cambia `yield from` por `return self` en `__iter__` y explica qué test falla; llama a `iter_lines` con una ruta mala y explica cuándo llega el error | 10 |
| Explica sus decisiones | Explica por qué `Series` no tiene `__contains__` ni hereda de `Sequence`, por qué `streams` importa `model` y no al revés, y qué comprueban los tests con `cycle` y `count` | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 10

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Data model | `Measurement.__str__` y `__len__`, `__iter__`, `__getitem__` y `__add__` en `Series`, como en la tabla del proyecto; pasan los tests de `Measurement` y `Series` de `test_datamodel.py` | 15 |
| Generadores | `core/streams.py` con `iter_lines`, `iter_measurements` y `running_mean`, perezosos de verdad; pasan sus tests de `test_datamodel.py` y los de las semanas anteriores siguen en verde | 15 |
| API y versión | Los tres nombres en `observatorio.core.__all__`; versión `0.11.0`; pasan `test_package.py` y `test_main.py`; el informe es idéntico al de la semana 10 | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_datamodel.py` con datos del dominio, que importan solo de `observatorio.core` (paso 14) | 20 |
| Calidad | `ruff check`, `ruff format --check` y `mypy` sin avisos; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-11` en `python-<nombre>-<apellido>`, README con `streams.py` en el árbol del paquete | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, el `AttributeError` del paso 9 y las dos preguntas del paso 16 | 20 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 12](../week-12-closures_decoradores_y_functools/README.md) |
