# Ejercicio 04 — Regresión con statsmodels

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-regresion-con-statsmodels.md)

## Objetivo

Medir una tendencia y comparar grupos con modelos, cada número con su incertidumbre:

- una recta con `linregress` de SciPy;
- la misma recta con las fórmulas de statsmodels, y su informe;
- variables con categorías, y el ANOVA como caso de la regresión;
- dos variables a la vez, predicciones con sus dos intervalos y los residuos;
- lo que cuesta cada biblioteca, en tiempo y en disco.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-28-estadistica_aplicada_con_scipy_y_statsmodels/2-practicas/ejercicio-04-regresion-con-statsmodels/starter
uv run python main.py
```

```
Ejercicio 04 · Regresión con statsmodels
(270, 3) · ['Norte', 'Sur', 'Centro']
```

90 días de la media diaria de tres estaciones, en una tabla larga (semana 27): una fila por día y estación. Las has generado con niveles de 18, 21 y 19 °C, una subida de 0,04 °C al día y ruido de 1,5 °C. Comprueba en cada paso si los modelos lo recuperan.

## Pasos

### 1. Una recta con SciPy

Descomenta el **PASO 1** y ejecuta:

```
pendiente 0.0482 °C/día · ordenada 17.76 °C
r = 0.664 · R² = 0.441 · p = 9.7e-13
IC 95 % de la pendiente: [0.0367, 0.0597] · en 90 días: 4.34 °C
```

- `linregress` ajusta `valor = ordenada + pendiente · día` por mínimos cuadrados, solo para el Norte.
- La pendiente (0,048) no es el 0,04 de verdad, pero su intervalo lo contiene. El intervalo se construye como en el ejercicio 02: el error estándar de la pendiente (`stderr`) por el t crítico, con n − 2 grados de libertad (la recta usa dos números).
- `r` es la correlación; R² = r², la fracción de la variación que explica la recta: un 44 %. El resto es el ruido diario.
- p es el de "la pendiente es 0". Con 90 días y una subida de 4 °C en total, no hay duda.

### 2. La misma recta con statsmodels

Descomenta el **PASO 2** y ejecuta:

```
RegressionResultsWrapper
             coef    error         p
Intercept   17.76   0.2979 6.071e-73
day       0.04817 0.005781  9.68e-13
             2,5 %   97,5 %
Intercept  17.1711  18.3551
day         0.0367   0.0597
R² = 0.441 · observaciones = 90
¿la misma pendiente que SciPy? True
```

- `smf.ols("value ~ day", data=norte)` describe el modelo con una fórmula: `value` explicado por `day`. `.fit()` lo ajusta y devuelve los resultados.
- `params`, `bse` (los errores estándar), `pvalues` y `conf_int()` son tablas de pandas, una fila por coeficiente. `Intercept` se añade solo.
- Mismos números que SciPy. Prueba `print(fit.summary())`: el informe completo, con R² ajustado, el estadístico F y pruebas sobre los residuos.

### 3. Variables con categorías

Descomenta el **PASO 3** y ejecuta:

```
Intercept              20.996
C(station)[T.Norte]    -1.089
C(station)[T.Sur]       1.559
dtype: float64
medias: {'Centro': 20.996, 'Norte': 19.907, 'Sur': 22.554}
Sur - Centro con pandas: 1.559
            df  sum_sq  mean_sq     F    PR(>F)
C(station)   2   318.8    159.4 45.68 8.666e-18
Residual   267   931.7     3.49   NaN       NaN
f_oneway de SciPy: F = 45.68, p = 8.7e-18
```

- `C(station)` trata la estación como categoría. El primer nivel en orden alfabético, `Centro`, es la **referencia**: `Intercept` es su media, y cada coeficiente es la **diferencia** con ella. `T.Sur` = 1,559 = la media del Sur menos la del Centro.
- `anova_lm` pregunta si **alguna** estación difiere, de una vez. `stats.f_oneway` con los tres grupos da el mismo F y el mismo p: el ANOVA es una regresión con una categoría.
- Las medias salen más altas que los niveles (18, 21, 19) porque son de 90 días que suben 0,04 al día: de media, 1,8 °C más.

### 4. Dos variables, predicciones y residuos

Descomenta el **PASO 4** y ejecuta:

```
{'Intercept': 19.0331, 'C(station)[T.Norte]': -1.0889, 'C(station)[T.Sur]': 1.5589, 'day': 0.0441}
R² solo con day: 0.283
R² con day y estación: 0.538
    mean  mean_ci_lower  mean_ci_upper  obs_ci_lower  obs_ci_upper
0  22.35          21.87          22.84         19.41         25.30
1  25.00          24.52          25.49         22.06         27.94
residuos · media -3.2e-14 · error típico 1.47
Shapiro-Wilk sobre los residuos: p = 0.886
```

- Con las dos variables, `day` es la subida dentro de cada estación (0,044, cerca del 0,04 real), y el `Intercept` (19,03) es el Centro en el día 0, cerca de su 19 real. R² casi se duplica: la estación explica mucha variación que antes era "ruido".
- `get_prediction` para el día 100 da **dos** intervalos. `mean_ci` es para la media de los días 100 del Norte (±0,5 °C); `obs_ci`, para **un** día 100 concreto (±2,9 °C), porque suma el ruido de cada día. Para avisar de la temperatura de un día, el segundo.
- El día 100 está fuera de los datos (0 a 89): extrapolas, poco, pero extrapolas.
- La media de los residuos es 0 salvo redondeo, por construcción. El error típico (1,47) recupera el ruido real (1,5). Shapiro-Wilk no encuentra nada raro en su forma.

### 5. Lo que cuesta cada biblioteca

Descomenta el **PASO 5** y ejecuta:

```
import scipy.stats: 0.50 s
import statsmodels.formula.api: 0.83 s
scipy: 112 MB
statsmodels, patsy y formulaic: 43 MB
```

Tus tiempos serán otros: son los de tu máquina.

- `import_seconds` importa cada módulo en un **proceso nuevo**, donde nada está cargado todavía. La primera llamada se descarta: el sistema operativo aún no tiene los archivos en memoria.
- statsmodels importa SciPy y pandas por dentro: su tiempo incluye el de SciPy.
- `installed_mb` suma los archivos que instaló cada paquete, según sus metadatos.
- Tu proyecto ya tiene SciPy (teoría 05). statsmodels serían 43 MB más y casi un segundo de `import`, para algo que `comparar` no necesita. Si un día tu Observatorio necesita los modelos de este ejercicio, la cuenta cambia.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'statsmodels'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `PatsyError: Error evaluating factor: NameError: name 'dia' is not defined` | Un nombre de la fórmula que no es una columna de `data`: las columnas se llaman `day`, `station` y `value` |
| Los coeficientes salen como `station[T.Sur]` en lugar de `C(station)[T.Sur]` | Escribiste `station` sin `C(...)`. Una columna de texto ya es una categoría, pero `C()` lo deja explícito, y así salen los nombres en este README |
| `KeyError: 'day'` en `fit.params` | Ajustaste el modelo con otra fórmula: mira `fit.params.index` |
| `obs_ci_lower` no aparece en la tabla | Llamaste a `predict` y no a `get_prediction(...).summary_frame()` |
| El paso 5 da tiempos muy distintos entre ejecuciones | Normal: depende de la caché del disco y de lo que haga tu máquina. Ejecuta varias veces |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Pruebas de hipótesis](../ejercicio-03-pruebas-de-hipotesis/README.md) | **Ejercicio 04 · Regresión con statsmodels** | [Proyecto · Comparar dos etiquetas](../../3-proyecto/README.md) |
