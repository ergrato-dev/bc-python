# 01 · Preparar las entradas

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué es una *feature* y por qué casi nunca es la columna tal como llega.
- Usar los transformadores de scikit-learn: `fit` aprende, `transform` aplica.
- Escalar con `StandardScaler`, codificar con `OneHotEncoder` y rellenar huecos con `SimpleImputer`.
- Derivar entradas nuevas de una fecha: la hora, el día de la semana, el fin de semana.

---

## 1. De la columna a la *feature*

En la semana 31, la única entrada de tus modelos era la etiqueta, convertida en columnas 0/1 con `get_dummies`. Una ***feature*** (característica) es cada columna de `X`, tal como la recibe el modelo. Casi nunca es la columna original:

- un texto (la zona) no es un número: hay que **codificarlo**;
- dos números en escalas muy distintas (una temperatura y unos milisegundos) no pesan igual para algunos modelos: hay que **escalarlos**;
- un hueco no es un número: hay que **rellenarlo** o quitar la fila;
- una fecha, tal cual, no dice nada; la hora o el día de la semana, sí: hay que **derivarlas**.

Preparar las entradas suele mejorar un modelo más que cambiar de modelo. Y es donde más fugas se cuelan (teoría 02).

## 2. Los transformadores: aprender y aplicar

Un **transformador** tiene la misma interfaz que un modelo, con `transform` en vez de `predict`:

- `fit(X)` **aprende** lo que necesita de los datos: una media, unas categorías;
- `transform(X)` lo **aplica** a cualquier tabla;
- `fit_transform(X)` hace las dos cosas con la misma tabla.

La regla es la misma que con los modelos: se aprende **solo** con el entrenamiento, y se aplica a las dos partes. Lo que se aprende acaba en atributos con `_`, como `coef_`.

## 3. Escalar: `StandardScaler`

`StandardScaler` resta la media y divide por la desviación: cada columna queda con media 0 y desviación 1.

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

train = pd.DataFrame({"temperatura": [12.0, 18.0, 24.0, 30.0]})
test = pd.DataFrame({"temperatura": [21.0, 40.0]})
scaler = StandardScaler().fit(train)
print(scaler.mean_, scaler.scale_.round(2))
print(scaler.transform(train).ravel().round(2))
print(scaler.transform(test).ravel().round(2))
```

```
[21.] [6.71]
[-1.34 -0.45  0.45  1.34]
[0.   2.83]
```

La prueba se escala con la media y la desviación **del entrenamiento**: 40 queda a 2,83 desviaciones. No sale entre −1,34 y 1,34 porque es más alto que cualquier medida de entrenamiento, y eso es justo lo que el modelo debe ver.

¿Cuándo hace falta? En los modelos que suman entradas con un peso y castigan los pesos grandes (Ridge y la logística con regularización, teoría 04) y en los que miden distancias (los vecinos del ejercicio 04 de la semana 31). En una regresión lineal sin regularización, escalar no cambia las predicciones, solo los coeficientes. Los árboles de la semana 33 no lo necesitan.

## 4. Codificar: `OneHotEncoder`

`OneHotEncoder` hace lo mismo que `get_dummies`, pero **aprende** las categorías:

```python
from sklearn.preprocessing import OneHotEncoder

zones_train = pd.DataFrame({"zona": ["Norte", "Sur", "Norte", "Centro"]})
zones_test = pd.DataFrame({"zona": ["Sur", "Oeste"]})
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(zones_train)
print(encoder.get_feature_names_out())
print(encoder.transform(zones_test))
print(pd.get_dummies(zones_test["zona"], dtype="float64"))
```

```
['zona_Centro' 'zona_Norte' 'zona_Sur']
[[0. 0. 1.]
 [0. 0. 0.]]
   Oeste  Sur
