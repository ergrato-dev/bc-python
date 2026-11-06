# Rúbrica de Evaluación — Semana 09: Clases y `dataclasses`

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 8 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué pasa, paso a paso, al ejecutar `north = Sensor("Norte", "µg/m³")`? ¿Qué es `self` dentro de `__init__`? | 10 |
| 2 | `north.record(12.5)` funciona, pero `def record(value):` da `takes 1 positional argument but 2 were given`. ¿Por qué dos? | 10 |
| 3 | `Sensor` tiene `kind = "aire"` en la clase. Después de `north.kind = "agua"`, ¿qué valen `north.kind`, `south.kind` y `Sensor.kind`? ¿Por qué? | 10 |
| 4 | Una clase tiene `readings = []` en la clase, fuera de `__init__`. ¿Qué pasa al añadir lecturas a dos objetos distintos? ¿Cómo lo evita `@dataclass`? | 10 |
| 5 | ¿Qué diferencia hay entre `__repr__` y `__str__`? Si solo escribes uno, ¿cuál y por qué? | 10 |
| 6 | Defines `__eq__` en `Thermometer` y `{kitchen}` da `TypeError: cannot use ... as a set element (unhashable type: ...)`. ¿Por qué Python quita el *hash*? ¿Qué lo arregla en una *dataclass*? | 10 |
| 7 | ¿Por qué en Python no se escriben `get_celsius()` y `set_celsius()` por adelantado? ¿Qué harías si un día hay que validar `celsius`? | 10 |
| 8 | ¿Qué métodos genera `@dataclass` y a partir de qué? ¿Por qué `Station("Norte", "Lima", "alta")` no falla aunque `altitude` sea `int`? | 10 |
| 9 | ¿Por qué `Measurement` es `frozen=True` y `Series` no? ¿Qué gana `Measurement` con ello, y qué no impide `frozen` en una clase con un campo `list`? | 10 |
| 10 | Tu `Series.means()` es `return label_means(values_by_label(self.records))`. ¿Por qué no copiar la lógica dentro del método? ¿Qué papel tiene `records`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Python crea un objeto vacío de tipo `Sensor` y llama a `Sensor.__init__(objeto, "Norte", "µg/m³")`. `self` es ese objeto recién creado: cada `self.name = name` le pone un atributo. Al terminar `__init__`, el objeto queda asignado a `north`.
2. Porque `north.record(12.5)` es `Sensor.record(north, 12.5)`: Python pasa el objeto como primer argumento. El método recibe dos y solo declara uno. Todo método necesita `self` como primer parámetro.
3. `"agua"`, `"aire"` y `"aire"`. Leer busca primero en el objeto y después en la clase, pero asignar siempre escribe en el objeto: `north` gana su propio `kind`, que tapa el de la clase. `south` no tiene uno propio y lee el de la clase, que no ha cambiado.
4. Los dos objetos comparten **una** lista, la de la clase: `self.readings.append(...)` lee el atributo, lo encuentra en la clase y cambia esa lista, y cada objeto ve las lecturas del otro. `@dataclass` no permite `= []` como valor por defecto (`ValueError: mutable default ...`) y obliga a `field(default_factory=list)`, que crea una lista nueva por objeto.
5. `__repr__` es para quien programa: sin ambigüedad, a ser posible el código que crea el objeto. Lo usan `repr()`, `!r`, las listas, el depurador y pytest. `__str__` es para quien lee el resultado, y lo usan `print()` y los f-strings. Si solo escribes uno, `__repr__`, porque `print()` lo usa cuando falta `__str__`.
6. Dos objetos iguales deben tener el mismo *hash*, y un `set` coloca cada objeto según el suyo. Si el termómetro cambiara de temperatura dentro del `set`, su *hash* cambiaría y el `set` no lo encontraría. Por eso, si defines `__eq__` en un objeto mutable, Python le quita el `__hash__`. `@dataclass(frozen=True)` hace el objeto inmutable y genera `__hash__` a partir de los campos.
7. Porque un atributo se puede convertir en propiedad más tarde sin cambiar a quien lo usa: `kitchen.celsius` se sigue escribiendo igual. Si hay que validar, `celsius` pasa a ser una `@property` con un *setter* que comprueba el valor y lo guarda en `self._celsius`. Como `__init__` asigna `self.celsius`, la validación se aplica también al crear el objeto.
8. `__init__`, `__repr__` y `__eq__` (y `__match_args__`), a partir de los campos declarados con `nombre: tipo`, en su orden. No falla porque Python no comprueba los tipos al ejecutar: son para el editor y para mypy, que sí avisaría. En la semana 13, Pydantic los comprobará.
9. `Measurement` es un valor: una medida no cambia después de leerse. Con `frozen=True` nadie la cambia por la espalda, tiene `__hash__` y puede ir en un `set`. `Series` va acumulando medidas con `add`, así que tiene que poder cambiar. `frozen` impide reasignar los campos, pero no cambiar lo que hay dentro de ellos: si un campo es una lista, se le puede seguir haciendo `append`, y además el objeto deja de tener *hash* (`unhashable type: 'list'`).
10. Porque la lógica ya existe, está probada por los tests de las semanas 5 y 6 y la usan otras partes del programa: copiarla duplicaría el código y los fallos. El método solo da un nombre cómodo a una combinación de funciones. `records` traduce las medidas a tuplas `(etiqueta, valor)`, el formato que esperan esas funciones, y es el único sitio que conoce los dos formatos.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-09` muestra un commit por paso (esqueleto, `frozen` y `slots`, validación, métodos, versión, `main`, tests), sin cambiar los tests del bootcamp | 8 |
| Reutiliza sin reescribir | Los métodos de `model.py` llaman a las funciones de las capas anteriores; `git diff main -- src/observatorio/core` solo muestra `model.py` nuevo y `__init__.py` ampliado | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy` y `--version`, en su máquina y en Docker | 6 |
| Rompe y explica | Pone sus umbrales al revés y explica la traza (por qué falla al arrancar y qué es `File "<string>"`); cambia `default_factory=list` por `= []` y explica el error | 10 |
| Explica sus decisiones | Explica por qué `Measurement` es `frozen` y `Series` no, para qué sirve `slots=True` y por qué `from_line` es un `@classmethod` | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 8

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Modelo | `core/model.py` con `Scale`, `Measurement` y `Series`, con las opciones de la tabla del proyecto; pasan los 29 tests de `test_model.py` y los de las semanas anteriores siguen en verde | 30 |
| API y versión | Las tres clases en `observatorio.core.__all__`; versión `0.9.0`; pasan `test_package.py` y `test_main.py` | 10 |
| `main` usa el modelo | `SCALE = Scale(UNIT, LOW, HIGH)` y una `Series` en lugar de la lista de tuplas; el informe es idéntico al de la semana 8 | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_model.py` con datos del dominio, que importan solo de `observatorio.core` (paso 12) | 20 |
| Calidad | `ruff check`, `ruff format --check` y `mypy` sin avisos; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-09` en `python-<nombre>-<apellido>`, README con `model.py` en el árbol del paquete | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, la escala del dominio con su error y la decisión `frozen` | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 10](../week-10-herencia_composicion_abc_y_protocol/README.md) |
