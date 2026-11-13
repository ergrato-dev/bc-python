"""Ejercicio 03 · El bucle de entrenamiento: predecir, medir, backward, step.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import warnings

import torch
from torch import nn

print("Ejercicio 03 · El bucle de entrenamiento")

# Doscientas horas de una avenida: miles de vehículos por hora, humedad (%) y PM2.5. Detrás,
# PM2.5 = 6 + 5 · vehículos - 0,1 · (humedad - 60), con ruido. La humedad lava el aire.
torch.manual_seed(34)
vehicles = torch.rand(200, 1) * 4
humidity = 30 + torch.rand(200, 1) * 65
pm25 = 6 + 5 * vehicles - 0.1 * (humidity - 60) + torch.randn(200, 1) * 1.5
print(f"{len(pm25)} horas · PM2.5 de {pm25.min().item():.1f} a {pm25.max().item():.1f}")


def train(model, x, y, optimizer, epochs):
    """Las cuatro líneas de cada época; devuelve la pérdida de la última."""
    loss_function = nn.MSELoss()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_function(model(x), y)
        loss.backward()
        optimizer.step()
    return loss.item()


# ============================================
# PASO 1: Descenso de gradiente a mano
# ============================================
# Descomenta las siguientes líneas:
# w = torch.zeros(1, requires_grad=True)
# b = torch.zeros(1, requires_grad=True)
# for epoch in range(201):
#     loss = ((vehicles * w + b - pm25) ** 2).mean()
#     loss.backward()
#     with torch.no_grad():
#         w -= 0.05 * w.grad
#         b -= 0.05 * b.grad
#     w.grad.zero_()
#     b.grad.zero_()
#     if epoch % 50 == 0:
#         print(f"época {epoch:3}: pérdida {loss.item():7.3f} · w {w.item():.3f} · b {b.item():.3f}")


# ============================================
# PASO 2: El ritmo de aprendizaje
# ============================================
# Descomenta las siguientes líneas:
# for rate in [0.001, 0.01, 0.05, 0.2]:
#     torch.manual_seed(34)
#     model = nn.Linear(1, 1)
#     last = train(model, vehicles, pm25, torch.optim.SGD(model.parameters(), lr=rate), 200)
#     print(f"ritmo {rate:<5}: pérdida tras 200 épocas {last:.3f}")


# ============================================
# PASO 3: Con nn.Linear, MSELoss y SGD
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(34)
# line = nn.Linear(1, 1)
# print("al empezar:", round(line.weight.item(), 3), round(line.bias.item(), 3))
# last = train(line, vehicles, pm25, torch.optim.SGD(line.parameters(), lr=0.05), 2000)
# print(
#     f"tras 2000 épocas: pérdida {last:.3f} · w {line.weight.item():.3f} · b {line.bias.item():.3f}"
# )
# ones = torch.ones(200, 1)
# exact = torch.linalg.lstsq(torch.cat([vehicles, ones], dim=1), pm25).solution
# print(f"mínimos cuadrados:            w {exact[0].item():.3f} · b {exact[1].item():.3f}")


# ============================================
# PASO 4: La forma del objetivo
# ============================================
# Descomenta las siguientes líneas:
# flat = pm25.squeeze(1)
# with warnings.catch_warnings(record=True) as caught:
#     warnings.simplefilter("always")
#     wrong = nn.MSELoss()(line(vehicles), flat)
# right = nn.MSELoss()(line(vehicles), pm25)
# print(f"objetivo {tuple(flat.shape)}: pérdida {wrong.item():.2f} · avisos {len(caught)}")
# print(f"objetivo {tuple(pm25.shape)}: pérdida {right.item():.2f}")
# print("la resta se hace", tuple((line(vehicles) - flat).shape))


# ============================================
# PASO 5: Escalar las entradas
# ============================================
# Descomenta las siguientes líneas:
# both = torch.cat([vehicles * 1000, humidity], dim=1)
# scaled = (both - both.mean(dim=0)) / both.std(dim=0)
# print("medias:", both.mean(dim=0).round(), "· tras escalar:", scaled.mean(dim=0).abs().round())
# for name, inputs in [("sin escalar", both), ("escaladas", scaled)]:
#     torch.manual_seed(34)
#     model = nn.Linear(2, 1)
#     last = train(model, inputs, pm25, torch.optim.SGD(model.parameters(), lr=0.05), 300)
#     print(f"{name:11}: pérdida tras 300 épocas {last:.3f}")


# ============================================
# PASO 6: SGD frente a Adam
# ============================================
# Descomenta las siguientes líneas:
# for rate in [0.001, 0.05, 0.5]:
#     results = []
#     for optimizer_class in [torch.optim.SGD, torch.optim.Adam]:
#         torch.manual_seed(34)
#         model = nn.Linear(2, 1)
#         results.append(
#             train(model, scaled, pm25, optimizer_class(model.parameters(), lr=rate), 300)
#         )
#     print(f"ritmo {rate:<5}: SGD {results[0]:9.3f} · Adam {results[1]:7.3f}")
