# Ejercicio 02 — Scope y funciones como valores

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-scope-y-efectos.md) y [03](../../1-teoria/03-funciones-como-valores.md)

## Objetivo

Comprobar dónde vive cada variable, provocar los dos errores clásicos de scope (`UnboundLocalError` y el valor por defecto mutable), pasar funciones a otras funciones, ordenar con `key=` y `lambda`, y escribir dos funciones recursivas. Ejercicio **guiado**: descomentas cada paso de `scope_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-04-funciones_scope_type_hints_y_pytest/2-practicas/ejercicio-02-scope-y-funciones-como-valores/starter
uv run python scope_lab.py
```

## Pasos

### 1. Local y global

Descomenta el **PASO 1**:

```
Total: 4.0 µg/m³
¿Existe total fuera? False
```

`total` nace al llamar a `label_total` y desaparece al terminar. `UNIT`, definida fuera de toda función, se puede **leer** desde dentro. `globals()` es el conjunto de nombres globales; `total` no está.

### 2. `UnboundLocalError`

Descomenta el **PASO 2** y ejecuta:

```
Traceback (most recent call last):
  ...
    visits += 1
    ^^^^^^
UnboundLocalError: cannot access local variable 'visits' where it is not associated with a value
```

`visits += 1` **asigna**, y al asignar dentro de una función Python decide que `visits` es local en toda ella. Para sumarle 1 primero tiene que leer esa variable local, que aún no tiene valor. La solución recomendada no es `global visits`, sino que la función reciba el valor y devuelva el nuevo: `def add_visit(visits: int) -> int: return visits + 1`.

Vuelve a **comentar** la línea `add_visit()` para seguir.

### 3. El valor por defecto mutable

Descomenta el **PASO 3**:

```
Con []:   [1.0, 2.0] [1.0, 2.0]
Con None: [1.0] [2.0]
```

Esperabas `[1.0] [2.0]` en las dos. La lista `[]` del valor por defecto se creó **una vez**, al definir la función, y todas las llamadas añaden a la misma. Las dos llamadas devolvieron esa misma lista, por eso se ve igual dos veces. La versión segura usa `None` y crea una lista nueva dentro, en cada llamada.

### 4. Funciones como valores

Descomenta el **PASO 4**:

```
upper:   NORTE SUR CENTRO 
initial: n s c 
shout:   HOLA
```

`apply(str.upper, words)` pasa la función **sin paréntesis**: no la llama, la entrega para que `apply` la llame con cada palabra. `shout = str.upper` le da otro nombre a la misma función. Prueba `apply(str.upper(), words)`: `TypeError`, porque `str.upper()` intenta llamarla sin texto.

### 5. `key=` y `lambda`

Descomenta el **PASO 5**:

```
Orden alfabético: ['Norte', 'Occidente', 'Sur']
Por longitud:     ['Sur', 'Norte', 'Occidente']
La más larga:     Occidente
Como texto:  ['12,5', '55,1', '8']
Como número: ['8', '12,5', '55,1']
```

Ordenados como texto, `"8"` va al final porque `"8" > "5"` carácter a carácter. `key` recibe una función que convierte cada elemento en lo que se compara; la `lambda` es una función de una línea, sin nombre, escrita justo donde se usa. Los elementos no cambian: siguen siendo textos.

### 6. Recursión

Descomenta el **PASO 6**:

```
5! = 120 | suma de dígitos de 2026: 10
```

`factorial(5)` llama a `factorial(4)`, que llama a `factorial(3)`… hasta `factorial(1)`, el **caso base**, que devuelve `1` sin llamar a nadie. Entonces las llamadas pendientes terminan en orden inverso: `2 * 1`, `3 * 2`, `4 * 6`, `5 * 24`. Prueba `print(factorial(5000))`:

```
RecursionError: maximum recursion depth exceeded
```

Python limita a unas 1 000 llamadas anidadas. Para muchas repeticiones, un bucle es mejor.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| El programa se detiene en el paso 2 y no ves los siguientes | Vuelve a comentar la línea `add_visit()` |
| `TypeError: 'str' object is not callable` | Pasaste el resultado de una llamada (`initial("x")`) en lugar de la función (`initial`) |
| `RecursionError` sin haberlo buscado | A tu función recursiva le falta el caso base o no se acerca a él |
| `NameError: name 'UNIT' is not defined` | Descomentaste la función sin la línea `UNIT = ...` |
| `sorted` "no ordena" | `sorted` devuelve una lista nueva: imprímela o guárdala; la original no cambia |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Definir funciones](../ejercicio-01-definir-funciones/README.md) | **Ejercicio 02 · Scope y funciones como valores** | [Ejercicio 03 · Type hints](../ejercicio-03-type-hints/README.md) |
