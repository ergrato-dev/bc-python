# 02 · Tipos avanzados

⏱️ 50 min

## 🎯 Objetivos

- Describir un diccionario con claves fijas con `TypedDict`.
- Elegir `Mapping` y `Sequence` en lugar de `dict` y `list` cuando una función solo lee.
- Escribir funciones y clases genéricas con `[T]`.
- Diferenciar un alias (`type`) de un tipo nuevo (`NewType`).
- Limitar valores con `Literal` y `Final`, y comprobar un `match` con `assert_never`.

---

## 1. `TypedDict`: un `dict` con claves fijas

`summary_data` devuelve un `dict[str, object]`. Para mypy, eso significa que puede tener cualquier clave y que cada valor es un `object`: `summary["mediana"] + 1` no pasaría, y `summary["media"]`, con una errata, sí.

```python
from typing import TypedDict


class Summary(TypedDict):
    registros: int
    con_valor: int
    mediana: float | None
    mayor_salto: float | None
```

`Summary` describe las claves y el tipo de cada una. En ejecución no existe: un `Summary` **es** un `dict`, y `json.dump` lo guarda igual. La diferencia está toda en mypy:

```
error: TypedDict "Summary" has no key "media"  [typeddict-item]
note: Did you mean "mediana"?
error: Missing key "mediana" for TypedDict "Summary"  [typeddict-item]
```

| Necesitas | Usa |
|---|---|
| Un JSON con claves conocidas que solo pasa de un sitio a otro | `TypedDict` |
| Un objeto con comportamiento (métodos, reglas al crearlo) | `@dataclass` |
| Validar datos de fuera, con conversión y errores claros | Un modelo de Pydantic (teoría 03) |

Las claves opcionales se marcan con `NotRequired[...]`, y todo el diccionario con `total=False`. No los necesitas esta semana.

---

## 2. `Mapping` y `Sequence`: pide solo lo que usas

Cambias `summary_data` para que devuelva un `Summary`, y mypy protesta en otro sitio:

```
error: Argument 1 to "write_json" has incompatible type "Summary"; expected "dict[str, object]"  [arg-type]
```

Un `Summary` no es un `dict[str, object]`, porque con un `dict[str, object]` se puede hacer `data["otra"] = "texto"`, y eso rompería el `Summary`. mypy no mira si `write_json` lo hace: solo mira lo que **podría** hacer con ese tipo. Lo mismo pasa con las listas:

```
error: Argument 1 to "total" has incompatible type "list[float]"; expected "list[float | None]"  [arg-type]
note: "list" is invariant -- see https://mypy.readthedocs.io/en/stable/common_issues.html#variance
note: Consider using "Sequence" instead, which is covariant
```

Una función que recibe `list[float | None]` podría añadir un `None` a tu lista de `float`. Por eso `list` es **invariante**: solo acepta exactamente `list[float | None]`.

Los tipos de solo lectura de `collections.abc` no tienen ese problema, porque no permiten cambiar nada:

| Si la función solo... | Pide | En lugar de |
|---|---|---|
| lee claves y valores | `Mapping[K, V]` | `dict[K, V]` |
| recorre e indexa | `Sequence[T]` | `list[T]` |
| recorre una vez | `Iterable[T]` | `list[T]` |

`write_json(data: Mapping[str, object], path)` acepta un `Summary`, un `dict` cualquiera o un `MappingProxyType`. La regla, como en la semana 10 con `Protocol`: pide lo mínimo que necesitas, devuelve lo más concreto que tienes.

---

## 3. Genéricos con `[T]`

Una función que devuelve el primer elemento de una secuencia funciona con cualquier tipo. Con `Sequence[object]` perderías el tipo; con `Any`, la comprobación. Una **variable de tipo** dice "lo que entra es lo que sale":

```python
from collections.abc import Sequence


def first[T](items: Sequence[T]) -> T:
    return items[0]


reveal_type(first(["Norte", "Sur"]))   # mypy: Revealed type is "str"
```

Es la sintaxis de Python 3.12. El `[**P, R]` de tus decoradores de la semana 12 es lo mismo, para firmas enteras. Una clase también puede ser genérica:

