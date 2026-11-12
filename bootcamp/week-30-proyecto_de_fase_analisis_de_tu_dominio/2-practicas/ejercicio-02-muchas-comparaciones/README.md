# Ejercicio 02 — Muchas comparaciones

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-muchas-comparaciones.md)

## Objetivo

Ver con simulaciones cuántos "hallazgos" salen por azar al comparar mucho, y qué hace cada corrección:

- una comparación sin diferencia, mil veces;
- diez comparaciones sin diferencia: al menos un falso positivo;
- veinte comparaciones, cuatro con diferencia real, sin corregir y con Bonferroni, Holm y Benjamini-Hochberg;
- BH calculado a mano frente a `scipy.stats.false_discovery_control`;
- mil análisis de veinte comparaciones, para medir cada corrección.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-30-proyecto_de_fase_analisis_de_tu_dominio/2-practicas/ejercicio-02-muchas-comparaciones/starter
uv run python main.py
```

```
Ejercicio 02 · Muchas comparaciones
20 comparaciones, 4 con diferencia real
```

`p_value(shift)` genera dos muestras de 30 valores de una campana de desviación 1, separadas por `shift`, y devuelve el p de Welch. Con `shift=0.0`, cualquier p pequeño es un falso positivo. `holm(p)` es la corrección de Holm, escrita a mano.

Todos los pasos sacan números al azar del mismo generador, con semilla: tus salidas coinciden con las del README si descomentas los pasos **en orden** y sin saltarte ninguno.

## Pasos

### 1. Una comparación sin diferencia

Descomenta el **PASO 1** y ejecuta:

```
p < 0.05 en 5.8% de 1000 comparaciones sin diferencia
```

Lo que promete α = 0,05: más o menos una de cada veinte comparaciones sin diferencia sale "significativa". Con mil, 5,8 % en vez de 5 %: el azar de la propia simulación.

### 2. Diez comparaciones sin diferencia

Descomenta el **PASO 2** y ejecuta:

```
con algún p < 0.05: 38.7% de 1000 análisis
la fórmula: 40.1%
```

`(families < 0.05).any(axis=1)`: en cada fila (un análisis de diez comparaciones), ¿alguna sale por debajo de 0,05? En cuatro de cada diez análisis, sí, aunque no haya ninguna diferencia. Es lo que dice la fórmula 1 − 0,95^10.

### 3. Veinte comparaciones, sin corregir

Descomenta el **PASO 3** y ejecuta:

```
p: [0.    0.    0.016 0.    1.    0.773 0.153 0.658 0.385 0.03  0.668 0.128
 0.079 0.116 0.296 0.42  0.047 0.501 0.783 0.981]
sin corregir: 6 hallazgos, 4 reales y 2 falsos
```

- Las cuatro primeras tienen diferencia real, y sus p son pequeños (0. significa que redondeado a tres decimales es 0).
- Dos de las dieciséis sin diferencia también bajan de 0,05: la décima (0,03) y la decimoséptima (0,047). En un informe sin corregir, aparecerían como hallazgos.

### 4. Bonferroni, Holm y Benjamini-Hochberg

Descomenta el **PASO 4** y ejecuta:

```
bonferroni: 3 hallazgos, 3 reales y 0 falsos
holm: 3 hallazgos, 3 reales y 0 falsos
bh: 3 hallazgos, 3 reales y 0 falsos
```

Las tres quitan los dos falsos, y las tres pierden un real: el tercero, con p = 0,016. En un solo análisis no se ve la diferencia entre ellas; el paso 6 la mide con mil.

### 5. BH a mano

Descomenta el **PASO 5** y ejecuta:

```
los tres menores, a mano: [0.0001 0.0001 0.0002]
los tres menores, scipy:  [0.0001 0.0001 0.0002]
iguales: True
```

Los pasos de la teoría 03, sección 3, con NumPy:

- `np.argsort(p)`: el orden de menor a mayor.
- `p[order] * len(p) / np.arange(1, len(p) + 1)`: el de puesto k, por m/k.
- `np.minimum.accumulate(scaled[::-1])[::-1]`: de abajo arriba, el menor visto hasta ahora.
- `by_hand[order] = ...`: cada p corregido, de vuelta a la posición de su comparación.

Comenta la última línea (`by_hand[order] = ...`) y cámbiala por `by_hand = np.minimum.accumulate(scaled[::-1])[::-1]`: `iguales` pasa a `False`. Los p corregidos están bien, pero en otro orden, cada uno en la comparación equivocada. `false_discovery_control` te ahorra este error.

### 6. Mil análisis de veinte comparaciones

Descomenta el **PASO 6** y ejecuta. Tarda unos segundos: son 20 000 pruebas.

```
corrección   reales  falsos  con algún falso  falsos/hallazgos
ninguna        3.89    0.77            54.3%             14.1%
bonferroni     3.02    0.04             4.4%              1.2%
holm           3.06    0.06             5.5%              1.5%
bh             3.50    0.20            18.0%              4.3%
```

Cada columna es una media de los mil análisis:

| Columna | Qué mide |
|---|---|
| `reales` | Cuántas de las 4 diferencias reales encuentra |
| `falsos` | Cuántos falsos positivos publica |
| `con algún falso` | En qué parte de los análisis hay al menos uno: lo que controla FWER |
| `falsos/hallazgos` | Qué parte de lo publicado es falso: lo que controla FDR |

- **Sin corregir**: más de la mitad de los análisis publican algún falso, y uno de cada siete hallazgos lo es.
- **Bonferroni y Holm** mantienen `con algún falso` cerca del 5 %: su promesa. Holm encuentra algo más que Bonferroni.
- **BH** deja un 18 % de análisis con algún falso, pero solo el 4,3 % de lo que publica es falso, por debajo del 5 % que promete. A cambio, encuentra 3,5 de las 4 diferencias reales, frente a 3,02 de Bonferroni.

Para terminar, escribe en un comentario al final de `main.py` qué corrección usarías para el informe de tu dominio y por qué, en dos frases.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus números no coinciden con los del README | Descomentaste los pasos en otro orden o te saltaste uno: todos usan el mismo generador |
| `AttributeError: module 'scipy.stats' has no attribute 'false_discovery_control'` | Ejecuta con `uv run`: usa SciPy 1.18.1, del `uv.lock` |
| `NameError: name 'p' is not defined` en el paso 4 | Descomenta antes el paso 3 |
| `NameError: name 'methods' is not defined` en el paso 5 | Descomenta antes el paso 4 |
| El paso 6 tarda más de un minuto | Normal en una máquina lenta; baja `range(1000)` a `range(200)`, y tus números serán otros |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · De la pregunta a la métrica](../ejercicio-01-de-la-pregunta-a-la-metrica/README.md) | **Ejercicio 02 · Muchas comparaciones** | [Ejercicio 03 · Un gráfico por afirmación](../ejercicio-03-un-grafico-por-afirmacion/README.md) |
