# 04 · *Dataclasses* inmutables y con `slots`

⏱️ 45 min

## 🎯 Objetivos

- Crear objetos inmutables con `frozen=True` y "cambiarlos" con `replace`.
- Explicar por qué un objeto inmutable puede ir en un `set` y uno mutable no.
- Ordenar objetos con `order=True` y excluir campos de la comparación.
- Explicar qué hace `slots=True` y cuándo usarlo.
- Usar `kw_only`, `ClassVar` y `match` con *dataclasses*.

---

## 1. `frozen=True`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Measurement:
    label: str
    value: float | None


north = Measurement("Norte", 12.5)
north.value = 13.0
```

```
dataclasses.FrozenInstanceError: cannot assign to field 'value'
```

Un objeto **inmutable** no cambia después de crearse, como una tupla o un texto. ¿Por qué querrías eso?

- **Nadie te lo cambia por la espalda.** Si pasas una medida a una función, sabes que vuelve igual. Con objetos mutables, cualquier función que los reciba puede modificarlos, y el fallo aparece lejos de donde se produjo.
- **Puede tener *hash*.** `@dataclass(frozen=True)` genera `__hash__` a partir de los campos: la medida puede ir en un `set` o ser clave de un diccionario, cosa que el termómetro de la teoría 02 perdió al definir `__eq__`.
- **Se lee mejor.** Quien ve `frozen=True` sabe que ese objeto es un valor, no algo con estado.

En tu proyecto, `Scale` y `Measurement` son inmutables; `Series`, que va acumulando medidas, no.

## 2. "Cambiar" un objeto inmutable

No se cambia: se crea otro con el campo nuevo.

```python
from dataclasses import replace

corrected = replace(north, value=13.0)   # Measurement(label='Norte', value=13.0)
north                                    # sigue siendo Measurement(label='Norte', value=12.5)
```

Desde Python 3.13 también existe `copy.replace(north, value=13.0)`, que sirve para *dataclasses*, `NamedTuple`, fechas y otros tipos. Las dos pasan por `__init__`, así que la validación de `__post_init__` vuelve a ejecutarse.

**Inmutable, pero solo por fuera.** `frozen` impide reasignar los campos, no cambiar lo que hay dentro de ellos:

```python
@dataclass(frozen=True)
class Route:
    name: str
    stops: list[str] = field(default_factory=list)


morning = Route("Mañana")
morning.stops.append("Norte")   # funciona: la lista es la misma, cambia por dentro
hash(morning)                   # TypeError: unhashable type: 'list'
```

Si quieres un objeto inmutable de verdad, usa campos inmutables: `tuple` en lugar de `list`, `frozenset` en lugar de `set`.

## 3. `order=True`

```python
@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int


sorted([Version(1, 0, 0), Version(0, 10, 0), Version(0, 9, 0)])
# [Version(major=0, minor=9, patch=0), Version(major=0, minor=10, patch=0), Version(major=1, minor=0, patch=0)]
```

`order=True` genera `<`, `<=`, `>` y `>=`, que comparan los campos **en orden de declaración**, como si fueran tuplas: primero `major`; si empatan, `minor`; y así. El orden de los campos decide el orden de los objetos. Para que un campo no cuente al comparar (ni en `==` ni en `<`), `field(compare=False)`:

```python
@dataclass(frozen=True, order=True)
class Item:
    value: float
    label: str = field(compare=False)
```

Si solo necesitas ordenar de una forma concreta una vez, `sorted(..., key=...)` (semana 5) sigue siendo más sencillo.

## 4. `slots=True`

Cada objeto guarda sus atributos en un diccionario, su `__dict__` (teoría 01). Un diccionario es flexible, pero:

- Acepta cualquier atributo: `north.unti = "°C"`, con una errata, crea un atributo nuevo sin avisar.
- Ocupa memoria: cada objeto lleva su propio diccionario.

Con `slots=True`, la clase reserva un hueco fijo para cada campo y sus objetos no tienen `__dict__`:

```python
@dataclass(slots=True)
class Slotted:
    label: str
    unit: str


