# Ejercicio 02 — `while`, `break` y `continue`

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-while-break-continue.md)

## Objetivo

Repetir mientras se cumpla una condición, saltar vueltas con `continue`, cortar el bucle con `break`, usar el `else` de los bucles y leer datos hasta un centinela. Ejercicio **guiado**: descomentas cada paso de `while_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-03-bucles_iteracion_y_depuracion/2-practicas/ejercicio-02-while-break-y-continue/starter
uv run python while_lab.py
```

```
Ejercicio 02 · while, break y continue
```

## Pasos

### 1. Una cuenta atrás

Descomenta el **PASO 1** y ejecuta:

```
  quedan 3
  quedan 2
  quedan 1
  ¡ya! seconds vale 0
```

La condición `seconds > 0` se mira antes de cada vuelta; con `seconds` en `0` es falsa y el bucle termina. Ahora **comenta** la línea `seconds -= 1` y ejecuta: `quedan 3` se repite sin fin, porque nada cambia la condición. Corta el programa con `Ctrl+C` (verás `KeyboardInterrupt`) y vuelve a descomentar la línea.

### 2. Sin saber cuántas vueltas

Descomenta el **PASO 2**:

```
Pasos de Collatz para 6: 8 y para 27: 111
```

Con un `for` tendrías que saber de antemano cuántas vueltas dar. Aquí no se sabe: el bucle sigue `while n != 1`. Comprueba a mano los 8 pasos de 6: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1.

### 3. `continue`

Descomenta el **PASO 3**:

```
Promedio sin los None: 20.0
Promedio de [None]: None
```

Cuando `value is None`, `continue` salta el resto del cuerpo y pasa al siguiente valor: ni se suma ni se cuenta. Si todos faltan, `count` queda en `0` y la expresión condicional evita dividir entre cero.

### 4. `break`

Descomenta el **PASO 4**:

```
    miro la posición 0: 12.5
    miro la posición 1: 55.1
Primera por encima de 50: 1
```

En cuanto `55.1 > 50.0`, `break` termina el bucle: las posiciones 2 y 3 ni se miran. Cambia el límite a `100.0`: recorre las cuatro y devuelve `None`.

### 5. El `else` de un bucle

Descomenta el **PASO 5**:

```
Primos hasta 30: 2 3 5 7 11 13 17 19 23 29 
```

En `is_prime`, si algún divisor divide a `n`, `break` sale y el `else` **no** se ejecuta: llega a `return False`. Si el `for` termina sin `break`, se ejecuta el `else`: `return True`. Léelo como "si no hubo `break`".

### 6. Centinela con `while True`

Descomenta el **PASO 6** y ejecuta. Ahora el programa espera: escribe `4`, Enter, `6.5`, Enter, `fin`, Enter.

```
número (o fin): 4
número (o fin): 6.5
número (o fin): fin

Leídos: 2 | suma: 10.5
```

`while True` no termina por la condición: la única salida es el `break` cuando llega `"fin"`. Los números también pueden llegar por una tubería:

```bash
printf "4\n6.5\nfin\n" | uv run python while_lab.py
```

Prueba con `6,5`: `float` no acepta la coma y sale `ValueError`. En el proyecto ya lo resuelve tu `parse_value`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| El programa no termina y repite lo mismo | Bucle infinito: `Ctrl+C`, y comprueba que el cuerpo cambia la variable de la condición |
| El programa se queda esperando sin mostrar nada más | Es el `input` del paso 6: escribe un número o `fin` |
| `EOFError: EOF when reading a line` | La entrada se acabó sin `fin` (por ejemplo, `printf "4\n"`): añade `fin` al final |
| `ValueError: could not convert string to float: '6,5'` | `float` usa punto decimal |
| `SyntaxError: 'break' outside loop` | El `break` quedó sin sangría, fuera del `while` |
| `is_prime` dice que 9 es primo | El `else` quedó con la sangría del `if` y no la del `for` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · `for` y `range`](../ejercicio-01-for-y-range/README.md) | **Ejercicio 02 · `while`, `break` y `continue`** | [Ejercicio 03 · Depuración](../ejercicio-03-depuracion/README.md) |
