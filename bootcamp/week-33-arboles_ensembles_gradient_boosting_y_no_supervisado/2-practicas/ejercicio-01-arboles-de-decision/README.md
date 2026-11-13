# Ejercicio 01 — Árboles de decisión

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-arboles-de-decision.md)

## Objetivo

Entrenar un árbol de decisión, leerlo y ver dónde acierta y dónde no:

- un árbol de dos niveles, escrito como preguntas de sí o no;
- sus predicciones, en escalones;
- la profundidad: dónde no aprende y dónde memoriza;
- un árbol frente a una recta, con datos que tienen umbrales;
- por qué a un árbol no le hace falta escalar;
- qué hace un árbol fuera de lo que vio.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/2-practicas/ejercicio-01-arboles-de-decision/starter
uv run python main.py
```

```
Ejercicio 01 · Árboles de decisión
1500 medidas · de 05/01 a 31/10
```

Medidas horarias de PM2.5 en cuatro zonas, como en la semana 32, pero ahora con **umbrales y cruces**: sube con el aire en calma (viento por debajo de 2 m/s), baja con lluvia (humedad por encima de 85 %), y la hora punta sube mucho más en el Centro que en las demás zonas. `x` tiene la hora, el día de la semana, la zona, la humedad y el viento. `tree(depth)` da un pipeline con la zona en one-hot y el resto **sin escalar**, delante de un `DecisionTreeRegressor`.

## Pasos

### 1. Un árbol de dos niveles

Descomenta el **PASO 1** y ejecuta:

```
|--- viento <= 1.9
|   |--- zona_Centro <= 0.5
|   |   |--- value: [25.0]
|   |--- zona_Centro >  0.5
|   |   |--- value: [35.0]
|--- viento >  1.9
|   |--- zona_Centro <= 0.5
|   |   |--- value: [15.0]
|   |--- zona_Centro >  0.5
|   |   |--- value: [24.1]
```

- `export_text` escribe el árbol como preguntas. La primera, la que más reduce el error: ¿el viento es de 1,9 o menos? Encontró sola el umbral de la calma, que en los datos está en 2.
- La segunda pregunta, en las dos ramas: ¿es el Centro? `zona_Centro <= 0.5` es "no es el Centro": la columna one-hot vale 0 o 1.
- Cada hoja predice la **media** de las medidas de entrenamiento que llegan a ella: 35,0 para el Centro en calma, 15,0 para las otras zonas con viento.

### 2. Predice en escalones

Descomenta el **PASO 2** y ejecuta:

```
20 vientos de 0 a 9.5 m/s · 2 predicciones distintas:
[15. 25.]
```

Veinte vientos distintos, para la misma hora, el mismo día y la misma zona (Norte): solo **dos** predicciones, las de las dos hojas a las que se puede llegar sin ser el Centro. Un árbol no dibuja una curva: dibuja escalones, uno por hoja. Con dos niveles, cuatro hojas como mucho.

### 3. La profundidad

Descomenta el **PASO 3** y ejecuta. Tarda unos segundos:

```
max_depth=1     MAE entrenamiento  5.49 · validación  5.50
max_depth=2     MAE entrenamiento  4.70 · validación  4.80
max_depth=4     MAE entrenamiento  3.29 · validación  3.47
max_depth=6     MAE entrenamiento  2.51 · validación  2.96
max_depth=10    MAE entrenamiento  1.14 · validación  3.35
max_depth=None  MAE entrenamiento  0.00 · validación  3.68
```

- Con **pocos** niveles, los dos errores altos y parecidos: el árbol no tiene preguntas suficientes. No aprende.
- Con `max_depth=None`, sin límite, sigue preguntando hasta que cada hoja tiene una sola medida: error 0 en entrenamiento. En validación, 3,68: ha memorizado el ruido.
- El mejor, alrededor de 6. `max_depth` es el hiperparámetro que más pesa en un árbol: la curva de validación de la semana 32, otra vez.

### 4. Un árbol frente a una recta

Descomenta el **PASO 4** y ejecuta:

```
recta               MAE [4.73 4.94 5.21 5.08 4.63] · media 4.92
árbol, max_depth=6  MAE [2.96 3.   2.91 3.08 2.84] · media 2.96
```

Los mismos pliegues para los dos. El árbol gana en los cinco, por casi dos puntos:

- la recta da un peso a la hora: más hora, más PM2.5, o menos. Pero la hora punta son las 7, 8 y 9, y las 18, 19 y 20: no hay recta que lo diga;
- y la recta suma efectos: no sabe que la hora punta sube más **en el Centro**. Un árbol pregunta primero por la zona y después por la hora, y el cruce sale solo.

Con la recta, tendrías que crear tú las entradas: `es_hora_punta`, `centro_y_punta`… (semana 32, teoría 01). El árbol las encuentra.

### 5. Al árbol no le importa la escala

Descomenta el **PASO 5** y ejecuta:

```
árbol: ¿las mismas predicciones? True
recta: ¿las mismas predicciones? False
```

`squeezed` cambia dos columnas: el viento, por su logaritmo; la humedad, dividida por 100. El árbol pregunta "¿viento ≤ 1,9?" o "¿log(1 + viento) ≤ 1,08?": separa las **mismas** medidas, y predice lo mismo. Solo le importa el **orden** de los valores. A la recta le cambia todo: el logaritmo dobla la relación.

Por eso `tree()` no escala: no sobra, pero no cambia nada. Y por eso tampoco hace falta escalar antes de un bosque o un boosting, que son muchos árboles.

### 6. Un árbol no extrapola

Descomenta el **PASO 6** y ejecuta:

```
árbol: días 45, 50 y 59 → [39.5 39.5 39.5]
recta: días 45, 50 y 59 → [42.5 45.  49.5]
de verdad: [42.5 45.  49.5]
```

Una tendencia sin ruido: medio punto más cada día. Los dos modelos entrenan con los días 0 a 39 y predicen los días 45, 50 y 59.

- La **recta** sigue la línea: acierta.
- El **árbol** da 39,5 a los tres: la media de su última hoja, la del día 39. Ninguna pregunta del árbol separa "más de 39" de "mucho más de 39": no vio nada ahí.

Con `--tiempo`, en el proyecto, el último pliegue tiene posiciones que el entrenamiento nunca vio: el árbol cae en su última hoja (proyecto, paso 5).

Para terminar, escribe en un comentario al final de `main.py` qué umbral o qué cruce esperas en tu dominio que un árbol encontraría y una recta no.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'small' is not defined` en el paso 2 | El paso 2 usa el árbol del paso 1: descoméntalo antes |
| `NameError: name 'line' is not defined` en el paso 5 | `line` es la recta del paso 4 |
| `ValueError: could not convert string to float: 'Centro'` | Entrenas el árbol sin el pipeline: la zona tiene que pasar por el `OneHotEncoder` |
| Tus números del paso 3 no coinciden | `random_state=33` en el árbol y en `KFold`: con empates entre preguntas, el árbol elige al azar |
| El árbol de `export_text` sale con `feature_0`, `feature_1`… | Falta `feature_names=names` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · PCA, y tus modelos y grupos](../../1-teoria/05-pca-y-tus-modelos-y-grupos.md) | **Ejercicio 01 · Árboles de decisión** | [Ejercicio 02 · Bosques aleatorios](../ejercicio-02-bosques-aleatorios/README.md) |
