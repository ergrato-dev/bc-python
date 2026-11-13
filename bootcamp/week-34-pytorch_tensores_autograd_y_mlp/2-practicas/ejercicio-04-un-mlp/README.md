# Ejercicio 04 — Un MLP

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-redes-neuronales-mlp.md)

## Objetivo

Entrenar una red neuronal que aprende la forma del día, y ver dónde se rompe:

- una recta frente a una red con una capa oculta;
- tres capas sin activación, frente a tres capas con ReLU;
- la red como clase `nn.Module`, con 2, 8, 32 y 128 neuronas;
- mini-lotes con `DataLoader`;
- una red grande con pocas medidas: el sobreajuste en las dos curvas;
- parar a tiempo y quedarse con la mejor red.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-34-pytorch_tensores_autograd_y_mlp/2-practicas/ejercicio-04-un-mlp/starter
uv run python main.py
```

```
Ejercicio 04 · Un MLP
entrenamiento (1600, 2) · validación (400, 2)
```

Dos mil horas de PM2.5 con dos entradas: la hora del día (continua: 7,5 son las 7:30) y si es fin de semana. Entre semana hay dos picos, a las 8 y a las 19, por el tráfico; el fin de semana, solo uno suave por la tarde. Las entradas y el PM2.5 van **escalados** (teoría 03, sección 4), y las horas, repartidas al azar: 1600 para entrenar y 400 para validar.

`fit(model)` entrena con Adam, ritmo 0,01 y 500 épocas, con todas las medidas de entrenamiento a la vez, y devuelve la pérdida en **validación**. Con el PM2.5 escalado, una pérdida de 1 es lo que se equivoca predecir siempre la media.

## Pasos

### 1. Una recta frente a una red

Descomenta el **PASO 1** y ejecuta. Tarda unos segundos:

```
recta          · validación 0.891
red de 32 ReLU · validación 0.152
```

- La **recta** (`nn.Linear(2, 1)`) apenas mejora la media: 0,89. Solo puede decir "más tarde, más PM2.5" (o menos) y "el fin de semana, tanto menos".
- La **red**: dos entradas, una capa oculta de 32 neuronas con ReLU y una salida. Baja a 0,15: ha encontrado los dos picos, y que el de la mañana desaparece el fin de semana. Nadie le ha dicho dónde están.

Ese cruce, "el pico de las 8 solo entre semana", es lo que un modelo lineal no ve sin una columna creada a mano (semana 32), y lo que un árbol encontraba con dos preguntas (semana 33).

### 2. Sin activación, una recta

Descomenta el **PASO 2** y ejecuta:

```
tres capas lineales · validación 0.891
tres capas con ReLU · validación 0.141
```

Tres `nn.Linear` seguidas, con 32 neuronas en cada capa oculta y más de mil parámetros: **0,891**, exactamente lo de la recta. Una capa lineal de una capa lineal es una capa lineal (teoría 04, sección 2): los parámetros de más no sirven para nada.

Las mismas tres capas con ReLU entre ellas: 0,141, un poco mejor que una sola capa oculta. La activación es lo que deja doblar.

### 3. La red como clase, y cuántas neuronas

Descomenta el **PASO 3** y ejecuta:

```
  2 neuronas ·   9 parámetros · validación 0.884
  8 neuronas ·  33 parámetros · validación 0.697
 32 neuronas · 129 parámetros · validación 0.152
