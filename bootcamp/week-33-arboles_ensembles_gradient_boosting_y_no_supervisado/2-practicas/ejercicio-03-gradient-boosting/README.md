# Ejercicio 03 — Gradient boosting

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-gradient-boosting.md)

## Objetivo

Construir un modelo árbol a árbol, cada uno corrigiendo los errores de los anteriores:

- el error en entrenamiento y en prueba, árbol a árbol;
- el ritmo de aprendizaje (`learning_rate`);
- parar a tiempo, sin decir cuántos árboles;
- categorías y huecos sin preparar, con `HistGradientBoostingRegressor`;
- cinco modelos con los mismos pliegues, como `competir`;
- clasificar las pocas horas de aire malo.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/2-practicas/ejercicio-03-gradient-boosting/starter
uv run python main.py
```

```
Ejercicio 03 · Gradient boosting
1500 medidas · de 05/01 a 31/10
```

Los datos del ejercicio 01, un reparto fijo (`train_x`, `test_x`…) y `pipe(model, scale)`: la zona en one-hot y el resto tal cual, o escalado si `scale=True`, para los modelos lineales.

## Pasos

### 1. Árbol a árbol

Descomenta el **PASO 1** y ejecuta:

```
  1 árboles: MAE entrenamiento 6.20 · prueba 6.02
 10 árboles: MAE entrenamiento 4.02 · prueba 3.81
 50 árboles: MAE entrenamiento 2.37 · prueba 2.48
100 árboles: MAE entrenamiento 2.13 · prueba 2.49
300 árboles: MAE entrenamiento 1.76 · prueba 2.61
```

`GradientBoostingRegressor` entrena 300 árboles pequeños (`max_depth=3`), uno detrás de otro: cada uno aprende **lo que les falta** a los anteriores, el residuo. `staged_predict` da la predicción después de cada árbol.

- Con un árbol, poco mejor que la media. Con cincuenta, ya cerca del mejor.
- En entrenamiento, el error baja **siempre**: cada árbol corrige un poco más.
- En prueba, baja hasta unos 50 a 100 árboles y después **sube**: los últimos árboles corrigen el ruido. Un bosque no sobreajusta por tener más árboles; un boosting, sí.

### 2. El ritmo de aprendizaje

Descomenta el **PASO 2** y ejecuta. Tarda unos segundos:

```
learning_rate=1.0  · 100 árboles · MAE 3.02
learning_rate=0.3  · 100 árboles · MAE 2.59
learning_rate=0.1  · 100 árboles · MAE 2.46
learning_rate=0.03 · 100 árboles · MAE 2.85
```

`learning_rate` dice qué parte de su corrección añade cada árbol.

- Con **1,0**, cada árbol corrige todo lo que puede: persigue el ruido desde el principio.
- Con **0,03**, cada árbol corrige un 3 %: con 100 árboles no le da tiempo a aprender.
- `learning_rate` y el número de árboles van juntos: si bajas uno, sube el otro. 0,1 es el valor por defecto, y suele ser un buen comienzo.

### 3. Parar a tiempo

Descomenta el **PASO 3** y ejecuta:

```
de 1000 árboles posibles usa 53 · MAE prueba 2.64
```

`early_stopping=True` aparta un 20 % del entrenamiento (`validation_fraction`) y, después de cada árbol, mide con él. Si en 10 árboles seguidos (`n_iter_no_change`) no mejora, para. `n_iter_` dice cuántos usó: 53 de los 1000 permitidos.

Así no tienes que elegir el número de árboles: lo elige con una validación interna. `HistGradientBoostingRegressor` lo hace solo a partir de 10 000 medidas (`early_stopping="auto"`); aquí lo forzamos.

### 4. Categorías y huecos, sin preparar

Descomenta el **PASO 4** y ejecuta:

```
zona como categoría y un 10 % de humedad sin dato: MAE 2.78
```

Sin pipeline:

- `categorical_features="from_dtype"` trata como categorías las columnas de tipo `category` de pandas: la zona, sin one-hot. Un corte puede separar {Centro, Este} de {Norte, Sur} de una vez.
- Los `NaN` de la humedad no dan error: en cada corte, el modelo aprende hacia qué lado mandar las medidas sin dato.

El MAE sube un poco respecto al paso 5 (2,67): le has quitado un 10 % de la humedad, y con ella el umbral de la lluvia.

### 5. Cinco modelos, los mismos pliegues

Descomenta el **PASO 5** y ejecuta. Tarda unos segundos:

```
referencia MAE [6.42 6.38 7.2  6.76 6.21] · media 6.60
lineal     MAE [4.73 4.94 5.21 5.08 4.63] · media 4.92
árbol      MAE [2.96 3.   2.91 3.08 2.84] · media 2.96
bosque     MAE [2.74 2.74 2.99 2.87 2.74] · media 2.82
boosting   MAE [2.57 2.61 2.63 2.98 2.58] · media 2.67
```

Lo que hace `competir` en tu proyecto, a mano. Con estos datos, cada modelo gana al anterior en casi todos los pliegues: el bosque pierde con el árbol en el tercero, y el boosting con el bosque en el cuarto. Por eso se mira la media **y** los pliegues. Con datos que tienen umbrales y cruces, los árboles ganan; entre ellos, el boosting suele ganar en datos de tabla como estos.

### 6. Clasificar las horas de aire malo

Descomenta el **PASO 6** y ejecuta:

```
5% de las horas, PM2.5 por encima de 35
referencia exactitud equilibrada 0.500
logística  exactitud equilibrada 0.499
boosting   exactitud equilibrada 0.850
```

Solo un 5 % de las horas pasan de 35: la clase rara de la semana 31.

- La **referencia** predice siempre "no": exactitud equilibrada 0,5.
- La **logística** tampoco encuentra esas horas: llegar a 35 pide **juntar** varias cosas (el Centro, la hora punta y la calma). Una suma de efectos con pesos no llega al umbral: en los cinco pliegues, la logística marca como malas 2 horas, de las 80 que lo son.
- El **boosting** pregunta por las tres cosas una detrás de otra: 0,850.

Para terminar, escribe en un comentario al final de `main.py` qué `learning_rate` y cuántos árboles probarías primero en tu dominio, y por qué usarías `early_stopping`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ValueError: could not convert string to float: 'Centro'` en el paso 4 | Falta `astype({"zona": "category"})`, o `categorical_features="from_dtype"` |
| `AttributeError: ... has no attribute 'n_iter_'` | Lees `n_iter_` antes de `fit`, o del pipeline: está en `named_steps["model"]` |
| `ValueError: Input X contains NaN` con `GradientBoostingRegressor` | El boosting clásico no admite huecos: usa `HistGradientBoostingRegressor` |
| Tus números del paso 1 no coinciden | `random_state=33` en el modelo y en `train_test_split` |
| El paso 2 tarda mucho | Son 4 modelos de 100 árboles por cinco pliegues: es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Bosques aleatorios](../ejercicio-02-bosques-aleatorios/README.md) | **Ejercicio 03 · Gradient boosting** | [Ejercicio 04 · Agrupar y reducir](../ejercicio-04-agrupar-y-reducir/README.md) |
