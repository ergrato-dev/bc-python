"""Ejercicio 03 · Entrenar de verdad: lotes, dropout, aumento de datos y puntos de control.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import pickle
from pathlib import Path

import torch
from sklearn.datasets import load_digits
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

print("Ejercicio 03 · Entrenar de verdad")

# Los dígitos del ejercicio 02, pero solo 200 para entrenar: con pocas imágenes, una red
# memoriza enseguida. 400 validan (para elegir) y el resto es la prueba (para medir, una vez).
digits = load_digits()
images = torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16
labels = torch.tensor(digits.target)
torch.manual_seed(35)
order = torch.randperm(len(labels))
train, validation, test = order[:200], order[200:600], order[600:]
print(f"entrenamiento {len(train)} · validación {len(validation)} · prueba {len(test)}")


def network(dropout: float = 0.0) -> nn.Sequential:
    """La CNN del ejercicio 02, con un Dropout antes de la última capa."""
    return nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Dropout(dropout),
        nn.Linear(64, 10),
    )


def accuracy(model: nn.Module, rows: torch.Tensor) -> float:
    model.eval()
    with torch.no_grad():
        return (model(images[rows]).argmax(dim=1) == labels[rows]).float().mean().item()


def shift(batch: torch.Tensor) -> torch.Tensor:
    """Cada imagen, movida al azar hasta un píxel en cada dirección: otro dígito igual."""
    moved = torch.empty_like(batch)
    for i, image in enumerate(batch):
        dy, dx = torch.randint(-1, 2, (2,)).tolist()
        moved[i] = torch.roll(image, shifts=(dy, dx), dims=(1, 2))
    return moved


def fit(model: nn.Module, epochs: int = 60, augment: bool = False, scheduler: bool = False) -> None:
    """Por lotes de 32, barajados en cada época; escribe el acierto cada 20 épocas."""
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    steps = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.3)
    loss_function = nn.CrossEntropyLoss()
    loader = DataLoader(TensorDataset(images[train], labels[train]), batch_size=32, shuffle=True)
    for epoch in range(1, epochs + 1):
        model.train()
        for x, y in loader:
            optimizer.zero_grad()
            loss_function(model(shift(x) if augment else x), y).backward()
            optimizer.step()
        if scheduler:
            steps.step()
        if epoch % 20 == 0:
            rate = optimizer.param_groups[0]["lr"]
            print(
                f"  época {epoch}: entrenamiento {accuracy(model, train):.3f}"
                f" · validación {accuracy(model, validation):.3f} · ritmo {rate:.4f}"
            )


# ============================================
# PASO 1: Lotes, y la distancia entre las dos curvas
# ============================================
# Descomenta las siguientes líneas:
# print("sin nada:")
# torch.manual_seed(35)
# plain = network()
# fit(plain)


# ============================================
# PASO 2: Dropout
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(35)
# dropping = network(dropout=0.5)
# one = images[:1]
# dropping.train()
# print(
#     f"en train(), dos veces: {[round(v, 2) for v in dropping(one)[0, :3].tolist()]}"
#     f" {[round(v, 2) for v in dropping(one)[0, :3].tolist()]}"
# )
# dropping.eval()
# print(
#     f"en eval(), dos veces:  {[round(v, 2) for v in dropping(one)[0, :3].tolist()]}"
#     f" {[round(v, 2) for v in dropping(one)[0, :3].tolist()]}"
# )
# print("con dropout:")
# torch.manual_seed(35)
# dropping = network(dropout=0.5)
# fit(dropping)


# ============================================
# PASO 3: Aumento de datos
# ============================================
# Descomenta las siguientes líneas:
# print("con imágenes movidas:")
# torch.manual_seed(35)
# augmented = network()
# fit(augmented, augment=True)
# La validación, con cada imagen movida al azar: dígitos que la red no ha visto así.
# torch.manual_seed(0)
# moved = shift(images[validation])
# for name, model in [("sin nada", plain), ("movidas", augmented)]:
#     with torch.no_grad():
#         hits = (model(moved).argmax(dim=1) == labels[validation]).float().mean().item()
#     print(f"{name:<8} · validación movida {hits:.3f}")


# ============================================
# PASO 4: Un ritmo que baja
# ============================================
# Descomenta las siguientes líneas:
# print("con imágenes movidas y un ritmo que baja:")
# torch.manual_seed(35)
# scheduled = network()
# fit(scheduled, augment=True, scheduler=True)


# ============================================
# PASO 5: Guardar y cargar
# ============================================
# Descomenta las siguientes líneas:
# path = Path("pesos.pt")
# torch.save(scheduled.state_dict(), path)
# copy = network()
# copy.load_state_dict(torch.load(path, weights_only=True))
# print(f"{path}: {path.stat().st_size} bytes · validación {accuracy(copy, validation):.3f}")
# torch.save(scheduled, Path("modelo.pt"))
# try:
#     torch.load(Path("modelo.pt"), weights_only=True)
# except pickle.UnpicklingError as problem:
#     print(f"modelo.pt: {str(problem).splitlines()[0][:60]}...")


# ============================================
# PASO 6: La prueba, una sola vez
# ============================================
# Descomenta las siguientes líneas:
# candidates = {
#     "sin nada": plain,
#     "dropout": dropping,
#     "movidas": augmented,
#     "movidas y ritmo": scheduled,
# }
# for name, model in candidates.items():
#     print(f"{name:<16} validación {accuracy(model, validation):.3f}")
# best = max(candidates, key=lambda name: accuracy(candidates[name], validation))
# print(f"elegida: {best} · prueba {accuracy(candidates[best], test):.3f}")
