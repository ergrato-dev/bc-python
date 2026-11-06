# 02 · Operadores y protocolos de contenedor

⏱️ 50 min

## 🎯 Objetivos

- Sobrecargar operadores aritméticos con `__add__`, `__mul__` y sus versiones por la derecha.
- Usar `NotImplemented` para que un operador falle bien con tipos que no conoce.
- Dar a una clase `len()`, `if`, `objeto[i]`, rebanadas e `in`.
- Saber qué te regala `collections.abc.Sequence` a cambio de dos métodos.

---

## 1. Operadores aritméticos

`a + b` llama a `a.__add__(b)`. Cada operador tiene su dunder:

| Operador | Dunder | Por la derecha | En el sitio |
|---|---|---|---|
| `a + b` | `__add__` | `__radd__` | `__iadd__` (`a += b`) |
| `a - b` | `__sub__` | `__rsub__` | `__isub__` |
| `a * b` | `__mul__` | `__rmul__` | `__imul__` |
| `a / b` | `__truediv__` | `__rtruediv__` | `__itruediv__` |
| `-a` | `__neg__` | | |
| `abs(a)` | `__abs__` | | |

```python
class Distance:
    def __init__(self, km: float) -> None:
        self.km = km

    def __add__(self, other: Distance) -> Distance:
        if not isinstance(other, Distance):
            return NotImplemented
        return Distance(self.km + other.km)

    def __mul__(self, factor: float) -> Distance:
        return Distance(self.km * factor)


Distance(1.5) + Distance(2.0)   # Distance(3.5)
Distance(1.5) * 3               # Distance(4.5)
```

Un operador **devuelve un objeto nuevo** y no cambia los operandos: `a + b` no modifica `a`, igual que `2 + 3` no cambia el `2`. Si quieres cambiar el objeto, eso es un método (`series.add(...)`) o `__iadd__`.

### `NotImplemented`: "no sé, pregunta al otro"

¿Qué pasa con `Distance(1.5) + 1`? El `isinstance` falla y `__add__` **devuelve** `NotImplemented` (una constante, no la excepción `NotImplementedError` de la semana 10). Python entiende "este operando no sabe" y prueba con el otro: `(1).__radd__(Distance(1.5))`. El `int` tampoco sabe, y entonces Python lanza el error de siempre:

```
TypeError: unsupported operand type(s) for +: 'Distance' and 'int'
```

Si en lugar de devolver `NotImplemented` dejas que el código siga, el error sale de dentro de tu método y no dice nada útil: `AttributeError: 'int' object has no attribute 'km'`. Lo verás en el paso 9 del proyecto.

La anotación `other: Distance` es para mypy: con ella, `Distance(1.5) + 1` es un error **antes de ejecutar** (`Unsupported operand types for + ("Distance" and "int")`). El `isinstance` es para la ejecución, donde nadie garantiza los tipos. Los dos se complementan.

### Por la derecha: `__radd__`

`sum(distancias)` empieza con `0` y hace `0 + Distance(1.5)`. Primero se pregunta al `int` (`(0).__add__(...)`), que devuelve `NotImplemented`, y luego a la distancia **por la derecha**: `Distance(1.5).__radd__(0)`.

```python
    def __radd__(self, other: object) -> Distance:
        if other == 0:
            return self
        return NotImplemented
```

Con ese método, `sum([Distance(1.5), Distance(2.0)])` da `Distance(3.5)`. Sin él: `TypeError: unsupported operand type(s) for +: 'int' and 'Distance'`. La otra salida es darle a `sum` el valor inicial: `sum(distancias, Distance(0))`.

**Cuándo sobrecargar operadores**: cuando el significado es obvio para cualquiera. `distancia + distancia` y `serie + serie` (juntar) lo son. `medida + medida` no (¿se suman los valores?, ¿se juntan las etiquetas?): mejor no escribirlo.

---

## 2. Verdad y tamaño: `__bool__` y `__len__`

`if x:` pregunta a `x.__bool__()`. Si la clase no lo tiene, pregunta a `x.__len__()` y `0` es falso. Si no tiene ninguno, el objeto **siempre es verdadero**.

```python
class Inbox:
    def __init__(self, messages: list[str]) -> None:
        self.messages = messages

    def __len__(self) -> int:
        return len(self.messages)


if Inbox([]):          # falso: __len__ da 0
    ...
```

Con `__len__` tienes `len()`, `if` y `bool()` a la vez. Escribe `__bool__` solo si "verdadero" no significa "no vacío" (una alarma que es verdadera si se pasa del límite). `__len__` debe devolver un `int` `>= 0`: si devuelve `-1`, `len()` lanza `ValueError: __len__() should return >= 0`.

---

## 3. Acceso por posición: `__getitem__`

`x[i]` llama a `x.__getitem__(i)`. Lo más sencillo es **delegar** en la lista que guardas (composición, semana 10):

```python
class Readings:
    def __init__(self, values: list[float]) -> None:
        self._values = values

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index: int) -> float:
        return self._values[index]
```

Delegando, los índices negativos (`r[-1]`) y el `IndexError` al pasarte del final te salen gratis. En un diccionario, `x["clave"]` llama al mismo método con la clave, y el error que se espera es `KeyError`.

### Rebanadas

