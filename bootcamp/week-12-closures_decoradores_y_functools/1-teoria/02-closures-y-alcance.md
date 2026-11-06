# 02 · Closures y alcance

⏱️ 50 min

## 🎯 Objetivos

- Prever qué variable usa Python cuando un nombre aparece en varios sitios (la regla LEGB).
- Explicar qué es una *closure* y qué guarda.
- Cambiar una variable de la función de fuera con `nonlocal` y saber por qué `global` casi nunca es la respuesta.
- Evitar la trampa de las closures creadas en un bucle.

---

## 1. Dónde busca Python un nombre: LEGB

Cuando escribes `limit` dentro de una función, Python busca ese nombre en cuatro sitios, en este orden, y usa el primero donde lo encuentra:

| Letra | Alcance | Qué hay |
|---|---|---|
| **L** | *Local* | Los parámetros y las variables que la función asigna |
| **E** | *Enclosing* | Las variables de las funciones que la rodean, si está definida dentro de otra |
| **G** | *Global* | Las variables del módulo (las de arriba del archivo) |
| **B** | *Built-in* | Lo que Python trae: `len`, `print`, `max`... |

![Cuatro cajas, una dentro de otra: built-in contiene global, global contiene enclosing y enclosing contiene local. Una búsqueda de limit sale de la caja local y va hacia fuera; se detiene en enclosing, donde make_threshold guardó limit = 10.0, y no llega al limit = 50.0 global](../0-assets/01-alcance-legb.svg)

```python
limit = 50.0                   # global


def is_high(value: float) -> bool:
    return value > limit       # L: no hay limit; E: no hay función de fuera; G: 50.0
```

### Asignar crea una variable local

La regla que más sorprende: si una función **asigna** un nombre en cualquier parte de su cuerpo, ese nombre es local en **toda** la función, también antes de la asignación.

```python
def change_limit() -> None:
    limit = 10.0               # una variable local nueva; la global no cambia
```

Y si lees antes de asignar:

```python
total = 0


def add() -> None:
    total += 1                 # total = total + 1: asigna, así que total es local
```

```
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
```

Python decide qué nombres son locales al **compilar** la función, no al ejecutarla línea a línea. ruff lo detecta sin ejecutar: ``F823 Local variable `total` referenced before assignment``.

### `global`, y por qué casi nunca

`global total` dentro de la función hace que `total` sea la del módulo. Funciona, pero cualquier función puede cambiar esa variable, los tests se pisan entre sí y el resultado depende del orden en que se llamaron. Lo has evitado desde la semana 3 pasando argumentos y devolviendo valores, y sigue siendo lo correcto. La única global habitual es una **constante** que nadie reasigna (`UNIT`, `LOW`, `HIGH`).

---

## 2. Closures

Vuelve a la fábrica de la teoría 01:

```python
def make_threshold(limit: float) -> Callable[[float], bool]:
    def is_above(value: float) -> bool:
        return value > limit       # E: limit es de make_threshold

    return is_above


above_50 = make_threshold(50.0)
above_10 = make_threshold(10.0)
above_50(12.5), above_10(12.5)     # (False, True)
```

Cuando `make_threshold` termina, sus variables locales deberían desaparecer. Pero `is_above` usa `limit`, así que Python lo guarda **junto a la función**. Una función que lleva consigo las variables de la función que la rodeaba se llama **closure** (*clausura*).

Cada llamada a `make_threshold` crea una función nueva con **su propio** `limit`: `above_50` y `above_10` no se estorban. Puedes ver lo que guarda:

```python
above_50.__closure__[0].cell_contents     # 50.0
above_50.__code__.co_freevars             # ('limit',)
```

Cada variable recordada vive en una **celda** (*cell*). La closure no copia el valor: guarda la celda, que apunta a la variable de fuera.

Una closure es una forma ligera de tener **estado sin clase**: `above(50.0)` en tu proyecto hace lo que haría una clase `Above` con un atributo `limit` y un método `__call__`, en cuatro líneas.

---

## 3. `nonlocal`: cambiar la variable de fuera

Leer una variable de fuera funciona sola. **Asignarla** la convertiría en local (sección 1). Para asignar la de la función que te rodea, decláralo con `nonlocal`:

```python
def make_counter() -> Callable[[], int]:
    count = 0

    def increment() -> int:
        nonlocal count             # count es la de make_counter
        count += 1
        return count

    return increment


counter = make_counter()
counter(), counter(), counter()    # (1, 2, 3)
make_counter()()                   # 1: cada contador tiene su count
```

| Palabra | Asigna en | Úsala |
|---|---|---|
| (ninguna) | El alcance local | Casi siempre |
| `nonlocal x` | La función que rodea a esta | Para estado en una closure (contadores, decoradores con memoria) |
| `global x` | El módulo | Casi nunca |

`nonlocal` solo vale dentro de una función anidada: en el nivel del módulo es un `SyntaxError: nonlocal declaration not allowed at module level`.

---

## 4. La trampa del bucle

```python
checks = [lambda value: value > limit for limit in (10.0, 30.0, 50.0)]
[check(20.0) for check in checks]          # [False, False, False]
```

Esperabas `[True, False, False]`. Las tres `lambda` guardan la **misma** celda, la variable `limit` del bucle, y la miran cuando se **llaman**, no cuando se crean. Para entonces el bucle terminó y `limit` vale `50.0`. Es el *late binding*: la closure recuerda la variable, no su valor en ese momento.

Dos arreglos:

```python
# 1. Un valor por defecto se calcula al crear la función
checks = [lambda value, limit=limit: value > limit for limit in (10.0, 30.0, 50.0)]

# 2. Una fábrica: cada llamada crea su propia celda
checks = [make_threshold(limit) for limit in (10.0, 30.0, 50.0)]
```

La fábrica se lee mejor y no añade un parámetro que nadie debe pasar. ruff avisa de la trampa: ``B023 Function definition does not bind loop variable `limit` ``.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `UnboundLocalError: cannot access local variable 'total' where it is not associated with a value` | Asignas una variable de fuera (`+=`) sin declararla | `nonlocal total`, o mejor, devuelve el valor |
| Una función cambia una variable y otra no lo ve | La asignación creó una local con el mismo nombre | No reutilices nombres de fuera; pasa y devuelve |
| `SyntaxError: nonlocal declaration not allowed at module level` | `nonlocal` fuera de una función anidada | Usa `nonlocal` solo dentro de la función de dentro |
| Todas las funciones de un bucle dan lo mismo | *Late binding*: comparten la variable del bucle | Una fábrica o un valor por defecto |
| Los tests pasan solos y fallan juntos | Una función cambia una variable `global` | Quita el `global`: pasa el estado como argumento |

---

## ✅ Qué debes saber al terminar

- [ ] El orden LEGB y en qué alcance está cada variable de un ejemplo.
- [ ] Por qué `total += 1` en una función anidada lanza `UnboundLocalError`.
- [ ] Qué es una closure y qué guarda `__closure__`.
- [ ] Cuándo usar `nonlocal` y por qué evitar `global`.
- [ ] Por qué las `lambda` de un bucle dan todas lo mismo y dos formas de arreglarlo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · Funciones como objetos](01-funciones-como-objetos.md) | **02 · Closures y alcance** | [03 · Decoradores](03-decoradores.md) |