Slotted("Norte", "µg/m³").unti = "°C"
```

```
AttributeError: 'Slotted' object has no attribute 'unti' and no __dict__ for setting new attributes
```

Una medida con dos campos ocupa unos 48 bytes con `slots` frente a más de 300 con su `__dict__` (medido con `sys.getsizeof` en CPython 3.14). Con diez medidas da igual; con un millón, en la fase 4, no. El precio: no puedes añadir atributos que no sean campos. En una clase de datos eso es justo lo que quieres, así que el modelo de tu proyecto lleva `slots=True` en las tres clases.

## 5. `kw_only` y `ClassVar`

`kw_only=True` obliga a pasar todos los campos por nombre, como el `*` de las funciones de la semana 4:

```python
@dataclass(frozen=True, kw_only=True)
class Scale:
    unit: str
    low: float
    high: float


Scale(unit="µg/m³", low=10.0, high=50.0)   # se lee sin mirar el orden de los campos
Scale("µg/m³", 10.0, 50.0)                 # TypeError: Scale.__init__() takes 1 positional argument but 4 were given
```

Úsalo cuando hay varios campos del mismo tipo y es fácil confundir el orden (`low` y `high` son dos `float`). Tu proyecto no lo usa para que `Scale(UNIT, LOW, HIGH)` quede corto, pero es una buena opción.

Un atributo de clase en una *dataclass* se marca con `ClassVar`, para que `@dataclass` no lo convierta en campo:

```python
from typing import ClassVar


@dataclass(frozen=True)
class Measurement:
    MISSING: ClassVar[str] = "sin dato"
    label: str
    value: float | None
```

## 6. *Dataclasses* y `match`

`@dataclass` genera también `__match_args__`, el orden de los campos para `match` (semana 2):

```python
match measurement:
    case Measurement(label, None):
        print(f"{label}: sin dato")
    case Measurement(label, value):
        print(f"{label}: {value}")
```

`case Measurement(label, None)` comprueba que es una `Measurement` y que su segundo campo es `None`, y guarda el primero en `label`.

## 7. Qué opciones usar

| Si la clase... | Usa |
|---|---|
| Es un valor: una medida, una escala, una versión, una coordenada | `frozen=True, slots=True` |
| Va acumulando o cambiando cosas: una serie, un contador, un carrito | `slots=True`, sin `frozen` |
| Tiene un orden natural | Añade `order=True` |
| Tiene varios campos fáciles de confundir | Añade `kw_only=True` |

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `FrozenInstanceError: cannot assign to field 'value'` | Asignas un campo de una *dataclass* `frozen` | `replace(obj, value=...)` crea otra |
| `TypeError: unhashable type: 'list'` al meter un objeto `frozen` en un `set` | Uno de sus campos es una lista | Usa una tupla, o no lo metas en un `set` |
| `TypeError: '<' not supported between instances of 'Version' and 'Version'` | Falta `order=True` | Añádelo, o usa `sorted(..., key=...)` |
| `AttributeError: ... and no __dict__ for setting new attributes` | Asignas un atributo que no es un campo en una clase con `slots` | Corrige el nombre, o decláralo como campo |
| `FrozenInstanceError` dentro de `__post_init__` | En una clase `frozen` no puedes asignar `self.level = ...` ni en `__post_init__` | Calcula el valor con una propiedad, o usa `object.__setattr__(self, "level", ...)` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué impide `frozen=True`, qué gana el objeto y qué no impide.
- [ ] Cómo "cambiar" un objeto inmutable con `replace`.
- [ ] Cómo compara `order=True` y cómo excluir un campo.
- [ ] Qué quita `slots=True`, qué ganas y qué pierdes.
- [ ] Para qué sirven `kw_only=True` y `ClassVar`.
- [ ] Qué opciones de `@dataclass` lleva una clase de valor y cuáles una que acumula datos.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · `dataclasses`](03-dataclasses.md) | **04 · *Dataclasses* inmutables y con `slots`** | [05 · Elegir el modelo](05-elegir-el-modelo.md) |
