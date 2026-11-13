"""Ejercicio 04 · Transfer learning: aprender con pocas etiquetas lo que otra red ya sabe ver.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import copy

import torch
from sklearn.datasets import load_digits
from torch import nn

print("Ejercicio 04 · Transfer learning")

# Una red de origen aprende a leer los diez dígitos con 900 imágenes. La tarea nueva es
# otra pregunta sobre otras imágenes, "¿es par?", y de ella solo tienes unas pocas
# etiquetadas: hasta 400. Las últimas 497 son la prueba de la tarea nueva.
digits = load_digits()
images = torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16
labels = torch.tensor(digits.target)
even = (labels % 2 == 0).long()
torch.manual_seed(35)
order = torch.randperm(len(labels))
source_rows, pool, test = order[:900], order[900:1300], order[1300:]
print(
    f"origen: {len(source_rows)} imágenes · tarea nueva: hasta {len(pool)}, y {len(test)} de prueba"
)


def features() -> nn.Sequential:
    """Las capas que miran la imagen: dos convoluciones, y la fila de 64 números."""
    return nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
    )


def fit(
    model: nn.Module, rows: torch.Tensor, y: torch.Tensor, epochs: int = 150, rate: float = 0.01
) -> None:
    """Entrena con todas las imágenes a la vez. Solo optimiza lo que no está congelado."""
    optimizer = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=rate)
    loss_function = nn.CrossEntropyLoss()
    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss_function(model(images[rows]), y[rows]).backward()
        optimizer.step()


def accuracy(model: nn.Module, rows: torch.Tensor, y: torch.Tensor) -> float:
    model.eval()
    with torch.no_grad():
        return (model(images[rows]).argmax(dim=1) == y[rows]).float().mean().item()


def count(model: nn.Module, trainable: bool = False) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad or not trainable)


def scratch(rows: torch.Tensor) -> nn.Sequential:
    """Una red nueva para "¿es par?" (dos clases), entrenada solo con rows."""
    torch.manual_seed(35)
    model = nn.Sequential(features(), nn.Linear(64, 2))
    fit(model, rows, even)
    return model


def transfer(rows: torch.Tensor) -> nn.Sequential:
    """Las capas de la red de origen, copiadas y congeladas, y una salida nueva."""
    borrowed = copy.deepcopy(source[0])
    for parameter in borrowed.parameters():
        parameter.requires_grad = False
    torch.manual_seed(35)
    model = nn.Sequential(borrowed, nn.Linear(64, 2))
    fit(model, rows, even)
    return model


# ============================================
# PASO 1: La red de origen
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(35)
# source = nn.Sequential(features(), nn.Linear(64, 10))
# fit(source, source_rows, labels)
# print(
#     f"origen, diez dígitos · {count(source)} parámetros"
#     f" · prueba {accuracy(source, test, labels):.3f}"
# )


# ============================================
# PASO 2: Desde cero, con 20 imágenes
# ============================================
# Descomenta las siguientes líneas:
# few = pool[:20]
# print(f"20 imágenes: {even[few].sum().item()} pares y {len(few) - even[few].sum().item()} impares")
# alone = scratch(few)
# print(f"desde cero · prueba {accuracy(alone, test, even):.3f}")


# ============================================
# PASO 3: Reutilizar lo que ya sabe ver
# ============================================
# Descomenta las siguientes líneas:
# helped = transfer(few)
# print(f"transfer learning · prueba {accuracy(helped, test, even):.3f}")


# ============================================
# PASO 4: Qué se ha entrenado
# ============================================
# Descomenta las siguientes líneas:
# print(f"parámetros: {count(helped)} · entrenables: {count(helped, trainable=True)}")
# for name, parameter in helped.named_parameters():
#     print(f"  {name:<12} {str(tuple(parameter.shape)):<14} requires_grad={parameter.requires_grad}")
# same = torch.equal(helped[0][0].weight, source[0][0].weight)
# print(f"¿los filtros son los de la red de origen? {same}")


# ============================================
# PASO 5: Afinar todo, despacio
# ============================================
# Descomenta las siguientes líneas:
# for parameter in helped.parameters():
#     parameter.requires_grad = True
# fit(helped, few, even, epochs=50, rate=0.001)
# print(f"afinada · prueba {accuracy(helped, test, even):.3f}")
# print(f"¿los filtros han cambiado? {not torch.equal(helped[0][0].weight, source[0][0].weight)}")


# ============================================
# PASO 6: ¿Cuántas imágenes hacen falta?
# ============================================
# Descomenta las siguientes líneas:
# for size in [10, 20, 50, 100, 400]:
#     rows = pool[:size]
#     print(
#         f"{size:3d} imágenes · desde cero {accuracy(scratch(rows), test, even):.3f}"
#         f" · transfer learning {accuracy(transfer(rows), test, even):.3f}"
#     )
