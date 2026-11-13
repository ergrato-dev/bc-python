# Ejercicio 01 — Preparar las entradas

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-preparar-las-entradas.md) y [02](../../1-teoria/02-pipelines.md)

## Objetivo

Convertir columnas en *features* con los transformadores de scikit-learn:

- mirar los datos: tipos y huecos;
- derivar la hora, el fin de semana y la hora punta de una fecha;
- escalar con `StandardScaler`, ajustado con el entrenamiento;
- codificar con `OneHotEncoder` y una zona que no vio;
- rellenar con `SimpleImputer` y marcar lo que faltaba;
- todo junto, cada columna a su manera, con `ColumnTransformer`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-32-features_pipelines_validacion_cruzada_y_tuning/2-practicas/ejercicio-01-preparar-las-entradas/starter
uv run python main.py
```

```
Ejercicio 01 · Preparar las entradas
1200 medidas · de 05/01 a 31/10
```

`air` tiene 1200 medidas horarias de partículas finas (PM2.5) en cuatro zonas. El comentario de arriba dice cómo se generan: más en hora punta y entre semana, menos con humedad alta. Los ejercicios 02, 03 y 04 usan los mismos datos.

## Pasos

### 1. Mirar los datos

Descomenta el **PASO 1** y ejecuta:

```
              momento    zona  humedad  pm25
0 2026-01-05 10:00:00     Sur     61.0   7.4
1 2026-01-05 18:00:00    Este     44.0  26.9
2 2026-01-06 03:00:00  Centro     83.0  15.5
huecos: {'momento': 0, 'zona': 0, 'humedad': 95, 'pm25': 0}
```

Cuatro columnas y ninguna lista para un modelo: una fecha, un texto, un número con 95 huecos y el objetivo. Antes de preparar nada, mira siempre qué tienes.

### 2. Derivar entradas de la fecha

Descomenta el **PASO 2** y ejecuta:

```
PM2.5 medio, fuera y en hora punta: [12.1, 20.3]
PM2.5 medio, entre semana y en finde: [15.4, 11.1]
```

- `momento` tal cual no dice nada; la hora, el fin de semana y la hora punta, sí. Ocho puntos más en hora punta, cuatro menos en fin de semana: es justo lo que dice el generador.
- `punta` es una entrada de **tu** conocimiento del dominio: el modelo no sabría que las 8 y las 19 se parecen y las 13 no. Con `hora` sola, una regresión lineal solo puede subir o bajar con la hora.
- `astype(int)`: `True` y `False` como 1 y 0.

### 3. Escalar con el entrenamiento

Descomenta el **PASO 3** y ejecuta:

```
media 11.58 · desviación 7.04
la hora de prueba, escalada: de -1.65 a 1.62
```

- Se reparte **antes** de preparar: el escalador aprende la media y la desviación **solo** del entrenamiento.
- La prueba se escala con esos números. Las horas van de 0 a 23, así que la prueba queda dentro del mismo intervalo que el entrenamiento.

### 4. Codificar la zona

Descomenta el **PASO 4** y ejecuta:

```
zonas aprendidas: ['Centro', 'Este', 'Norte', 'Sur']
[[0. 0. 0. 1.]
 [0. 0. 0. 0.]]
```

El codificador aprende las cuatro zonas, en orden alfabético. Sur es la cuarta columna. Puerto no estaba: con `handle_unknown="ignore"`, fila de ceros.

Quita `handle_unknown="ignore"` y ejecuta: `ValueError: Found unknown categories ['Puerto'] in column 0 during transform`. Vuelve a ponerlo.

### 5. Rellenar la humedad

Descomenta el **PASO 5** y ejecuta:

```
mediana del entrenamiento: 63.0
['humedad' 'missingindicator_humedad']
[[63.  1.]
 [35.  0.]]
```

- La primera fila no tenía humedad: recibe la mediana del entrenamiento, 63, y un 1 en la columna nueva.
- La segunda sí: se queda con su 35 y un 0.
- `add_indicator=True` añade esa columna: el modelo puede aprender si "faltaba la humedad" dice algo. Aquí faltan al azar, así que no dirá nada; en tu dominio, quizá sí.

### 6. Todo junto, columna a columna

Descomenta el **PASO 6** y ejecuta:

```
la prueba, preparada: 300 filas × 9 columnas
  zona__zona_Centro
  zona__zona_Este
  zona__zona_Norte
  zona__zona_Sur
  humedad__humedad
  humedad__missingindicator_humedad
  hora__hora
  tal_cual__finde
  tal_cual__punta
```

- Un transformador por grupo de columnas, cada uno con su nombre. `"passthrough"` deja las columnas tal cual: ya son 0 y 1.
- `momento` y `pm25` no salen: el `ColumnTransformer` descarta lo que no nombra.
- Los nombres de salida son `grupo__columna`: así sabrás qué coeficiente es de qué (ejercicio 02).

Para terminar, escribe en un comentario al final de `main.py` qué entradas derivarías en tu dominio (de una fecha, de un cociente, de un umbral) y cuál de ellas podría ser una fuga.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'train' is not defined` en el paso 4 | El reparto está en el paso 3: descoméntalo antes |
| `KeyError: 'hora'` en el paso 3 o 6 | Falta el paso 2: crea las columnas derivadas |
| `ValueError: Found unknown categories` | Falta `handle_unknown="ignore"` en el `OneHotEncoder` |
| `ValueError: Input X contains NaN` | Un escalador o un modelo recibió la humedad sin rellenar: pasa antes por `SimpleImputer` |
| La salida del paso 4 es `<Compressed Sparse Row ...>` | Falta `sparse_output=False` |
| `Expected a 2-dimensional container but got <class 'pandas.Series'> instead` | `train["hora"]` con un corchete: los transformadores quieren `train[["hora"]]` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Validación anidada y tu modelo ajustado](../../1-teoria/05-validacion-anidada-y-tu-modelo-ajustado.md) | **Ejercicio 01 · Preparar las entradas** | [Ejercicio 02 · Pipelines sin fugas](../ejercicio-02-pipelines-sin-fugas/README.md) |
