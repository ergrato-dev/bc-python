# 01 · Funciones como objetos

⏱️ 45 min

## 🎯 Objetivos

- Tratar una función como un valor más: guardarla en una variable, en una lista o en un diccionario.
- Pasar funciones como argumento (`key=`, `map`, `filter` y funciones propias).
- Escribir funciones que devuelven funciones.
- Anotar con `Callable` el tipo de una función que se pasa o se devuelve.

---

## 1. Una función es un objeto

`def` hace dos cosas: crea un objeto función y lo guarda con un nombre. Ese objeto se usa como cualquier otro valor:

```python
def to_fahrenheit(celsius: float) -> float:
    """Grados Celsius a Fahrenheit."""
    return celsius * 9 / 5 + 32


convert = to_fahrenheit          # otro nombre para el mismo objeto, sin paréntesis
convert(10.0)                    # 50.0
convert is to_fahrenheit         # True
to_fahrenheit.__name__           # 'to_fahrenheit'
to_fahrenheit.__doc__            # 'Grados Celsius a Fahrenheit.'
type(to_fahrenheit)              # <class 'function'>
```

La diferencia está en los paréntesis: `to_fahrenheit` **es** la función; `to_fahrenheit(10.0)` la **llama** y vale `50.0`. Como es un valor, cabe en una estructura de datos:

```python
conversions = {
    "F": to_fahrenheit,
    "K": lambda celsius: celsius + 273.15,
}
conversions["K"](10.0)           # 283.15
```

Un diccionario de funciones sustituye a una cadena de `if unit == "F": ... elif unit == "K": ...`: añadir una unidad es añadir una entrada.

Que las funciones sean objetos como cualquier otro se dice así: en Python, las funciones son **de primera clase** (*first-class*). Todo lo de esta semana (closures, decoradores, `functools`) se apoya en esto.

---

## 2. `lambda`: una función sin nombre

```python
lambda celsius: celsius + 273.15
```

Una `lambda` es una función de **una sola expresión**, sin `return` ni nombre. Sirve para funciones pequeñas que se escriben donde se usan, casi siempre como argumento. Si la vas a guardar en una variable, escribe un `def`: tendrá nombre en los errores y admite *docstring* (ruff lo pide con la regla `E731`, que no está activa por defecto).

---

## 3. Funciones que reciben funciones

Una función que recibe o devuelve funciones se llama **de orden superior** (*higher-order*). Ya usas varias:

```python
readings = [("Norte", 12.5), ("Sur", 8.0), ("Centro", 55.1)]

sorted(readings, key=lambda reading: reading[1])     # por valor
max(readings, key=lambda reading: reading[1])        # ('Centro', 55.1)
list(map(abs, [-1.5, 2.0]))                          # [1.5, 2.0]
list(filter(lambda v: v > 10, [12.5, 8.0]))          # [12.5]
```

`key=` recibe una función y la llama una vez por elemento: es la que usaste en la semana 5 con `top`. Para `map` y `filter`, una *comprehension* suele leerse mejor (`[abs(v) for v in values]`); se usan con funciones que ya tienen nombre, como `map(abs, values)`.

Escribir las tuyas es igual de sencillo:

```python
def apply_to_values(function: Callable[[float], float], values: list[float]) -> list[float]:
    return [function(value) for value in values]


apply_to_values(to_fahrenheit, [0.0, 10.0])          # [32.0, 50.0]
```

Es lo que hace `Series.where` en tu proyecto: recibe la regla que decide qué medidas se quedan, y la serie no necesita saber cuál es.

```python
series.where(lambda m: m.label == "Norte")
series.where(lambda m: m.has_value)
```

---

## 4. Funciones que devuelven funciones

Dentro de una función puedes definir otra y devolverla:

```python
def make_threshold(limit: float) -> Callable[[float], bool]:
    def is_above(value: float) -> bool:
        return value > limit

    return is_above            # sin paréntesis: devuelve la función, no la llama


above_50 = make_threshold(50.0)
above_50(55.1)                 # True
above_50(12.5)                 # False
```

`make_threshold` es una **fábrica de funciones**. Lo curioso es que `is_above` sigue usando `limit` cuando `make_threshold` ya terminó. Cómo lo consigue es el tema de la teoría 02: es una *closure*.

---

## 5. El tipo de una función: `Callable`

`collections.abc.Callable` describe una función por lo que recibe y lo que devuelve:

| Anotación | Significa |
|---|---|
| `Callable[[float], float]` | Recibe un `float`, devuelve un `float` |
| `Callable[[Measurement], bool]` | Una regla para `Series.where` |
| `Callable[[], int]` | Sin argumentos, devuelve un `int` |
| `Callable[..., float]` | Cualquier argumento, devuelve un `float` (mypy deja de comprobar los argumentos) |

mypy comprueba que la función que pasas encaja:

```python
apply_to_values(str.upper, [1.0])
# error: Argument 1 to "apply_to_values" has incompatible type
# "Callable[[str], str]"; expected "Callable[[float], float]"  [arg-type]
```

`Callable` también es un `Protocol` (semana 10): cualquier objeto con `__call__` encaja, sea una función, una `lambda`, un método o una instancia de una clase que defina `__call__`.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: 'float' object is not callable` | Pasaste `to_fahrenheit(10.0)` (el resultado) donde se esperaba la función | Pasa `to_fahrenheit`, sin paréntesis |
| Se imprime `<function to_fahrenheit at 0x...>` | Olvidaste los paréntesis al llamar | `to_fahrenheit(10.0)` |
| `sorted` ordena por la etiqueta y no por el valor | Sin `key=`, las tuplas se comparan por el primer elemento | `key=lambda reading: reading[1]` |
| Una `lambda` larga que nadie entiende | Más de una idea en una expresión | Escribe un `def` con nombre |
| `mypy`: `incompatible type "Callable[[str], str]"; expected ...` | La función que pasas no recibe o no devuelve lo que se pide | Pasa otra función, o revisa la anotación |

---

## ✅ Qué debes saber al terminar

- [ ] Qué diferencia hay entre `función` y `función()`.
- [ ] Guardar funciones en un diccionario y elegir una por clave.
- [ ] Cuándo usar una `lambda` y cuándo un `def`.
- [ ] Qué es una función de orden superior y tres ejemplos de la biblioteca estándar.
- [ ] Anotar con `Callable[[...], ...]` una función que se pasa o se devuelve.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 12](../README.md) | **01 · Funciones como objetos** | [02 · Closures y alcance](02-closures-y-alcance.md) |
