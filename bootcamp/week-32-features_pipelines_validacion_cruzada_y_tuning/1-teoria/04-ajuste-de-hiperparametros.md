# 04 · Ajuste de hiperparámetros

⏱️ 50 min

## 🎯 Objetivos

- Distinguir un parámetro, que el modelo aprende, de un hiperparámetro, que eliges tú.
- Explicar la regularización: `alpha` en Ridge y `C` en la regresión logística.
- Leer una curva de validación: el error en entrenamiento y en validación para cada valor.
- Buscar el mejor valor con `GridSearchCV` y `RandomizedSearchCV`, y leer `best_params_` y `cv_results_`.

---

## 1. Parámetros e hiperparámetros

- Los **parámetros** los aprende `fit` de los datos: `coef_` e `intercept_`.
- Los **hiperparámetros** los eliges tú **antes** de `fit`, en el constructor: `Ridge(alpha=10)`, `KNeighborsRegressor(n_neighbors=5)`, `OneHotEncoder(handle_unknown=...)`.

Un hiperparámetro mal elegido puede hacer que un buen modelo sobreajuste o no aprenda nada. **Ajustarlo** (*tuning*) es probar varios valores y quedarse con el que mejor predice medidas nuevas, medido con validación cruzada.

## 2. La regularización

Con pocos casos y muchas entradas, una regresión lineal encuentra pesos para todo: también para el ruido. Cincuenta medidas, treinta entradas, y solo tres que influyen (3, −2 y 1):

```python
import numpy as np
from sklearn.linear_model import Ridge

rng = np.random.default_rng(4)
x = rng.normal(size=(50, 30))
y = 3 * x[:, 0] - 2 * x[:, 1] + x[:, 2] + rng.normal(0, 2, 50)
for alpha in [0.01, 10.0, 1000.0]:
    coef = Ridge(alpha=alpha).fit(x, y).coef_
    print(alpha, coef[:3].round(2), np.abs(coef[3:]).mean().round(2))
```

```
0.01 [ 3.21 -1.78  0.61] 0.29
10.0 [ 2.55 -1.51  0.63] 0.16
1000.0 [ 0.16 -0.14  0.07] 0.02
```

**Ridge** es una regresión lineal que castiga los pesos grandes. `alpha` dice cuánto:

- `alpha=0.01`: casi una regresión lineal. Acierta las tres, pero da a cada una de las 27 inútiles un peso medio de 0,29: ruido aprendido.
- `alpha=10`: encoge todo. Las útiles bajan un poco, las inútiles a la mitad.
- `alpha=1000`: encoge tanto que no queda nada: predice casi la media.

Regularizar cambia sesgo por varianza: un modelo un poco peor en entrenamiento, pero más estable con datos nuevos. Como el castigo depende del tamaño de los pesos, las entradas deben estar en la misma escala: por eso el `StandardScaler` (teoría 01).

En `LogisticRegression` la regularización ya viene puesta, con **`C`**, que va **al revés**: `C` es el inverso de la fuerza. `C=0.01`, mucha regularización; `C=100`, poca. Por defecto, `C=1`.

## 3. La curva de validación

`validation_curve` hace una validación cruzada por cada valor del hiperparámetro:

```python
from sklearn.model_selection import KFold, validation_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

model = Pipeline([("scale", StandardScaler()), ("model", Ridge())])
folds = KFold(5, shuffle=True, random_state=4)
alphas = [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
train, test = validation_curve(
    model, x, y, param_name="model__alpha", param_range=alphas, cv=folds, scoring="r2"
)
for alpha, train_r2, test_r2 in zip(alphas, train.mean(axis=1), test.mean(axis=1)):
    print(f"{alpha:>7} {train_r2:.2f} {test_r2:.2f}")
```

```
   0.01 0.95 -0.00
    0.1 0.95 0.04
    1.0 0.95 0.30
   10.0 0.90 0.59
  100.0 0.55 0.30
 1000.0 0.11 0.00
```

Es la curva del sobreajuste de la semana 31 (teoría 02), girada:

- **A la izquierda**, poca regularización: R² 0,95 en entrenamiento y 0 en validación. Sobreajuste: memoriza.
- **A la derecha**, demasiada: los dos bajan. Infraajuste: no aprende.
- **En medio**, `alpha=10`: el mejor R² en validación, 0,59, con el de entrenamiento todavía alto.

