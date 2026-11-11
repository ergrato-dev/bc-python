# 04 · Regresión con statsmodels

⏱️ 45 min

## 🎯 Objetivos

- Ajustar una recta con SciPy y con statsmodels, y leer pendiente, intervalo, p-valor y R².
- Escribir modelos con fórmulas, incluidas variables con categorías.
- Ver que comparar grupos (ANOVA) es un caso de la regresión.
- Distinguir el intervalo de la media del intervalo de predicción.
- Revisar los residuos, y no confundir relación con causa.

---

## 1. Una tendencia con su incertidumbre

¿Sube la temperatura del Norte con los días? Una **regresión lineal** busca la recta `valor = a + b · día` que pasa más cerca de los puntos: la que hace mínima la suma de los cuadrados de las distancias verticales (**mínimos cuadrados**, *OLS*, *ordinary least squares*).

Con SciPy, para una sola variable:

```python
line = stats.linregress(norte["day"], norte["value"])
```

```
pendiente 0.0482 °C/día · ordenada 17.76 °C
r = 0.664 · R² = 0.441 · p = 9.7e-13
IC 95 % de la pendiente: [0.0367, 0.0597] · en 90 días: 4.34 °C
```

- La **pendiente** (0,048 °C/día) es lo que cambia el valor por cada día más. Su intervalo, construido con t como en la teoría 02 (`stderr` y n − 2 grados de libertad), contiene el 0,04 con el que se generaron los datos.
- El **p-valor** es el de la hipótesis nula "la pendiente es 0" (teoría 03).
- **R²** es la fracción de la variación del valor que explica la recta: el 44 %. El resto es ruido o cosas que el modelo no tiene.

---

## 2. statsmodels: el modelo como fórmula

statsmodels es la biblioteca de Python para **modelos estadísticos**: regresión, series temporales, modelos lineales generalizados. Donde SciPy da funciones sueltas, statsmodels da un modelo con todo su informe. Su interfaz de fórmulas escribe el modelo como en R:

```python
import statsmodels.formula.api as smf

fit = smf.ols("value ~ day", data=norte).fit()
fit.params      # coeficientes
fit.bse         # sus errores estándar
fit.conf_int()  # sus intervalos del 95 %
fit.pvalues     # sus p-valores
fit.rsquared    # R²
fit.summary()   # el informe completo
```

```
             coef    error         p
Intercept   17.76   0.2979 6.071e-73
day       0.04817 0.005781  9.68e-13
```

- `"value ~ day"` se lee "value explicado por day". Las columnas salen de `data`, un `DataFrame` largo (semana 27).
- `Intercept` (la ordenada en el origen) se añade solo.
- La pendiente es la misma que da `linregress`. statsmodels admite además muchas variables, categorías y otros modelos.

---

## 3. Variables con categorías

¿Y si la variable es la estación? `C(station)` le dice a la fórmula que es una categoría:

```python
groups = smf.ols("value ~ C(station)", data=readings).fit()
```

```
Intercept              20.996
C(station)[T.Norte]    -1.089
C(station)[T.Sur]       1.559
```

- Una categoría se convierte en columnas de 0 y 1, una por nivel **menos uno**: el primero en orden alfabético (`Centro`) es la **referencia**.
- `Intercept` es la media de la referencia (20,996), y cada coeficiente es la **diferencia** con ella: el Sur, 1,559 °C más que el Centro. Es lo mismo que restar las medias con pandas, pero ahora cada diferencia trae su error estándar, su intervalo y su p-valor.

Para preguntar "¿hay alguna diferencia entre las tres estaciones?" de una vez, el **ANOVA** (análisis de la varianza):

```
            df  sum_sq  mean_sq     F    PR(>F)
C(station)   2   318.8    159.4 45.68 8.666e-18
Residual   267   931.7     3.49   NaN       NaN
f_oneway de SciPy: F = 45.68, p = 8.7e-18
```

`anova_lm` sobre el modelo y `stats.f_oneway` sobre los grupos dan el mismo F y el mismo p. Comparar grupos es una regresión con una categoría. Un p pequeño dice que **alguna** estación difiere; cuál, lo dicen los coeficientes (o las comparaciones por parejas, con la corrección de la teoría 03).

---

## 4. Varias variables a la vez

```python
both = smf.ols("value ~ day + C(station)", data=readings).fit()
```

```
R² solo con day: 0.283
R² con day y estación: 0.538
```

Cada coeficiente es ahora el efecto de **su** variable con las demás fijas: la pendiente de `day` (0,044) es la de dentro de cada estación, y los coeficientes de estación, las diferencias a igual día. Añadir la estación explica casi el doble de variación.

---

## 5. Predecir, con dos intervalos distintos

```python
future = pd.DataFrame({"day": [100, 100], "station": ["Norte", "Sur"]})
both.get_prediction(future).summary_frame(alpha=0.05)
```

