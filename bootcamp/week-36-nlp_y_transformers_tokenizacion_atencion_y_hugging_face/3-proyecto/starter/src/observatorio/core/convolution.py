"""Una red convolucional que pronostica el siguiente valor de la serie, a partir de los anteriores.

Qué: windows corta la serie en ventanas (unos cuantos valores seguidos y el que viene después),
cnn construye la red (una capa Conv1d, ReLU y una capa lineal), fit la entrena con mini-lotes
y parada temprana, y forecast reparte por tiempo, escala, entrena y mide el MAE en prueba
frente a la referencia. save y load guardan y cargan los pesos; freeze congela la capa
convolucional para reentrenar solo la salida con otros datos (transfer learning).
Para qué: es el entrenamiento de verdad de la semana 35: lotes, validación, quedarse con la
mejor época, y reutilizar una red ya entrenada en lugar de empezar de cero.
Impacto: importa torch: core/__init__.py no lo reexporta, y la CLI lo importa solo en
`pronosticar`.
"""

import copy
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from observatorio.core.learning import SEED
from observatorio.core.neural import tensor
from observatorio.core.validation import ordered

# Valores de cada ventana, filtros de la capa convolucional y tamaño de cada filtro.
WINDOW = 8
CHANNELS = 4
KERNEL = 3
# Épocas como máximo, ritmo de Adam, medidas por lote y épocas sin mejorar antes de parar.
EPOCHS = 100
RATE = 0.01
BATCH = 32
PATIENCE = 10
# Las primeras ventanas entrenan, las siguientes validan y las últimas son la prueba.
TRAIN_SHARE = 0.7
VALIDATION_SHARE = 0.15
# Con menos ventanas, la validación y la prueba tendrían una o dos.
MINIMUM = 20


@dataclass(frozen=True)
class Forecast:
    """La pérdida en validación de cada época, la mejor, y el MAE en prueba de la red y de la
    referencia."""

    parameters: int
    trainable: int
    sizes: tuple[int, int, int]
    losses: tuple[float, ...]
    best: int
    mae: float
    baseline: float

    @property
    def improves(self) -> bool:
        """Si la red se equivoca menos que la referencia en prueba. Empatar no es mejorar."""
        return self.mae < self.baseline


def windows(values: np.ndarray, size: int) -> tuple[torch.Tensor, torch.Tensor]:
    """Cada tramo de `size` valores seguidos, con forma (ventanas, 1 canal, size), y el valor
    que viene justo después, con forma (ventanas, 1)."""
    x = np.lib.stride_tricks.sliding_window_view(values[:-1], size)
    return tensor(x).unsqueeze(1), tensor(values[size:]).reshape(-1, 1)


def cnn(size: int, channels: int = CHANNELS) -> nn.Sequential:
    """Una capa convolucional (channels filtros de KERNEL valores), ReLU, y una capa lineal
    que mira lo que han visto todos los filtros en toda la ventana."""
    return nn.Sequential(
        nn.Conv1d(1, channels, KERNEL),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(channels * (size - KERNEL + 1), 1),
    )


def freeze(model: nn.Sequential) -> None:
    """Congela la capa convolucional: sus pesos ya no cambian al entrenar."""
    for parameter in model[0].parameters():
        parameter.requires_grad_(False)


