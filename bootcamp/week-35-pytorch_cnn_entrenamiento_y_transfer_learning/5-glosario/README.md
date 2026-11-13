# Glosario — Semana 35

| Término | Definición |
|---|---|
| **Acierto** (*accuracy*) | La parte de los ejemplos cuya clase predicha es la correcta |
| **Afinar** (*fine-tuning*) | Seguir entrenando toda una red ya entrenada, con un ritmo pequeño, para ajustarla a una tarea nueva |
| **Aumento de datos** (*data augmentation*) | Fabricar variantes de los ejemplos de entrenamiento (moverlos, girarlos, añadir ruido) que siguen teniendo la misma etiqueta |
| **Canal** | Cada una de las variables que se miden en la misma posición: el gris de una imagen (1 canal), sus colores (3), o los mapas que da una capa convolucional |
| **CNN** (red convolucional) | Una red con capas convolucionales: filtros que se deslizan sobre la imagen o la serie |
| **Congelar** | Poner `requires_grad = False` en unos parámetros para que el entrenamiento no los cambie |
| **Convolución** | Deslizar un filtro sobre una serie o una imagen y sumar, en cada posición, los valores por los pesos. `F.conv1d`, `nn.Conv2d` |
| ***CrossEntropyLoss*** | La pérdida para clasificar: recibe una puntuación por clase y la clase correcta como entero |
| ***Dropout*** | Una capa que, en entrenamiento, apaga al azar una parte de los números que le llegan. `nn.Dropout(p)` |
| **Filtro** (*kernel*) | Los pesos que se deslizan en una convolución. Una capa aprende varios |
| ***Flatten*** | Una capa que pone los mapas en una sola fila de números, para una capa lineal. `nn.Flatten()` |
| **Mapa** (*feature map*) | La salida de un filtro sobre toda la entrada: dónde aparece su patrón |
| ***MaxPool2d*** | Parte cada mapa en cuadrados y se queda con el máximo de cada uno. Sin parámetros |
| **Paciencia** (*patience*) | Las épocas sin mejorar en validación que se esperan antes de parar |
| **Parada temprana** (*early stopping*) | Parar de entrenar cuando la validación deja de mejorar, y quedarse con la mejor época |
| **Paso** (*stride*) | Cuántas posiciones avanza el filtro cada vez |
| **Pesos preentrenados** | Los parámetros de una red ya entrenada con muchos datos, publicados para reutilizarlos |
| ***pickle*** | El formato de Python para guardar objetos. Al cargarse puede ejecutar código: por eso `weights_only=True` |
| **Punto de control** (*checkpoint*) | Los pesos guardados de una red, con lo necesario para reconstruirla |
| **Puntuación** (*logit*) | Un número por clase que da la red; gana el más alto |
| **Relleno** (*padding*) | Ceros añadidos a los bordes para que el filtro pueda empezar en el primer valor |
| ***Scheduler*** | Lo que baja el ritmo de aprendizaje a lo largo de las épocas. `StepLR` |
| ***softmax*** | Convierte las puntuaciones en probabilidades positivas que suman 1 |
| ***state_dict*** | El diccionario con todos los parámetros de una red, por nombre |
| **Transfer learning** (aprendizaje por transferencia) | Reutilizar las capas de una red entrenada para otra tarea, y entrenar solo lo nuevo |
| **Validación** | La parte de los datos con la que se elige (épocas, hiperparámetros, qué red); la prueba solo mide |
| **Ventana** | Unos valores seguidos de una serie, con los que se pronostica el siguiente |
| ***weights_only*** | La opción de `torch.load` que solo acepta tensores, números, textos, listas y diccionarios |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
