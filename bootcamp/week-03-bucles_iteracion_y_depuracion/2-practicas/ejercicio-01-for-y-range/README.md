# Ejercicio 01 — `for` y `range`

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-for-e-iterables.md) y [03](../../1-teoria/03-patrones-de-bucle.md)

## Objetivo

Recorrer textos, rangos y listas con `for`, y escribir a mano los patrones que usarás toda la semana: contador, acumulador, numerar con `enumerate`, emparejar con `zip`, bucles anidados y máximo. Ejercicio **guiado**: descomentas cada paso de `loops_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-03-bucles_iteracion_y_depuracion/2-practicas/ejercicio-01-for-y-range/starter
uv run python loops_lab.py
```

```
Ejercicio 01 · for y range
```

Cada paso que descomentes añade sus líneas debajo. Para descomentar en VS Code: selecciona las líneas y `Ctrl+K Ctrl+U`.

## Pasos

### 1. `for` recorre un texto

Descomenta el **PASO 1** y ejecuta. Líneas nuevas:

```
Vocales en 'Murciélago': 5
  vuelta con 'a'
  vuelta con 'b'
  vuelta con 'c'
```

`count_vowels` empieza con `count = 0` **antes** del bucle y suma 1 en cada vocal. El segundo `for` muestra que el cuerpo se ejecuta una vez por carácter, con `letter` cambiando en cada vuelta. Cambia `"abc"` por `""` y ejecuta: el cuerpo no se ejecuta ninguna vez.

### 2. `range`

Descomenta el **PASO 2**:

```
range(5): [0, 1, 2, 3, 4]
range(1, 6): [1, 2, 3, 4, 5]
range(10, 0, -3): [10, 7, 4, 1]
range(5, 5): []
```

El final **nunca** se incluye: `range(5)` da cinco números, del 0 al 4. Para contar del 1 al 5, `range(1, 6)`. `list(...)` solo sirve para verlos; en un `for` no hace falta.

### 3. Acumuladores

Descomenta el **PASO 3**:

```
1 + 2 + ... + 100 = 5050
5! = 120 y 0! = 1
```

La suma arranca en `0` y el producto en `1`: si `product` empezara en `0`, todo daría `0`. `factorial(0)` da `1` porque `range(2, 1)` está vacío y el bucle no da ninguna vuelta.

Prueba el error típico: mueve `total = 0` **dentro** del `for` (una sangría más) y ejecuta. `sum_up_to(100)` da `100`: el acumulador se reinicia en cada vuelta. Devuélvelo a su sitio.

### 4. `enumerate` y `zip`

Descomenta el **PASO 4**:

```
  1. Norte
  2. Sur
  3. Centro
  Norte     12.5
  Sur        8.0
  Centro    55.1
```

`enumerate(stations, start=1)` da parejas `(número, estación)` y el `for` las desempaqueta en dos nombres. `zip` avanza por las dos listas a la vez. Quita `55.1` de `readings` y ejecuta: `zip` para en la lista más corta y `Centro` desaparece sin aviso.

### 5. Bucles anidados

Descomenta el **PASO 5**:

```
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
```

El `for` de fuera da 3 vueltas (filas); en **cada una**, el de dentro da 5 (columnas). `line = ""` va dentro del de fuera: cada fila empieza vacía. `f"{...:>4}"` alinea cada número en 4 caracteres (semana 2).

### 6. El máximo a mano

Descomenta el **PASO 6**:

```
Mayor de [12.5, 8.0, 55.1]: 55.1
Mayor de [-3.0, -1.5]: -1.5
Mayor de []: None
```

`best = None` significa "todavía no he visto ningún valor". Cambia `best = None` por `best = 0` y ejecuta: con negativos dice que el mayor es `0`, un valor que ni siquiera está en la lista. Vuelve a `None`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `IndentationError: expected an indented block` | Al descomentar quedó una línea del cuerpo sin sangría: debe tener 4 espacios más que el `for` |
| `IndentationError: unexpected indent` | Quitaste también el espacio después de `#`; con `Ctrl+K Ctrl+U` no pasa |
| La suma da el último número y no el total | El acumulador está dentro del bucle: va antes del `for` |
| `TypeError: 'int' object is not iterable` | Escribiste `for i in 5`: un número no se recorre; usa `range(5)` |
| `range(1, 5)` no llega al 5 | El final no se incluye: `range(1, 6)` |
| `zip` "pierde" un elemento | Las listas tienen distinto largo: `zip` para en la más corta |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Depuración](../../1-teoria/05-depuracion.md) | **Ejercicio 01 · `for` y `range`** | [Ejercicio 02 · `while`, `break` y `continue`](../ejercicio-02-while-break-y-continue/README.md) |