0    0.0  1.0
1    1.0  0.0
```

- El codificador recuerda las tres zonas del entrenamiento, y la prueba sale con **esas** tres columnas, en ese orden. `get_dummies` crea columnas con lo que ve: con la prueba, otras dos, y el modelo no sabría qué hacer con ellas.
- Oeste no estaba en el entrenamiento. Con `handle_unknown="ignore"` es una fila de ceros: "ninguna zona conocida". Sin él, `transform` falla: `ValueError: Found unknown categories ['Oeste'] in column 0 during transform`.
- `sparse_output=False` devuelve una tabla normal. Por defecto devuelve una matriz *dispersa*, que solo guarda los unos: con miles de categorías ahorra mucha memoria.

Por eso, en la semana 31, `features` creaba las columnas con **todas** las medidas antes de repartir. Era seguro porque solo usaba la etiqueta, pero no sabía qué hacer con una etiqueta nueva. En tu proyecto, `OneHotEncoder` sustituye a `get_dummies`.

## 5. Rellenar huecos: `SimpleImputer`

```python
import numpy as np
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="median").fit(pd.DataFrame({"humedad": [40.0, np.nan, 60.0, 90.0]}))
print(imputer.statistics_)
print(imputer.transform(pd.DataFrame({"humedad": [np.nan, 55.0]})).ravel())
```

```
[60.]
[60. 55.]
```

Aprende la mediana del entrenamiento (60) y la pone en cada hueco. `strategy` puede ser `"mean"`, `"median"`, `"most_frequent"` o `"constant"`. Rellenar inventa un dato; a veces el hueco **es** información (el sensor falla cuando hace frío), y entonces conviene añadir una columna "faltaba" (`add_indicator=True`).

Tu Observatorio no lo necesita: las medidas sin valor no tienen nada que predecir, y `known` las quita. Las entradas, la etiqueta y la posición, nunca faltan.

## 6. Derivar entradas

Una fecha no es útil tal cual; lo que esconde, sí:

```python
moments = pd.Series(pd.to_datetime(["2026-11-09 07:30", "2026-11-14 19:05", "2026-11-15 13:00"]))
derived = pd.DataFrame(
    {"hora": moments.dt.hour, "dia": moments.dt.day_of_week, "finde": moments.dt.day_of_week >= 5}
)
print(derived)
```

```
   hora  dia  finde
0     7    0  False
1    19    5   True
2    13    6   True
```

Otras ideas: un cociente (consumo por habitante), una diferencia (temperatura de hoy menos la de ayer), un umbral que conoces de tu dominio. Cada una es una hipótesis: "esto ayuda a predecir". La validación cruzada (teoría 03) dirá si es verdad.

Ojo con lo que derivas: "la media de las medidas del sensor" o "la medida de mañana" son fugas (semana 31, teoría 05). Una entrada solo vale si la tendrías **en el momento de predecir**.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| `fit` del escalador con todas las medidas | La prueba influye en la escala: una fuga pequeña | `fit` con el entrenamiento (teoría 02) |
| `get_dummies` por separado en cada parte | Columnas distintas en entrenamiento y prueba | `OneHotEncoder` |
| `OneHotEncoder()` sin `handle_unknown` | Una categoría nueva rompe `predict` | `handle_unknown="ignore"` |
| Numerar las categorías | Un orden y unas distancias que no existen | One-hot |
| Rellenar sin pensar | Un dato inventado que esconde un patrón | `add_indicator=True`, o quitar la fila |
| Derivar con el futuro | Un modelo perfecto que falla al usarlo | Solo lo que sabrías al predecir |

## ✅ Qué debes saber al terminar

- Qué hacen `fit`, `transform` y `fit_transform` en un transformador, y con qué parte de los datos se ajusta.
- Cuándo hace falta escalar y cuándo no.
- Qué ventajas tiene `OneHotEncoder` sobre `get_dummies`, y qué hace `handle_unknown="ignore"`.
- Cómo rellenar huecos y qué se pierde al hacerlo.
- Cómo sacar entradas de una fecha, y cuándo una entrada derivada es una fuga.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 32](../README.md) | **01 · Preparar las entradas** | [02 · Pipelines](02-pipelines.md) |