Los valores se prueban en **potencias de 10**: el efecto de `alpha` va por órdenes de magnitud, y entre 10 y 11 no hay diferencia que medir.

## 4. `GridSearchCV`: probar una rejilla

`GridSearchCV` prueba cada combinación de una **rejilla** con validación cruzada, elige la mejor y reentrena con **todos** los datos:

```python
import pandas as pd
from sklearn.model_selection import GridSearchCV

search = GridSearchCV(model, {"model__alpha": alphas}, cv=folds, scoring="r2")
search.fit(x, y)
print(search.best_params_, round(search.best_score_, 3))
columns = ["param_model__alpha", "mean_test_score", "std_test_score", "rank_test_score"]
print(pd.DataFrame(search.cv_results_)[columns].round(3).to_string(index=False))
```

```
{'model__alpha': 10.0} 0.594
 param_model__alpha  mean_test_score  std_test_score  rank_test_score
               0.01           -0.002           0.327                6
               0.10            0.043           0.313                4
               1.00            0.298           0.194                3
              10.00            0.594           0.142                1
             100.00            0.301           0.083                2
            1000.00            0.003           0.058                5
```

- La rejilla es un diccionario: el nombre del parámetro **con el paso del pipeline** (`model__alpha`, teoría 02, sección 3) y la lista de valores. Con dos parámetros, prueba todas las parejas: 6 × 4 valores son 24 combinaciones, por 5 pliegues, 120 entrenamientos.
- `best_params_` y `best_score_`: el ganador y su media en validación.
- `cv_results_`: todo lo probado. Mira también la desviación: si la del segundo cubre la diferencia con el primero, los dos son igual de buenos.
- Después de `fit`, `search` **es** el mejor modelo, reentrenado con todos los datos: `search.predict(x_nuevo)` funciona.

## 5. `RandomizedSearchCV`: probar al azar

Con muchos hiperparámetros, la rejilla crece muy rápido. `RandomizedSearchCV` prueba `n_iter` combinaciones al azar, sacadas de una distribución:

```python
from scipy.stats import loguniform
from sklearn.model_selection import RandomizedSearchCV

randomized = RandomizedSearchCV(
    model,
    {"model__alpha": loguniform(0.01, 1000)},
    n_iter=20,
    cv=folds,
    scoring="r2",
    random_state=4,
)
randomized.fit(x, y)
print(round(float(randomized.best_params_["model__alpha"]), 2), round(randomized.best_score_, 3))
```

```
9.7 0.593
```

`loguniform` reparte los valores por igual entre cada potencia de 10. Veinte intentos llegan casi al mismo sitio que la rejilla. Con un solo hiperparámetro, la rejilla basta; con tres o cuatro, el azar encuentra antes las zonas buenas.

## 6. Un número optimista

`best_score_` es la media del **ganador** entre seis. Si los seis fueran igual de buenos, el que más saca es el que tuvo más suerte en estos pliegues: es el jardín de los senderos de la semana 30, con hiperparámetros. Por eso `best_score_` es **optimista**, y no sirve como medida final del modelo. La teoría 05 muestra cuánto, y cómo medir sin ese sesgo.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| Ajustar con la prueba | Una medida final optimista | Validación cruzada en el entrenamiento |
| Valores de 1 en 1 | Muchas pruebas para nada | Potencias de 10 |
| Regularizar sin escalar | Castiga más las entradas con números grandes | `StandardScaler` en el pipeline |
| Pensar que `C` alto regulariza más | Al revés: `C` es el inverso | `C` bajo, más regularización |
| `{"alpha": ...}` con un pipeline | `ValueError: Invalid parameter` | `{"model__alpha": ...}` |
| Dar `best_score_` como resultado final | Optimista: es el mejor entre varios | Validación anidada (teoría 05) |

## ✅ Qué debes saber al terminar

- Qué diferencia un parámetro de un hiperparámetro.
- Qué hace `alpha` en Ridge, qué hace `C` en la logística, y por qué hay que escalar.
- Cómo leer una curva de validación: dónde sobreajusta y dónde no aprende.
- Cómo se usan `GridSearchCV` y `RandomizedSearchCV`, y qué guardan `best_params_`, `best_score_` y `cv_results_`.
- Por qué `best_score_` es optimista.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Validación cruzada](03-validacion-cruzada.md) | **04 · Ajuste de hiperparámetros** | [05 · Validación anidada y tu modelo ajustado](05-validacion-anidada-y-tu-modelo-ajustado.md) |
