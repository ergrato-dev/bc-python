# Ejercicio 03 — Validación cruzada

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-validacion-cruzada.md)

## Objetivo

Medir un modelo con muchos repartos, y elegir cómo repartir:

- diez semillas, diez resultados;
- cinco pliegues con `cross_val_score`, frente a la referencia en los mismos pliegues;
- el error en entrenamiento y en prueba con `cross_validate`;
- qué pasa al no mezclar unos datos ordenados;
- una zona que el modelo nunca vio, con `LeaveOneGroupOut`;
- un cambio con el tiempo, al azar y con `TimeSeriesSplit`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-32-features_pipelines_validacion_cruzada_y_tuning/2-practicas/ejercicio-03-validacion-cruzada/starter
uv run python main.py
```

```
Ejercicio 03 · Validación cruzada
1200 medidas · de 05/01 a 31/10
```

Los datos de los ejercicios 01 y 02, con las columnas derivadas, `x` e `y` sin repartir, y `model`: el pipeline del ejercicio 02 con Ridge. `cross_val_score` lo clona en cada pliegue, así que puedes usarlo tantas veces como quieras.

## Pasos

### 1. Diez repartos, diez resultados

Descomenta el **PASO 1** y ejecuta:

```
R² con diez semillas: de 0.771 a 0.819
```

El mismo modelo, los mismos datos: casi cinco centésimas de diferencia solo por qué medidas caen en prueba. Un reparto te habría dado uno de esos números.

### 2. Cinco pliegues, frente a la referencia

Descomenta el **PASO 2** y ejecuta:

```
modelo:     [0.807 0.801 0.81  0.781 0.827] · 0.805 ± 0.015
referencia: [-0.    -0.008 -0.005 -0.001 -0.   ]
gana en 5 de 5 pliegues
```

- `folds` es el **mismo** reparto para los dos: por eso se pueden comparar pliegue a pliegue.
- La referencia, `DummyRegressor()`, predice la media del entrenamiento: R² un poco por debajo de 0 en cada pliegue, porque la media de la prueba no es exactamente esa.
- El modelo gana en los cinco, y por mucho: mejora de verdad.

### 3. El error en entrenamiento y en prueba

Descomenta el **PASO 3** y ejecuta:

```
MAE en prueba:         [2.54 2.44 2.51 2.52 2.28]
MAE en entrenamiento:  [2.42 2.45 2.43 2.43 2.49]
```

- `scoring="neg_mean_absolute_error"` da el error en negativo: más es mejor, siempre. El `-` lo vuelve positivo.
- Los dos errores son parecidos: el modelo no memoriza. Una regresión lineal con nueve entradas y 960 medidas no tiene con qué sobreajustar.

### 4. Sin mezclar, con los datos ordenados

Descomenta el **PASO 4** y ejecuta:

```
ordenados por PM2.5, sin mezclar: [-2.93 -3.88 -6.22 -9.67 -0.63]
ordenados por PM2.5, mezclando:   [0.84 0.79 0.78 0.8  0.81]
```

Alguien ordenó la tabla por PM2.5. `KFold(5)` sin `shuffle` corta trozos seguidos: el primer pliegue prueba con las 240 medidas más limpias y entrena con las demás. Cada prueba es de un rango que el entrenamiento casi no tiene, y su media es muy distinta: R² muy negativos. Mezclando, todo vuelve a la normalidad.

Es lo que hace `cv=5` en una regresión: `KFold` **sin** mezclar. Si tus datos vienen ordenados por algo, pasa siempre un `KFold` con `shuffle=True`.

### 5. Una zona que nunca vio

Descomenta el **PASO 5** y ejecuta:

```
al azar: MAE medio 2.46
Centro fuera: MAE 8.29
Este fuera: MAE 2.68
Norte fuera: MAE 3.05
Sur fuera: MAE 7.09
```

`LeaveOneGroupOut` deja fuera una zona entera en cada pliegue, en orden alfabético. Para una zona nueva, el modelo no sabe su nivel: predice como "ninguna zona conocida".

- Este y Norte están cerca de la media de las zonas, y casi no se nota.
- Centro (+12) y Sur (0) están en los extremos: el error se triplica.

¿Qué cifra das? Si vas a predecir en estas cuatro zonas, la del azar. Si vas a instalar el sensor en una zona nueva, la de los grupos: el modelo sabe de horas y de días, pero no de zonas que no conoce. `GroupKFold` hace lo mismo con muchos grupos, juntando varios en cada pliegue.

### 6. Cuando algo cambia con el tiempo

Descomenta el **PASO 6** y ejecuta:

```
Centro, antes y después de julio: [20.8, 12.1]
al azar    MAE [3.   3.04 2.94 3.06 2.82] · media 2.97
por tiempo MAE [2.55 2.55 3.08 3.94 3.59] · media 3.14
```

En julio, una zona de bajas emisiones baja ocho puntos el Centro. El modelo no tiene ninguna entrada que lo sepa.

- **Al azar**, cada pliegue entrena con medidas de antes y de después: aprende un Centro "intermedio" y se equivoca un poco con las dos épocas, por igual.
- **Por tiempo**, los primeros pliegues entrenan y prueban antes de julio: bien. Los dos últimos prueban **después** de julio con un modelo que ha visto sobre todo el Centro de antes: el error sube a 3,94.

El reparto por tiempo cuenta lo que pasará al usar el modelo: el mundo cambia y tu modelo llega tarde. Al azar, lo esconde.

Para terminar, escribe en un comentario al final de `main.py` cómo repartirías tus datos: al azar, por grupos (¿cuáles?) o por tiempo, y por qué.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'folds' is not defined` | `folds` se crea en el paso 2: descoméntalo antes |
| `ValueError: The 'groups' parameter should not be None` | Falta `groups=air["zona"]` en el paso 5 |
| Tus números del paso 2 no coinciden | `KFold` sin `random_state=32`: otra mezcla cada vez |
| R² negativos en el paso 2 | Usas `KFold(5)` sin `shuffle` y la tabla está ordenada: mira el paso 4 |
| MAE negativos | Falta el `-` delante: `neg_mean_absolute_error` da el error en negativo |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Pipelines sin fugas](../ejercicio-02-pipelines-sin-fugas/README.md) | **Ejercicio 03 · Validación cruzada** | [Ejercicio 04 · Ajuste de hiperparámetros](../ejercicio-04-ajuste-de-hiperparametros/README.md) |
