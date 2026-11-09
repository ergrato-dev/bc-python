# 04 · Datos que faltan, estadística y azar

⏱️ 50 min

## 🎯 Objetivos

- Generar números aleatorios **reproducibles** con `np.random.default_rng` y una semilla.
- Representar un dato que falta con NaN, y calcular sin que lo estropee todo.
- Entender por qué NumPy avisa en lugar de fallar, y controlar esos avisos.
- Resumir una columna: media, mediana, desviación, cuartiles e histograma.
- Encontrar valores atípicos con puntuaciones z, y conocer su punto débil.

---

## 1. Azar que se repite

Para probar un análisis necesitas datos de ejemplo, y para comparar dos versiones de un programa, que sean **los mismos** cada vez (semana 22). NumPy genera números aleatorios con un **generador**, que nace de una **semilla**:

```python
rng = np.random.default_rng(23)
rng.normal(40, 10, size=4).round(1)          # [45.5 42.2 39.4 16.8]
rng.integers(0, 100, size=4)                 # [12 65 65 85]
rng.choice(["Norte", "Sur", "Este"], size=4) # ['Sur' 'Norte' 'Norte' 'Norte']
```

Otro generador con la misma semilla da la misma secuencia: `np.random.default_rng(23).normal(40, 10, size=4)` vuelve a dar `[45.5 42.2 39.4 16.8]`. Con otra semilla, otra secuencia.

| Método | Qué da |
|---|---|
| `rng.normal(media, desviación, size)` | Valores con forma de campana alrededor de la media |
| `rng.uniform(bajo, alto, size)` | Valores repartidos por igual en el intervalo |
| `rng.integers(bajo, alto, size)` | Enteros, sin incluir `alto` |
| `rng.choice(opciones, size)` | Elementos de una lista, con repetición |
| `rng.random(size)` | Valores entre 0 y 1: `rng.random(1000) < 0.05` es una máscara con un 5 % de `True` |

En código antiguo verás `np.random.seed(23)` y `np.random.normal(...)`. Es la interfaz vieja: un único generador **global** que cualquier biblioteca puede mover sin que lo sepas. La documentación de NumPy recomienda `default_rng`: cada parte del programa tiene su generador, y su secuencia no depende de lo que hagan las demás.

---

## 2. NaN, el dato que falta

Tu Observatorio tiene medidas sin valor (`"NA"`), que hasta ahora eran `None`. En un array de `float64`, `None` no cabe (teoría 01). Su sitio lo ocupa **NaN** (*not a number*), un valor especial de la coma flotante:

```python
values = np.array([12.5, np.nan, 55.1, 8.0, np.nan])
np.isnan(values)   # [False  True False False  True]
```

NaN tiene tres propiedades que hay que conocer:

1. **No es igual a nada, ni a sí mismo**: `np.nan == np.nan` es `False`. Para buscarlo, `np.isnan`, nunca `==`.
2. **Se contagia**: cualquier operación con un NaN da NaN. `values.sum()`, `values.mean()` y `values.max()` dan `nan`.
3. **Las comparaciones dan `False`**: `np.nan > 50` y `np.nan < 50` son las dos `False`. Un NaN nunca entra en una máscara de "alto" ni de "bajo".

Para calcular sin los NaN tienes dos caminos:

```python
np.nansum(values), np.nanmean(values), np.nanmax(values)   # 75.6 25.2 55.1
present = values[~np.isnan(values)]                        # [12.5 55.1  8. ]
```

Las funciones `nan*` (`nansum`, `nanmean`, `nanstd`, `nanmedian`, `nanpercentile`...) ignoran los NaN. Quitarlos con una máscara te deja un array con solo los presentes, sobre el que funcionan todas las funciones, y además sabes cuántos faltaban: `np.count_nonzero(np.isnan(values))`. Tu Observatorio usa el segundo camino: quita los NaN una vez y calcula todo lo demás sobre `present`.

NaN solo existe en los tipos de coma flotante. Un array de enteros no puede tener datos que faltan: `np.array([1, np.nan], dtype=np.int64)` da `ValueError: cannot convert float NaN to integer`. Por eso, en pandas (semana 24), una columna de enteros con un dato que falta pasa a `float64`.

