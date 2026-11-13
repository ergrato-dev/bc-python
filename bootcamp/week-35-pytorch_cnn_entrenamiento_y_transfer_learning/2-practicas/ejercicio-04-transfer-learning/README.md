# Ejercicio 04 — Transfer learning

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-transfer-learning.md)

## Objetivo

Reutilizar una red que ya sabe leer dígitos para una tarea nueva con muy pocas etiquetas:

- la red de origen, entrenada con los diez dígitos;
- la tarea nueva, "¿es par?", con 20 imágenes, desde cero;
- la misma tarea con las capas de origen copiadas y congeladas;
- qué se ha entrenado y qué no;
- afinar toda la red con un ritmo pequeño;
- cuántas imágenes hacen falta para que empezar de cero gane.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-35-pytorch_cnn_entrenamiento_y_transfer_learning/2-practicas/ejercicio-04-transfer-learning/starter
uv run python main.py
```

```
Ejercicio 04 · Transfer learning
origen: 900 imágenes · tarea nueva: hasta 400, y 497 de prueba
```

Los 1797 dígitos, repartidos al azar en tres grupos que no se tocan:

- **900** para la red de origen, con su número (0 a 9);
- **hasta 400** para la tarea nueva, etiquetadas solo con "par" o "impar": en la realidad, las pocas que alguien ha tenido tiempo de etiquetar;
- **497** de prueba para la tarea nueva.

`features()` son las capas que miran la imagen: las dos convoluciones de los ejercicios anteriores y `Flatten`, que da 64 números. `scratch(rows)` entrena una red nueva para "¿es par?" solo con `rows`; `transfer(rows)` hace lo mismo con las capas de origen congeladas. `fit` solo optimiza los parámetros que no están congelados.

## Pasos

### 1. La red de origen

Descomenta el **PASO 1** y ejecuta. Tarda unos segundos:

```
origen, diez dígitos · 1898 parámetros · prueba 0.974
```

La CNN del ejercicio 02, entrenada con 900 imágenes para leer el número. Lee bien: 97,4 % en las imágenes de prueba. Esta red no sabe nada de pares e impares; sabe distinguir trazos.

### 2. Desde cero, con 20 imágenes

Descomenta el **PASO 2** y ejecuta:

```
20 imágenes: 7 pares y 13 impares
desde cero · prueba 0.865
```

Una red nueva, la misma forma pero con 2 salidas, entrenada solo con 20 imágenes etiquetadas: 86,5 % de acierto. Con 20 imágenes tiene que aprender a la vez a ver trazos y qué trazos hacen un número par.

### 3. Reutilizar lo que ya sabe ver

Descomenta el **PASO 3** y ejecuta:

```
transfer learning · prueba 0.895
```

`transfer` copia `source[0]` (las capas que miran) con `copy.deepcopy`, pone `requires_grad = False` en todos sus parámetros y añade una salida nueva de 2 clases. Solo esa salida se entrena, con las mismas 20 imágenes: 89,5 %, tres puntos más. La red de origen ya sabía distinguir un 3 de un 8; solo había que decirle cuáles son pares.

### 4. Qué se ha entrenado

Descomenta el **PASO 4** y ejecuta:

```
parámetros: 1378 · entrenables: 130
  0.0.weight   (8, 1, 3, 3)   requires_grad=False
  0.0.bias     (8,)           requires_grad=False
  0.3.weight   (16, 8, 3, 3)  requires_grad=False
  0.3.bias     (16,)          requires_grad=False
  1.weight     (2, 64)        requires_grad=True
  1.bias       (2,)           requires_grad=True
¿los filtros son los de la red de origen? True
```

- 1378 parámetros: los 1248 de las convoluciones de origen y los 130 de la salida nueva (64 × 2 + 2). Solo esos 130 se han entrenado.
- Los nombres dicen dónde está cada uno: `0.3.weight` es la capa 3 de `features` (la segunda `Conv2d`), dentro de la capa 0 del modelo.
- Los filtros siguen siendo exactamente los de la red de origen: congelar funciona.

### 5. Afinar todo, despacio

Descomenta el **PASO 5** y ejecuta:

```
afinada · prueba 0.901
¿los filtros han cambiado? True
```

Ahora se descongela todo y se entrena 50 épocas más con un ritmo de 0,001, diez veces menor. Los filtros se ajustan un poco a "¿es par?" y el acierto sube a 90,1 %. Con el ritmo de 0,01 y solo 20 imágenes, los filtros se moverían tanto que olvidarían lo que sabían: pruébalo cambiando `rate=0.001` por `rate=0.05`: el acierto baja a 0,797, peor que desde cero.

### 6. ¿Cuántas imágenes hacen falta?

Descomenta el **PASO 6** y ejecuta. Tarda un poco más:

```
 10 imágenes · desde cero 0.791 · transfer learning 0.813
 20 imágenes · desde cero 0.865 · transfer learning 0.895
 50 imágenes · desde cero 0.873 · transfer learning 0.899
100 imágenes · desde cero 0.932 · transfer learning 0.920
400 imágenes · desde cero 0.966 · transfer learning 0.944
```

- Con **10, 20 y 50** imágenes, gana el *transfer learning*: lo que la red de origen aprendió con 900 imágenes compensa las pocas etiquetas.
- Con **100 y 400**, gana empezar de cero: hay bastantes imágenes para aprender capas a medida, y las congeladas, hechas para leer el número, limitan.

Es una sola semilla y un solo reparto: las diferencias de un punto pueden cambiar con otra semilla. El patrón (ayuda con pocas, estorba con muchas) es el habitual. Con redes de origen entrenadas con millones de imágenes, la ventaja con pocas etiquetas es mucho mayor que aquí.

Para terminar, escribe en un comentario al final de `main.py` qué tarea de tu dominio tiene muchos datos sin etiquetar, o con otra etiqueta, y otra con muy pocos, y si una red entrenada con la primera podría servir para la segunda.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `¿los filtros son los de la red de origen? False` en el paso 4 | Falta `requires_grad = False`, o `fit` no filtra los parámetros congelados |
| La red de origen también cambia al afinar | Falta `copy.deepcopy`: las dos redes comparten las mismas capas |
| `IndexError: Target 5 is out of bounds` | Las clases de "¿es par?" son 0 y 1: usa `even`, no `labels`, con una salida de 2 |
| El acierto de transfer learning ronda 0,5 | La salida nueva no se entrena: comprueba que es una `nn.Linear(64, 2)` nueva y que tiene `requires_grad=True` |
| El paso 6 tarda | Entrena diez redes: unos segundos es normal |
| Tus números difieren en el tercer decimal | Otro procesador suma en otro orden: es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Entrenar de verdad](../ejercicio-03-entrenar-de-verdad/README.md) | **Ejercicio 04 · Transfer learning** | [Proyecto](../../3-proyecto/README.md) |
