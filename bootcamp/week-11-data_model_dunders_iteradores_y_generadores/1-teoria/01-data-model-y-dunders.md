# 01 · El data model y los dunders

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es el *data model* de Python y por qué `len(x)` no es un método de `x`.
- Escribir `__repr__` y `__str__`, y saber quién usa cada uno.
- Escribir `__eq__` y `__hash__` sin romper los `set` ni los diccionarios.
- Ordenar objetos propios con `__lt__` y `functools.total_ordering`.
- Reconocer qué dunders te escribe ya `@dataclass`.

---

## 1. La sintaxis de Python es una llamada a un método

Desde la semana 1 escribes `len(lista)`, `a + b`, `print(x)`, `a == b` o `for x in lista`. Ninguna de esas operaciones está "dentro" del lenguaje para unos tipos concretos: cada una **llama a un método especial** del objeto. Python define una lista de esos métodos y de cuándo los llama: es el ***data model*** (modelo de datos).

| Escribes | Python llama a |
|---|---|
| `len(x)` | `type(x).__len__(x)` |
| `str(x)`, `print(x)`, `f"{x}"` | `type(x).__str__(x)` |
| `repr(x)` | `type(x).__repr__(x)` |
| `a == b` | `type(a).__eq__(a, b)` |
| `a < b` | `type(a).__lt__(a, b)` |
| `a + b` | `type(a).__add__(a, b)` |
| `x[i]` | `type(x).__getitem__(x, i)` |
| `v in x` | `type(x).__contains__(x, v)` |
| `for v in x` | `type(x).__iter__(x)` y luego `__next__` |
| `if x:` | `type(x).__bool__(x)` o, si no hay, `__len__` |

Sus nombres empiezan y terminan con **dos guiones bajos**: *double underscore*, abreviado ***dunder***. `__len__` se lee "dunder len". También se llaman **métodos mágicos**, aunque no tienen nada de magia: son métodos normales con un nombre que Python conoce.

![A la izquierda, lo que escribes: len(serie), serie[0], for m in serie, a + b, str(m), a == b; a la derecha, el dunder al que llama Python en la clase del objeto](../0-assets/01-sintaxis-y-dunders.svg)

Fíjate en el `type(x)`: Python busca el dunder **en la clase**, no en el objeto. Ponerle a un objeto un atributo `obj.__len__ = ...` no cambia lo que hace `len(obj)`.

### ¿Por qué `len(x)` y no `x.len()`?

Porque así **todas** las colecciones se miden igual: listas, cadenas, diccionarios, `range` y tu `Series`. Si escribes `__len__` en tu clase, `len()` funciona con ella y, de paso, todo lo que se apoya en `len()`: `if serie:`, `bool(serie)`, `isinstance(serie, Sized)`. Tu clase entra en el idioma de Python en lugar de inventar el suyo (`serie.size()`, `serie.count()`, `serie.length`...).

**Regla**: no llames a los dunders directamente (`x.__len__()`); usa la sintaxis (`len(x)`). Los dunders se **escriben**, no se llaman.

---

## 2. `__repr__` y `__str__`: dos textos para dos lectores

Una clase sin dunders se imprime así:

```python
class Reading:
    def __init__(self, label: str, value: float) -> None:
        self.label = label
        self.value = value


print(Reading("Norte", 12.5))   # <__main__.Reading object at 0x7f3a2c1b9e50>
```

Es el `__repr__` que hereda de `object`: el nombre de la clase y una dirección de memoria. Útil para saber que es un `Reading`, inútil para saber **cuál**.

| Método | Para quién | Quién lo usa |
|---|---|---|
| `__repr__` | Quien programa: debe decir sin ambigüedad qué objeto es. Si se puede, que parezca el código que lo crea | `repr(x)`, la consola, el depurador, **los elementos de una lista o un diccionario** al imprimirlos, `f"{x!r}"` |
| `__str__` | Quien lee el resultado: un texto legible | `print(x)`, `str(x)`, `f"{x}"` |

```python
class Reading:
    def __init__(self, label: str, value: float) -> None:
        self.label = label
        self.value = value

    def __repr__(self) -> str:
        return f"Reading({self.label!r}, {self.value!r})"

    def __str__(self) -> str:
        return f"{self.label}: {self.value} µg/m³"


reading = Reading("Norte", 12.5)
print(reading)            # Norte: 12.5 µg/m³
print(repr(reading))      # Reading('Norte', 12.5)
print([reading])          # [Reading('Norte', 12.5)]
```

- `!r` dentro del *f-string* aplica `repr()` a cada atributo: `'Norte'` lleva comillas y se ve que es un `str`.
- Si solo escribes `__repr__`, `str()` lo usa también (el `__str__` de `object` llama a `__repr__`). Si solo escribes `__str__`, la lista sigue mostrando `<... object at 0x...>`. **Si escribes uno, escribe `__repr__`.**
- `__str__` y `__repr__` deben devolver `str`. Si devuelven otra cosa: `TypeError: __str__ returned non-string (type float)`.

En tu proyecto, `Measurement` ya tiene el `__repr__` de `@dataclass` (`Measurement(label='Norte', value=12.5)`), y esta semana le das un `__str__` que la escribe como línea: `Norte;12,5`. Es la inversa de `Measurement.from_line`.

---

## 3. `__eq__` y `__hash__`

Sin `__eq__`, `a == b` compara **identidad**, como `a is b`: dos objetos con los mismos datos no son iguales.

