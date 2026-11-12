# 01 · Aprender de los datos

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué es el aprendizaje supervisado y en qué se diferencia de lo que hiciste en la fase 4.
- Nombrar las piezas de un problema: casos, entradas (*features*), objetivo (*target*), `X` e `y`.
- Distinguir regresión de clasificación por el tipo del objetivo.
- Usar la interfaz común de scikit-learn: `fit`, `predict` y `score`.

---

## 1. De describir a predecir

En la fase 4 **describiste** tus datos: medias, intervalos, diferencias entre etiquetas. La pregunta era "¿cómo son las medidas que tengo?". En la fase 5 la pregunta cambia: "dada una medida **nueva**, ¿qué valor tendrá?".

Un **modelo** es una función que, a partir de unas entradas, devuelve una predicción. En vez de escribirla tú (`if zona == "Sur": return 30`), le das ejemplos con su respuesta y un algoritmo **ajusta** la función a esos ejemplos. Eso es el **aprendizaje supervisado**: supervisado porque cada ejemplo trae la respuesta correcta.

| Fase 4 | Fase 5 |
|---|---|
| ¿Difiere la media del Sur de la del Norte? | ¿Qué valor tendrá la próxima medida del Sur? |
| Se mide con un intervalo y un p-valor | Se mide con el error en medidas que el modelo no vio |
| Usa todos los datos | Aparta una parte para probar (teoría 02) |

Las dos preguntas están relacionadas. Si las zonas no difieren, saber la zona no ayuda a predecir el valor: lo comprobarás en el proyecto.

## 2. Casos, entradas y objetivo

Cada fila de tu instantánea es un **caso** (una medida). Para un modelo, cada caso tiene dos partes:

- **Entradas** (*features*): lo que sabes antes de predecir. En el Observatorio, la etiqueta.
- **Objetivo** (*target*): lo que quieres predecir. El valor, o el nivel.

Por convención, las entradas de todos los casos forman una tabla `X` (mayúscula: dos dimensiones, una fila por caso y una columna por entrada) y los objetivos un vector `y` (minúscula: una dimensión, uno por caso).

```
          X                     y
  etiqueta = Norte  Sur      valor
  caso 0      1.0   0.0      12.5
  caso 1      0.0   1.0      31.2
  caso 2      1.0   0.0       9.8
```

Los modelos de scikit-learn solo entienden números. Una entrada de texto como la etiqueta se convierte en una columna 0/1 por cada valor posible: se llama **one-hot**, y la teoría 03 la usa.

## 3. Regresión o clasificación

El tipo del objetivo decide el tipo de problema:

| Objetivo | Problema | Ejemplo en el Observatorio | Se mide con |
|---|---|---|---|
| Un número | **Regresión** | El valor de la medida | Cuánto se equivoca (teoría 03) |
| Una categoría | **Clasificación** | El nivel: bajo, medio o alto | Cuántas acierta, y cuáles (teoría 04) |

El mismo dato puede ser las dos cosas. El nivel sale del valor con tus umbrales de la semana 2: predecir el valor y aplicarle los umbrales es una regresión; predecir el nivel directamente es una clasificación. En el proyecto haces las dos.

## 4. La interfaz de scikit-learn

scikit-learn tiene decenas de modelos, y todos se usan igual. Cada uno es una clase; un objeto de esa clase es un **estimador**:

```python
import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])  # horas de sol
y = np.array([12.1, 14.0, 15.9, 18.2, 19.8])         # temperatura

model = LinearRegression()
model.fit(x, y)
print(model.coef_, model.intercept_)
print(model.predict([[6.0]]))
```

```
[1.96] 10.120000000000001
[21.88]
```

| Método o atributo | Qué hace |
|---|---|
| `LinearRegression()` | Crea el estimador, con sus opciones (hiperparámetros); aún no sabe nada |
| `fit(X, y)` | Aprende de los ejemplos y devuelve el propio estimador |
| `coef_`, `intercept_` | Lo aprendido: acaban en `_` porque solo existen después de `fit` |
| `predict(X)` | Una predicción por fila de `X` |
| `score(X, y)` | Una métrica por defecto: R² en regresión, exactitud en clasificación |

`X` siempre tiene dos dimensiones, aunque haya una sola entrada: `[[1.0], [2.0]]`, no `[1.0, 2.0]`. Con una dimensión, `fit` falla con `Expected 2D array, got 1D array instead`.

Como `fit` devuelve el estimador, se puede encadenar: `LinearRegression().fit(x, y).predict(nuevos)`. Cambiar de modelo es cambiar una línea: `KNeighborsRegressor()` en vez de `LinearRegression()`, y el resto igual.

## 5. Lo que el modelo aprendió

`coef_` = 1,96 e `intercept_` = 10,12 dicen que el modelo es `temperatura = 1,96 · horas + 10,12`: cada hora de sol, casi dos grados más. Es la recta de la regresión de la semana 28, ajustada por mínimos cuadrados.

Un modelo lineal se puede leer así. Otros (los árboles y ensembles de la semana 33, las redes de la semana 34) no tienen una fórmula que leer, y se juzgan solo por cómo predicen. Por eso la pregunta central de esta semana no es "¿qué aprendió?", sino "¿predice bien medidas que no vio?" (teoría 02).

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| `X` de una dimensión | `ValueError: Expected 2D array` | `x.reshape(-1, 1)` o `frame[["columna"]]` |
| Pasar texto como entrada | `ValueError: could not convert string to float` | One-hot (teoría 03) |
| Leer `coef_` antes de `fit` | `AttributeError` | `fit` primero |
| Llamar clasificación a predecir un número | Métricas que no tienen sentido | Mirar el tipo del objetivo |
| Poner el objetivo entre las entradas | Un modelo perfecto que no sirve (teoría 05) | Separar `X` de `y` con cuidado |

## ✅ Qué debes saber al terminar

- Qué es un modelo supervisado y en qué cambia la pregunta respecto a la fase 4.
- Qué son casos, entradas, objetivo, `X` e `y`, y por qué `X` tiene dos dimensiones.
- Cuándo un problema es de regresión y cuándo de clasificación.
- Qué hacen `fit`, `predict` y `score`, y qué significa el `_` final de `coef_`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 31](../README.md) | **01 · Aprender de los datos** | [02 · Entrenar y probar](02-entrenar-y-probar.md) |
