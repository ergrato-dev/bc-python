"""Ejercicio 02 · Una CNN: dígitos escritos a mano.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import torch
from sklearn.datasets import load_digits
from torch import nn

print("Ejercicio 02 · Una CNN")

# 1797 dígitos de 8 x 8 píxeles (0 a 16) y su número. Los píxeles se pasan a 0..1, y cada
# imagen lleva un canal: (imágenes, canales, alto, ancho), lo que espera Conv2d.
digits = load_digits()
images = torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16
labels = torch.tensor(digits.target)
torch.manual_seed(35)
order = torch.randperm(len(labels))
train, test = order[:1200], order[1200:]
print(f"entrenamiento {tuple(images[train].shape)} · prueba {tuple(images[test].shape)}")


def fit(model: nn.Module, x: torch.Tensor, y: torch.Tensor, epochs: int = 150) -> nn.Module:
    """Entrena con todas las imágenes a la vez; CrossEntropyLoss: una puntuación por clase."""
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_function = nn.CrossEntropyLoss()
    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss_function(model(x), y).backward()
        optimizer.step()
    model.eval()
    return model


def accuracy(model: nn.Module, x: torch.Tensor, y: torch.Tensor) -> float:
    """La parte de las imágenes cuyo número acierta: la clase con la puntuación más alta."""
    with torch.no_grad():
        return (model(x).argmax(dim=1) == y).float().mean().item()


def count(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


# ============================================
# PASO 1: Un MLP, la referencia
# ============================================
# Descomenta las siguientes líneas:
# Flatten pone los 64 píxeles en fila: el MLP no sabe qué píxel está al lado de cuál.
# torch.manual_seed(35)
# mlp = nn.Sequential(nn.Flatten(), nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
# fit(mlp, images[train], labels[train])
# print(
#     f"MLP · {count(mlp)} parámetros"
#     f" · acierto en prueba {accuracy(mlp, images[test], labels[test]):.3f}"
# )


# ============================================
# PASO 2: Una CNN
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(35)
# cnn = nn.Sequential(
#     nn.Conv2d(1, 8, kernel_size=3, padding=1),
#     nn.ReLU(),
#     nn.MaxPool2d(2),
#     nn.Conv2d(8, 16, kernel_size=3, padding=1),
#     nn.ReLU(),
#     nn.MaxPool2d(2),
#     nn.Flatten(),
#     nn.Linear(16 * 2 * 2, 10),
# )
# fit(cnn, images[train], labels[train])
# print(
#     f"CNN · {count(cnn)} parámetros"
#     f" · acierto en prueba {accuracy(cnn, images[test], labels[test]):.3f}"
# )


# ============================================
# PASO 3: La forma, capa a capa
# ============================================
# Descomenta las siguientes líneas:
# x = images[:1]
# for layer in cnn:
#     x = layer(x)
#     params = count(layer)
#     print(f"{type(layer).__name__:<10} → {str(tuple(x.shape)):<16} {params:>4} parámetros")


# ============================================
# PASO 4: Mover el dígito un píxel
# ============================================
# Descomenta las siguientes líneas:
# Cada imagen de prueba, desplazada un píxel a la derecha: el mismo número.
# shifted = torch.roll(images[test], shifts=1, dims=3)
# shifted[..., 0] = 0
# print(
#     f"desplazadas · MLP {accuracy(mlp, shifted, labels[test]):.3f}"
#     f" · CNN {accuracy(cnn, shifted, labels[test]):.3f}"
# )


# ============================================
# PASO 5: Qué confunde
# ============================================
# Descomenta las siguientes líneas:
# with torch.no_grad():
#     predicted = cnn(images[test]).argmax(dim=1)
# mistakes = [(int(a), int(p)) for a, p in zip(labels[test], predicted) if a != p]
# print(f"{len(mistakes)} errores de {len(test)}")
# pairs = torch.tensor(mistakes).unique(dim=0, return_counts=True)
# for (actual, guess), times in sorted(
#     zip(pairs[0].tolist(), pairs[1].tolist()), key=lambda t: -t[1]
# )[:3]:
#     print(f"  un {actual} leído como {guess}: {times} veces")


# ============================================
# PASO 6: Las puntuaciones y las probabilidades
# ============================================
# Descomenta las siguientes líneas:
# La salida son 10 puntuaciones; softmax las convierte en probabilidades que suman 1.
# with torch.no_grad():
#     scores = cnn(images[test])
# probabilities = scores.softmax(dim=1)
# print(f"la primera es un {labels[test[0]].item()}")
# print(f"puntuaciones de la primera: {[round(v, 1) for v in scores[0].tolist()]}")
# print(f"probabilidades:             {[round(v, 2) for v in probabilities[0].tolist()]}")
# La imagen de la que la red está menos segura: su probabilidad más alta es la más baja.
# doubt = probabilities.max(dim=1).values.argmin()
# top = probabilities[doubt].topk(2)
# print(
#     f"la más dudosa es un {labels[test[doubt]].item()}: "
#     f"{top.indices[0].item()} con {top.values[0].item():.2f},"
#     f" {top.indices[1].item()} con {top.values[1].item():.2f}"
# )
