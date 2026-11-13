# Webgrafía — Semana 35

Casi todo en inglés, de la documentación oficial de cada proyecto. Las guías siguen la última versión; si algo no coincide con PyTorch 2.15, manda lo que ves al ejecutar.

| Recurso | Para qué |
|---|---|
| [CNN Explainer](https://poloclub.github.io/cnn-explainer/) | Una CNN en el navegador: pasa el ratón por cada capa y ves los filtros, los mapas, ReLU y el *pooling*. Las teorías 01 y 02 |
| [CS231n: Convolutional Neural Networks](https://cs231n.github.io/convolutional-networks/) | Los apuntes de Stanford: filtros, relleno, paso, canales y *pooling*, con la fórmula del tamaño y la cuenta de parámetros. Las teorías 01 y 02 |
| [PyTorch: Conv1d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv1d.html) | Los parámetros de `nn.Conv1d` y la forma de la entrada y la salida. La teoría 02, sección 4 |
| [PyTorch: Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) | `nn.Conv2d`, con la fórmula del tamaño de salida. La teoría 01, sección 6 |
| [PyTorch: MaxPool2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html) | El *pooling* por máximo. La teoría 01, sección 6 |
| [PyTorch: CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) | La pérdida para clasificar: qué espera como puntuaciones y como clases. La teoría 02, sección 2 |
| [PyTorch: Training a Classifier](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html) | Una CNN para fotos pequeñas en color, de principio a fin. Las teorías 02 y 03 |
| [PyTorch: Dropout](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html) | Qué apaga, y por qué solo en entrenamiento. La teoría 03, sección 3 |
| [PyTorch: StepLR](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.StepLR.html) | El *scheduler* de la teoría 03, sección 5; en el menú, los demás |
| [PyTorch: Saving and Loading Models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) | `state_dict`, `torch.save`, `torch.load` y los puntos de control. La teoría 03, sección 7 |
| [PyTorch: torch.load](https://docs.pytorch.org/docs/stable/generated/torch.load.html) | `weights_only` y el aviso de seguridad sobre `pickle`. La teoría 03, sección 7 |
| [PyTorch: Transfer Learning for Computer Vision](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) | Una ResNet preentrenada, congelada y afinada para una tarea de dos clases. La teoría 04 |
| [torchvision: Models and pre-trained weights](https://docs.pytorch.org/vision/stable/models.html) | Las redes preentrenadas de torchvision, con sus pesos y su acierto. La teoría 04, sección 5 |
| [Hugging Face: The Model Hub](https://huggingface.co/docs/hub/models-the-hub) | Qué es el Hub de modelos y qué trae cada ficha. La teoría 04, sección 5, y la semana 36 |
| [NumPy: sliding_window_view](https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html) | Ventanas sin copiar. La teoría 02, sección 4, y `windows` del proyecto |
| [scikit-learn: load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html) | Los 1797 dígitos de 8 × 8 de los ejercicios |
| [Red neuronal convolucional](https://es.wikipedia.org/wiki/Red_neuronal_convolucional) (en español) | Qué es una CNN, sus capas y su historia. Las teorías 01 y 02 |
| [Aprendizaje por transferencia](https://es.wikipedia.org/wiki/Aprendizaje_por_transferencia) (en español) | La idea del *transfer learning*. La teoría 04 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
