# Ejercicio 02 — Una CNN

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-redes-convolucionales.md)

## Objetivo

Entrenar tu primera red convolucional y compararla con un MLP:

- un MLP con los 64 píxeles en fila, la referencia;
- una CNN con dos bloques de convolución y *pooling*;
- la forma de un dígito, capa a capa;
- qué pasa con los dos si mueves el dígito un píxel;
- qué dígitos confunde la CNN;
- de las puntuaciones a las probabilidades.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-35-pytorch_cnn_entrenamiento_y_transfer_learning/2-practicas/ejercicio-02-una-cnn/starter
uv run python main.py
```

```
Ejercicio 02 · Una CNN
entrenamiento (1200, 1, 8, 8) · prueba (597, 1, 8, 8)
```

Los 1797 dígitos de `load_digits`, con los píxeles pasados de 0..16 a 0..1 y un canal: `(imágenes, 1, 8, 8)`. Repartidos al azar: 1200 para entrenar y 597 de prueba. Aquí sí se puede repartir al azar: los dígitos no son una serie.

`fit(model, x, y)` entrena 150 épocas con Adam y `CrossEntropyLoss`, con todas las imágenes a la vez. `accuracy` da la parte de imágenes cuyo número acierta: la clase con la puntuación más alta (teoría 02, sección 2).

## Pasos

### 1. Un MLP, la referencia

Descomenta el **PASO 1** y ejecuta:

```
MLP · 2410 parámetros · acierto en prueba 0.983
```

`nn.Flatten()` pone los 8 × 8 píxeles en una fila de 64, y el MLP de la semana 34, con 32 neuronas ocultas y 10 salidas, una por dígito: 65 × 32 + 33 × 10 = 2410 parámetros. Acierta el 98,3 %: los dígitos de 8 × 8 son fáciles.

### 2. Una CNN

Descomenta el **PASO 2** y ejecuta. Tarda unos segundos:

```
CNN · 1898 parámetros · acierto en prueba 0.973
```

La CNN de la teoría 02: menos parámetros, y un acierto parecido, algo menor. Con imágenes tan pequeñas y centradas, ver los píxeles en fila no es un problema. Sigue al paso 4 antes de decidir cuál es mejor.

### 3. La forma, capa a capa

Descomenta el **PASO 3** y ejecuta:

```
Conv2d     → (1, 8, 8, 8)       80 parámetros
ReLU       → (1, 8, 8, 8)        0 parámetros
MaxPool2d  → (1, 8, 4, 4)        0 parámetros
Conv2d     → (1, 16, 4, 4)    1168 parámetros
ReLU       → (1, 16, 4, 4)       0 parámetros
MaxPool2d  → (1, 16, 2, 2)       0 parámetros
Flatten    → (1, 64)             0 parámetros
Linear     → (1, 10)           650 parámetros
```

Un dígito recorre la red capa a capa. Solo las convoluciones y la lineal tienen parámetros: 80 + 1168 + 650 = 1898. Los mapas encogen (8, 4, 2) y los canales crecen (1, 8, 16). La teoría 02, sección 1, explica cada número; el diagrama de esa sección es esta tabla dibujada.

### 4. Mover el dígito un píxel

Descomenta el **PASO 4** y ejecuta:

```
desplazadas · MLP 0.451 · CNN 0.685
```

Las mismas imágenes de prueba, movidas un píxel a la derecha (`torch.roll` y una columna de ceros a la izquierda). Para una persona, el mismo número.

- El **MLP** pasa de 0,983 a 0,451: aprendió qué píxeles concretos se encienden en cada dígito, y ahora se encienden otros.
- La **CNN** baja de 0,973 a 0,685: sus filtros encuentran los trazos donde estén, y el *pooling* perdona movimientos pequeños. También baja: el borde derecho se pierde y la capa final sigue mirando posiciones.

En una foto real, el objeto nunca está en el mismo píxel. Ahí está la ventaja de la CNN, y en el ejercicio 03 la harás mayor.

### 5. Qué confunde

Descomenta el **PASO 5** y ejecuta:

```
16 errores de 597
  un 5 leído como 9: 2 veces
  un 6 leído como 1: 2 veces
  un 8 leído como 1: 2 veces
```

Los pares (real, leído) de los 16 errores, con los tres más repetidos. Es la matriz de confusión de la semana 31 contada a mano: en lugar de una cifra, dónde se equivoca. Un 5 y un 9 se parecen arriba; un 8 mal escrito tiene un trazo vertical como un 1.

### 6. Las puntuaciones y las probabilidades

Descomenta el **PASO 6** y ejecuta:

```
la primera es un 5
puntuaciones de la primera: [-10.6, -5.6, -16.1, 0.5, -10.1, 17.9, -8.2, -4.5, 0.8, 4.2]
probabilidades:             [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
la más dudosa es un 6: 0 con 0.48, 8 con 0.27
```

- La red da 10 **puntuaciones**; la del 5, 17,9, muy por encima de las demás. `softmax` las convierte en probabilidades: casi 1 para el 5.
- La imagen de prueba de la que la red está **menos segura**: un 6 al que da un 48 % de ser un 0 y un 27 % de ser un 8. Falla, pero sabe que duda. Una aplicación real podría pedir a una persona que revise las imágenes con la probabilidad más alta por debajo de 0,6.

Para terminar, escribe en un comentario al final de `main.py` qué umbral de probabilidad usarías para pedir una revisión a mano si la red leyera datos de tu dominio, y por qué.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied (1200x64 and ...)` | La última capa es `nn.Linear(16 * 2 * 2, 10)`: 64 entradas |
| `RuntimeError: expected target dtype to be Long or Byte, but got Float` | Las clases van como enteros: `torch.tensor(digits.target)`, sin `dtype=torch.float32` |
| El acierto ronda 0,1 | La red no entrena: comprueba `optimizer.zero_grad()`, `backward()` y `step()` en `fit` |
| `NameError: name 'cnn' is not defined` en el paso 3 | Los pasos usan lo de los anteriores: descomenta también el paso 2 |
| El paso 2 tarda | 150 épocas con 1200 imágenes por una CNN: unos segundos es normal |
| Tus números difieren en el tercer decimal | Otro procesador suma en otro orden: es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · La convolución](../ejercicio-01-la-convolucion/README.md) | **Ejercicio 02 · Una CNN** | [Ejercicio 03 · Entrenar de verdad](../ejercicio-03-entrenar-de-verdad/README.md) |
