# 02 · Propiedades y métodos especiales

⏱️ 45 min

## 🎯 Objetivos

- Escribir `__repr__` y `__str__`, y explicar quién usa cada uno.
- Escribir `__eq__` y explicar por qué la clase deja de servir en un `set`.
- Calcular y validar atributos con `@property`.
- Crear objetos de otra forma con `@classmethod` y explicar qué es un `@staticmethod`.
- Explicar la convención del guion bajo (`_celsius`).

---

## 1. Métodos especiales

Los métodos con dos guiones bajos a cada lado, como `__init__`, son **métodos especiales** (en inglés, *dunder methods*, de *double underscore*). No los llamas tú: los llama Python cuando usas el objeto de cierta forma. `len(x)` llama a `x.__len__()`, `a + b` a `a.__add__(b)` y `print(x)` a `x.__str__()`. Esta semana ves los tres que necesita cualquier clase de datos; en la semana 11, el resto.

## 2. `__repr__` y `__str__`

Sin ellos, un objeto se imprime así:

```
<thermometer.Thermometer object at 0x7723183cc590>
```

El módulo, la clase y una dirección de memoria: nada útil para depurar.

```python
class Thermometer:
    def __init__(self, name: str, celsius: float) -> None:
        self.name = name
        self.celsius = celsius

    def __repr__(self) -> str:
        return f"Thermometer({self.name!r}, {self.celsius!r})"

    def __str__(self) -> str:
        return f"{self.name}: {self.celsius} °C"
```

| | `__repr__` | `__str__` |
|---|---|---|
| Para quién | Quien programa | Quien lee el resultado |
| Lo usan | `repr()`, `!r` en un f-string, las listas y diccionarios al imprimirse, el depurador, pytest | `print()`, `str()`, los f-strings |
| Forma | Sin ambigüedad; si se puede, el código que crea el objeto: `Thermometer('Cocina', 21.5)` | Libre: `Cocina: 21.5 °C` |

Si solo escribes uno, que sea `__repr__`: `print()` lo usa cuando falta `__str__`. Y te lo ahorrarás casi siempre, porque `@dataclass` lo genera (teoría 03).

## 3. `__eq__`

Por defecto, `a == b` es lo mismo que `a is b`: dos objetos distintos nunca son iguales, aunque tengan los mismos datos.

```python
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Thermometer):
            return NotImplemented
        return (self.name, self.celsius) == (other.name, other.celsius)
```

`other` puede ser cualquier cosa (por eso el tipo `object`). Si no es un termómetro, devolver `NotImplemented` le dice a Python "no sé compararme con esto": prueba el `__eq__` del otro objeto y, si tampoco sabe, responde `False`.

Al definir `__eq__`, Python pone el `__hash__` de la clase a `None`, y el objeto ya no puede ir en un `set` ni ser clave de un diccionario:

```
TypeError: cannot use 'thermometer.Thermometer' as a set element (unhashable type: 'Thermometer')
```

Es a propósito. Un `set` coloca cada objeto según su *hash*, y dos objetos iguales deben tener el mismo. Si el termómetro cambiara de temperatura dentro del `set`, cambiaría su *hash* y el `set` ya no lo encontraría. Un objeto que se compara por sus datos solo puede tener *hash* si esos datos no cambian: es lo que da `frozen=True` (teoría 04).

## 4. `@property`

Una **propiedad** es un método que se lee como un atributo, sin paréntesis:

```python
    @property
    def fahrenheit(self) -> float:
        return round(self.celsius * 9 / 5 + 32, 1)


kitchen.fahrenheit       # 70.7: se calcula cada vez, nunca se queda desfasado
kitchen.fahrenheit = 0   # AttributeError: property 'fahrenheit' of 'Thermometer' object has no setter
```

Con un *setter*, la propiedad puede **validar** lo que se le asigna:

```python
ABSOLUTE_ZERO = -273.15

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < ABSOLUTE_ZERO:
            raise ValueError(f"temperatura imposible: {value} °C (mínimo {ABSOLUTE_ZERO})")
        self._celsius = value
```

