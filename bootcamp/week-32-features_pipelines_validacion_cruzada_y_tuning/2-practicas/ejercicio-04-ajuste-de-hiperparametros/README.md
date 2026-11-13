# Ejercicio 04 — Ajuste de hiperparámetros

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-ajuste-de-hiperparametros.md) y [05](../../1-teoria/05-validacion-anidada-y-tu-modelo-ajustado.md)

## Objetivo

Buscar el mejor valor de un hiperparámetro, y medir el resultado sin hacer trampa:

- la curva de validación de `n_neighbors`: dónde memoriza y dónde no aprende;
- una rejilla con dos hiperparámetros, con `GridSearchCV`;
- casi lo mismo con mucho menos trabajo, con `RandomizedSearchCV`;
- un `best_score_` con suerte, cinco veces;
- la validación anidada de esos cinco;
- dos modelos ajustados, comparados de forma honrada.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-32-features_pipelines_validacion_cruzada_y_tuning/2-practicas/ejercicio-04-ajuste-de-hiperparametros/starter
uv run python main.py
```

```
Ejercicio 04 · Ajuste de hiperparámetros
1200 medidas · de 05/01 a 31/10
```

Los datos de los ejercicios anteriores, y `model`: el mismo pipeline, ahora con `KNeighborsRegressor`, que predice la media de las `n_neighbors` medidas más parecidas. `folds` y `scoring` son los de siempre: cinco pliegues con semilla y el MAE en negativo.

Tus salidas coinciden con las del README si descomentas los pasos **en orden**: el paso 4 saca números del mismo generador que los datos.

## Pasos

### 1. La curva de validación

Descomenta el **PASO 1** y ejecuta:

```
n_neighbors=1    MAE entrenamiento 0.21 · validación 4.20
n_neighbors=3    MAE entrenamiento 2.53 · validación 3.74
n_neighbors=10   MAE entrenamiento 3.59 · validación 4.04
n_neighbors=30   MAE entrenamiento 4.71 · validación 4.86
n_neighbors=100  MAE entrenamiento 5.40 · validación 5.45
n_neighbors=300  MAE entrenamiento 5.53 · validación 5.55
```

- **Un vecino**: en entrenamiento, el vecino más parecido de cada medida es ella misma, y el error es casi 0. En validación, 4,20. Memoriza.
- **Trescientos**: promedia tanto que todo se parece a la media. Los dos errores, altos. No aprende.
- El mejor, alrededor de 3. Aquí `n_neighbors` va al revés que `alpha`: pocos vecinos, poco regularizado.

### 2. Una rejilla con dos hiperparámetros

Descomenta el **PASO 2** y ejecuta. Tarda unos segundos:

```
8 combinaciones · mejor: {'model__n_neighbors': 5, 'model__weights': 'distance'}
  {'model__n_neighbors': 5, 'model__weights': 'distance'} · MAE 3.654 ± 0.180
  {'model__n_neighbors': 3, 'model__weights': 'distance'} · MAE 3.703 ± 0.100
  {'model__n_neighbors': 5, 'model__weights': 'uniform'} · MAE 3.735 ± 0.189
```

- Cuatro valores de `n_neighbors` por dos de `weights`: ocho combinaciones, cuarenta entrenamientos.
- `weights="distance"`: los vecinos más cercanos pesan más. Gana en los dos primeros puestos.
- Los tres primeros se separan menos que su desviación (±0,18): son igual de buenos. Elegir "el mejor" entre ellos es casi echarlo a suertes.

### 3. Probar al azar

Descomenta el **PASO 3** y ejecuta:

```
al azar, 15 intentos: {'model__n_neighbors': 4, 'model__weights': 'distance'} · MAE 3.646
```

`randint(1, 200)` saca números enteros entre 1 y 199. Con quince intentos de un espacio de casi cuatrocientas combinaciones, llega al mismo sitio que la rejilla. Por eso, con muchos hiperparámetros, el azar suele ser mejor apuesta que una rejilla gruesa.

### 4. Un ganador con suerte

Descomenta el **PASO 4** y ejecuta:

```
intento 1: {'model__n_neighbors': 14} · best_score_ 0.650
intento 2: {'model__n_neighbors': 2} · best_score_ 0.629
intento 3: {'model__n_neighbors': 15} · best_score_ 0.578
intento 4: {'model__n_neighbors': 18} · best_score_ 0.544
intento 5: {'model__n_neighbors': 30} · best_score_ 0.637
```

Cinco veces: ochenta casos con diez columnas al azar y un nivel "alto" o "normal" al azar. No hay nada que aprender; la exactitud equilibrada debería rondar 0,5. Los cinco `best_score_` están **por encima**, de 0,544 a 0,650: el mejor de treinta, medido con los mismos pliegues con los que se eligió, siempre parece aprender algo. Y cada vez elige un `n_neighbors` distinto: no hay un valor bueno, solo el que tuvo suerte.

### 5. Validación anidada

Descomenta el **PASO 5** y ejecuta:

```
intento 1: anidada 0.613
intento 2: anidada 0.543
intento 3: anidada 0.433
intento 4: anidada 0.482
intento 5: anidada 0.550
```

Los mismos cinco, con la búsqueda dentro de cada pliegue externo. Cada número es más bajo que su `best_score_`, y su media, 0,524, ronda el 0,5 del azar. Con ochenta casos, un pliegue externo tiene dieciséis: por eso se mueve tanto de un intento a otro, de 0,433 a 0,613. La anidada no quita el ruido; quita el **sesgo** de elegir y medir con lo mismo.

### 6. ¿Vecinos o Ridge?

Descomenta el **PASO 6** y ejecuta. Tarda un rato:

```
vecinos, anidada: MAE [3.64 3.56 3.51 3.93 3.72] · media 3.67
Ridge, anidada:   MAE [2.54 2.46 2.46 2.37 2.45] · media 2.46
```

Dos modelos, cada uno con su búsqueda, medidos con los **mismos** pliegues externos. Ridge gana en los cinco, por más de un punto. Los vecinos tienen que adivinar que "punta" o "Centro" importan más que la hora escalada; Ridge aprende un peso para cada uno, y los datos se generaron justo así: sumando efectos. El modelo más flexible no siempre es el mejor; el que se parece a cómo funcionan tus datos, sí.

Para terminar, escribe en un comentario al final de `main.py` qué hiperparámetro ajustarías en tu dominio y qué valores probarías.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'search' is not defined` en el paso 6 | `search` es la rejilla del paso 2: descoméntalo antes |
| `NameError: name 'attempts' is not defined` | El paso 5 usa los intentos del paso 4 |
| Tus números del paso 4 no coinciden | Descomentaste en otro orden: el paso 4 usa el mismo generador que los datos |
| `ValueError: Invalid parameter 'n_neighbors'` | Falta el paso del pipeline: `model__n_neighbors` |
| El paso 6 tarda mucho | Son dos búsquedas por cada uno de cinco pliegues: unos 400 entrenamientos. Es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Validación cruzada](../ejercicio-03-validacion-cruzada/README.md) | **Ejercicio 04 · Ajuste de hiperparámetros** | [Proyecto · Tu modelo ajustado](../../3-proyecto/README.md) |