```python
class Station:
    def __init__(self, code: str) -> None:
        self.code = code

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Station):
            return NotImplemented
        return self.code == other.code


Station("N-01") == Station("N-01")    # True
Station("N-01") == "N-01"             # False
```

- El parámetro es `other: object`, no `other: Station`: `==` debe aceptar **cualquier** cosa. mypy lo exige (la firma de `object.__eq__` es así).
- Si `other` no es una estación, **devuelve** `NotImplemented`: le dice a Python "no sé compararme con eso". Python prueba entonces `other.__eq__(self)` y, si tampoco sabe, da `False`. No lances una excepción: `==` nunca debería fallar.

### La trampa del `__hash__`

Un `set` o un diccionario encuentran sus elementos con el ***hash***, un número que se calcula con `hash(x)`. La regla es: **si `a == b`, entonces `hash(a) == hash(b)`**. El `__hash__` de `object` usa la identidad, y con tu `__eq__` dos estaciones iguales tendrían *hash* distinto. Por eso, al definir `__eq__`, Python **pone `__hash__ = None`**:

```python
{Station("N-01")}
```

```
TypeError: cannot use 'Station' as a set element (unhashable type: 'Station')
```

Si el objeto no cambia (es inmutable), dale un `__hash__` con los **mismos datos** que compara `__eq__`:

```python
    def __hash__(self) -> int:
        return hash(self.code)
```

Si el objeto puede cambiar, no le des `__hash__`: si `code` cambiara mientras la estación está en un `set`, el `set` la buscaría en el sitio equivocado. Es la razón de `frozen=True` en la semana 9: una *dataclass* `frozen` con `eq=True` recibe `__hash__`; una mutable, no.

---

## 4. Ordenar: `__lt__` y `total_ordering`

`sorted()`, `min()`, `max()` y `list.sort()` solo necesitan `<`, que es `__lt__`:

```python
from functools import total_ordering


@total_ordering
class Level:
    NAMES = ("bajo", "medio", "alto")

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Level):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other: Level) -> bool:
        return self.NAMES.index(self.name) < self.NAMES.index(other.name)


sorted([Level("alto"), Level("bajo")])   # [bajo, alto], no alfabético
Level("alto") >= Level("medio")          # True
```

Hay seis comparaciones (`<`, `<=`, `>`, `>=`, `==`, `!=`). `!=` sale solo de `__eq__`. Las otras tres de orden las deduce `@total_ordering` a partir de `__eq__` y una de ellas (`__lt__`, normalmente). Sin ninguna, el decorador falla al crear la clase: `ValueError: must define at least one ordering operation: < > <= >=`.

Antes de escribirlo a mano, mira si te basta con `sorted(..., key=...)` (semana 5): ordenar por un campo no necesita dunders. `__lt__` es para cuando el objeto tiene **un orden natural** que siempre es el mismo.

---

## 5. Lo que ya te escribe `@dataclass`

En la semana 9, `@dataclass` te ahorró escribir dunders. Ahora sabes cuáles:

| Opción | Dunders que genera |
|---|---|
| Por defecto | `__init__`, `__repr__`, `__eq__` (compara la clase y los campos en orden) |
| `frozen=True` | Además `__setattr__` y `__delattr__` que lanzan `FrozenInstanceError`, y `__hash__` con los campos |
| `order=True` | `__lt__`, `__le__`, `__gt__` y `__ge__`, comparando los campos como una tupla |
| `slots=True` | `__slots__` (no es un método, pero también es parte del *data model*) |

`@dataclass` **no** genera `__str__`, `__len__`, `__iter__`, `__getitem__` ni operadores: eso depende de qué significa tu clase, y lo escribes tú. Si escribes en la clase un dunder que `@dataclass` iba a generar (por ejemplo, `__repr__`), se respeta el tuyo.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `print(x)` muestra `<... object at 0x...>` | La clase no tiene `__repr__` ni `__str__`, o el nombre está mal (`__repr` o `_repr_`) | Dos guiones bajos a cada lado, dentro de la clase |
| `RecursionError` al imprimir | `__repr__` usa `{self!r}` o `repr(self)`: se llama a sí mismo | Usa los atributos: `{self.label!r}` |
| `TypeError: __str__ returned non-string (type float)` | `__str__` devuelve `self.value` | Devuelve siempre un `str`: `f"{self.value}"` |
| `TypeError: cannot use 'X' as a set element (unhashable type: 'X')` | Definiste `__eq__` y Python borró `__hash__` | Si es inmutable, `__hash__` con los mismos datos que `__eq__` (o `@dataclass(frozen=True)`) |
| `mypy`: `Argument 1 of "__eq__" is incompatible with supertype "builtins.object"` | Escribiste `other: Station` en `__eq__` | `other: object` y `isinstance` dentro |
| `ValueError: must define at least one ordering operation: < > <= >=` | `@total_ordering` sin `__lt__` (ni ningún otro de orden) | Escribe `__lt__` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué es el *data model* y qué dunder llama Python con `len(x)`, `x[i]`, `a + b` o `if x:`.
- [ ] Quién usa `__repr__` y quién `__str__`, y cuál escribir si solo escribes uno.
- [ ] Por qué `__eq__` recibe `other: object` y devuelve `NotImplemented` con un tipo que no conoce.
- [ ] Por qué al definir `__eq__` desaparece `__hash__`, y cuándo devolverlo.
- [ ] Qué hace `@total_ordering` y qué dunders genera `@dataclass` con cada opción.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 11](../README.md) | **01 · El data model y los dunders** | [02 · Operadores y contenedores](02-operadores-y-contenedores.md) |