```
    mean  mean_ci_lower  mean_ci_upper  obs_ci_lower  obs_ci_upper
0  22.35          21.87          22.84         19.41         25.30
1  25.00          24.52          25.49         22.06         27.94
```

| Intervalo | Responde | Ancho aquí |
|---|---|---|
| `mean_ci` | ¿Dónde está la **media** de los días 100 del Norte? | ±0,5 °C |
| `obs_ci` | ¿Dónde caerá **un** día 100 concreto del Norte? | ±2,9 °C |

El de predicción añade el ruido de cada día (1,47 °C de error típico) a la incertidumbre de la recta. Si vas a avisar de una temperatura de mañana, el que te interesa es el ancho.

Y el día 100 está **fuera** de los datos (0 a 89). Extrapolar un poco es razonable; extrapolar a un año supone que la tendencia sigue recta, y nada en los datos lo dice.

---

## 6. Revisar los residuos

Los **residuos** son lo que el modelo no explica: valor observado menos valor ajustado. Los intervalos y los p-valores de OLS suponen que:

| Supuesto | Qué falla si no | Cómo mirarlo |
|---|---|---|
| La relación es lineal | La recta no describe los datos | Residuos frente a valores ajustados: sin forma |
| Los residuos son independientes | Errores estándar demasiado pequeños (pasa con series de tiempo: un día caluroso sigue a otro) | Residuos en orden de tiempo |
| Dispersión constante | Intervalos falsos en una parte del rango | El mismo gráfico: sin forma de embudo |
| Residuos aproximadamente normales | Con pocos datos, p-valores poco fiables | Histograma, `stats.shapiro` |

```
residuos · media -3.2e-14 · error típico 1.47
Shapiro-Wilk sobre los residuos: p = 0.886
```

La media de los residuos es 0 por construcción. El error típico (1,47) se acerca al ruido real (1,5). Shapiro-Wilk no encuentra nada raro, pero recuerda la teoría 03: con muchos datos rechaza por desviaciones sin importancia, y con pocos no ve nada. Un gráfico de residuos (semana 27) dice más que un p-valor.

---

## 7. Relación no es causa

Una pendiente significativa dice que dos cosas varían juntas, no que una cause la otra. Si las alertas suben con la temperatura, puede que el calor las cause, que las dos dependan de la hora del día, o que en verano haya más sensores. Solo un experimento (cambias una cosa y nada más) o un análisis que tenga en cuenta las demás causas lo separan. Cuando escribas "explica" o "efecto" en tu informe, piensa si los datos te dejan.

---

## 8. SciPy, statsmodels y lo que viene

| Herramienta | Para qué | Precio (ejercicio 04) |
|---|---|---|
| `scipy.stats` | Distribuciones, pruebas, `linregress`, bootstrap | 112 MB, `import` en 0,5 s |
| statsmodels | Modelos con su informe: fórmulas, categorías, predicciones, residuos, series temporales | 43 MB más (con patsy y formulaic), necesita SciPy y pandas; `import` en 0,8 s |
| scikit-learn (semana 31) | Predecir bien datos nuevos: validación, *pipelines*, muchos modelos | Otra dependencia |

statsmodels responde "¿qué relación hay, y con cuánta incertidumbre?"; scikit-learn, "¿cómo predigo mejor?". Para tu proyecto, `comparar` solo necesita dos pruebas y un intervalo: SciPy basta (teoría 05).

---

## 9. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Leer R² alto como "el modelo es correcto" | R² no dice si la forma es la buena | Mirar los residuos |
| Leer cada coeficiente de categoría como la media del grupo | Es la **diferencia** con la referencia | `Intercept` + coeficiente, o `groupby().mean()` |
| Usar `mean_ci` para avisar de un valor concreto | Es para la media; un valor varía mucho más | `obs_ci` |
| Extrapolar lejos | Nada dice que la recta siga | Predecir dentro del rango, o decirlo |
| "La temperatura causa las alertas" por una pendiente | Relación no es causa | Buscar las otras explicaciones |
| Regresión con datos de serie sin mirar la independencia | Errores estándar demasiado optimistas | Residuos en orden; modelos de series temporales |

---

## ✅ Qué debes saber al terminar

- [ ] Ajustar una recta con `linregress` y con `smf.ols`, y leer pendiente, intervalo, p y R².
- [ ] Qué significan los coeficientes de `C(station)`, y cuál es la referencia.
- [ ] Por qué `anova_lm` y `f_oneway` dan lo mismo.
- [ ] Cuándo usar `mean_ci` y cuándo `obs_ci`.
- [ ] Qué supuestos revisar en los residuos.
- [ ] Qué hace statsmodels que no hace SciPy, y lo que cuesta.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Pruebas de hipótesis](03-pruebas-de-hipotesis.md) | **04 · Regresión con statsmodels** | [05 · Estadística en un proyecto](05-estadistica-en-un-proyecto.md) |
