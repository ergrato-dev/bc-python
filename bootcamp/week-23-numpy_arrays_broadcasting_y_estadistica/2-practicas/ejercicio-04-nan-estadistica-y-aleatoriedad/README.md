# Ejercicio 04 — NaN, estadística y aleatoriedad

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-datos-que-faltan-estadistica-y-azar.md)

## Objetivo

Todo lo que necesita el comando `estadisticas` de tu proyecto, pieza a pieza:

- generar datos aleatorios que se repiten;
- tratar los datos que faltan con NaN;
- ver los avisos de NumPy y controlarlos;
- resumir una columna: media, mediana, desviación y cuartiles;
- dibujar un histograma en la terminal;
- encontrar atípicos con puntuaciones z, y ver su punto débil.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-23-numpy_arrays_broadcasting_y_estadistica/2-practicas/ejercicio-04-nan-estadistica-y-aleatoriedad/starter
uv run python main.py
```

```
Ejercicio 04 · NaN, estadística y aleatoriedad
```

## Pasos

### 1. Números aleatorios que se repiten

Descomenta el **PASO 1** y ejecuta:

```
normal:   [45.5 42.2 39.4 16.8]
enteros:  [12 65 65 85]
etiquetas: ['Sur' 'Norte' 'Norte' 'Norte']
otra vez, misma semilla: [45.5 42.2 39.4 16.8]
otra semilla:            [53.5 43.4 28.4 38.1]
```

Un generador con semilla 23 da siempre la misma secuencia, en tu máquina y en la de cualquiera: por eso tus números coinciden con estos. Otro generador con la misma semilla repite los mismos; con otra semilla, otros.

Cada llamada **avanza** el generador: `rng.integers` no empieza desde el principio, sigue donde lo dejó `rng.normal`. Si añades una llamada en medio, todo lo que viene detrás cambia.

### 2. NaN, el dato que falta

Descomenta el **PASO 2** y ejecuta:

```
nan == nan: False · isnan: [False  True False False  True]
sum nan · mean nan · max nan
nansum 75.6 · nanmean 25.20 · nanmax 55.1
presentes: [12.5 55.1  8. ] · faltan: 2
ValueError: cannot convert float NaN to integer
```

- NaN no es igual ni a sí mismo: para encontrarlo, `np.isnan`.
- Un NaN contagia cualquier cálculo: la suma, la media y el máximo dan `nan`.
- Las funciones `nan*` lo ignoran. Otra forma: quitarlo con la máscara `~np.isnan(values)` y calcular con los presentes. Es la que usa tu Observatorio.
- Un array de enteros no admite NaN: los datos que faltan obligan a usar `float64`.

### 3. Avisos en lugar de errores

Descomenta el **PASO 3** y ejecuta:

```
main.py:45: RuntimeWarning: Mean of empty slice
  print("media de nada:", np.nanmean(np.array([np.nan, np.nan])))
...
media de nada: nan
dividir por cero, sin avisos: [inf nan]
FloatingPointError: divide by zero encountered in divide
```

El aviso sale por stderr y puede aparecer antes que el resto, con la ruta completa delante de `main.py`. La media de dos NaN es la media de **nada**: NumPy da `nan` y avisa, pero no para el programa.

`np.errstate` cambia qué hace NumPy dentro de un bloque `with`: `"ignore"` calla los avisos (para cuando `inf` o `nan` es justo lo que quieres) y `"raise"` los convierte en una excepción que puedes capturar. Fuera del `with`, todo vuelve a ser como antes.

### 4. El resumen de una columna

Descomenta el **PASO 4** y ejecuta:

```
con valor 961 · sin dato 39
media 39.64 · mediana 39.73
std población 9.951 · std muestra 9.956
Q1 32.72 · Q2 39.73 · Q3 46.58 · rango intercuartílico 13.86
mínimo 1.41 · máximo 72.09
```

1 000 valores de una normal de media 40 y desviación 10, con un 5 % convertido en NaN por una máscara aleatoria (`rng.random(1000) < 0.05`). Las medidas salen cerca de 40 y 10, no exactas: es una muestra.

- La mediana es Q2, el percentil 50: por eso coinciden.
- `ddof=1` divide por `n − 1` en lugar de `n`. Con 961 valores casi no cambia; pandas usa `ddof=1` por defecto y NumPy, `ddof=0`.
- La mitad central de los valores está entre Q1 y Q3: un rango de 13.86.

### 5. Histograma

Descomenta el **PASO 5** y ejecuta:

```
conteos: [  5  54 318 404 166  14] · suman 961
bordes:  [ 1.4 13.2 25.  36.7 48.5 60.3 72.1]
   1.4 –   13.2                                 5
  13.2 –   25.0  ████                           54
  25.0 –   36.7  ████████████████████████       318
  36.7 –   48.5  ██████████████████████████████ 404
  48.5 –   60.3  ████████████                   166
  60.3 –   72.1  █                              14
```

`np.histogram` reparte los valores en 6 intervalos iguales entre el mínimo y el máximo, y cuenta cuántos caen en cada uno. Hay 7 bordes para 6 intervalos. La barra de cada uno mide `conteo / conteo máximo × 30` caracteres: la campana de la normal aparece en la terminal. Es exactamente lo que escribe `estadisticas` en tu proyecto.

Prueba con `bins=20`: más detalle, más ruido.

### 6. Puntuaciones z y atípicos

Descomenta el **PASO 6** y ejecuta:

```
atípicos (|z| > 3): [ 10  59 393 500] [120.    1.4  72.1 -30. ] [ 7.6 -3.6  3.1 -6.6]
fuera de 2 desviaciones: 3.1% (en una normal, alrededor del 4,6 %)
```

Metes dos picos falsos en las posiciones 10 y 500: 120 y −30. La puntuación z de cada valor dice a cuántas desviaciones está de la media; con |z| > 3 salen los dos picos (z de 7.6 y −6.6) y los dos extremos reales de la muestra (1.4 y 72.1).

Pero en una normal, alrededor del 4,6 % de los valores queda a más de 2 desviaciones, y aquí solo un 3,1 %. Los dos picos **inflan** la desviación, de 9.96 a 10.52, y todas las z se encogen: los atípicos esconden a los demás. Sin los picos, la misma cuenta da un 3,6 %. Por eso tu Observatorio te deja elegir el umbral con `--umbral`, y por eso conviene mirar también los cuartiles (teoría 04, sección 6).

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus números aleatorios no coinciden con el README | ¿Semilla 23? ¿Has descomentado los pasos en orden? Cada llamada avanza el generador, y el paso 4 sigue con el `rng` del paso 1 |
| `NameError: name 'rng' is not defined` en el paso 4 | Descomenta también el paso 1 |
| `ValueError: autodetected range of [nan, nan] is not finite` | Pasas a `np.histogram` el array con NaN: usa `present` |
| No ves el `RuntimeWarning` del paso 3 | Se escribe en stderr: si rediriges con `2>/dev/null`, no sale |
| `atípicos` no incluye el −30 ni el 1.4 | Falta `np.abs`: sin él solo encuentras los muy altos, porque los muy bajos tienen z negativa |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Broadcasting y ejes](../ejercicio-03-broadcasting-y-ejes/README.md) | **Ejercicio 04 · NaN, estadística y aleatoriedad** | [Proyecto](../../3-proyecto/README.md) |
