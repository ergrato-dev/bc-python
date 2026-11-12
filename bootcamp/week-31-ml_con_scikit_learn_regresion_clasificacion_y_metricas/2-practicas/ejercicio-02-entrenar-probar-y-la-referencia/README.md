# Ejercicio 02 — Entrenar, probar y la referencia

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-entrenar-y-probar.md) y [03](../../1-teoria/03-regresion-y-sus-metricas.md)

## Objetivo

Medir un modelo como se debe, con medidas que no vio y al lado de una referencia:

- repartir con `train_test_split`, con semilla;
- estratificar, y ver qué pasa con una clase poco frecuente si no lo haces;
- MAE, RMSE y R², a mano y con scikit-learn;
- el error en entrenamiento frente al de prueba, y un modelo que memoriza;
- `DummyRegressor`, la referencia;
- los residuos por zona.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/2-practicas/ejercicio-02-entrenar-probar-y-la-referencia/starter
uv run python main.py
```

```
Ejercicio 02 · Entrenar, probar y la referencia
200 medidas · nivel alto: 10%
```

`frame` tiene doscientas medidas con su zona, la hora y el valor, y un nivel: "alto" para el 10 % de valores más altos, "normal" para el resto. El comentario no dice cómo se generan: lo descubres midiendo.

Los pasos 1 a 3 reparten siempre igual, con semilla. Tus salidas coinciden con las del README si descomentas los pasos **en orden**.

## Pasos

### 1. Repartir

Descomenta el **PASO 1** y ejecuta:

```
entrenamiento: 150 · prueba: 50
primeras filas de prueba: [148, 8, 79, 137, 147]
misma semilla, mismo reparto: True
otra semilla, otro reparto: True
```

- `test_size=0.25`: 50 de 200 a prueba.
- Las filas se mezclan antes de repartir: las de prueba no son las 50 últimas.
- Con la misma `random_state`, el mismo reparto; con otra, otro. Quita `random_state=31` de la primera línea y ejecuta dos veces: las primeras filas cambian cada vez. Vuelve a ponerlo.

### 2. Estratificar

Descomenta el **PASO 2** y ejecuta:

```
semilla 1: altos en prueba  7 al azar, 5 estratificado
semilla 2: altos en prueba  3 al azar, 5 estratificado
semilla 3: altos en prueba  4 al azar, 5 estratificado
```

Hay 20 medidas de nivel alto, el 10 %. En una prueba de 50 tocan 5. Al azar, según la semilla, salen 7, 3 o 4: con 3, la prueba tiene casi la mitad de altos de los que debería, y cualquier métrica sobre ellos es poco fiable. Con `stratify=frame["nivel"]`, siempre 5.

### 3. Las métricas, a mano y con scikit-learn

Descomenta el **PASO 3** y ejecuta:

```
MAE  a mano 3.540 · scikit-learn 3.540
RMSE a mano 4.698 · scikit-learn 4.698
R²   a mano 0.458 · scikit-learn 0.458
```

- Las entradas son la zona en one-hot. `x.loc[train.index]` toma las filas de entrenamiento por su índice: `train_test_split` lo conserva.
- `errors` son los residuos: real menos predicho.
- MAE es la media de sus valores absolutos; RMSE, la raíz de la media de sus cuadrados; R², uno menos la suma de sus cuadrados entre la de las diferencias con la media (teoría 03, sección 3).

### 4. Entrenamiento y prueba

Descomenta el **PASO 4** y ejecuta:

```
zona, R²: entrenamiento 0.586 · prueba 0.458
hora, 1 vecino, R²: entrenamiento 0.985 · prueba -1.919
```

- Con la zona, el R² baja algo de entrenamiento a prueba, como es normal: un modelo siempre se ajusta un poco a su ruido.
- Con la hora y un solo vecino, el modelo **memoriza**: casi perfecto en entrenamiento (cada medida es su propio vecino), y en prueba mucho peor que predecir la media. La hora no tiene nada que ver con el valor: lo que se aprendió era ruido. Es el sobreajuste de la teoría 02, sección 2.

### 5. La referencia

Descomenta el **PASO 5** y ejecuta:

```
la referencia predice siempre 24.58, la media: 24.58
MAE: modelo 3.54 · referencia 5.46
R²:  modelo 0.458 · referencia -0.026
```

- `DummyRegressor(strategy="mean")` ignora `X` y predice la media del entrenamiento.
- El modelo de zonas se equivoca 3,54 de media; sin saber la zona, 5,46. Saber la zona ayuda: el modelo **mejora** la referencia.
- La referencia tiene un R² algo negativo en prueba: la media del entrenamiento no es exactamente la de la prueba (teoría 03, sección 4).

### 6. Los residuos

Descomenta el **PASO 6** y ejecuta:

```
residuo medio por zona, referencia y modelo:
        referencia  modelo
zona                      
Centro        2.30    0.68
Este         -3.59    0.63
Norte        -2.77    2.33
Sur           7.32   -1.49
```

- La referencia se queda corta en el Sur (residuo +7,32: el real es más alto que lo predicho) y en el Centro, y se pasa en el Norte y el Este. Es lo que esconden los datos: el Sur suma 12, el Centro 6, y el Norte y el Este nada.
- El modelo reparte el error mucho mejor. Lo que queda no es cero porque las medias de la prueba no son las del entrenamiento: con unas 12 medidas por zona en prueba, varían por azar.

Para terminar, escribe en un comentario al final de `main.py`, en dos frases, qué métrica usarías para explicar este modelo a alguien de tu dominio y por qué.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus números no coinciden | Descomentaste en otro orden, o quitaste un `random_state` sin volver a ponerlo |
| `NameError: name 'train' is not defined` | Descomenta antes el paso 1 |
| `NameError: name 'x_train' is not defined` en el paso 5 | Descomenta antes el paso 3 |
| `ValueError: The least populated class in y has only 1 member` | Estratificas por una columna con una clase de una sola fila: no ocurre con estos datos; revisa que `stratify` sea `frame["nivel"]` |
| `KeyError` en `x.loc[train.index]` | Cambiaste `frame` después de repartir: repártelo y créale las entradas a la vez |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Tu primer modelo](../ejercicio-01-tu-primer-modelo/README.md) | **Ejercicio 02 · Entrenar, probar y la referencia** | [Ejercicio 03 · Clasificar y medir](../ejercicio-03-clasificar-y-medir/README.md) |
