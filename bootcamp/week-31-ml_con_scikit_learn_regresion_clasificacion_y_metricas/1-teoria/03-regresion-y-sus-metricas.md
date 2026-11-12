# 03 · Regresión y sus métricas

⏱️ 50 min

## 🎯 Objetivos

- Ajustar una regresión lineal con varias entradas y leer sus coeficientes.
- Convertir una etiqueta en entradas numéricas con one-hot, y saber qué predice entonces el modelo.
- Calcular e interpretar MAE, RMSE y R², y saber cuándo usar cada una.
- Leer un R² negativo y los residuos de un modelo.

---

## 1. Una recta con varias entradas

Con una entrada, la regresión lineal ajusta una recta. Con varias, ajusta un coeficiente por entrada:

```
predicción = intercept_ + coef_[0] · x0 + coef_[1] · x1 + ...
```

`fit` elige los coeficientes que hacen mínima la suma de los errores al cuadrado en el entrenamiento (mínimos cuadrados, como en la semana 28). No hay nada que configurar: `LinearRegression()` sin argumentos.

## 2. Una etiqueta como entradas: one-hot

Una etiqueta no es un número, y numerarla (Norte = 1, Sur = 2, Centro = 3) inventaría un orden y unas distancias que no existen: el Centro no es "tres veces" el Norte. Lo correcto es una columna por etiqueta, con 1 en la de su fila y 0 en las demás:

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

frame = pd.DataFrame(
    {
        "etiqueta": ["Norte", "Norte", "Sur", "Sur", "Sur", "Centro"],
        "valor": [10.0, 14.0, 30.0, 33.0, 36.0, 50.0],
    }
)
x = pd.get_dummies(frame["etiqueta"], dtype="float64")
print(x)
model = LinearRegression().fit(x, frame["valor"])
print(model.predict(x).round(2))
print(frame.groupby("etiqueta")["valor"].mean().to_dict())
```

```
   Centro  Norte  Sur
0     0.0    1.0  0.0
1     0.0    1.0  0.0
2     0.0    0.0  1.0
3     0.0    0.0  1.0
4     0.0    0.0  1.0
5     1.0    0.0  0.0
[12. 12. 33. 33. 33. 50.]
{'Centro': 50.0, 'Norte': 12.0, 'Sur': 33.0}
```

- `pd.get_dummies` crea una columna por etiqueta distinta, en orden alfabético. `dtype="float64"` da 0.0 y 1.0 en vez de `True` y `False`.
- Con solo la etiqueta como entrada, la regresión lineal predice **la media de cada etiqueta**. Es lo mejor que puede hacer: la media es el número que hace mínimo el error al cuadrado de un grupo.

Así se une con la semana 30: allí comparaste las medias de cada zona; aquí las usas para predecir. Si las medias no difieren, predecir con ellas es casi igual que predecir con la media de todo, que es la referencia.

`get_dummies` tiene un límite: crea las columnas que ve. Si una etiqueta solo aparece en los datos nuevos, el modelo recibe una columna que no conoce. Tu Observatorio lo evita creando las columnas con todas las medidas antes de repartir; la semana 32 lo resuelve bien con `OneHotEncoder` dentro de un *pipeline*.

## 3. Tres métricas de error

Cuatro medidas reales y sus predicciones:

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error

real = np.array([10.0, 20.0, 30.0, 40.0])
predicted = np.array([12.0, 18.0, 33.0, 30.0])
print(mean_absolute_error(real, predicted))
print(root_mean_squared_error(real, predicted))
print(r2_score(real, predicted))
```

```
4.25
5.408326913195984
0.766
```

Los errores son 2, 2, 3 y 10.

| Métrica | Cálculo | Aquí | Se lee |
|---|---|---|---|
| **MAE** (error absoluto medio) | Media de \|real − predicción\| | (2 + 2 + 3 + 10) / 4 = 4,25 | "Se equivoca 4,25 unidades de media", en tu unidad |
| **RMSE** (raíz del error cuadrático medio) | Raíz de la media de los errores al cuadrado | √((4 + 4 + 9 + 100) / 4) = 5,41 | En tu unidad, pero castiga más los errores grandes |
| **R²** (coeficiente de determinación) | 1 − (suma de errores²) / (suma de (real − media)²) | 1 − 117 / 500 = 0,766 | Qué parte de la variación explica el modelo, sin unidad |

- **MAE** es la más fácil de explicar a quien no sabe estadística. Un error de 10 pesa lo mismo que diez errores de 1.
- **RMSE** siempre es mayor o igual que MAE. Si es mucho mayor, hay errores grandes: aquí, el 10. Úsala cuando equivocarse mucho una vez sea peor que equivocarse poco muchas.
- **R²** compara con predecir siempre la media: 1 es perfecto, 0 es lo mismo que la media, y por debajo de 0 es **peor** que la media. Sirve para comparar problemas con unidades distintas.

En scikit-learn, cada métrica recibe primero lo real y después lo predicho: `metrica(y_true, y_pred)`. En MAE y RMSE el orden da igual; en R² no.

## 4. R² negativo

```python
print(r2_score(real, np.full(4, real.mean())))
print(r2_score(real, np.full(4, 40.0)))
```

```
0.0
-1.7999999999999998
```

Predecir siempre la media da R² = 0; predecir siempre 40, R² = −1,8. En **entrenamiento**, una regresión lineal nunca baja de 0, porque podría elegir predecir la media. En **prueba** sí puede: la media del entrenamiento no es la de la prueba, y un modelo sobreajustado se equivoca más que ella.

Por eso, en la prueba, incluso la referencia tiene un R² algo por debajo de 0: con los datos de ejemplo del starter, −0,000. Y un modelo que no aprende nada puede quedar un poco peor que ella: −0,006.

## 5. Mirar los residuos

Un **residuo** es `real − predicción`. Una métrica resume todos en un número; mirarlos dice dónde falla el modelo:

- Si los residuos de una etiqueta son casi todos positivos, el modelo la subestima.
- Si crecen con el valor, el error no es igual para todas las medidas: el RMSE mezcla dos comportamientos.
- Un residuo enorme puede ser un error de medida, como los atípicos de la semana 29.

```python
residuals = y_test - model.predict(x_test)
print(residuals.groupby(test["etiqueta"]).mean())
```

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| Numerar las etiquetas | Un orden y unas distancias que no existen | One-hot |
| `get_dummies` por separado en entrenamiento y prueba | Columnas distintas en cada parte | Una vez, o `OneHotEncoder` (semana 32) |
| Dar solo el R² | Nadie sabe cuánto se equivoca, en unidades | MAE o RMSE además |
| Leer R² = 0,766 como "acierta el 77 %" | Una interpretación que no es | "Explica el 77 % de la variación" |
| `r2_score(pred, real)` | Otro número | Primero lo real |
| Pensar que R² no puede ser negativo | No ver que el modelo es peor que la media | En prueba, sí puede |

## ✅ Qué debes saber al terminar

- Qué ajusta `LinearRegression` y cómo se lee con varias entradas.
- Qué es one-hot, cómo se hace con `get_dummies`, y que con solo la etiqueta el modelo predice la media de cada una.
- Cómo se calculan MAE, RMSE y R², en qué unidad está cada una y cuándo usarlas.
- Por qué en prueba R² puede ser negativo, y qué cuentan los residuos.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Entrenar y probar](02-entrenar-y-probar.md) | **03 · Regresión y sus métricas** | [04 · Clasificación y sus métricas](04-clasificacion-y-sus-metricas.md) |
