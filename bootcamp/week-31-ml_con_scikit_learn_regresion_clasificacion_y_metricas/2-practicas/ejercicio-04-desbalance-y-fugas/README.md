# Ejercicio 04 — Desbalance y fugas

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-clasificacion-y-sus-metricas.md) y [05](../../1-teoria/05-fugas-de-datos-y-tu-primer-modelo.md)

## Objetivo

Ver cuatro formas en que una buena métrica miente, y cómo descubrirlas:

- una exactitud del 96 % sin aprender nada;
- `class_weight="balanced"` para que la clase rara cuente;
- el objetivo disfrazado de entrada;
- calcular con la prueba, en veinte repartos;
- medidas repetidas a los dos lados del reparto.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/2-practicas/ejercicio-04-desbalance-y-fugas/starter
uv run python main.py
```

```
Ejercicio 04 · Desbalance y fugas
1000 lecturas · con fallo: 3.9%
```

`readings` tiene mil lecturas de sensores con su batería (0 a 100), su temperatura y si el sensor falló poco después. Fallan 39: los fallos son **raros**. El starter reparte en entrenamiento y prueba, estratificado: 700 y 300, con 12 fallos en prueba.

`show(name, said)` escribe en una línea la exactitud, la exactitud equilibrada, y la precisión y la exhaustividad de la clase "sí" (fallo).

Tus salidas coinciden con las del README si descomentas los pasos **en orden**: el paso 6 saca números del mismo generador que los datos.

## Pasos

### 1. Una exactitud del 96 % sin aprender nada

Descomenta el **PASO 1** y ejecuta:

```
referencia   exactitud 0.960 · equilibrada 0.500 · precisión 0.00 · exhaustividad 0.00
```

La referencia dice siempre "no" y acierta 288 de 300. Un 96 % que no encuentra ni un fallo: exhaustividad 0. La exactitud equilibrada, 0,5, dice la verdad.

### 2. Un modelo que tampoco avisa

Descomenta el **PASO 2** y ejecuta:

```
logística    exactitud 0.960 · equilibrada 0.500 · precisión 0.00 · exhaustividad 0.00
probabilidad de fallo más alta en prueba: 0.14
```

La regresión logística da **exactamente** lo mismo que la referencia. Ha aprendido algo (la probabilidad de fallo cambia con la batería), pero ninguna lectura llega a 0,5: la más alta es 0,14. Con un 4 % de fallos, casi ningún caso es "más probable que falle que no", y `predict` dice siempre "no".

Mirando solo la exactitud, dirías que el modelo funciona. Mirando solo la de la referencia, que no aporta nada. Las dos lecturas son incompletas: la probabilidad tiene información, el umbral 0,5 la tira.

### 3. Pesar las clases

Descomenta el **PASO 3** y ejecuta:

```
equilibrada  exactitud 0.643 · equilibrada 0.734 · precisión 0.09 · exhaustividad 0.83
coef_ (batería, temperatura): [-0.033 -0.01 ]
```

- `class_weight="balanced"` hace que cada fallo cuente tanto como unas 25 lecturas sin fallo: las dos clases pesan lo mismo al aprender.
- Ahora encuentra 10 de los 12 fallos (exhaustividad 0,83), a cambio de muchas falsas alarmas: solo el 9 % de sus avisos son fallos. La exactitud **baja** al 64 % y la equilibrada **sube** al 73 %.
- `coef_` dice qué aprendió: cada punto de batería baja la probabilidad de fallo; la temperatura apenas pesa, porque no influye (−0,01 es ruido).

¿Es mejor modelo? Depende de lo que cueste revisar un sensor frente a que falle sin aviso. Es la decisión del umbral de la teoría 04, sección 2, hecha al entrenar.

### 4. El objetivo disfrazado

Descomenta el **PASO 4** y ejecuta:

```
nivel, con temperatura: exactitud equilibrada 0.996
nivel, sin ella: exactitud equilibrada 0.333
```

El nivel (bajo, medio, alto) sale de la temperatura con dos umbrales: 15 y 25. Con la temperatura entre las entradas, el modelo solo aprende los umbrales y acierta casi siempre. Sin ella, con la batería, que no tiene nada que ver, acierta como la referencia: 1/3.

Es la fuga del valor y el nivel en tu Observatorio (teoría 05, sección 2). Un 0,996 no es un buen modelo: es una pregunta que ya tenía la respuesta.

### 5. Calcular con la prueba

Descomenta el **PASO 5** y ejecuta. Tarda unos segundos:

```
con fuga: R² medio 0.18 · 20 de 20 repartos con R² > 0
sin fuga: R² medio -0.35 · 0 de 20 repartos con R² > 0
```

El ejemplo de la teoría 05, sección 3, repetido con veinte datos distintos: sesenta sensores, valores al azar, y como entrada la media de cada sensor.

- **Con fuga**, la media usa todas las medidas, también las de prueba: en los veinte repartos el modelo "explica" algo de un valor que es puro azar.
- **Sin fuga**, la media solo usa el entrenamiento: en ninguno. Y de media, peor que la media de todo, porque con cinco medidas por sensor la media de cada uno es casi solo ruido.

`fillna(fallback)` da la media general a los sensores que no salen en el entrenamiento: sin ella, tendrían un hueco y `predict` fallaría.

Un solo reparto con R² = 0,18 podría parecer suerte. Veinte de veinte es la fuga.

### 6. Medidas repetidas

Descomenta el **PASO 6** y ejecuta:

```
sin repetir: R² en prueba -0.821
cada una dos veces: R² en prueba 0.544
```

Trescientas medidas al azar: la hora no dice nada del valor. Con un vecino, el modelo memoriza y en prueba es mucho peor que la media.

Con **cada medida dos veces**, como pasa al cargar el mismo archivo dos veces, muchas medidas de prueba tienen su gemela en entrenamiento, y el vecino más cercano es ella: R² 0,544, en datos sin ninguna relación. Antes de repartir, busca duplicados: `frame.duplicated().sum()`.

Para terminar, escribe en un comentario al final de `main.py` cuál de estas cuatro trampas podría darse con los datos de tu dominio, y cómo la descubrirías.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus números del paso 6 no coinciden | Descomentaste en otro orden: usa el mismo generador que los datos |
| `NameError: name 'show' is not defined` | Borraste la función al descomentar: está antes del paso 1 |
| `UndefinedMetricWarning` en el paso 1 | Falta `zero_division=0` en `show`: la referencia nunca dice "sí" |
| `ConvergenceWarning` en algún paso | La logística no terminó de ajustar: `LogisticRegression(max_iter=1000)` le da más iteraciones |
| `ValueError: Input X contains NaN` en el paso 5 | Falta `fillna(fallback)`: un sensor de prueba no estaba en el entrenamiento |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Clasificar y medir](../ejercicio-03-clasificar-y-medir/README.md) | **Ejercicio 04 · Desbalance y fugas** | [Proyecto · Tu primer modelo](../../3-proyecto/README.md) |
