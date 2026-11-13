# Ejercicio 01 — La convolución

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-la-convolucion.md)

## Objetivo

Ver qué hace una convolución antes de meterla en una red:

- un filtro que se desliza sobre un día de PM2.5, a mano y con `F.conv1d`;
- un filtro que detecta subidas;
- cómo cambian la salida el relleno y el paso;
- dos filtros que encuentran los bordes de un dígito escrito a mano;
- una capa `nn.Conv2d`: sus filtros, sus parámetros y `MaxPool2d`;
- por qué una convolución no crece con la imagen y una capa lineal sí.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-35-pytorch_cnn_entrenamiento_y_transfer_learning/2-practicas/ejercicio-01-la-convolucion/starter
uv run python main.py
```

```
Ejercicio 01 · La convolución
un día: (24,) valores
```

La primera vez, uv instala PyTorch (solo CPU, como en la semana 34), NumPy y scikit-learn: tarda un poco. scikit-learn se usa solo por `load_digits`, 1797 dígitos de 8 × 8 píxeles escritos a mano que vienen dentro del paquete, sin descargar nada.

## Pasos

### 1. Un filtro que se desliza

Descomenta el **PASO 1** y ejecuta:

```
a mano:  (22,) · [11.0, 10.3, 10.3, 11.7, 15.7]
conv1d:  (1, 1, 22) · [11.0, 10.3, 10.3, 11.7, 15.7]
¿iguales? True
```

- A mano: cada salida es la suma de tres horas seguidas por `[1/3, 1/3, 1/3]`, la media móvil de tres horas. La primera, (12 + 11 + 10) / 3 = 11.
- `F.conv1d` hace lo mismo, con la serie como `(lotes, canales, longitud)` = `(1, 1, 24)` y el filtro como `(salidas, entradas, tamaño)` = `(1, 1, 3)`.
- 24 horas y un filtro de 3: 22 salidas. Las dos últimas horas no pueden ser el principio de un trío.

### 2. Un filtro que detecta subidas

Descomenta el **PASO 2** y ejecuta:

```
subidas: [-2.0, -1.0, 1.0, 4.0, 11.0, 21.0, 19.0, -2.0, -16.0, -13.0, -7.0, -3.0, 0.0, 4.0, 9.0, 15.0, 12.0, -5.0, -15.0, -12.0, -9.0, -6.0]
sube más a las 6 h · baja más a las 9 h
```

`[-1, 0, 1]` da, en cada hora, la siguiente menos la anterior. La mayor subida, 21, es de las 5 a las 7 (de 14 a 35): el tráfico de la mañana. La mayor bajada, −16, de las 8 a las 10. Por la tarde, otra subida (15) y otra bajada (−15).

Cambia el filtro por `[1.0, -2.0, 1.0]`: da valores grandes y negativos en los picos (sube y luego baja). ¿En qué horas?

### 3. Relleno y paso

Descomenta el **PASO 3** y ejecuta:

```
padding=0 stride=1: 22 valores
padding=1 stride=1: 24 valores
padding=0 stride=2: 11 valores
padding=1 stride=3: 8 valores
```

Comprueba cada línea con la fórmula de la teoría 01, `(n + 2p − k) // s + 1`. Con `padding=1`, un cero a cada lado, y la salida mide lo mismo que la entrada: lo que usan las CNN para que el tamaño solo lo cambie el *pooling*.

### 4. En dos dimensiones

Descomenta el **PASO 4** y ejecuta:

```
. . . # # . . .
. . # # # # . .
. . # . . # # .
. . # . . # # .
. . # . . # # .
. . # . . # . .
. . # . # # . .
. . . # # . . .
bordes: (1, 2, 6, 6)
verticales:
# # . . . -
# . - . . -
# . - # # -
# . - # # -
# . - # . -
# . . . . -
horizontales:
. . . . . #
. . - - . .
. . . . . .
. . . . . .
. . # # . .
. . # . . -
```

- El primer dígito de `load_digits`: un 0.
- Dos filtros de 3 × 3 a la vez: `vertical` resta la columna izquierda de la derecha, y `horizontal` es el mismo girado. Van juntos en un tensor `(2, 1, 3, 3)`: 2 filtros, 1 canal de entrada. La salida tiene 2 canales, uno por filtro, de 6 × 6.
- `#` es una respuesta muy positiva; `-`, muy negativa. El filtro vertical marca el lado izquierdo del 0 (de blanco a negro) con `#` y el derecho (de negro a blanco) con `-`. El horizontal marca la parte de arriba y la de abajo.

Una CNN aprende filtros como estos, y muchos más, sin que nadie se los escriba.

### 5. Una capa: muchos filtros que aprende sola

Descomenta el **PASO 5** y ejecuta:

```
filtros: (8, 1, 3, 3) · sesgos: (8,)
parámetros: 80
mapas: (1, 8, 8, 8) · tras MaxPool2d(2): (1, 8, 4, 4)
```

`nn.Conv2d(1, 8, kernel_size=3, padding=1)` crea 8 filtros de 3 × 3 al azar y 8 sesgos: 80 parámetros. Cada filtro da un mapa de 8 × 8 (gracias a `padding=1`), y `MaxPool2d(2)` deja el máximo de cada cuadrado de 2 × 2: mapas de 4 × 4, sin parámetros.

### 6. Los mismos pesos en todas partes

Descomenta el **PASO 6** y ejecuta:

```
  8 x 8   · conv: (8, 8, 8), 80 parámetros · lineal: 4160 parámetros
 28 x 28  · conv: (8, 28, 28), 80 parámetros · lineal: 615440 parámetros
224 x 224 · conv: (8, 224, 224), 80 parámetros · lineal: 2517681152 parámetros
```

La **misma** capa de 80 parámetros funciona con imágenes de cualquier tamaño: sus filtros se deslizan, y la salida crece con la imagen. Una capa lineal que diera una salida por píxel necesita un peso por cada par de píxeles: con una foto de 224 × 224, más de 2500 millones, unos 10 GB en `float32`. Por eso el paso no la crea: la calcula.

Para terminar, escribe en un comentario al final de `main.py` qué filtro de tres valores usarías para detectar en tu dominio un salto brusco, y si te interesaría más la subida, la bajada o las dos.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `RuntimeError: Expected 2D (unbatched) or 3D (batched) input to conv1d` | La serie va con forma `(1, 1, 24)`: `day.reshape(1, 1, -1)` |
| `RuntimeError: ... Kernel size can't be greater than actual input size` | El filtro es más largo que la serie (o que la imagen tras el *pooling*) |
| `RuntimeError: Given groups=1, weight of size [2, 1, 3, 3], expected input[...] to have 1 channels` | La imagen va como `(1, 1, 8, 8)`: lote, canal, alto y ancho |
| Los `#` y `-` del paso 4 salen al revés | Restaste al revés: `[[-1, 0, 1]]` marca con `#` el paso de blanco a negro hacia la derecha |
| La primera ejecución tarda mucho | uv descarga PyTorch (unos 200 MB): solo la primera vez |
| Tus números difieren en el último decimal | Otro procesador suma en otro orden: es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Pronosticar en tu Observatorio](../../1-teoria/05-pronosticar-en-tu-observatorio.md) | **Ejercicio 01 · La convolución** | [Ejercicio 02 · Una CNN](../ejercicio-02-una-cnn/README.md) |
