# Ejercicio 01 — Distribuciones con scipy.stats

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-variables-aleatorias-y-distribuciones.md)

## Objetivo

Hacerle preguntas a un modelo de probabilidad y ver cómo se comportan las muestras que salen de él:

- una distribución normal y sus métodos `cdf`, `sf`, `ppf` y `pdf`;
- muestras al azar reproducibles, y la ley de los grandes números;
- conteos con la binomial y la Poisson;
- el teorema central del límite con una distribución muy asimétrica;
- ajustar un modelo a unos datos, y lo que eso hace con las colas.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-28-estadistica_aplicada_con_scipy_y_statsmodels/2-practicas/ejercicio-01-distribuciones-con-scipy/starter
uv run python main.py
```

```
Ejercicio 01 · Distribuciones con scipy.stats
```

La primera vez, `uv` instala NumPy y SciPy en un entorno solo para este ejercicio. El modelo de partida es la temperatura a mediodía de la estación Norte: una normal de media 20 °C y desviación 3 °C. `rng` es un generador con semilla: los valores al azar salen iguales en tu máquina que aquí.

## Pasos

### 1. Una distribución y sus cuatro preguntas

Descomenta el **PASO 1** y ejecuta:

```
media: 20.0 · desviación: 3.0
densidad en 20 °C: 0.133 · en 26 °C: 0.018
P(T <= 23): 0.8413
P(T > 26):  0.0228
el 95 % de los días, por debajo de: 24.93
intervalo con el 95 % central: [14.12, 25.88]
¿cdf y ppf se deshacen? True
```

- `stats.norm(loc=20, scale=3)` crea la distribución con sus parámetros fijados: `loc` es la media y `scale` la desviación (no la varianza).
- `cdf(23)`: el 84 % de los días, como mucho 23 °C. `sf(26)`: un 2,3 % de los días pasan de 26 °C, unos ocho al año.
- `ppf(0.95)` hace lo contrario que `cdf`: dada una probabilidad, el valor. Por eso `ppf(cdf(23))` vuelve a dar 23.
- `pdf(20)` es la altura de la curva, no una probabilidad: la probabilidad de un valor exacto es 0. Compara 0,133 en 20 °C con 0,018 en 26 °C: los valores cerca de la media son unas siete veces más densos.
- `interval(0.95)` es la media ± 1,96 desviaciones. Lo usarás mucho: entre esos dos valores cae el 95 % de los días.

### 2. Muestras al azar y la ley de los grandes números

Descomenta el **PASO 2** y ejecuta:

```
30 días: [16.4 20.4 19.3 18.4 20.9] ...
media de la muestra: 20.29 · desviación (ddof=1): 3.18
n =        10: media 19.530 · error 0.470
n =       100: media 19.820 · error 0.180
n =    10_000: media 20.030 · error 0.030
n = 1_000_000: media 19.999 · error 0.001
```

- `rvs` saca valores al azar del modelo. Con `random_state=rng`, cada llamada sigue la secuencia del mismo generador: vuelve a ejecutar y salen los mismos números.
- Una muestra de 30 días no da exactamente 20 y 3: da 20,29 y 3,18. Es lo normal. La teoría 02 dice cuánto puede alejarse.
- Con más datos, la media se acerca a 20 (ley de los grandes números). Pero despacio: cien mil veces más datos no dan cien mil veces menos error.

### 3. Contar sucesos: binomial y Poisson

Descomenta el **PASO 3** y ejecuta:

```
binomial · media: 2.0 · P(0 fallos): 0.1216
P(5 o más fallos): 0.0432
Poisson · P(0 alertas): 0.0498 · P(más de 6): 0.0335
alertas por hora en 8 horas: [3 2 1 5 2 2 1 3]
¿la densidad de un discreto? False · ¿y su pmf? True
```

- **Binomial**: 20 lecturas, cada una falla con probabilidad 0,1. De media fallan 2, pero solo un lote de cada ocho sale sin ningún fallo.
- `sf(4)` es P(X > 4), es decir, 5 o más: un 4 % de los lotes. Si un lote da 5 fallos, puede ser mala suerte; si lo dan tres lotes seguidos, mira el sensor.
- **Poisson**: sucesos que llegan cada uno por su lado, con una media por intervalo. Con 3 alertas por hora de media, una hora de cada veinte no llega ninguna.
- Una distribución discreta tiene `pmf` (la probabilidad de cada valor exacto) y no `pdf`. Los demás métodos (`cdf`, `sf`, `ppf`, `rvs`) son los mismos.

### 4. El teorema central del límite

Descomenta el **PASO 4** y ejecuta:

```
esperas · media: 20.1 · asimetría: 1.96
medias de  2: desviación 14.08 (20 / √2 = 14.14) · asimetría 1.39
medias de 10: desviación  6.27 (20 / √10 =  6.32) · asimetría 0.60
medias de 50: desviación  2.82 (20 / √50 =  2.83) · asimetría 0.28
```

- La espera entre alertas es **exponencial**: muchas esperas cortas y unas pocas muy largas. Su asimetría (`stats.skew`) es casi 2; la de una normal, 0.
- `rvs(size=(20_000, n))` saca 20 000 muestras de n esperas a la vez, una por fila, y `mean(axis=1)` da la media de cada una.
- Las medias se reparten cada vez más **simétricas** (la asimetría baja a 0,28 con 50) y su desviación es la de los datos entre √n. Eso dice el teorema central del límite, y es lo que hace funcionar los intervalos y las pruebas de los ejercicios 02 y 03.

### 5. Ajustar un modelo a unos datos

Descomenta el **PASO 5** y ejecuta:

```
normal ajustada a los 30 días: 20.29 3.12
n: 30 · mínimo: 13.28 · máximo: 27.02
asimetría: -0.01 · curtosis: -0.32
¿cuántos días de 1000 pasarían de 26 °C? 34
¿y con el modelo de verdad? 23
```

- `stats.norm.fit` busca la normal que mejor explica los 30 días. Su desviación (3,12) divide entre n, no entre n - 1: sale un poco menor que la del paso 2 (3,18).
- `stats.describe` resume la muestra. Una asimetría y una curtosis cerca de 0 son lo que esperas de una normal.
- Con el modelo ajustado, 34 días de cada 1000 pasarían de 26 °C; con el de verdad, 23. Un error pequeño en los parámetros mueve mucho la cola, y la cola es justo lo que importa si avisas de días de calor.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'scipy'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| Tus números al azar no coinciden con los del README | Descomentaste los pasos en otro orden, o volviste a crear `rng`: cada paso usa la secuencia donde la dejó el anterior |
| `AttributeError: 'rv_discrete_frozen' object has no attribute 'pdf'` | Las discretas usan `pmf` |
| `TypeError` en `stats.norm(20, 3, 1)` | Una normal tiene dos parámetros: `loc` y `scale` |
| La desviación del paso 2 sale 3,12 | Falta `ddof=1` en `days.std` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Estadística en un proyecto](../../1-teoria/05-estadistica-en-un-proyecto.md) | **Ejercicio 01 · Distribuciones con scipy.stats** | [Ejercicio 02 · Intervalos de confianza y bootstrap](../ejercicio-02-intervalos-y-bootstrap/README.md) |