`x[1:3]` también llama a `__getitem__`, pero con un objeto `slice(1, 3, None)`. Si quieres que una rebanada devuelva un objeto de tu clase (como `lista[1:3]` devuelve otra lista), compruébalo:

```python
    def __getitem__(self, index: int | slice) -> float | Track:
        if isinstance(index, slice):
            return Track(self._values[index])
        return self._values[index]
```

El tipo de retorno `float | Track` obliga a quien llama a comprobar qué le ha llegado; la forma precisa usa `@overload` (semana 13). Si no necesitas rebanadas, como tu `Series`, acepta solo `int`.

### El `for` del pasado

Una clase con `__getitem__` y sin `__iter__` **entra en un `for`**: Python pide `[0]`, `[1]`, `[2]`... hasta el primer `IndexError`. Es el protocolo de iteración antiguo, que se conserva por compatibilidad. Ni `isinstance(x, Iterable)` ni mypy lo reconocen. Si quieres que tu clase se recorra, escribe `__iter__` (teoría 03).

---

## 4. Pertenencia: `__contains__`

`v in x` llama a `x.__contains__(v)`. Si no existe, Python **recorre** el objeto (con `__iter__` o, si no, con `__getitem__`) y compara cada elemento con `==`. Para tu `Series` no hace falta escribirlo: con `__iter__` y el `__eq__` de `Measurement`, `Measurement("Norte", 12.5) in serie` ya funciona.

Escribe `__contains__` cuando puedas responder más rápido que recorriendo, como un `set` (semana 6), o cuando `in` deba buscar otra cosa:

```python
    def __contains__(self, label: object) -> bool:
        return label in self._entries    # busca etiquetas en un dict: O(1)
```

Cuidado: si `in` busca etiquetas pero `for` da valores, el objeto confunde. Que los dos hablen de lo mismo.

---

## 5. `collections.abc.Sequence`: dos métodos, siete regalos

En la semana 10 viste que `collections.abc` tiene clases abstractas para los contenedores. Si heredas de `Sequence` y escribes sus dos métodos abstractos, recibes los métodos plantilla:

```python
from collections.abc import Sequence


class Week(Sequence[str]):
    DAYS = ("lun", "mar", "mié", "jue", "vie", "sáb", "dom")

    def __len__(self) -> int:
        return len(self.DAYS)

    def __getitem__(self, index: int) -> str:  # type: ignore[override]
        return self.DAYS[index]


week = Week()
"vie" in week          # True: __contains__ de Sequence
week.index("vie")      # 4
list(reversed(week))   # ['dom', 'sáb', ...]: __reversed__ de Sequence
```

| Clase de `collections.abc` | Escribes | Recibes |
|---|---|---|
| `Sized` | `__len__` | Nada: solo le sirve a `isinstance`, que lo reconoce sin heredar |
| `Iterable` | `__iter__` | Nada: solo le sirve a `isinstance`, que lo reconoce sin heredar |
| `Container` | `__contains__` | Nada: solo le sirve a `isinstance`, que lo reconoce sin heredar |
| `Sequence` | `__len__`, `__getitem__` | `__contains__`, `__iter__`, `__reversed__`, `index`, `count` |
| `Mapping` | `__getitem__`, `__iter__`, `__len__` | `__contains__`, `keys`, `items`, `values`, `get`, `__eq__` |

¿Y tu `Series`? No hereda de `Sequence`: solo necesita cuatro dunders, que escribes en cuatro líneas, y no quieres `index` ni `count`, que no significan nada para una serie de medidas. Igual que en la semana 10: hereda cuando la clase **es** eso en todo.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: unsupported operand type(s) for +: 'X' and 'int'` | No hay `__add__` para ese tipo (o devuelve `NotImplemented`) | Es lo correcto si no tiene sentido; si sí, amplía `__add__` o escribe `__radd__` |
| `AttributeError: 'int' object has no attribute 'km'` dentro de `__add__` | El operador no comprueba el tipo de `other` | `if not isinstance(other, Distance): return NotImplemented` |
| `sum(objetos)` falla con `'int' and 'X'` | `sum` empieza por `0` | `__radd__` que acepte `0`, o `sum(objetos, X(0))` |
| `a + b` cambia `a` | `__add__` modifica `self` | Crea y devuelve un objeto nuevo |
| `TypeError: object of type 'X' has no len()` | Falta `__len__` | Escríbelo, delegando en la colección de dentro |
| `TypeError: 'X' object is not subscriptable` | Falta `__getitem__` | Escríbelo |
| `ValueError: __len__() should return >= 0` | `__len__` devuelve un negativo | Devuelve el tamaño real |

---

## ✅ Qué debes saber al terminar

- [ ] Qué dunder llama cada operador y qué son las versiones `__r*__` e `__i*__`.
- [ ] La diferencia entre devolver `NotImplemented` y lanzar `NotImplementedError`.
- [ ] Por qué `sum` necesita `__radd__` o un valor inicial.
- [ ] Qué hace `if x:` cuando la clase no tiene `__bool__`.
- [ ] Qué recibe `__getitem__` con `x[1:3]`.
- [ ] Cuándo escribir `__contains__` y qué hace `in` sin él.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · El data model y los dunders](01-data-model-y-dunders.md) | **02 · Operadores y contenedores** | [03 · Iteradores](03-iteradores.md) |
