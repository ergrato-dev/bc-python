# Ejercicio 02 — Autograd

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-autograd.md)

## Objetivo

Pedir a PyTorch las derivadas y comprobar que son las que esperas:

- una derivada con autograd, frente a la que calculas a mano;
- los gradientes de una recta, frente a su fórmula;
- la regla de la cadena a través de ReLU, y una neurona que no aprende;
- gradientes que se acumulan si no los pones a cero;
- `no_grad`, `detach` e `item`;
- cinco pasos de descenso de gradiente escritos a mano.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-34-pytorch_tensores_autograd_y_mlp/2-practicas/ejercicio-02-autograd/starter
uv run python main.py
```

```
Ejercicio 02 · Autograd
6 horas · ozono de 47.0 a 90.0
```

Seis horas de un sensor: la temperatura y el ozono. Con más calor y más sol, más ozono: detrás hay una recta, ozono = 3 · temperatura + 10, con algo de ruido. Seis medidas, para que puedas hacer las cuentas a mano si quieres.

## Pasos

### 1. Una derivada, a mano y con autograd

Descomenta el **PASO 1** y ejecuta:

```
en 20.0: autograd  -20.0 · a mano  -19.999
en 30.0: autograd    0.0 · a mano    0.001
en 45.0: autograd   30.0 · a mano   30.001
```

La pérdida es `(guess - 30)²`: el error al cuadrado de una predicción frente a un valor de 30. En cada punto:

- **autograd**: `requires_grad=True`, `backward()` y `guess.grad`. Exacto: `2 · (guess - 30)`.
- **a mano**: mueve `guess` una milésima y mira cuánto cambia la pérdida. Casi lo mismo, con un error en la tercera cifra decimal.

Fíjate en el signo. En 20, negativo: subir `guess` baja la pérdida. En 45, positivo: hay que bajarlo. En 30, cero: es el mínimo, y no hay hacia dónde moverse.

### 2. Los gradientes de una recta

Descomenta el **PASO 2** y ejecuta:

```
pérdida 894.50 · w.grad -1200.00 · b.grad -59.00
fórmula: -1200.00 · -59.00
```

Una recta `w · temperatura + b` con `w = 2` y `b = 0`, y el error cuadrático medio de las seis horas. Las predicciones (24 a 54) se quedan muy cortas frente al ozono (47 a 90): los dos gradientes son negativos, hay que subir `w` y `b`.

`w.grad` es veinte veces `b.grad`: el gradiente de `w` lleva multiplicada la temperatura, que ronda 20 (teoría 02, sección 3). La segunda línea calcula las dos derivadas con su fórmula: los mismos números. `.detach()` saca el error del grafo para calcular la fórmula sin anotar nada.

### 3. La regla de la cadena y una neurona apagada

Descomenta el **PASO 3** y ejecuta:

```
peso  1.5: salida 9.0 · gradiente 6.0
peso -1.5: salida 0.0 · gradiente 0.0
```

`relu(peso · 2) · 3`: tres operaciones encadenadas, como una neurona pequeña. Con peso 1,5, ReLU deja pasar el 3, y la salida es 9. La derivada, por la regla de la cadena: 2 (de la multiplicación) × 1 (ReLU, con un positivo) × 3 = 6.

Con peso -1,5, la entrada de ReLU es negativa: la salida es 0 y la derivada de ReLU es **0**. Todo el gradiente se multiplica por 0: el peso no recibe ninguna señal para cambiar. Es una **neurona muerta**: si todas las medidas le llegan en negativo, no aprende nunca. Por eso los pesos iniciales son pequeños y al azar: unas neuronas empiezan activas con unas medidas y otras con otras.

### 4. Los gradientes se acumulan

Descomenta el **PASO 4** y ejecuta:

```
backward 1: w.grad -1200.00
backward 2: w.grad -2400.00
backward 3: w.grad -3600.00
tras zero_(): 0.0
```

Tres veces la misma pérdida, tres `backward()`, sin poner a cero entre medias: el gradiente se **suma**. En un bucle de entrenamiento, el tercer paso usaría tres veces el gradiente que toca. Sin ningún error.

`zero_()`, con guion bajo al final, cambia el tensor **en su sitio**: es la convención de PyTorch para las operaciones que modifican en lugar de devolver uno nuevo. Un optimizador lo hace con `optimizer.zero_grad()`.

### 5. `no_grad` y `detach`

Descomenta el **PASO 5** y ejecuta:

```
dentro de no_grad: False
Can't call numpy() on Tensor that requires grad
con detach: 4.0 · con item: 4.0
```

- Dentro de `with torch.no_grad():`, el resultado no arrastra historia: `requires_grad` es `False`. Es lo que se usa para predecir con un modelo ya entrenado.
- `doubled` viene de `w`, que pide gradientes: NumPy no puede quedárselo, porque perdería la historia. `.detach()` da el mismo número sin historia; `.item()`, un `float` de Python.

### 6. Bajar por la pendiente, a mano

Descomenta el **PASO 6** y ejecuta:

```
paso 1: pérdida  894.50 · w 4.400 · b 0.118
paso 2: pérdida  360.04 · w 2.888 · b 0.048
paso 3: pérdida  148.08 · w 3.840 · b 0.097
paso 4: pérdida   64.02 · w 3.241 · b 0.071
paso 5: pérdida   30.68 · w 3.618 · b 0.092
```

El descenso de gradiente, con lo que ya tienes: en cada paso, la pérdida, `backward()`, un paso de 0,002 veces el gradiente en contra (dentro de `no_grad`) y los gradientes a cero. La pérdida baja de 894 a 31 en cinco pasos.

Mira `w`: 4,4, 2,9, 3,8, 3,2, 3,6. **Zigzaguea** alrededor del 3 de la recta de verdad: cada paso se pasa un poco del fondo hacia el otro lado. El ritmo 0,002 parece pequeño, pero el gradiente de `w` es enorme (la temperatura ronda 20, y entra al cuadrado): con 0,005 se pasaría cada vez más lejos y la pérdida subiría. Pruébalo. Es la razón por la que se escalan las entradas (teoría 03, sección 4), y lo verás en el ejercicio 03.

`b` apenas se mueve, de 0 a 0,09: su gradiente es mucho menor. Con un único ritmo para los dos, uno avanza demasiado y el otro casi nada. Adam lo resuelve con un ritmo para cada parámetro.

Para terminar, escribe en un comentario al final de `main.py` qué parámetro de un modelo de tu dominio tendría un gradiente mucho mayor que los demás, y por qué.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `AttributeError: 'NoneType' object has no attribute 'item'` | Lees `.grad` antes de `backward()`, o el tensor no tiene `requires_grad=True` |
| `RuntimeError: grad can be implicitly created only for scalar outputs` | `backward()` sobre un tensor de varios números: falta `.mean()` |
| `RuntimeError: a leaf Variable that requires grad is being used in an in-place operation` | `w -= ...` fuera de `with torch.no_grad():` |
| En el paso 4 sale siempre -1200 | Pones a cero dentro del bucle: el paso enseña justo lo contrario |
| En el paso 6 la pérdida sube | Has subido el ritmo: con 0,005 diverge. Vuelve a 0,002 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Tensores](../ejercicio-01-tensores/README.md) | **Ejercicio 02 · Autograd** | [Ejercicio 03 · El bucle de entrenamiento](../ejercicio-03-el-bucle-de-entrenamiento/README.md) |