def count(model: nn.Module, trainable: bool = False) -> int:
    """Cuántos parámetros tiene la red; con trainable, solo los que el entrenamiento cambia."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad or not trainable)


def fit(
    model: nn.Module,
    train: tuple[torch.Tensor, torch.Tensor],
    validation: tuple[torch.Tensor, torch.Tensor],
    epochs: int = EPOCHS,
    patience: int = PATIENCE,
) -> tuple[tuple[float, ...], int]:
    """Entrena por mini-lotes y mide la validación tras cada época. Para tras `patience`
    épocas sin mejorar y devuelve el modelo a su mejor época. Devuelve la pérdida en
    validación de cada época y el índice de la mejor."""
    optimizer = torch.optim.Adam(model.parameters(), lr=RATE)
    loss_function = nn.MSELoss()
    # shuffle: otro orden en cada época, con la semilla de torch.
    loader = DataLoader(TensorDataset(*train), batch_size=BATCH, shuffle=True)
    losses: list[float] = []
    best, best_state = 0, copy.deepcopy(model.state_dict())
    for epoch in range(epochs):
        model.train()
        for x, y in loader:
            optimizer.zero_grad()
            loss_function(model(x), y).backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            loss = loss_function(model(validation[0]), validation[1]).item()
        if loss < min(losses, default=float("inf")):
            # deepcopy: state_dict son los tensores de la red, que el entrenamiento sigue cambiando.
            best, best_state = epoch, copy.deepcopy(model.state_dict())
        losses.append(loss)
        if epoch - best >= patience:
            break
    model.load_state_dict(best_state)
    return tuple(losses), best


def forecast(
    frame: pd.DataFrame,
    window: int = WINDOW,
    epochs: int = EPOCHS,
    patience: int = PATIENCE,
    seed: int = SEED,
    label: str | None = None,
    start: nn.Sequential | None = None,
) -> tuple[Forecast, nn.Sequential]:
    """Entrena una red que pronostica cada valor con los `window` anteriores, en orden de
    llegada, y la mide en prueba frente a la media. Con label, solo la serie de esa etiqueta;
    con start, reentrena esa red con su capa convolucional congelada."""
    rows = ordered(frame)
    if label is not None:
        rows = rows[rows["etiqueta"] == label]
    values = rows["valor"].to_numpy()
    if len(values) < window + MINIMUM:
        raise ValueError(
            f"hacen falta al menos {window + MINIMUM} valores para ventanas de {window},"
            f" y hay {len(values)}"
        )
    # Por tiempo, sin barajar: la red solo ve el pasado de lo que pronostica.
    total = len(values) - window
    train_end, validation_end = (
        int(total * TRAIN_SHARE),
        int(total * (TRAIN_SHARE + VALIDATION_SHARE)),
    )
    # El escalado sale solo de los valores que ven las ventanas de entrenamiento.
    seen = values[: train_end + window]
    center, spread = float(seen.mean()), float(seen.std(ddof=1))
    x, y = windows((values - center) / spread, window)
    torch.manual_seed(seed)
    model = cnn(window) if start is None else start
    if start is not None:
        freeze(model)
    losses, best = fit(
        model,
        (x[:train_end], y[:train_end]),
        (x[train_end:validation_end], y[train_end:validation_end]),
        epochs,
        patience,
    )
    model.eval()
    with torch.no_grad():
        predicted = model(x[validation_end:]) * spread + center
    actual = tensor(values[window + validation_end :]).reshape(-1, 1)
    result = Forecast(
        count(model),
        count(model, trainable=True),
        (train_end, validation_end - train_end, total - validation_end),
        losses,
        best,
        float((predicted - actual).abs().mean()),
        float((actual - center).abs().mean()),
    )
    return result, model


def save(model: nn.Sequential, window: int, path: Path) -> None:
    """Guarda los pesos y la ventana, no el objeto: load no ejecuta nada al leerlos."""
    # open: si no se puede escribir, un OSError como los de cualquier archivo.
    with path.open("wb") as file:
        torch.save({"window": window, "state": model.state_dict()}, file)


def load(path: Path) -> tuple[nn.Sequential, int]:
    """La red y su ventana. weights_only: solo tensores y números; un archivo con otra cosa
    (código que pickle ejecutaría) lanza pickle.UnpicklingError."""
    checkpoint = torch.load(path, weights_only=True)
    model = cnn(checkpoint["window"])
    model.load_state_dict(checkpoint["state"])
    return model, checkpoint["window"]