---

## 3. Avisos en lugar de errores

Dividir por cero en Python lanza `ZeroDivisionError`. En NumPy, no:

```python
np.array([1.0, 0.0]) / 0
# RuntimeWarning: divide by zero encountered in divide
# RuntimeWarning: invalid value encountered in divide
# [inf nan]
```

Con un millón de valores, que uno sea problemático no debería tirar el cálculo de los demás: NumPy pone `inf` o `nan` en esa posición y **avisa** con un `RuntimeWarning` en stderr (semana 14). Lo mismo pasa al promediar nada:

```python
np.nanmean(np.array([np.nan, np.nan]))
# RuntimeWarning: Mean of empty slice
# nan
```

Un aviso no para el programa, así que es fácil que un NaN viaje sin que nadie lo vea hasta el informe final. Tres formas de controlarlos:

| Cómo | Para qué |
|---|---|
| Comprobar antes: `if present.size == 0:` | Lo mejor: el caso especial queda escrito y probado |
| `with np.errstate(divide="ignore", invalid="ignore"):` | Sabes que puede pasar y el `inf` o el `nan` es la respuesta que quieres |
| `with np.errstate(divide="raise"):` | Prefieres un `FloatingPointError` que te pare: `divide by zero encountered in divide` |

Tu Observatorio usa la primera: `zscores` comprueba que la desviación no es 0 antes de dividir, y un test convierte los avisos en errores (`warnings.simplefilter("error")`) para demostrar que no avisa (teoría 05).

---

## 4. El resumen de una columna

Con 1 000 valores de una normal de media 40 y desviación 10, y un 5 % de NaN (ejercicio 04):

```python
present = sample[~np.isnan(sample)]                # 961 con valor, 39 sin dato
present.mean(), np.median(present)                 # 39.64 · 39.73
present.std(), present.std(ddof=1)                 # 9.951 · 9.956
q1, q2, q3 = np.percentile(present, [25, 50, 75])  # 32.72 · 39.73 · 46.58
present.min(), present.max()                       # 1.41 · 72.09
```

| Medida | Qué dice | Cuidado con |
|---|---|---|
| Media | El centro, si los valores se reparten por igual | Un solo valor extremo la arrastra |
| Mediana (`np.median`) | El valor del medio: la mitad por debajo | Nada: es robusta frente a extremos |
| Desviación (`std`) | Cuánto se separan de la media, en sus unidades | `ddof` (abajo) |
| Percentil `p` (`np.percentile`) | El valor por debajo del cual queda el `p` % | Interpola entre valores: `[1, 2, 3, 4]` da Q1 = 1.75 |
| Cuartiles Q1, Q2, Q3 | Los percentiles 25, 50 y 75; Q2 es la mediana | Q3 − Q1 es el **rango intercuartílico** |

`ddof` decide si la desviación divide por `n` (`ddof=0`, la **de la población**, la de NumPy por defecto) o por `n − 1` (`ddof=1`, la **de la muestra**, que corrige que estimas a partir de unos pocos valores). Con 961 valores la diferencia es mínima, 9.951 frente a 9.956; con 5, se nota. pandas usa `ddof=1` por defecto y NumPy `ddof=0`: si comparas sus resultados (semana 24), mira este parámetro antes de buscar un error. Tu Observatorio usa la de NumPy, y lo dice en su docstring.

---

## 5. Histograma

Un **histograma** reparte los valores en intervalos iguales y cuenta cuántos caen en cada uno:

```python
counts, edges = np.histogram(present, bins=6)
counts   # [  5  54 318 404 166  14]: suman 961
edges    # [ 1.4 13.2 25.  36.7 48.5 60.3 72.1]: 7 bordes para 6 intervalos
```

`edges` tiene un elemento más que `counts`: el intervalo `i` va de `edges[i]` a `edges[i + 1]`. Todos incluyen su borde izquierdo y el último, también el derecho, para que el máximo cuente. Con una barra proporcional a cada conteo, la forma de campana aparece en la terminal:

```
   1.4 –   13.2                                 5
  13.2 –   25.0  ████                           54
  25.0 –   36.7  ████████████████████████       318
  36.7 –   48.5  ██████████████████████████████ 404
  48.5 –   60.3  ████████████                   166
  60.3 –   72.1  █                              14
```

`np.histogram` no acepta NaN (`ValueError: autodetected range of [nan, nan] is not finite`): quítalos antes. En la semana 27 dibujarás histogramas de verdad con matplotlib; por debajo, calculan esto.

---

## 6. Puntuaciones z y atípicos

La **puntuación z** de un valor dice a cuántas desviaciones está de la media: `(valor − media) / desviación`. Una z de +2 es "dos desviaciones por encima". En una distribución normal, alrededor del 95 % de los valores tiene |z| ≤ 2 y el 99,7 %, |z| ≤ 3: un valor más lejos es **atípico** y merece una mirada (un sensor roto, una errata, o algo que de verdad pasó).

Con NumPy, una máscara y sus posiciones:

```python
z = (spiky - spiky.mean()) / spiky.std()
found = np.flatnonzero(np.abs(z) > 3)
```

En el ejercicio 04 metes dos picos, 120 y −30, en los datos de la sección 4:

```
atípicos (|z| > 3): [ 10  59 393 500] [120.    1.4  72.1 -30. ] [ 7.6 -3.6  3.1 -6.6]
```

Salen los dos picos, y también los dos extremos de verdad de la muestra. Pero mira esto:

```
fuera de 2 desviaciones: 3.1% (en una normal, alrededor del 4,6 %)
```

Los picos **inflan la desviación**: con ellos pasa de 9.96 a 10.52, todas las z se encogen y menos valores parecen lejanos. Es el punto débil de las z: la media y la desviación que usas para medir lo raro se calculan **con** lo raro. Si hubiera muchos picos, podrían esconderse unos a otros.

Una alternativa que no se deja arrastrar usa los cuartiles: es atípico lo que queda por debajo de `Q1 − 1,5 × (Q3 − Q1)` o por encima de `Q3 + 1,5 × (Q3 − Q1)`. Es la regla de los diagramas de caja (semana 27). Con los mismos datos marca 9 valores en lugar de 4: otra regla, otra respuesta. Ninguna es "la verdad"; tu trabajo es elegir una, decir cuál, y mirar lo que encuentra. Tu Observatorio usa z con un umbral que eliges con `--umbral`, y la semana 28 vuelve sobre estas preguntas con estadística de verdad.

---

## 7. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `values == np.nan` | NaN no es igual a nada: siempre `False` | `np.isnan(values)` |
| `values.mean()` con NaN dentro | Da `nan`: el NaN se contagia | `np.nanmean` o quitar los NaN con una máscara |
| `np.random.seed(...)` y funciones globales | Un generador compartido que otras bibliotecas pueden mover | `rng = np.random.default_rng(semilla)` |
| Sin semilla en un análisis que comparas | Cada ejecución da otros datos | Semilla fija, y dila |
| Ignorar un `RuntimeWarning` | Un `nan` o un `inf` viaja hasta el resultado | Comprueba el caso antes, o `np.errstate` a propósito |
| Comparar `std` de NumPy y de pandas | `ddof=0` frente a `ddof=1` | Pasa `ddof` explícito |
| `np.histogram` con NaN | `ValueError: autodetected range ... is not finite` | Quítalos antes |
| Creer que |z| > 3 encuentra todos los atípicos | Los extremos inflan la desviación | Mira también los cuartiles, y los datos |

---

## ✅ Qué debes saber al terminar

- [ ] Generar datos reproducibles con `default_rng` y una semilla, y por qué no `np.random.seed`.
- [ ] Las tres propiedades de NaN, y los dos caminos para calcular sin ellos.
- [ ] Por qué NumPy avisa en lugar de fallar, y cómo controlarlo.
- [ ] Media, mediana, desviación con su `ddof`, percentiles e histograma.
- [ ] Encontrar atípicos con z, y por qué los propios atípicos los esconden.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Operaciones, ejes y broadcasting](03-operaciones-ejes-y-broadcasting.md) | **04 · Datos que faltan, estadística y azar** | [05 · NumPy en un proyecto](05-numpy-en-un-proyecto.md) |