128 neuronas · 513 parámetros · validación 0.143
```

`Daily` es la red del paso 1 escrita como clase `nn.Module`: las capas en `__init__`, el camino en `forward`. Con `n` neuronas, `(2 + 1) · n + (n + 1)` parámetros.

- Con **2 neuronas**, dos "codos": no le da para dos picos. Casi una recta.
- Con **8**, mejor, pero 500 épocas no le bastan para colocar bien sus pocos codos.
- Con **32**, 129 parámetros: el salto grande. El mismo número de parámetros que la red de tu proyecto con los datos de ejemplo, por casualidad: allí son 6 entradas y 16 neuronas.
- Con **128**, apenas mejora. Más neuronas, más tiempo, y con pocas medidas, más riesgo de memorizar (paso 5).

`hidden` es un hiperparámetro, como `max_depth` en un árbol: se elige con validación.

### 4. Mini-lotes

Descomenta el **PASO 4** y ejecuta:

```
25 lotes de 64 por época
época 10:  250 pasos · validación 0.421
época 20:  500 pasos · validación 0.304
época 30:  750 pasos · validación 0.275
época 40: 1000 pasos · validación 0.268
```

`DataLoader` sirve las 1600 medidas en 25 lotes de 64, barajados en cada época. Cada lote es **un paso** del optimizador.

- En 40 épocas, 1000 pasos: el doble que los 500 de `fit`, y aun así se queda en 0,27, peor que el 0,15 del paso 3. Cada paso mira solo 64 medidas: su gradiente apunta más o menos hacia el fondo, no exactamente, y por paso se avanza menos.
- Lo que gana es que cada paso es barato, y la memoria: con un millón de medidas no podrías pasarlas todas a la vez. Con 1600 sí, y entrenar sin lotes es más sencillo. Por eso el proyecto no usa lotes.

Cambia `range(1, 41)` por `range(1, 201)` y `epoch % 10` por `epoch % 50`: en la época 200, con 5000 pasos, llega a 0,143.

### 5. Pocas medidas, una red grande

Descomenta el **PASO 5** y ejecuta. Tarda unos segundos:

```
época   10: entrenamiento 0.738 · validación 0.855
época   50: entrenamiento 0.152 · validación 0.197
época  100: entrenamiento 0.081 · validación 0.152
época  300: entrenamiento 0.068 · validación 0.192
época 1000: entrenamiento 0.029 · validación 0.247
```

Solo **60** medidas para entrenar, y una red con dos capas ocultas de 256 neuronas: más de 66 000 parámetros. En cada época se miden las dos pérdidas.

- Hasta la época 100, las dos bajan juntas: la red aprende la forma del día.
- Después, la de **entrenamiento** sigue bajando, hasta 0,03, y la de **validación** sube, de 0,15 a 0,25. La red persigue el ruido de sus 60 medidas: memoriza.

Es la curva de validación de la semana 31, ahora a lo largo de las épocas: no hace falta cambiar el modelo para que sobreajuste, basta con entrenarlo demasiado.

### 6. Parar a tiempo

Descomenta el **PASO 6** y ejecuta:

```
paró en la época 129; la mejor, la 79, con validación 0.147
```

La misma red y las mismas 60 medidas, pero mirando la pérdida de validación en **cada** época:

- si mejora la mejor, se guarda una copia de los pesos con `copy.deepcopy(big.state_dict())`. `state_dict()` es un diccionario con todos los parámetros; sin `deepcopy`, guardarías una referencia a los mismos tensores, que el entrenamiento sigue cambiando;
- si pasan 50 épocas (`patience`) sin mejorar, para;
- al final, `load_state_dict` devuelve la red a la mejor época.

Paró en la 129 y se quedó con la 79: validación 0,147, casi como la red de 1600 medidas del paso 3. Es la parada temprana del `HistGradientBoosting` de la semana 33, hecha a mano. Ojo: la parte con la que eliges la época ya no es una medida limpia de la red; para eso haría falta una tercera parte, de prueba.

Para terminar, escribe en un comentario al final de `main.py` qué entradas de tu dominio darían una relación con picos o cruces como esta, y cuántas medidas tendrías para entrenar.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: Daily.__init__() missing 1 required positional argument: 'hidden'` | `Daily(32)`: la clase pide el número de neuronas |
| `AttributeError: cannot assign module before Module.__init__() call` | Falta `super().__init__()` al principio de `__init__` |
| La pérdida de validación del paso 6 no coincide con la del paso 5 en la época 79 | Es la misma red: comprueba que las dos usan `torch.manual_seed(34)` justo antes de crearla |
| `TypeError: 'NoneType' object is not iterable` en `load_state_dict` | Nunca mejoró: `best_state` sigue en `None`. Mira si la pérdida es `nan` |
| Los pasos 5 y 6 tardan | Son 1000 épocas de una red de 66 000 parámetros: unos segundos es normal |
| Tus números difieren en el tercer decimal | Otro procesador suma en otro orden: es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · El bucle de entrenamiento](../ejercicio-03-el-bucle-de-entrenamiento/README.md) | **Ejercicio 04 · Un MLP** | [Proyecto](../../3-proyecto/README.md) |
