"""Ejercicio 04 · Un MLP: capas, mini-lotes y sobreajuste.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

print("Ejercicio 04 · Un MLP")

# Dos mil horas de PM2.5: la hora del día (continua, 7.5 son las 7:30) y si es fin de
# semana. Entre semana, dos picos (8 y 19 h, el tráfico); el fin de semana, solo uno suave
# por la tarde. Ninguna recta lo dibuja, y el pico de la mañana depende del día.
torch.manual_seed(34)
hour = torch.rand(2000, 1) * 24
weekend = (torch.rand(2000, 1) < 2 / 7).float()
morning = 20 * torch.exp(-((hour - 8) ** 2) / 3) * (1 - weekend)
evening = 15 * torch.exp(-((hour - 19) ** 2) / 4) * (1 - 0.6 * weekend)
pm25 = 14 + morning + evening + torch.randn(2000, 1) * 2

# Entradas y objetivo escalados; 1600 horas para entrenar y 400 para validar.
x = torch.cat([(hour - 12) / 7, weekend * 2 - 1], dim=1)
y = (pm25 - pm25.mean()) / pm25.std()
order = torch.randperm(2000)
train_x, train_y = x[order[:1600]], y[order[:1600]]
val_x, val_y = x[order[1600:]], y[order[1600:]]
print(f"entrenamiento {tuple(train_x.shape)} · validación {tuple(val_x.shape)}")

loss_function = nn.MSELoss()


def fit(model, epochs=500, rate=0.01):
    """Entrena con todas las medidas de entrenamiento a la vez; devuelve la pérdida de
    validación."""
    optimizer = torch.optim.Adam(model.parameters(), lr=rate)
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_function(model(train_x), train_y)
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        return loss_function(model(val_x), val_y).item()


# ============================================
# PASO 1: Una recta frente a una red
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(34)
# print(f"recta          · validación {fit(nn.Linear(2, 1)):.3f}")
# torch.manual_seed(34)
# network = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 1))
# print(f"red de 32 ReLU · validación {fit(network):.3f}")


# ============================================
# PASO 2: Sin activación, una recta
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(34)
# stacked = nn.Sequential(nn.Linear(2, 32), nn.Linear(32, 32), nn.Linear(32, 1))
# print(f"tres capas lineales · validación {fit(stacked):.3f}")
# torch.manual_seed(34)
# deep = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 1))
# print(f"tres capas con ReLU · validación {fit(deep):.3f}")


# ============================================
# PASO 3: La red como clase, y cuántas neuronas
# ============================================
# Descomenta las siguientes líneas:
# class Daily(nn.Module):
#     """La hora y el fin de semana, una capa oculta con ReLU y el PM2.5."""

#     def __init__(self, hidden: int) -> None:
#         super().__init__()
#         self.hidden = nn.Linear(2, hidden)
#         self.output = nn.Linear(hidden, 1)

#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         return self.output(torch.relu(self.hidden(x)))


# for hidden in [2, 8, 32, 128]:
#     torch.manual_seed(34)
#     model = Daily(hidden)
#     count = sum(parameter.numel() for parameter in model.parameters())
#     print(f"{hidden:3} neuronas · {count:3} parámetros · validación {fit(model):.3f}")


# ============================================
# PASO 4: Mini-lotes
# ============================================
# Descomenta las siguientes líneas:
# batches = DataLoader(TensorDataset(train_x, train_y), batch_size=64, shuffle=True)
# print(f"{len(batches)} lotes de 64 por época")
# torch.manual_seed(34)
# model = Daily(32)
# optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
# for epoch in range(1, 41):
#     model.train()
#     for batch_x, batch_y in batches:
#         optimizer.zero_grad()
#         loss = loss_function(model(batch_x), batch_y)
#         loss.backward()
#         optimizer.step()
#     if epoch % 10 == 0:
#         model.eval()
#         with torch.no_grad():
#             held = loss_function(model(val_x), val_y).item()
#         print(f"época {epoch}: {epoch * len(batches):4} pasos · validación {held:.3f}")


# ============================================
# PASO 5: Pocas medidas, una red grande
# ============================================
# Descomenta las siguientes líneas:
# few_x, few_y = train_x[:60], train_y[:60]
# torch.manual_seed(34)
# big = nn.Sequential(nn.Linear(2, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 1))
# optimizer = torch.optim.Adam(big.parameters(), lr=0.01)
# history = []
# for epoch in range(1, 1001):
#     big.train()
#     optimizer.zero_grad()
#     loss = loss_function(big(few_x), few_y)
#     loss.backward()
#     optimizer.step()
#     big.eval()
#     with torch.no_grad():
#         history.append((loss.item(), loss_function(big(val_x), val_y).item()))
# for epoch in [10, 50, 100, 300, 1000]:
#     trained, held = history[epoch - 1]
#     print(f"época {epoch:4}: entrenamiento {trained:.3f} · validación {held:.3f}")


# ============================================
# PASO 6: Parar a tiempo
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(34)
# big = nn.Sequential(nn.Linear(2, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 1))
# optimizer = torch.optim.Adam(big.parameters(), lr=0.01)
# best, best_epoch, best_state, patience = float("inf"), 0, None, 50
# for epoch in range(1, 1001):
#     big.train()
#     optimizer.zero_grad()
#     loss_function(big(few_x), few_y).backward()
#     optimizer.step()
#     big.eval()
#     with torch.no_grad():
#         held = loss_function(big(val_x), val_y).item()
#     if held < best:
#         best, best_epoch, best_state = held, epoch, copy.deepcopy(big.state_dict())
#     elif epoch - best_epoch >= patience:
#         break
# big.load_state_dict(best_state)
# print(f"paró en la época {epoch}; la mejor, la {best_epoch}, con validación {best:.3f}")
