# Ejercicio 04 — Generadores

⏱️ 1 h · Teoría previa: [04](../../1-teoria/04-generadores.md) y [05](../../1-teoria/05-pipelines-perezosos.md)

## Objetivo

Ver cómo `yield` pausa una función, medir cuánta memoria ahorra un generador frente a una lista, recorrer un generador que no termina nunca con `islice`, montar una tubería de generadores que lee un valor cada vez y usar `yield from`. Es lo que hacen `iter_lines`, `iter_measurements` y `running_mean` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `generator_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-11-data_model_dunders_iteradores_y_generadores/2-practicas/ejercicio-04-generadores/starter
uv run python generator_lab.py
```

```
Ejercicio 04 · Generadores
```

Los pasos no dependen unos de otros, pero descomenta en orden. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. `yield` pausa la función

Descomenta el **PASO 1** y ejecuta:

```
Llamar no ejecuta nada: generator
    empieza
    antes de dar 2
next: 2
    antes de dar 1
next: 1
    termina
next con valor por defecto: fin
    empieza
    antes de dar 3
    antes de dar 2
    antes de dar 1
    termina
Con un for: [3, 2, 1]
```

Sigue los mensajes con el código delante:

- `countdown(2)` **no** imprime `empieza`: una función con `yield` devuelve un objeto `generator` sin ejecutar ni una línea.
- El primer `next` ejecuta desde el principio hasta el primer `yield`, da `2` y se **pausa** ahí, con `start` intacto.
- El segundo `next` sigue justo después del `yield`: resta `1`, vuelve al `while` y da `1`.
- El tercero sale del `while`, imprime `termina` y, al acabar la función, el generador lanza `StopIteration` (aquí recogido por el valor por defecto).

Es un iterador como la `Countdown` del ejercicio 03, sin escribir `__iter__`, `__next__` ni guardar el estado en `self`.

### 2. Memoria: lista frente a generador

Descomenta el **PASO 2** y ejecuta:

```
Lista: 8,448,728 bytes · generador: 208 bytes
Misma suma: True
¿Y si sumo otra vez el generador? 0
```

La lista guarda el millón de cuadrados a la vez: unos 8 MB solo para las referencias (sin contar los números). La **expresión generadora**, entre paréntesis en lugar de corchetes, ocupa lo mismo con un millón que con diez: calcula cada cuadrado cuando `sum` se lo pide. Las dos dan la misma suma, pero el generador se ha **gastado**: la segunda suma no recorre nada y da `0`. Tus cifras pueden variar un poco con otra versión de Python.

### 3. Generadores infinitos e `islice`

Descomenta el **PASO 3** y ejecuta:

```
Las 4 primeras: [10.0, 12.5, 15.0, 17.5]
Hasta pasar de 20: [10.0, 12.5, 15.0, 17.5, 20.0]
En lotes de 2: [(1.0, 2.0), (3.0, 4.0), (5.0,)]
```

`readings_forever` tiene un `while True` y no termina nunca. No pasa nada mientras nadie le pida todos los valores: `islice(gen, 4)` pide cuatro y para, `takewhile` para en el primero que no cumple la condición, y `batched` agrupa lo que le llega. **Nunca** hagas `list(readings_forever(...))` sin uno de ellos: se llenaría la memoria. Es el caso de un sensor que manda lecturas sin parar.

### 4. Una tubería de generadores

Descomenta el **PASO 4** y ejecuta:

```
Tubería creada; aún no se ha leído nada
    lee 'Norte;12,5'
Primer valor alto: 12.5
    lee '# nota'
    lee 'Sur;NA'
    lee 'Centro;8'
    lee 'basura'
    lee 'Este;55,1'
El resto: [55.1]
```

`above(parse(read(RAW)), 10.0)` encadena tres generadores y no lee nada al crearse. El primer `next` tira de la cadena: `above` pide un valor a `parse`, que pide una línea a `read`, que la lee. `Norte;12,5` atraviesa las tres etapas y sale antes de que se lea la segunda línea. Las demás se leen después, solo cuando `list` pide el resto. `above` usa una expresión generadora en lugar de `yield`: para un filtro sencillo es lo mismo.

### 5. `yield from` y el retorno de un generador

Descomenta el **PASO 5** y ejecuta:

```
yield from: [12.5, 48.9, 8.0]
1: Norte;12,5 · 2: Sur;8
StopIteration con valor: sin más líneas
```

`yield from values` da, uno a uno, todos los valores de otro iterable: equivale a `for value in values: yield value`. Un generador también puede hacer `return valor`: no lo recibe un `for`, sino la `StopIteration` final, en `stop.value`. Por eso el tipo de `numbered` es `Generator[str, None, str]` (da `str`, no recibe nada, devuelve `str`) y no `Iterator[str]`, que no admite `return` con valor: mypy daría `No return value expected`. Es un uso raro: lo normal es `Iterator[...]` y un generador que solo da valores.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Se imprime `empieza` al crear el generador | La función no tiene `yield`: sin él es una función normal |
| `TypeError: 'generator' object is not subscriptable` | Un generador no admite `gen[0]`: usa `next(gen)` o `islice` |
| `TypeError: object of type 'generator' has no len()` | Un generador no sabe cuántos valores dará: conviértelo en lista si necesitas `len` |
| El programa no termina en el paso 3 | Hiciste `list(...)` sobre `readings_forever` sin `islice` ni `takewhile`: corta con `Ctrl+C` |
| En el paso 4 se leen todas las líneas antes del primer valor | Alguna etapa usa corchetes (`[...]`, una lista) en lugar de paréntesis o `yield` |
| `AttributeError: module 'itertools' has no attribute 'batched'` | Ejecutaste con otro Python (`batched` llegó en 3.12): usa `uv run python`, que toma el 3.14 del ejercicio |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Iteradores](../ejercicio-03-iteradores/README.md) | **Ejercicio 04 · Generadores** | [Proyecto](../../3-proyecto/README.md) |
