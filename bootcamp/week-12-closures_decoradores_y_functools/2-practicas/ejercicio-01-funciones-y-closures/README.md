# Ejercicio 01 — Funciones y closures

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-funciones-como-objetos.md) y [02](../../1-teoria/02-closures-y-alcance.md)

## Objetivo

Usar funciones como valores (en variables, diccionarios y argumentos), ver dónde busca Python cada nombre, escribir closures con y sin `nonlocal` y caer en la trampa de las closures de un bucle para saber salir. Es lo que hacen `Series.where` y `above` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `closure_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-12-closures_decoradores_y_functools/2-practicas/ejercicio-01-funciones-y-closures/starter
uv run python closure_lab.py
```

```
Ejercicio 01 · Funciones y closures
```

Descomenta en orden: el paso 5 usa `make_threshold`, del paso 4. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. Una función es un objeto

Descomenta el **PASO 1** y ejecuta:

```
Otro nombre, la misma función: True 50.0
Tiene atributos: to_fahrenheit · Grados Celsius a Fahrenheit.
Su tipo: function
  10 °C en F: 50.00
  10 °C en K: 283.15
```

`convert = to_fahrenheit`, sin paréntesis, no llama a nada: da otro nombre al mismo objeto (`is` dice `True`). Una función tiene atributos como cualquier objeto: `__name__` y `__doc__`. Y cabe en un diccionario: `conversions` guarda una función con nombre y una `lambda`, y el `for` las llama sin saber cuál es cuál. Añadir una unidad es añadir una entrada, sin otro `elif`.

### 2. Funciones que reciben funciones

Descomenta el **PASO 2** y ejecuta:

```
Ordenadas por valor: ['Sur', 'Norte', 'Este', 'Centro']
La más alta: ('Centro', 55.1)
Dobles: [2.0, 5.0]
Con map: [1.5, 2.0, 3.0]
```

`sorted` y `max` reciben `value_of` en `key=` y la llaman una vez por tupla: ordenan por lo que devuelve. Sin `key=`, ordenarían por la etiqueta, el primer elemento. `apply_to_values` es tuya y hace lo mismo que `map`: recibe una función y la aplica. Su primer parámetro está anotado con `Callable[[float], float]`: mypy rechazaría `apply_to_values(str.upper, ...)`.

### 3. El alcance de una variable (LEGB)

Descomenta el **PASO 3** y ejecuta:

```
Lee la global: True
  Dentro, otra variable: 10.0
La global no cambia: 50.0
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
```

- `is_high` **lee** `limit`: no la encuentra en local y la toma del módulo (G).
- `change_limit` **asigna** `limit = 10.0`: eso crea una variable local con el mismo nombre. La global sigue en `50.0`.
- `add` hace `total += 1`, que es `total = total + 1`: como asigna, `total` es local en **toda** `add`, y al leerla todavía no tiene valor.

La línea de `total += 1` lleva `# noqa: F823, F841` porque ruff detecta el error sin ejecutar y aquí lo provocas a propósito. Quita el comentario y ejecuta `uvx ruff@0.17.3 check closure_lab.py` para verlo: ``F823 Local variable `total` referenced before assignment``.

### 4. Closures y `nonlocal`

Descomenta el **PASO 4** y ejecuta:

```
¿55,1 > 50? True · ¿8 > 10? False
Lo que recuerda above_50: 50.0
Contador: 1 2 3 · otro: 1
```

`make_threshold(50.0)` ya terminó cuando llamas a `above_50`, pero `is_above` sigue viendo `limit`: Python lo guardó en una **celda** junto a la función. Eso es una closure, y `__closure__[0].cell_contents` te deja verla. Cada llamada a la fábrica crea su celda: `above_10` tiene la suya.

`make_counter` va más allá: `increment` **cambia** `count`. Sin `nonlocal count` pasaría lo del paso 3; con él, `count` es la de `make_counter`. `counter` y `other` tienen cada uno su `count`. Es estado sin escribir una clase.

### 5. La trampa de las closures en un bucle

Descomenta el **PASO 5** y ejecuta:

```
Tarde, ¿20 supera cada límite? [False, False, False]
Con valor por defecto: [True, False, False]
Con una fábrica: [True, False, False]
```

¿Por qué `[False, False, False]`? Las tres `lambda` de `late` guardan la **misma** variable `limit`, la del bucle, y la miran al **llamarlas**. Para entonces el bucle terminó y `limit` vale `50.0`: `20 > 50` tres veces. Es el *late binding*.

- Con `limit=limit`, el valor por defecto se calcula al **crear** cada `lambda`: cada una guarda su límite.
- Con `make_threshold(limit)`, cada llamada a la fábrica crea su propia celda. Se lee mejor y es lo que hace `above` en tu proyecto.

La primera línea lleva `# noqa: B023`: es el aviso de ruff para esta trampa (``B023 Function definition does not bind loop variable `limit` ``).

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: value_of() missing 1 required positional argument: 'reading'` | Escribiste `key=value_of()`, con paréntesis: pasa `value_of`, sin llamarla |
| Se imprime `<function make_threshold.<locals>.is_above at 0x...>` | Falta llamar a la función que devuelve la fábrica: `above_50(55.1)` |
| `NameError: name 'make_threshold' is not defined` en el paso 5 | Descomenta antes el paso 4 |
| `SyntaxError: no binding for nonlocal 'count' found` | La línea `count = 0` no está en `make_counter`, o la sangría no coincide |
| El contador vuelve siempre a `1` | Llamas a `make_counter()()` cada vez: guarda el contador en una variable y llámala a ella |
| `TypeError: 'NoneType' object is not subscriptable` en `__closure__` | La función no usa ninguna variable de fuera: no es una closure y `__closure__` es `None` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · functools](../../1-teoria/05-functools.md) | **Ejercicio 01 · Funciones y closures** | [Ejercicio 02 · Decoradores](../ejercicio-02-decoradores/README.md) |
