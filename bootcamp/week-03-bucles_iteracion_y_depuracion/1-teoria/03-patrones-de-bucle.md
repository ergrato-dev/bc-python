# 03 · Patrones de bucle

⏱️ 50 min

## 🎯 Objetivos

- Reconocer los seis patrones que resuelven casi todos los bucles: contador, acumulador, máximo, búsqueda, filtro y racha.
- Elegir bien el valor inicial de cada variable y dónde se crea.
- Seguir un bucle a mano con una tabla de traza antes de ejecutarlo.

---

## 1. La estructura común

Casi todos los bucles que procesan datos tienen tres partes:

```python
count = 0                    # 1. antes: preparas las variables
for value in values:         # 2. durante: cada vuelta las actualiza
    if value >= limit:
        count += 1
print(count)                 # 3. después: usas el resultado
```

El error más común de toda la semana es poner la parte 1 **dentro** del bucle: la variable se reinicia en cada vuelta y al final solo refleja la última. Si un resultado te sale "como si solo contara el último", busca eso primero.

## 2. Contador

Cuántos elementos cumplen algo. Empieza en `0` y suma `1`:

```python
high = 0
for value in [60.0, 20.0, 70.0, 80.0]:
    if value >= 50:
        high += 1
# high == 3
```

Para contar varias categorías a la vez, un contador por categoría con `if`/`elif` (en la semana 5 lo harás con un diccionario, y en la fase 4 pandas lo hará en una línea):

```python
low = medium = high = 0
for level in ["bajo", "alto", "medio", "alto"]:
    if level == "bajo":
        low += 1
    elif level == "medio":
        medium += 1
    elif level == "alto":
        high += 1
```

`low = medium = high = 0` crea los tres nombres con el mismo valor; como los `int` son inmutables, cambiar uno no cambia los otros.

## 3. Acumulador

Combinar todos los elementos en un resultado. Empieza en el **elemento neutro** de la operación:

| Operación | Empieza en | Por qué |
|---|---|---|
| Suma | `0` | `0 + x == x` |
| Producto | `1` | `1 * x == x`; con `0` todo daría `0` |
| Texto | `""` | `"" + s == s` |
| Lista | `[]` | Vacía, y vas añadiendo con `append` |

```python
total = 0.0
count = 0
for value in [12.5, 8.0, 55.1]:
    total += value
    count += 1
average = total / count if count > 0 else None
```

Comprueba siempre el caso vacío: sin elementos, `count` queda en `0` y dividir lanza `ZeroDivisionError`.

## 4. Máximo y mínimo

Guarda el mejor visto hasta ahora. Empieza en `None` ("aún no he visto ninguno"), no en `0`:

```python
best = None
for value in [-3.0, -1.5, -7.2]:
    if best is None or value > best:
        best = value
# best == -1.5
```

Con `best = 0` el resultado sería `0`, un valor que no está en los datos. Python ya trae `max()` y `min()`, que usarás cuando solo quieras el valor; el patrón a mano sirve cuando además necesitas **otra cosa** del ganador, como su etiqueta.

## 5. Búsqueda

¿Hay alguno que cumpla algo? ¿Cuál es el primero? Para en cuanto lo encuentras:

```python
found = None
for station, value in zip(stations, readings):
    if value > 50:
        found = station
        break
```

Dentro de una función, `return` en cuanto lo encuentras y `return None` al final (teoría 02).

## 6. Filtro

Quedarte con los que cumplen algo, en otra lista:

```python
rows = []
for line in lines:
    if line.startswith("#"):
        continue
    rows.append(line)
```

## 7. Racha

La mayor cantidad de elementos **seguidos** que cumplen algo: cuántos días seguidos en nivel alto. Dos variables: la racha actual y la mejor.

```python
best = 0
current = 0
for level in ["alto", "alto", "medio", "alto"]:
    if level == "alto":
        current += 1
        best = max(best, current)
    else:
        current = 0
# best == 2
```

`best` se actualiza **en cada vuelta que la racha crece**, no cuando se corta: si la racha más larga es la última, nunca se corta y se perdería.

## 8. La tabla de traza

Antes de ejecutar un bucle, síguelo a mano: una fila por vuelta, una columna por variable. Para la racha de arriba:

| Vuelta | `level` | `current` | `best` |
|---|---|---|---|
| antes | — | 0 | 0 |
| 1 | `"alto"` | 1 | 1 |
| 2 | `"alto"` | 2 | 2 |
| 3 | `"medio"` | 0 | 2 |
| 4 | `"alto"` | 1 | 2 |

Si tu tabla y el programa no coinciden, uno de los dos está mal, y la tabla te dice en qué vuelta. Es lo mismo que hace un depurador (teoría 05), pero en papel. En los tests del proyecto, el resultado esperado sale de una tabla así.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| El total es solo el último valor | El acumulador se crea dentro del bucle | Créalo antes del `for` |
| El producto siempre da 0 | El acumulador del producto empieza en `0` | Empieza en `1` |
| El máximo de valores negativos es `0` | `best` empieza en `0` | Empieza en `None` |
| `ZeroDivisionError` en el promedio | No había elementos | `total / count if count > 0 else None` |
| La racha más larga sale corta | Solo actualizas `best` cuando la racha se corta | Actualízala cada vez que crece |

## ✅ Qué debes saber al terminar

- [ ] Las tres partes de un bucle y qué va antes, durante y después.
- [ ] El valor inicial correcto para un contador, una suma, un producto, un texto y un máximo.
- [ ] Cómo buscar el primero que cumple algo sin recorrer el resto.
- [ ] Cómo calcular una racha con dos variables.
- [ ] Cómo escribir una tabla de traza para comprobar un bucle antes de ejecutarlo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · `while`, `break`, `continue` y `else`](02-while-break-continue.md) | **03 · Patrones de bucle** | [04 · Leer muchas líneas](04-leer-muchas-lineas.md) |
