# Ejercicio 01 — Tu primer modelo

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-aprender-de-los-datos.md) y [03](../../1-teoria/03-regresion-y-sus-metricas.md)

## Objetivo

Usar la interfaz de scikit-learn de principio a fin y ver qué aprende un modelo:

- `X` e `y`, y el error de pasar `X` con una dimensión;
- `fit`, `coef_` e `intercept_`, comparados con `np.polyfit`;
- `predict` y `score`;
- una regresión con dos entradas;
- una etiqueta en one-hot, y por qué el modelo predice la media de cada una;
- otro modelo, `KNeighborsRegressor`, con las mismas tres líneas.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/2-practicas/ejercicio-01-tu-primer-modelo/starter
uv run python main.py
```

```
Ejercicio 01 · Tu primer modelo
50 días, columnas: sol, nubes, temperatura
```

La primera ejecución tarda unos segundos: `uv` instala NumPy, pandas y scikit-learn en el entorno del ejercicio. `days` tiene cincuenta días con sus horas de sol, su nubosidad (de 0 a 1) y su temperatura. El comentario de arriba dice cómo se generan: así sabrás si el modelo aprende lo que debe.

## Pasos

### 1. X e y

Descomenta el **PASO 1** y ejecuta:

```
X: (50, 1) · y: (50,)
con una dimensión: Expected a 2-dimensional container but got <class 'pandas.Series'> instead
```

- `days[["sol"]]`, con **dos** corchetes, es una tabla de una columna: forma `(50, 1)`. Es `X`.
- `days["temperatura"]`, con uno, es una serie: forma `(50,)`. Es `y`.
- `days["sol"]`, con uno, también es una serie, y `fit` la rechaza como `X`: aunque haya una sola entrada, `X` tiene una fila por caso y una columna por entrada.

### 2. fit y lo aprendido

Descomenta el **PASO 2** y ejecuta:

```
fit devuelve el mismo objeto: True
coef_: [1.525] · intercept_: 9.762
np.polyfit: 1.525 · 9.762
```

- `fit` devuelve el propio estimador: por eso se puede escribir `LinearRegression().fit(x, y)` en una línea.
- El modelo aprendió `temperatura = 1,525 · sol + 9,762`. Los datos se generaron con 1,5 por hora de sol: lo ha encontrado.
- `np.polyfit(..., 1)` ajusta la misma recta por mínimos cuadrados (semana 28): mismos números.
- `intercept_` no es 12, como en la fórmula de los datos, porque la nubosidad no está entre las entradas y el modelo la "absorbe" en el término independiente. El paso 4 lo arregla.

### 3. predict y score

Descomenta el **PASO 3** y ejecuta:

```
predicciones para 0, 6 y 12 horas: [ 9.8 18.9 28.1]
a mano, 6 horas: 18.9
R² en los mismos días: 0.892
```

- `predict` recibe una tabla con **las mismas columnas** que en `fit` (`sol`) y devuelve una predicción por fila.
- A mano, `intercept_ + coef_[0] · 6`: lo mismo. Un modelo lineal es solo esa cuenta.
- `score` da el R² (teoría 03). Aquí se mide con los mismos días con los que aprendió: es optimista, y el ejercicio 02 lo corrige.

### 4. Varias entradas

Descomenta el **PASO 4** y ejecuta:

```
entradas: ['sol', 'nubes'] · coef_: [ 1.52 -4.2 ]
intercept_: 12.08
R² con sol y nubes: 0.929
```

- `feature_names_in_` guarda los nombres de las columnas de `X`, en el orden de `coef_`.
- Con la nubosidad, el modelo encuentra los tres números de la fórmula: 1,5 por hora de sol, −4 con el cielo cubierto y 12 de base. Lo que falta hasta los valores exactos es el ruido.
- El R² sube de 0,892 a 0,929: la nubosidad explica parte de lo que antes era "error".

### 5. Una etiqueta, en one-hot

Descomenta el **PASO 5** y ejecuta:

```
   Centro  Norte  Sur
0     0.0    1.0  0.0
1     0.0    0.0  1.0
2     0.0    1.0  0.0
predice: {'Norte': 12.0, 'Sur': 32.0, 'Centro': 50.0}
medias:  {'Centro': 50.0, 'Norte': 12.0, 'Sur': 32.0}
```

- `pd.get_dummies` crea una columna por zona, en orden alfabético, con un 1 en la de cada fila.
- Con solo la zona como entrada, la regresión lineal predice **la media de cada zona**: lo mejor que puede hacer si no sabe nada más. Es la base del comando `modelo` de tu proyecto.

Prueba a numerar las zonas en vez de usar one-hot: cambia `onehot` por `zones["zona"].map({"Norte": 1, "Centro": 2, "Sur": 3}).to_frame()` y ejecuta:

```
predice: {'Norte': 19.0, 'Sur': 39.0, 'Centro': 29.0}
```

Ya no son las medias: el modelo busca una recta que pase por "1", "2" y "3", como si el Centro estuviera entre el Norte y el Sur, y se equivoca en las tres. Deshaz el cambio.

### 6. Otro modelo, la misma interfaz

Descomenta el **PASO 6** y ejecuta:

```
5 vecinos, para 0, 6 y 12 horas: [ 8.8 18.7 28.2]
R² de 5 vecinos: 0.924
R² de 1 vecino: 0.977
```

- `KNeighborsRegressor(n_neighbors=5)` predice la media de los 5 días con las horas de sol más parecidas. No tiene `coef_`: no hay fórmula que leer.
- Cambiar de modelo es cambiar la línea que lo crea: `fit`, `predict` y `score` son iguales.
- Con **1** vecino, el R² en los mismos días sube a 0,977: cada día es su propio vecino más cercano y se "predice" a sí mismo. No llega a 1 porque hay días con las mismas horas de sol y distinta temperatura. ¿Es mejor modelo? Con estos números no se puede saber: falta medirlo con días que no vio. Es el ejercicio 02.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Ejecuta con `uv run`, desde la carpeta `starter` |
| `NameError: name 'x' is not defined` | Descomenta antes el paso 1 |
| `NameError: name 'model' is not defined` en el paso 3 | Descomenta antes el paso 2 |
| `NameError: name 'new' is not defined` en el paso 6 | Descomenta antes el paso 3 |
| `UserWarning: X does not have valid feature names` | Pasaste a `predict` una lista o un array, y `fit` recibió una tabla: usa un `DataFrame` con las mismas columnas |
| `IndentationError` | Al descomentar, quita solo `# ` del principio y mantén los espacios de dentro |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Fugas de datos y tu primer modelo](../../1-teoria/05-fugas-de-datos-y-tu-primer-modelo.md) | **Ejercicio 01 · Tu primer modelo** | [Ejercicio 02 · Entrenar, probar y la referencia](../ejercicio-02-entrenar-probar-y-la-referencia/README.md) |
