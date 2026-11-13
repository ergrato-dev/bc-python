# Ejercicio 03 — El bucle de entrenamiento

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-descenso-de-gradiente.md)

## Objetivo

Escribir el bucle con el que se entrena cualquier red de PyTorch, y ver qué lo estropea:

- el descenso de gradiente a mano, con `w` y `b`;
- cuatro ritmos de aprendizaje: lento, bien, rápido y uno que diverge;
- el mismo modelo con `nn.Linear`, `nn.MSELoss` y `torch.optim.SGD`, frente a la solución exacta;
- un objetivo con la forma equivocada;
- dos entradas en escalas muy distintas, sin escalar y escaladas;
- SGD frente a Adam con tres ritmos.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-34-pytorch_tensores_autograd_y_mlp/2-practicas/ejercicio-03-el-bucle-de-entrenamiento/starter
uv run python main.py
```

```
Ejercicio 03 · El bucle de entrenamiento
200 horas · PM2.5 de 2.4 a 29.3
```

Doscientas horas de una avenida: miles de vehículos por hora, la humedad y el PM2.5. Detrás hay una recta: PM2.5 = 6 + 5 · vehículos - 0,1 · (humedad - 60), con ruido. Los tres van en columnas `(200, 1)`. `train(model, x, y, optimizer, epochs)` tiene las cuatro líneas de cada época de la teoría 03 y devuelve la pérdida de la última.

## Pasos

### 1. Descenso de gradiente a mano

Descomenta el **PASO 1** y ejecuta:

```
época   0: pérdida 294.971 · w 3.909 · b 1.592
época  50: pérdida   5.259 · w 5.658 · b 4.284
época 100: pérdida   5.071 · w 5.423 · b 4.885
época 150: pérdida   5.049 · w 5.342 · b 5.092
época 200: pérdida   5.046 · w 5.315 · b 5.163
```

Solo con los vehículos. `w` y `b` empiezan en 0. En 50 épocas, la pérdida cae de 295 a 5,3; después, `w` y `b` siguen ajustándose despacio: `w` baja de 5,66 a 5,32 mientras `b` sube. Se compensan: si la recta sube menos, tiene que empezar más arriba.

¿Por qué no llega a 5 y 6? Porque falta la humedad, que también mueve el PM2.5: con una sola entrada, esta es la mejor recta posible (el paso 3 lo comprueba).

### 2. El ritmo de aprendizaje

Descomenta el **PASO 2** y ejecuta:

```
ritmo 0.001: pérdida tras 200 épocas 9.564
ritmo 0.01 : pérdida tras 200 épocas 5.644
ritmo 0.05 : pérdida tras 200 épocas 5.047
ritmo 0.2  : pérdida tras 200 épocas inf
```

Ahora con `nn.Linear(1, 1)`, la misma semilla para todos y 200 épocas:

- **0,001**: avanza, pero en 200 épocas no llega.
- **0,01**: casi.
- **0,05**: llega, a la misma pérdida que el paso 1.
- **0,2**: `inf`. Cada paso se pasa del fondo y cae más arriba, hasta que el número no cabe en un `float32`.

Cambia las 200 épocas por 2000 y vuelve a ejecutar: 0,01 llega también, y 0,001 se queda en 5,64, todavía lejos. 0,2 da `nan`. Un ritmo pequeño solo es lento; uno grande no llega nunca.

### 3. Con `nn.Linear`, `MSELoss` y `SGD`

Descomenta el **PASO 3** y ejecuta:

```
al empezar: 0.744 -0.769
tras 2000 épocas: pérdida 5.046 · w 5.300 · b 5.201
mínimos cuadrados:            w 5.300 · b 5.201
```

- `nn.Linear(1, 1)` no empieza en 0: empieza con un peso y un sesgo al azar, pequeños. Con `torch.manual_seed(34)`, siempre los mismos.
- Tras 2000 épocas, el descenso de gradiente llega a la recta **exacta**: `torch.linalg.lstsq` la calcula con la fórmula de mínimos cuadrados (la que usa `LinearRegression` de scikit-learn), y coincide en los tres decimales.

Para una recta, la fórmula es más rápida. El descenso de gradiente es el que funciona igual con una red de tres capas, donde no hay fórmula.

### 4. La forma del objetivo

Descomenta el **PASO 4** y ejecuta:

```
objetivo (200,): pérdida 78.24 · avisos 1
objetivo (200, 1): pérdida 5.05
la resta se hace (200, 200)
```

La misma recta del paso 3, ya entrenada, medida con dos objetivos: la columna de siempre, `(200, 1)`, y la misma aplanada, `(200,)`.

- Con `(200, 1)`, la pérdida de verdad: 5,05.
- Con `(200,)`, 78,24 y **un aviso**, no un error. La salida es `(200, 1)`: por broadcasting, la resta da `(200, 200)`, cada predicción menos cada objetivo (teoría 01, sección 5).

Si entrenas con la forma equivocada, el modelo minimiza esa tabla de 40 000 diferencias: aprende a predecir la media. Busca el aviso `Using a target size` en tu terminal, y si lo ves, `y.reshape(-1, 1)`.

### 5. Escalar las entradas

Descomenta el **PASO 5** y ejecuta:

```
medias: tensor([2022.,   62.]) · tras escalar: tensor([0., 0.])
sin escalar: pérdida tras 300 épocas nan
escaladas  : pérdida tras 300 épocas 2.334
```

Dos entradas: los vehículos, ahora en **unidades** (de 0 a 4000), y la humedad (de 30 a 95).

- **Sin escalar**: `nan`. El gradiente del peso de los vehículos lleva multiplicados miles: con el ritmo 0,05, el primer paso ya salta lejísimos.
- **Escaladas**, a media 0 y desviación 1 con `(x - media) / desviación`: la pérdida baja a 2,33, mucho menos que los 5,05 de la recta con solo los vehículos. La humedad explica lo que faltaba.

Aquí se escala con todas las medidas, porque no hay prueba. En el proyecto, con la media y la desviación del **entrenamiento** (teoría 05, sección 2).

### 6. SGD frente a Adam

Descomenta el **PASO 6** y ejecuta:

```
ritmo 0.001: SGD    84.528 · Adam 263.809
ritmo 0.05 : SGD     2.334 · Adam  20.909
ritmo 0.5  : SGD     2.334 · Adam   2.334
```

Con las entradas escaladas, 300 épocas y tres ritmos. ¿Adam peor que SGD? Mira **por qué**:

- Adam da pasos de un tamaño parecido al ritmo, sea cual sea el gradiente. Con 0,05 y 300 épocas, el sesgo avanza como mucho unos 15. Pero el PM2.5 medio ronda 16: el sesgo no llega. Con 0,001, avanza 0,3.
- SGD da pasos proporcionales al gradiente, que es grande cuando el sesgo está lejos: llega antes.
- Con 0,5, los dos llegan.

La lección no es "SGD es mejor": es que Adam necesita el **objetivo** escalado. Pruébalo: cambia `pm25` por `(pm25 - pm25.mean()) / pm25.std()` en la llamada a `train` del paso 6. Con el PM2.5 escalado, el sesgo empieza ya cerca: con 0,001, Adam baja a 0,078 y SGD se queda en 0,147, y con 0,05 y 0,5 los dos llegan a 0,056 (es la misma pérdida de 2,33, dividida por la varianza del PM2.5). Por eso el proyecto escala el valor antes de entrenar y deshace el escalado al predecir.

Para terminar, escribe en un comentario al final de `main.py` qué columnas de tu dominio necesitarías escalar antes de entrenar una red, y en qué unidades están.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'line' is not defined` en el paso 4 | El paso 4 usa la recta del paso 3: descoméntalo antes |
| `NameError: name 'scaled' is not defined` en el paso 6 | `scaled` viene del paso 5 |
| La pérdida es `nan` o `inf` | Ritmo demasiado alto, o entradas sin escalar: es lo que enseñan los pasos 2 y 5 |
| `UserWarning: Using a target size ... different to the input size` | El objetivo es `(n,)` y la salida `(n, 1)`: `y.reshape(-1, 1)` |
| `RuntimeError: addmm: mat1 and mat2 shapes cannot be multiplied (200x2 and 1x1)` | Dos entradas en `nn.Linear(1, 1)`: el primer número es cuántas entradas, `nn.Linear(2, 1)` |
| Tus números difieren en el tercer decimal | Otro procesador suma en otro orden: es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Autograd](../ejercicio-02-autograd/README.md) | **Ejercicio 03 · El bucle de entrenamiento** | [Ejercicio 04 · Un MLP](../ejercicio-04-un-mlp/README.md) |
