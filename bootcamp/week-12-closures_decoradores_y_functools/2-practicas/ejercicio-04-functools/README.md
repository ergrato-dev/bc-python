# Ejercicio 04 — functools

⏱️ 1 h · Teoría previa: [05](../../1-teoria/05-functools.md)

## Objetivo

Fijar argumentos con `partial`, medir lo que ahorra `cache`, ver cómo `lru_cache` descarta resultados y por qué una lista no sirve de argumento, plegar una lista con `reduce` y elegir la función por el tipo con `singledispatch`. Es lo que hace `describe` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `functools_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-12-closures_decoradores_y_functools/2-practicas/ejercicio-04-functools/starter
uv run python functools_lab.py
```

```
Ejercicio 04 · functools
```

Los pasos no dependen unos de otros, pero descomenta en orden. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. `partial` fija argumentos

Descomenta el **PASO 1** y ejecuta:

```
10 °C en F: 50.0 · 55,1 µg/m³ en ppb: 28.0
Qué guarda: convert () {'factor': 0.509}
int con base fija: 10
```

`partial(convert, factor=9 / 5, offset=32)` crea una función de un solo argumento: llama a `convert` con lo que le pases y los argumentos fijados. Es una closure sin escribir la fábrica, y te deja ver qué guarda: la función (`func`), los posicionales (`args`, aquí ninguno) y los nombrados (`keywords`). También vale para funciones que no son tuyas: `partial(int, base=2)` lee binario.

### 2. `cache` recuerda resultados

Descomenta el **PASO 2** y ejecuta:

```
Sin caché: 121393 con 242,785 llamadas
Con caché: 121393 · CacheInfo(hits=23, misses=26, maxsize=None, currsize=26)
Otra vez: 121393 · CacheInfo(hits=24, misses=26, maxsize=None, currsize=26)
```

`ways(25)` se llama a sí misma dos veces en cada paso y repite los mismos cálculos miles de veces: 242.785 llamadas. Con `@cache`, cada `steps` se calcula **una vez** (26 *misses*, de 0 a 25) y las demás veces se lee de la caché (*hits*). La segunda llamada a `ways_cached(25)` no calcula nada: un *hit* más. El `global calls` de `ways` es solo para contar; en tu código, evítalo (teoría 02).

### 3. `lru_cache` con tope y argumentos que no valen

Descomenta el **PASO 3** y ejecuta:

```
    calculo el nivel de 55.1
    calculo el nivel de 12.5
    calculo el nivel de 8.0
CacheInfo(hits=2, misses=3, maxsize=2, currsize=2)
Con una tupla: 3.5
Con una lista: unhashable type: 'list'
```

Con `maxsize=2`, la caché guarda los dos valores usados más recientemente. Sigue la lista `[55.1, 12.5, 55.1, 8.0, 55.1]`:

1. `55.1` y `12.5`: no están, se calculan.
2. `55.1`: *hit*.
3. `8.0`: no está; la caché está llena y descarta el usado hace más tiempo, `12.5`.
4. `55.1`: *hit*, porque se usó en el punto 2.

La caché es un diccionario, y sus claves son los argumentos: deben ser *hashables*. Una tupla vale; una lista lanza `TypeError`.

### 4. `reduce` pliega una secuencia

Descomenta el **PASO 4** y ejecuta:

```
Suma con reduce: 124.5
La más larga: Oriente
```

`reduce(func, values, 0.0)` combina de dos en dos: `func(func(func(func(0.0, 12.5), 8.0), 55.1), 48.9)`. Para sumar, `sum(values)` hace lo mismo y se lee mejor. `reduce` tiene sentido cuando no hay una función hecha, como quedarte con la etiqueta más larga (con un empate, la primera). Aun así, `max(labels, key=len)` también lo hace: casi siempre hay una alternativa más clara.

### 5. `singledispatch` elige por el tipo

Descomenta el **PASO 5** y ejecuta:

```
un valor: 12.5
una etiqueta: 'Norte'
una lista de 2: un valor: 8.0, una etiqueta: 'Sur'
TypeError: describe no acepta int
TypeError: describe no acepta NoneType
```

`@functools.singledispatch` convierte `describe` en la versión **por defecto**, y cada `@describe.register` añade una versión para el tipo de la anotación de su primer parámetro. La de `list` llama a `describe` con cada elemento: cada uno va a su versión.

Las dos últimas líneas son la trampa. `3` es un `int`, y aunque a mypy le vale un `int` donde pides `float`, a `singledispatch` no: `int` no es subclase de `float`, así que va a la versión por defecto. Para aceptarlo, registra `int | float`. `None` tampoco tiene versión: el `TypeError` de la versión por defecto lo dice.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: convert() got multiple values for argument 'factor'` | Llamaste a `to_ppb(55.1, 1.0)`: el segundo posicional cae en `factor`, que ya está fijado. Para cambiarlo, por nombre: `to_ppb(55.1, factor=1.0)` |
| El paso 2 tarda mucho | Subiste el `25`: sin caché, las llamadas casi se duplican con cada escalón más |
| `CacheInfo(hits=0, ...)` | Llamas a `ways` en lugar de `ways_cached` |
| ``TypeError: Invalid first argument to `register()` `` | Una implementación de `describe` no tiene anotación en el primer parámetro |
| `describe(12.5)` lanza `TypeError` | Falta el `@describe.register` encima de la versión de `float` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Decoradores con argumentos](../ejercicio-03-decoradores-con-argumentos/README.md) | **Ejercicio 04 · functools** | [Proyecto](../../3-proyecto/README.md) |
