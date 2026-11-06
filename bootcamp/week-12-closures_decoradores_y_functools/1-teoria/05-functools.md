# 05 · functools

⏱️ 50 min

## 🎯 Objetivos

- Fijar argumentos de una función con `partial`.
- Recordar resultados con `cache` y `lru_cache`, y saber cuándo **no** usarlos.
- Calcular una propiedad una sola vez con `cached_property`.
- Plegar una secuencia con `reduce` y elegir la función según el tipo con `singledispatch`.
- Entender el diseño de la capa 11 del Observatorio y cómo se prueban closures y decoradores.

---

## 1. `partial`: fijar argumentos

```python
from functools import partial


def convert(value: float, factor: float, offset: float = 0.0) -> float:
    return value * factor + offset


to_fahrenheit = partial(convert, factor=9 / 5, offset=32)
to_fahrenheit(10.0)                     # 50.0
from_binary = partial(int, base=2)
from_binary("1010")                     # 10
```

`partial(func, *args, **kwargs)` devuelve un objeto que, al llamarlo, llama a `func` con esos argumentos ya puestos y los nuevos detrás. Es la closure de la teoría 02 sin escribir la fábrica: `to_fahrenheit.func`, `.args` y `.keywords` dicen qué guarda. Úsalo para dar una función con la forma que pide otra, por ejemplo para `map` o para `key=`.

---

## 2. `cache` y `lru_cache`: recordar resultados

Una función **pura** (mismo argumento, mismo resultado, sin efectos) puede guardar lo que ya calculó:

```python
from functools import cache


@cache
def ways(steps: int) -> int:
    """Formas de subir steps escalones de uno en uno o de dos en dos."""
    return 1 if steps <= 1 else ways(steps - 1) + ways(steps - 2)


ways(25)                 # 121393, con 26 cálculos en lugar de 242.785
ways.cache_info()        # CacheInfo(hits=23, misses=26, maxsize=None, currsize=26)
```

El decorador guarda un diccionario `argumentos → resultado`. Si llegan argumentos que ya vio (*hit*), devuelve el resultado guardado sin llamar a la función; si no (*miss*), la llama y lo guarda.

| Decorador | Guarda | Úsalo cuando |
|---|---|---|
| `@cache` | Todo, sin límite | Los argumentos posibles son pocos |
| `@lru_cache(maxsize=128)` | Los `maxsize` usados más recientemente (*Least Recently Used*) | Pueden llegar muchos argumentos distintos |

Tres condiciones para usarlos:

1. **Argumentos *hashables***: son claves de un diccionario. Con una lista: `TypeError: unhashable type: 'list'`. Pasa una tupla.
2. **Función pura**: si la función lee un archivo o la hora, la caché devolvería datos viejos.
3. **No en métodos**: `@lru_cache` sobre un método guarda `self` en la caché, que mantiene vivo cada objeto para siempre. ruff avisa: ``B019 Use of `functools.lru_cache` or `functools.cache` on methods can lead to memory leaks``.

`ways.cache_clear()` vacía la caché, por ejemplo entre tests.

### `cached_property`

Una `@property` se calcula cada vez que la lees. `@cached_property` la calcula la primera vez y guarda el resultado en el `__dict__` del objeto:

```python
class Report:
    def __init__(self, values: list[float]) -> None:
        self.values = values

    @cached_property
    def total(self) -> float:
        return sum(self.values)        # una sola vez por objeto
```

No funciona con `slots=True`, porque esos objetos no tienen `__dict__`: `TypeError: No '__dict__' attribute on 'Series' instance to cache 'total' property.` Tu `Series` tiene *slots* (semana 9) y es mutable: un total guardado quedaría viejo tras `add`. Por eso no lo usa.

---

## 3. `reduce`: plegar una secuencia

```python
from functools import reduce

reduce(lambda acc, v: acc + v, [12.5, 8.0, 55.1], 0.0)    # 75.6
```

`reduce(func, iterable, inicial)` va combinando: `func(func(func(0.0, 12.5), 8.0), 55.1)`. Casi todo lo que harías con `reduce` ya tiene función propia (`sum`, `max`, `min`, `math.prod`, `"".join`, `any`, `all`), más legible y más rápida. Úsalo cuando no la haya, y pásale siempre el valor inicial: con una lista vacía y sin él, `TypeError: reduce() of empty iterable with no initial value`.

---

## 4. `singledispatch`: una función por tipo

Quieres una función `describe` que acepte una medida, una serie o una escala y escriba una frase distinta para cada una. Con `if isinstance(...)` encadenados, cada tipo nuevo obliga a tocar la misma función. `singledispatch` reparte por el tipo del **primer argumento**:

```python
from functools import singledispatch


@singledispatch
def describe(item: object) -> str:
    raise TypeError(f"describe no acepta {type(item).__name__}")


@describe.register
def _(item: Measurement) -> str:
    text = "sin dato" if item.value is None else str(item.value).replace(".", ",")
    return f"{item.label}: {text}"


@describe.register
def _(item: Series) -> str:
    return f"medidas: {len(item)} · etiquetas: {len(item.labels())}"


describe(Measurement("Norte", 12.5))     # 'Norte: 12,5'
describe(Series())                       # 'medidas: 0 · etiquetas: 0'
describe(12)                             # TypeError: describe no acepta int
```

- La función decorada con `@singledispatch` es la versión **por defecto**: la que se usa si ningún tipo registrado encaja.
- `@describe.register` lee la anotación del primer parámetro para saber a qué tipo corresponde. Las implementaciones se llaman `_` porque nadie las llama por su nombre.
- Busca por la jerarquía de clases: una subclase usa la versión de su clase base. `describe.registry` es el diccionario `tipo → función`.
- Acepta uniones: `def _(item: int | float)`.

**Trampa**: a mypy le vale un `int` donde pides `float`, pero a `singledispatch` no. `int` no es subclase de `float`: si solo registras `float`, `describe(3)` va a la versión por defecto.

Es un decorador con estado (el registro) y otra forma del polimorfismo de la semana 10: allí cada clase traía su método; aquí la función crece por fuera, sin tocar las clases. `functools.singledispatchmethod` hace lo mismo con métodos.

---

## 5. La capa 11 del Observatorio

| Pieza | Herramienta | Por qué así |
|---|---|---|
| `Series.where(keep)` | Función como argumento | La serie no sabe qué regla aplicas: basta con una función `Measurement → bool` |
| `above(limit)` | Closure | Una regla con un parámetro, en cuatro líneas y sin clase |
| `skip_missing` | Decorador con `wraps` | Las funciones de conversión no tienen que comprobar `None` cada una |
| `rounded(digits)` | Decorador con argumento y `ParamSpec` | Redondear al presentar, sin tocar el cálculo; mypy sigue comprobando las llamadas |
| `describe` | `singledispatch` | Una frase por tipo del modelo, sin `isinstance` en cadena |
| `functional.py` aparte | Dependencia en un sentido | `functional` importa `model`; `model` no importa `functional` |
| Sin `cache` | Sección 2 | Las funciones del núcleo son rápidas y `Series` es mutable: nada que ganar, un riesgo de datos viejos |

`main` no cambia esta semana. En la semana 15, la CLI con Typer registra comandos con decoradores, y estas piezas le darán filtros (`--above 50`) sin escribir uno por comando.

---

## 6. Probar closures y decoradores

Un decorador se prueba decorando una función pequeña **dentro** del test:

```python
def test_skip_missing_returns_none_without_calling_the_function() -> None:
    calls: list[float] = []

    @skip_missing
    def remember(value: float) -> float:
        calls.append(value)
        return value

    assert remember(None) is None
    assert calls == []                  # la original ni se llamó
```

Lo que conviene comprobar:

1. **El resultado** con un caso normal.
2. **Si llama o no a la original**: una lista que apunta las llamadas lo dice sin más herramientas (en la semana 14 lo harás con *mocks*).
3. **Que conserva la identidad**: `__name__`, `__doc__` y `__wrapped__`. Sin `wraps` falla aquí.
4. **Que cada closure tiene su estado**: dos `above` con límites distintos no se estorban.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: unhashable type: 'list'` | Una lista como argumento de una función con `@cache` | Pasa una tupla |
| La función con caché devuelve datos viejos | No es pura: lee archivos, la hora o algo mutable | Quita la caché, o `cache_clear()` cuando cambie el dato |
| `B019 ... on methods can lead to memory leaks` | `@lru_cache` sobre un método | Una función a nivel de módulo, o `cached_property` |
| `TypeError: No '__dict__' attribute on ... to cache ...` | `cached_property` en una clase con `slots=True` | Quita `slots`, o usa una `property` |
| `TypeError: reduce() of empty iterable with no initial value` | `reduce` sin valor inicial y con una secuencia vacía | Pásale el tercer argumento |
| `describe(3)` va a la versión por defecto | Solo registraste `float` | Registra `int \| float` |
| ``TypeError: Invalid first argument to `register()` `` | La implementación no tiene anotación en el primer parámetro | Anota el tipo: `def _(item: Series)` |

---

## ✅ Qué debes saber al terminar

- [ ] Fijar argumentos con `partial` y qué guarda.
- [ ] Las tres condiciones para usar `cache` o `lru_cache`, y qué es un *hit*.
- [ ] Por qué `cached_property` no sirve en tu `Series`.
- [ ] Qué hace `reduce` y qué función usarías en su lugar casi siempre.
- [ ] Registrar tipos en una función `singledispatch` y qué pasa con un tipo no registrado.
- [ ] Qué comprueba un buen test de un decorador.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Decoradores con argumentos](04-decoradores-con-argumentos.md) | **05 · functools** | [Ejercicio 01 · Funciones y closures](../2-practicas/ejercicio-01-funciones-y-closures/README.md) |