El valor de verdad se guarda en `self._celsius`. Si el *setter* hiciera `self.celsius = value`, se llamaría a sí mismo sin fin (`RecursionError`). Y como `__init__` hace `self.celsius = celsius`, también pasa por el *setter*: no se puede crear un termómetro imposible.

Lo importante: quien usaba `kitchen.celsius` sigue escribiendo exactamente lo mismo. En Python **se empieza con atributos normales** y se cambian a propiedad solo cuando hace falta calcular o validar. No escribas `get_celsius()` y `set_celsius()` "por si acaso", como en Java.

## 5. El guion bajo

Python no tiene atributos privados. Hay una convención: un nombre que empieza por `_`, como `_celsius` o el `_round1` de la semana 8, dice "es interno, no lo uses desde fuera; puede cambiar sin avisar". Nada lo impide, y los tests a veces lo leen. Con dos guiones bajos delante (`__celsius`), Python cambia el nombre por dentro (`_Thermometer__celsius`) para evitar choques con clases hijas. Casi nunca hace falta: usa uno.

## 6. `@classmethod` y `@staticmethod`

```python
    @classmethod
    def from_fahrenheit(cls, name: str, fahrenheit: float) -> Thermometer:
        return cls(name, cls.to_celsius(fahrenheit))

    @staticmethod
    def to_celsius(fahrenheit: float) -> float:
        return round((fahrenheit - 32) * 5 / 9, 1)


Thermometer.from_fahrenheit("Houston", 98.6)   # Houston: 37.0 °C
Thermometer.to_celsius(212.0)                  # 100.0
```

| | Recibe | Para qué |
|---|---|---|
| Método normal | El objeto, en `self` | Casi todo |
| `@classmethod` | La clase, en `cls` | Crear objetos de otra forma: un **constructor alternativo**. `dict.fromkeys`, `Path.cwd` y `datetime.fromisoformat` son de este tipo |
| `@staticmethod` | Nada | Una función que tiene que ver con la clase pero no necesita ni objeto ni clase |

`from_fahrenheit` llama a `cls(...)` y no a `Thermometer(...)` para que, en una clase hija (semana 10), cree un objeto de la hija. En tu proyecto, `Measurement.from_line("Norte;12,5")` es un constructor alternativo: crea la medida a partir de una línea de texto, y devuelve `None` si la línea no vale.

Desde Python 3.14, una clase puede nombrarse a sí misma en sus tipos sin comillas, como el `-> Thermometer` de arriba: las anotaciones se evalúan solo cuando alguien las pide (PEP 649). En código antiguo verás `-> "Thermometer"` o `from __future__ import annotations` para lo mismo.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| Se imprime `<... object at 0x...>` | La clase no tiene `__repr__` | Escríbelo, o usa `@dataclass` |
| `TypeError: cannot use '...' as a set element (unhashable type: ...)` | La clase define `__eq__` y no es inmutable | `@dataclass(frozen=True)` si los datos no cambian; si cambian, no la metas en un `set` |
| `TypeError: 'float' object is not callable` | Escribiste `kitchen.fahrenheit()` | Una propiedad se lee sin paréntesis |
| `RecursionError: maximum recursion depth exceeded` | El *setter* asigna a la propiedad (`self.celsius = ...`) | Guarda en el atributo interno: `self._celsius = ...` |
| `AttributeError: property 'celsius' of 'Thermometer' object has no setter` | Una propiedad sin *setter* recibe una asignación, a veces en `__init__` | Añade `@celsius.setter`, o no la asignes |

---

## ✅ Qué debes saber al terminar

- [ ] Qué es un método especial y quién lo llama.
- [ ] La diferencia entre `__repr__` y `__str__`, y cuál escribir si solo escribes uno.
- [ ] Cómo se escribe `__eq__`, para qué sirve `NotImplemented` y por qué la clase pierde su *hash*.
- [ ] Cuándo usar una propiedad y por qué no se escriben *getters* y *setters* por adelantado.
- [ ] Qué significa un guion bajo delante de un nombre.
- [ ] La diferencia entre un método normal, un `@classmethod` y un `@staticmethod`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · Clases y objetos](01-clases-y-objetos.md) | **02 · Propiedades y métodos especiales** | [03 · `dataclasses`](03-dataclasses.md) |
