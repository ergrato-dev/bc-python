# Glosario — Semana 34

| Término | Definición |
|---|---|
| **Activación (función de)** | Una función no lineal entre capa y capa, como ReLU. Sin ella, varias capas lineales son una sola |
| **Adam** | Optimizador que ajusta un ritmo para cada parámetro con la historia de sus gradientes. `torch.optim.Adam` |
| **Autograd** | El sistema de PyTorch que anota las operaciones y calcula los gradientes con `backward()` |
| ***Backward*** (vuelta) | Recorrer el grafo desde la pérdida hasta los parámetros, aplicando la regla de la cadena |
| **Broadcasting** | Operar tensores de formas distintas estirando las dimensiones de tamaño 1, comparando desde la derecha |
| **Capa oculta** | Una capa entre la entrada y la salida. Sus neuronas no se ven desde fuera |
| ***DataLoader*** | Sirve un `Dataset` en lotes, barajados si se pide. `torch.utils.data.DataLoader` |
| **Descenso de gradiente** | Mover cada parámetro un poco en contra de su gradiente, y repetir, para bajar la pérdida |
| ***Device*** (dispositivo) | Dónde vive un tensor: `cpu`, `cuda` (tarjeta NVIDIA) o `mps` (Mac) |
| ***dtype*** | El tipo de los números de un tensor. Las redes usan `float32` |
| **Época** | Una pasada por todas las medidas de entrenamiento |
| ***Forward*** (ida) | Calcular la salida y la pérdida a partir de las entradas. En un `nn.Module`, el método `forward` |
| **Gradiente** | Las derivadas de la pérdida respecto de cada parámetro. Su signo dice hacia dónde moverlo |
| **Grafo de operaciones** | Lo que PyTorch anota al calcular con tensores que piden gradientes: cada operación y de qué salió |
| **Mini-lote** | Un grupo pequeño de medidas con el que se da un paso del optimizador |
| **MLP** (perceptrón multicapa) | Una red de capas lineales con activaciones entre ellas |
| **Neurona** | Suma sus entradas por sus pesos, añade su sesgo y aplica la activación |
| **Neurona muerta** | Una neurona ReLU que recibe siempre entradas negativas: su gradiente es 0 y no aprende |
| ***nn.Module*** | La clase base de toda red de PyTorch: registra sus capas y parámetros |
| **Optimizador** | Lee los gradientes y da el paso. `optimizer.step()` y `optimizer.zero_grad()` |
| **Parada temprana** | Quedarse con la red de la época con menor pérdida de validación |
| **Paso** | Una actualización de los parámetros por el optimizador |
| **Pérdida** | El error que se minimiza al entrenar, como el error cuadrático medio. `nn.MSELoss` |
| **Peso** | Un parámetro que multiplica una entrada. Con el sesgo, lo que aprende una capa |
| **Regla de la cadena** | La derivada de una composición es el producto de las derivadas de cada paso |
| **ReLU** | `max(0, x)`: deja los positivos y cambia los negativos por 0. `nn.ReLU` |
| **Ritmo de aprendizaje** (*learning rate*) | Cuánto se mueve cada parámetro en cada paso. Demasiado alto diverge; demasiado bajo no llega |
| **Sesgo** (*bias*) | Un parámetro que se suma a la salida de una neurona |
| **SGD** | Descenso de gradiente estocástico: el mismo ritmo para todos los parámetros. `torch.optim.SGD` |
| ***state_dict*** | Un diccionario con todos los parámetros de una red: para guardarla o recuperarla |
| **Tensor** | Una tabla de números de cualquier número de dimensiones, con tipo y dispositivo, que puede pedir gradientes |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
