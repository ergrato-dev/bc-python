# Ejercicio 02 — Decoradores

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-decoradores.md)

## Objetivo

Escribir un decorador a mano, ver que `@` es solo un atajo, descubrir lo que se pierde sin `functools.wraps`, hacer un decorador que vale para cualquier función y apilar dos. Es lo que hace `skip_missing` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `decorator_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-12-closures_decoradores_y_functools/2-practicas/ejercicio-02-decoradores/starter
uv run python decorator_lab.py
```

```
Ejercicio 02 · Decoradores
```

Descomenta en orden: el paso 2 usa `announce`, del paso 1. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. Un decorador escrito a mano

Descomenta el **PASO 1** y ejecuta:

```
Sin decorar: 50.0
    llamo a to_fahrenheit(10.0)
Decorada a mano: 50.0
```

`announce` recibe una función y devuelve **otra**, `wrapper`, que imprime el aviso, llama a la original y devuelve su resultado. `wrapper` recuerda `func`: es una closure (ejercicio 01, paso 4). `announced = announce(to_fahrenheit)` es una función nueva; `to_fahrenheit` sigue intacta.

Observa el orden: `llamo a ...` sale **antes** que `Decorada a mano: 50.0`, porque `print` evalúa primero sus argumentos, y uno de ellos es la llamada a `wrapper`.

### 2. La sintaxis `@` y lo que se pierde

Descomenta el **PASO 2** y ejecuta:

```
    llamo a to_kelvin(10.0)
Con @: 283.15
¿Cómo se llama? wrapper · ¿y su docstring? None
```

`@announce` encima de `def to_kelvin` es exactamente `to_kelvin = announce(to_kelvin)`: el nombre `to_kelvin` ya no apunta a tu función, sino al `wrapper`. Por eso se llama `wrapper` y no tiene *docstring*. Un error dentro mostraría `wrapper` en la traza, y `help(to_kelvin)` no diría nada útil.

### 3. `functools.wraps`

Descomenta el **PASO 3** y ejecuta:

```
Con wraps: to_rankine · Grados Celsius a Rankine.
La original sigue dentro: 491.67
```

`@functools.wraps(func)` encima del `wrapper` copia el nombre, el *docstring* y otros datos de la original, y guarda la original en `__wrapped__`. Así puedes probarla sin el decorador: `to_rankine.__wrapped__(0.0)` no imprime el aviso. El `# type: ignore[attr-defined]` está porque `announce_wrapped` promete devolver un `Callable[[float], float]`, y mypy no sabe que ese `Callable` tiene `__wrapped__`.

**Regla**: todo `wrapper` lleva `@functools.wraps(func)`.

### 4. Un decorador para cualquier función

Descomenta el **PASO 4** y ejecuta:

```
    mean: llamada 1
Media: 15.0
    mean: llamada 2
Media: 2.0
    label_of: llamada 1
Etiqueta: NORTE
```

`announce` solo valía para funciones de un `float`. `counted` decora `mean` (una lista) y `label_of` (un texto y un argumento con nombre) porque su `wrapper` recibe `*args` y `**kwargs` y se los pasa enteros a la original.

Cada función decorada lleva **su** contador: `calls` vive en la closure de cada llamada a `counted`, y `nonlocal` deja sumarle uno. Por eso `label_of` empieza en `1` aunque `mean` vaya por `2`.

La firma de `counted`, con `[**P, R]`, el parámetro `func: Callable[P, R]` y el retorno `Callable[P, R]`, dice a mypy que la función decorada tiene los **mismos** parámetros y el mismo retorno que la original. Compruébalo: añade `mean("10")` justo debajo de la línea de `Etiqueta:` y ejecuta `uvx --from mypy==2.4.1 mypy decorator_lab.py`:

```
decorator_lab.py:98: error: Argument 1 to "mean" has incompatible type "str"; expected "list[float]"  [arg-type]
```

Tu número de línea puede ser otro. Bórrala.

### 5. Apilar decoradores

Descomenta el **PASO 5** y ejecuta:

```
bold encima de italic: <b><i>Observatorio</i></b>
italic encima de bold: <i><b>capa 11</b></i>
```

Los decoradores se aplican **de abajo arriba**: `title = bold(italic(title))`. `italic` envuelve primero, `bold` queda por fuera. Al cambiar el orden en `subtitle`, cambia el resultado. Con decoradores que hacen cosas distintas (saltar los `None`, redondear), el orden decide si funciona o no.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: 'NoneType' object is not callable` | Al decorador le falta `return wrapper` |
| La función decorada devuelve `None` | El `wrapper` llama a `func(...)` sin `return` |
| En el paso 3 sigue saliendo `wrapper` | `@functools.wraps(func)` debe ir encima de `def wrapper`, dentro del decorador |
| `TypeError: counted.<locals>.wrapper() got an unexpected keyword argument 'upper'` | El `wrapper` no tiene `**kwargs` |
| `UnboundLocalError: cannot access local variable 'calls' ...` | Falta `nonlocal calls` dentro del `wrapper` |
| `SyntaxError` en `[**P, R]` | Ejecutaste con un Python anterior al 3.12: usa `uv run python`, que toma el 3.14 del ejercicio |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Funciones y closures](../ejercicio-01-funciones-y-closures/README.md) | **Ejercicio 02 · Decoradores** | [Ejercicio 03 · Decoradores con argumentos](../ejercicio-03-decoradores-con-argumentos/README.md) |
