# Ejercicio 03 — Clasificar y medir

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-clasificacion-y-sus-metricas.md)

## Objetivo

Entrenar una regresión logística y leer todo lo que dice:

- las probabilidades de `predict_proba` y el umbral de `predict`;
- la matriz de confusión, casilla a casilla;
- exactitud, precisión, exhaustividad y F1, a mano y con scikit-learn;
- qué pasa al mover el umbral;
- la referencia y la exactitud equilibrada;
- tres clases y `classification_report`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/2-practicas/ejercicio-03-clasificar-y-medir/starter
uv run python main.py
```

```
Ejercicio 03 · Clasificar y medir
400 días · con aviso: 30%
```

`days` tiene cuatrocientos días con su temperatura máxima, su humedad y si hubo aviso por calor. El aviso es más probable con calor y humedad, pero no es seguro: ningún modelo puede acertar todos. El starter ya reparte en entrenamiento y prueba, estratificado por el aviso: 300 y 100 días.

Tus salidas coinciden con las del README si descomentas los pasos **en orden**: el paso 6 saca números del mismo generador que los datos.

## Pasos

### 1. Probabilidades

Descomenta el **PASO 1** y ejecuta:

```
classes_: ['no', 'sí']
     temperatura  humedad  p_no  p_si
303         29.8     67.0  0.73  0.27
247         21.4     52.0  1.00  0.00
19          36.1     35.0  0.31  0.69
cada fila suma 1: True
predict es 'sí' desde 0,5: True
```

- `classes_` da el orden de las columnas de `predict_proba`: la segunda es la de "sí".
- A 21 grados, la probabilidad de aviso es 0,00 (redondeada); a 36, 0,69. Con dos entradas, la logística combina las dos.
- `predict` dice "sí" exactamente cuando la probabilidad de "sí" llega a 0,5.

### 2. La matriz de confusión

Descomenta el **PASO 2** y ejecuta:

```
[[26  4]
 [ 2 68]]
VP 26 · FN 4 · FP 2 · VN 68
```

- Con `labels=["sí", "no"]`, la primera fila y la primera columna son "sí", la clase que importa.
- 30 días de prueba tuvieron aviso: el modelo encontró 26 y se le escaparon 4. Dio 2 falsas alarmas entre 70 días sin aviso.
- `(tp, fn), (fp, tn) = matrix` desempaqueta las dos filas. Cambia `labels` a `["no", "sí"]` y ejecuta: la matriz se da la vuelta y los nombres quedan mal. Deshaz el cambio.

### 3. Exactitud, precisión, exhaustividad y F1

Descomenta el **PASO 3** y ejecuta:

```
exactitud     a mano 0.940 · 0.940
precisión     a mano 0.929 · 0.929
exhaustividad a mano 0.867 · 0.867
F1            a mano 0.897 · 0.897
```

Con los números del paso 2: (26 + 68) / 100; 26 / 28; 26 / 30; y la media armónica de las dos. `pos_label="sí"` dice cuál es la clase positiva: sin él, scikit-learn no sabe si "sí" o "no", y falla.

### 4. Mover el umbral

Descomenta el **PASO 4** y ejecuta:

```
umbral  avisos  precisión  exhaustividad
   0.2      41       0.68           0.93
  0.35      32       0.84           0.90
   0.5      28       0.93           0.87
  0.65      26       0.92           0.80
   0.8      22       0.95           0.70
```

- Con el umbral bajo, el modelo avisa más (41 veces): encuentra el 93 % de los días con aviso, pero una de cada tres alarmas es falsa.
- Con el umbral alto, avisa menos (22): casi nunca se equivoca al avisar, pero se le escapa el 30 %.
- La precisión no siempre sube: de 0,5 a 0,65 baja un poco, de 0,93 a 0,92, porque con pocos casos cada día cuenta mucho.

¿Qué umbral elegirías si un aviso que falta costara diez veces más que una falsa alarma? Escríbelo en un comentario al final de `main.py`.

### 5. La referencia y la exactitud equilibrada

Descomenta el **PASO 5** y ejecuta:

```
modelo     exactitud 0.940 · equilibrada 0.919
referencia exactitud 0.700 · equilibrada 0.500
```

- La referencia dice siempre "no": acierta los 70 días sin aviso, el 70 %, sin aprender nada.
- Su exactitud equilibrada es 0,5: acierta toda la clase "no" y nada de la "sí", (1 + 0) / 2.
- El modelo mejora las dos. Con un 70 % gratis, un modelo con exactitud 0,75 apenas aportaría; la equilibrada lo deja claro.

### 6. Tres clases

Descomenta el **PASO 6** y ejecuta:

```
              precision    recall  f1-score   support

    amarillo       0.90      0.53      0.67        34
        rojo       0.42      1.00      0.59         5
       verde       0.87      0.97      0.91        61

    accuracy                           0.82       100
   macro avg       0.73      0.83      0.72       100
weighted avg       0.86      0.82      0.81       100
```

Ahora el aviso tiene tres colores. `LogisticRegression` los aprende sin cambiar nada: una probabilidad por clase.

- **Rojo**, con solo 5 días en prueba, tiene exhaustividad 1,00 (los encuentra todos) y precisión 0,42 (más de la mitad de sus rojos eran amarillos).
- **Amarillo** se confunde con los otros dos: solo encuentra la mitad.
- **`macro avg`** pesa igual las tres clases: el F1 malo de rojo y amarillo lo baja a 0,72. **`weighted avg`** pesa por `support`, y verde, la clase más frecuente y la más fácil, lo sube a 0,81. Si te importa el rojo, mira la macro.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus números del paso 6 no coinciden | Descomentaste en otro orden: los datos de los colores usan el mismo generador |
| `ValueError: pos_label=1 is not a valid label` | Falta `pos_label="sí"` |
| `NameError: name 'probabilities' is not defined` | Descomenta antes el paso 1 |
| `NameError: name 'tp' is not defined` en el paso 3 | Descomenta antes el paso 2 |
| `UndefinedMetricWarning` | Un umbral con el que el modelo no dice nunca "sí": `zero_division=0` lo silencia y da 0 |
| La tabla del paso 4 sale descolocada | Los `:>6` y `:>9.2f` alinean las columnas: no los quites |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Entrenar, probar y la referencia](../ejercicio-02-entrenar-probar-y-la-referencia/README.md) | **Ejercicio 03 · Clasificar y medir** | [Ejercicio 04 · Desbalance y fugas](../ejercicio-04-desbalance-y-fugas/README.md) |
