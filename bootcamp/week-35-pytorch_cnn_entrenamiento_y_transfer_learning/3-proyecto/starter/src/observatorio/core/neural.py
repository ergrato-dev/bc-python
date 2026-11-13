"""Una red neuronal pequeña (un MLP) en PyTorch, entrenada con un bucle escrito a mano.

Qué: mlp construye la red (una capa oculta con ReLU), train la entrena época a época
(predicción, pérdida, gradientes, paso del optimizador) y learn reparte las medidas,
prepara las entradas y el valor con el entrenamiento, entrena y mide el MAE en prueba
frente a la referencia, que predice siempre la media.
Para qué: scikit-learn esconde el bucle en `fit`; en PyTorch lo escribes tú, y ves cómo
baja la pérdida. Es el mismo bucle que entrena las redes grandes de la semana 35.
Impacto: importa torch, que tarda en cargarse: core/__init__.py no lo reexporta, y la CLI
lo importa solo en `red`.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from torch import nn

from observatorio.core.learning import SEED, split
from observatorio.core.validation import INPUTS, prepare

# Neuronas de la capa oculta, épocas (pasadas por todo el entrenamiento) y ritmo de
# aprendizaje de Adam: valores pequeños que entrenan en un segundo con miles de medidas.
HIDDEN = 16
EPOCHS = 300
RATE = 0.01


@dataclass(frozen=True)
class Training:
    """La pérdida de cada época y el MAE en prueba de la red y de la referencia."""

    parameters: int
    losses: tuple[float, ...]
    mae: float
    baseline: float

    @property
    def learned(self) -> bool:
        """Si la pérdida de la última época es menor que la de la primera."""
        return self.losses[-1] < self.losses[0]

    @property
    def improves(self) -> bool:
        """Si la red se equivoca menos que la referencia en prueba. Empatar no es mejorar."""
        return self.mae < self.baseline


def tensor(values: object) -> torch.Tensor:
    """Una tabla o una columna como tensor de float32, el tipo con el que trabaja nn."""
    return torch.from_numpy(np.asarray(values, dtype=np.float32))


def mlp(inputs: int, hidden: int = HIDDEN) -> nn.Sequential:
    """Entradas, una capa oculta con ReLU y una salida: el valor predicho."""
    return nn.Sequential(nn.Linear(inputs, hidden), nn.ReLU(), nn.Linear(hidden, 1))


def train(
    model: nn.Module, x: torch.Tensor, y: torch.Tensor, epochs: int, rate: float
) -> tuple[float, ...]:
    """Entrena con todas las medidas a la vez en cada época; devuelve la pérdida de cada una."""
    optimizer = torch.optim.Adam(model.parameters(), lr=rate)
    loss_function = nn.MSELoss()
    losses = []
    model.train()
    for _ in range(epochs):
        # Los gradientes se acumulan: sin ponerlos a cero, cada paso sumaría los anteriores.
        optimizer.zero_grad()
        loss = loss_function(model(x), y)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return tuple(losses)


def learn(
    frame: pd.DataFrame,
    hidden: int = HIDDEN,
    epochs: int = EPOCHS,
    rate: float = RATE,
    seed: int = SEED,
) -> Training:
    """Entrena un MLP que predice el valor y lo mide en prueba frente a la media."""
    train_rows, test_rows = split(frame, seed=seed)
    # sparse_threshold=0: siempre una matriz densa, aunque haya muchas etiquetas.
    prepared = prepare().set_params(sparse_threshold=0.0).fit(train_rows[INPUTS])
    x_train = tensor(prepared.transform(train_rows[INPUTS]))
    x_test = tensor(prepared.transform(test_rows[INPUTS]))
    # El valor también se escala: una red que empieza prediciendo cerca de 0 tardaría
    # cientos de épocas solo en llegar a valores de 50. Se escala con el entrenamiento.
    center, spread = float(train_rows["valor"].mean()), float(train_rows["valor"].std())
    y_train = tensor((train_rows["valor"] - center) / spread).reshape(-1, 1)
    y_test = tensor(test_rows["valor"]).reshape(-1, 1)
    # La semilla fija los pesos iniciales: sin ella, cada ejecución da otra red.
    torch.manual_seed(seed)
    model = mlp(x_train.shape[1], hidden)
    losses = train(model, x_train, y_train, epochs, rate)
    model.eval()
    with torch.no_grad():
        predicted = model(x_test) * spread + center
    return Training(
        sum(parameter.numel() for parameter in model.parameters()),
        losses,
        float((predicted - y_test).abs().mean()),
        float((y_test - center).abs().mean()),
    )