```python
class Window[T]:
    def __init__(self, size: int) -> None:
        self.size = size
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items = [*self.items, item][-self.size :]


window = Window[float](2)
window.push("alto")   # mypy: Argument 1 to "push" of "Window" has incompatible type "str"; expected "float"
```

`reveal_type(x)` sirve para preguntar: mypy escribe el tipo que deduce como una nota, y Python escribe el tipo real en ejecución (`Runtime type is 'str'`). Úsalo para mirar y bórralo después.

---

## 4. Alias y `NewType`

Desde la semana 5 tu proyecto tiene `Record = tuple[str, float | None]`. En Python 3.12+ se escribe con la palabra `type`:

```python
type Record = tuple[str, float | None]
```

Un **alias** es otro nombre para el mismo tipo: un `tuple[str, float | None]` cualquiera vale donde se pide un `Record`. A veces quieres lo contrario, que mypy **no** mezcle dos cosas que en ejecución son iguales:

```python
from typing import NewType

Celsius = NewType("Celsius", float)


def to_fahrenheit(value: Celsius) -> float:
    return value * 9 / 5 + 32


to_fahrenheit(Celsius(10.0))   # bien
to_fahrenheit(10.0)            # mypy: incompatible type "float"; expected "Celsius"
```

`Celsius(10.0)` devuelve el mismo `float`: no cuesta nada al ejecutar. Sirve para unidades, identificadores (`StationId`) o textos ya validados.

---

## 5. `Literal`, `Final` y `assert_never`

`Literal` limita un tipo a unos valores concretos. Tus niveles son cuatro textos fijos:

```python
from typing import Final, Literal

type Level = Literal["bajo", "medio", "alto"]
HIGH: Final = 50.0
```

mypy rechaza `color("altísimo")` y `HIGH = 60.0`. Python no comprueba ninguna de las dos cosas al ejecutar: las anotaciones no se ejecutan.

Con un `Literal`, mypy puede comprobar que un `match` cubre todos los casos:

```python
from typing import assert_never


def advice(level: Level) -> str:
    match level:
        case "bajo":
            return "sin aviso"
        case "medio":
            return "vigilar"
        case "alto":
            return "alerta"
        case _:
            assert_never(level)
```

Si borras el `case "alto"`, mypy ve que `"alto"` llega al `case _`:

```
error: Argument 1 to "assert_never" has incompatible type "Literal['alto']"; expected "Never"  [arg-type]
```

`Never` es el tipo sin valores: `assert_never` solo acepta lo que no puede pasar. Si mañana añades un nivel, mypy te dice en qué `match` falta.

> Tu `classify` de la semana 2 devuelve `str`, no `Literal[...]`. Cambiarlo obligaría a revisar todo lo que lo usa, y no ganarías nada en esta capa. Un tipo más preciso vale la pena donde evita errores reales, no en todas partes.

---

## 🧯 Errores típicos

| Error | Causa | Solución |
|---|---|---|
| `incompatible type "Summary"; expected "dict[str, object]"` | La función pide `dict` y le pasas un `TypedDict` | Que pida `Mapping[str, object]` si solo lee |
| `"list" is invariant` | Pasas `list[float]` donde se pide `list[float \| None]` | `Sequence[float \| None]` si la función no cambia la lista |
| `TypedDict "..." has no key "..."` | Una clave mal escrita | La nota `Did you mean` dice cuál querías |
| `Need type annotation for "items"` | Una lista vacía sin anotar dentro de una clase genérica | `self.items: list[T] = []` |
| `assert_never` con `expected "Never"` | Al `match` le falta un caso | Añade el `case` que dice el error |

---

## ✅ Qué debes saber al terminar

- [ ] Cuándo usar `TypedDict`, `@dataclass` o un modelo de Pydantic.
- [ ] Por qué `list` es invariante y qué pides en su lugar.
- [ ] Escribir una función genérica con `[T]` y comprobarla con `reveal_type`.
- [ ] La diferencia entre `type Record = ...` y `NewType`.
- [ ] Hacer que mypy compruebe que un `match` cubre todos los valores de un `Literal`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · mypy estricto](01-mypy-estricto.md) | **02 · Tipos avanzados** | [03 · Modelos de Pydantic](03-modelos-pydantic.md) |
