# 03 · Gradient boosting

⏱️ 50 min

## 🎯 Objetivos

- Explicar el *boosting*: árboles pequeños en fila, cada uno aprende el error de los anteriores.
- Ajustar sus dos hiperparámetros principales, `learning_rate` y el número de árboles, juntos.
- Parar a tiempo con `early_stopping`.
- Usar `HistGradientBoostingRegressor` y `HistGradientBoostingClassifier`, con huecos y categorías.
- Decidir entre un árbol, un bosque y un boosting con validación cruzada, no por fama.

---

## 1. Corregir el error, árbol a árbol

Un bosque entrena muchos árboles **a la vez**, cada uno por su cuenta, y hace la media. El ***boosting*** los entrena **en fila**: cada árbol aprende lo que les falta a los anteriores. Con los datos de las teorías 01 y 02, a mano:

```python
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(33)
x = pd.DataFrame(
    {"viento": rng.uniform(0, 10, 300).round(1), "humedad": rng.uniform(30, 98, 300).round()}
)
y = 15 + 15 * (x["viento"] < 2) - 8 * (x["humedad"] > 85) + rng.normal(0, 3, 300)

prediction = np.full(300, y.mean())
print(f"empieza con la media, {y.mean():.1f} · MAE {np.abs(y - prediction).mean():.2f}")
for step in range(1, 4):
    residual = y - prediction
    stump = DecisionTreeRegressor(max_depth=1).fit(x, residual)
    prediction = prediction + stump.predict(x)
    rule = f"{x.columns[stump.tree_.feature[0]]} <= {stump.tree_.threshold[0]:.1f}"
    print(f"árbol {step}: pregunta {rule} · MAE {np.abs(y - prediction).mean():.2f}")
```

```
empieza con la media, 16.4 · MAE 5.68
árbol 1: pregunta viento <= 1.9 · MAE 3.25
árbol 2: pregunta humedad <= 86.5 · MAE 2.44
árbol 3: pregunta humedad <= 77.5 · MAE 2.43
```

1. Empieza prediciendo la **media** para todas las horas.
2. Calcula el **residuo** de cada hora: lo que falta, `y - prediction`.
3. Entrena un árbol de un nivel para predecir **el residuo**, no `y`. El primero encuentra la calma.
4. Suma su predicción a la que había. Vuelve al paso 2.

El segundo árbol ya no ve la calma (está corregida) y encuentra la lluvia. El tercero no encuentra nada que valga la pena: lo que queda es ruido. Cada árbol es **débil** (un nivel, o pocos), pero la suma aprende.

Se llama ***gradient boosting*** porque el residuo es la dirección en la que el error baja más deprisa (el gradiente, para el error cuadrático). Con otras pérdidas, como la de la clasificación, cada árbol aprende el gradiente de esa pérdida.

## 2. El ritmo y el número de árboles

En la práctica, no se suma todo lo que predice cada árbol: solo una parte, el **`learning_rate`**. Cada árbol corrige un poco, y hacen falta más:

```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score

folds = KFold(5, shuffle=True, random_state=33)
for rate, trees in [(1.0, 10), (0.1, 10), (0.1, 100), (0.01, 100), (0.01, 1000)]:
    model = GradientBoostingRegressor(
        n_estimators=trees, learning_rate=rate, max_depth=2, random_state=33
    )
    mae = -cross_val_score(model, x, y, cv=folds, scoring="neg_mean_absolute_error").mean()
    print(f"learning_rate={rate:<4} · {trees:>4} árboles · MAE {mae:.2f}")
```

```
learning_rate=1.0  ·   10 árboles · MAE 2.84
learning_rate=0.1  ·   10 árboles · MAE 3.08
learning_rate=0.1  ·  100 árboles · MAE 2.63
learning_rate=0.01 ·  100 árboles · MAE 3.14
learning_rate=0.01 · 1000 árboles · MAE 2.62
```

- Con **1,0** y 10 árboles, cada uno corrige todo lo que puede: aprende deprisa, ruido incluido.
- Con **0,1**, 10 árboles no llegan; 100, sí, y mejor que con 1,0.
- Con **0,01**, 100 árboles se quedan cortos; 1000 llegan al mismo sitio que 0,1 con 100.

`learning_rate` por número de árboles es lo que el modelo "avanza": si divides uno por diez, multiplica el otro por diez. Un ritmo bajo con muchos árboles suele generalizar algo mejor, pero tarda más. Y, a diferencia de un bosque, **demasiados árboles sobreajustan**: los últimos corrigen el ruido (ejercicio 03, paso 1).

Los otros hiperparámetros controlan cada árbol, como en la teoría 01: `max_depth` (3 por defecto en `GradientBoostingRegressor`) o `max_leaf_nodes` (31 en los `HistGradientBoosting*`), y `min_samples_leaf`.

## 3. Parar a tiempo

Como sobran árboles a partir de cierto punto, lo cómodo es dejar que el modelo pare solo:

```python
from sklearn.ensemble import HistGradientBoostingRegressor

model = HistGradientBoostingRegressor(max_iter=500, early_stopping=True, random_state=33).fit(x, y)
print(f"usa {model.n_iter_} árboles de 500")
```

```
usa 58 árboles de 500
```

