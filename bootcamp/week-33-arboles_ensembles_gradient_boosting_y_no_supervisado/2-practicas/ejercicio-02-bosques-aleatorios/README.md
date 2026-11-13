# Ejercicio 02 — Bosques aleatorios

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-bosques-aleatorios.md)

## Objetivo

Ver por qué cien árboles distintos predicen mejor que uno, y qué columnas usan:

- un árbol cambia con cada muestra; un bosque, casi nada;
- un bosque frente a un árbol sin límite y uno podado;
- cuántos árboles hacen falta;
- la nota *out-of-bag*, sin validación cruzada;
- las importancias por impureza, y una columna de ruido que parece útil;
- las importancias por permutación, que no se dejan engañar.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/2-practicas/ejercicio-02-bosques-aleatorios/starter
uv run python main.py
```

```
Ejercicio 02 · Bosques aleatorios
1500 medidas · de 05/01 a 31/10
```

Los datos del ejercicio 01, con una columna más: `ruido`, números al azar entre 0 y 100 que no tienen nada que ver con el PM2.5. `pipe(model)` pone la zona en one-hot delante de cualquier modelo.

## Pasos

### 1. Un árbol cambia con cada muestra

Descomenta el **PASO 1** y ejecuta. Tarda unos segundos:

```
 hora  dia  zona  humedad  viento  ruido
    0    0 Norte     56.0     1.8   16.5 · PM2.5 de verdad 30.1
árbol  con cinco muestras: [22.9 24.8 29.6 23.3 28.4]
bosque con cinco muestras: [28.4 28.1 27.8 28.1 28.1]
```

La primera medida, fuera del entrenamiento. Cinco repartos distintos de las demás, y cinco predicciones para ella:

- **Un árbol** sin límite da de 22,9 a 29,6: cada muestra lo lleva a otra hoja, con otras pocas medidas. Tiene mucha **varianza**.
- **Un bosque** de cien árboles da de 27,8 a 28,4: los errores de cada árbol van en direcciones distintas, y en la media se cancelan.

### 2. Un bosque frente a sus árboles

Descomenta el **PASO 2** y ejecuta:

```
árbol sin límite   MAE medio 3.70
árbol, max_depth=6 MAE medio 3.04
bosque de 100      MAE medio 2.85
```

Los árboles del bosque **no tienen límite**: cada uno memoriza su muestra. Aun así, el bosque gana al árbol podado. Para un árbol, podar es la única forma de no memorizar; un bosque deja que cada árbol memorice y lo arregla con la media.

### 3. Cuántos árboles

Descomenta el **PASO 3** y ejecuta. Tus tiempos serán otros:

```
  1 árboles: MAE 4.02 · 0.0 s
  5 árboles: MAE 3.13 · 0.1 s
 20 árboles: MAE 2.92 · 0.2 s
100 árboles: MAE 2.85 · 1.2 s
300 árboles: MAE 2.85 · 3.7 s
```

- Un árbol solo es **peor** que el árbol sin límite del paso 2 (4,02 frente a 3,70): entrena con una muestra con repetición, en la que falta más o menos un tercio de las medidas y otras salen dos o tres veces.
- De 100 a 300, el mismo error y el triple de tiempo. Más árboles nunca empeoran un bosque, pero llega un punto en que tampoco lo mejoran.

### 4. La nota sin validación cruzada: out-of-bag

Descomenta el **PASO 4** y ejecuta:

```
R² out-of-bag 0.825 · validación cruzada 0.820
```

Cada árbol entrena con una muestra con repetición: deja fuera más o menos un tercio de las medidas. `oob_score=True` predice cada medida solo con los árboles que no la vieron, y calcula el R². Casi lo mismo que cinco pliegues, con un solo entrenamiento.

### 5. Importancias por impureza

Descomenta el **PASO 5** y ejecuta:

```
viento         0.298
zona_Centro    0.202
humedad        0.169
hora           0.158
zona_Sur       0.105
ruido          0.040
dia            0.019
zona_Este      0.005
zona_Norte     0.004
```

`feature_importances_` suma cuánto baja el error cada corte con cada columna, en todos los árboles. Suman 1. El viento y el Centro, arriba: los umbrales del ejercicio 01.

Pero mira `ruido`: 0,040, **el doble que `dia`**. Los datos no dependen de ninguna de las dos. `ruido` tiene muchos valores distintos, y un árbol sin límite encuentra siempre un corte que separa por casualidad unas pocas medidas de entrenamiento. Las importancias por impureza se miden con el **entrenamiento**: premian las columnas con muchos valores, sirvan o no.

### 6. Importancias por permutación

Descomenta el **PASO 6** y ejecuta. Tarda unos segundos:

```
cuánto sube el MAE al barajar cada columna:
zona       3.43
viento     2.62
humedad    1.41
hora       1.27
dia        0.01
ruido     -0.01
```

`permutation_importance` baraja una columna en la **prueba**, deja las demás igual y mide cuánto empeora el modelo. Diez veces cada una, con la media.

- Barajar la zona sube el MAE en 3,43 puntos: el modelo la necesita. Aquí la zona es una columna, no cuatro: se baraja antes del pipeline.
- `dia` y `ruido`, alrededor de 0: barajarlas no cambia nada. El modelo no las usa para predecir medidas nuevas, aunque las usara para memorizar el entrenamiento.

Cuando quieras saber qué columnas importan, usa la permutación con datos que el modelo no vio.

Para terminar, escribe en un comentario al final de `main.py` qué columna de tu dominio crees que saldría arriba en las importancias, y cuál podría colarse como `ruido`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'forest' is not defined` en el paso 5 | `forest` es el bosque del paso 4: descoméntalo antes |
| `ValueError: Length of values ... does not match length of index` en el paso 5 | Los nombres tienen que salir del pipeline: `get_feature_names_out()`, no `x.columns` |
| `UserWarning: Some inputs do not have OOB scores` | Con muy pocos árboles, alguna medida está en todas las muestras. Con 100 no pasa |
| Tus importancias del paso 6 no coinciden | `random_state=33` en el bosque y en `permutation_importance` |
| El paso 3 tarda mucho | 300 árboles por cinco pliegues son 1500 árboles. Añade `n_jobs=-1` al bosque |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Árboles de decisión](../ejercicio-01-arboles-de-decision/README.md) | **Ejercicio 02 · Bosques aleatorios** | [Ejercicio 03 · Gradient boosting](../ejercicio-03-gradient-boosting/README.md) |