Con `early_stopping=True`, aparta un 10 % del entrenamiento (`validation_fraction`) y mide con él después de cada árbol. Si en 10 árboles seguidos (`n_iter_no_change`) no mejora, para, y `n_iter_` dice cuántos usó. Es una validación interna: tu validación cruzada sigue haciendo falta para medir el resultado.

Por defecto (`early_stopping="auto"`), solo lo hace con más de 10 000 medidas.

## 4. HistGradientBoosting

scikit-learn tiene dos versiones:

- `GradientBoostingRegressor` y `GradientBoostingClassifier`: los clásicos. Lentos con muchas medidas, y no admiten huecos.
- **`HistGradientBoostingRegressor`** y **`HistGradientBoostingClassifier`**: antes de entrenar, reparten cada columna en 255 intervalos (`max_bins`) y buscan los cortes entre intervalos, no entre todos los valores. Mucho más rápidos con miles de medidas, y con dos cosas más:

```python
holes = x.copy()
holes.loc[::10, "humedad"] = np.nan
zones = holes.assign(zona=pd.Categorical(rng.choice(["Centro", "Norte"], 300)))
native = HistGradientBoostingRegressor(categorical_features="from_dtype", random_state=33)
mae = -cross_val_score(native, zones, y, cv=folds, scoring="neg_mean_absolute_error").mean()
print(f"{holes['humedad'].isna().sum()} huecos y una categoría, sin preparar: MAE {mae:.2f}")
```

```
30 huecos y una categoría, sin preparar: MAE 3.03
```

- **Huecos**: en cada corte, aprende hacia qué lado mandar las medidas sin dato. Sin `SimpleImputer`.
- **Categorías**: con `categorical_features="from_dtype"`, las columnas de tipo `category` de pandas se tratan como categorías, sin one-hot. Un corte puede separar varias categorías de una vez.

Son los que usa tu Observatorio, con la preparación de la semana 32 por delante: así los cinco modelos de `competir` reciben exactamente las mismas entradas.

## 5. ¿Árbol, bosque o boosting?

Los tres, con los mismos pliegues:

```python
from sklearn.ensemble import RandomForestRegressor

for name, model in [
    ("árbol", DecisionTreeRegressor(max_depth=4, random_state=33)),
    ("bosque", RandomForestRegressor(100, random_state=33)),
    ("boosting", HistGradientBoostingRegressor(random_state=33)),
]:
    mae = -cross_val_score(model, x, y, cv=folds, scoring="neg_mean_absolute_error")
    print(f"{name:<8} MAE {mae.round(2)} · media {mae.mean():.2f}")
```

```
árbol    MAE [2.72 2.67 2.39 2.83 2.56] · media 2.63
bosque   MAE [2.9  2.88 2.55 3.02 2.86] · media 2.84
boosting MAE [2.89 2.71 2.42 3.06 3.03] · media 2.82
```

Gana el **árbol**, en los cinco pliegues. Estos datos son dos umbrales y ruido: un árbol de cuatro niveles los dibuja enteros, y lo que añaden el bosque y el boosting es ruido aprendido. En el ejercicio 03, con la hora punta, la zona, sus cruces y más columnas, el orden se da la vuelta: el boosting gana, el bosque después y el árbol el último.

| Modelo | Bueno para | Cuidado con |
|---|---|---|
| Árbol | Pocos umbrales; explicar el modelo a alguien | La varianza: limítalo siempre |
| Bosque | Un buen resultado sin ajustar casi nada; `oob_score` gratis | Lento de predecir con muchos árboles; no extrapola |
| Boosting | Suele ganar en datos de tabla con muchas columnas | Sobreajusta con demasiados árboles: `early_stopping`; `learning_rate` y el número de árboles, juntos |

No hay un modelo que gane siempre. Lo que lo decide son **tus datos**, con validación cruzada, frente a la referencia y con los mismos pliegues: es lo que hace `competir`.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| Subir `n_estimators` en un boosting "porque más es mejor" | Los últimos árboles aprenden el ruido | `early_stopping=True`, o elegirlo con validación cruzada |
| Cambiar `learning_rate` sin cambiar el número de árboles | Se queda corto o se pasa | Ajustar los dos juntos |
| `GradientBoostingRegressor` con huecos | `ValueError: Input X contains NaN` | `HistGradientBoostingRegressor` |
| Elegir boosting porque gana en las competiciones | Con pocos datos o pocos efectos, un árbol o un lineal ganan | Validación cruzada con tus datos |
| Leer `n_iter_` como la mejor medida del modelo | Es una validación interna, de un reparto | Validación cruzada por fuera |

## ✅ Qué debes saber al terminar

- Qué diferencia el *boosting* del *bagging*: en fila y corrigiendo, frente a en paralelo y promediando.
- Qué es el residuo, y por qué cada árbol aprende el de los anteriores.
- Cómo se relacionan `learning_rate` y el número de árboles, y por qué un boosting puede sobreajustar con demasiados.
- Qué hace `early_stopping`, y qué añaden los `HistGradientBoosting*`: velocidad, huecos y categorías.
- Por qué el mejor modelo depende de tus datos, no de su fama.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Bosques aleatorios](02-bosques-aleatorios.md) | **03 · Gradient boosting** | [04 · Agrupar con KMeans](04-agrupar-con-kmeans.md) |
