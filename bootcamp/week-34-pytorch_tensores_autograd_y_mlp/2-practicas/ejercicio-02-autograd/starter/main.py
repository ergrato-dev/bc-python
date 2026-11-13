"""Ejercicio 02 · Autograd: gradientes que PyTorch calcula solo.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import torch

print("Ejercicio 02 · Autograd")

# Seis horas de un sensor: la temperatura (°C) y el ozono (µg/m³). Con más sol y calor,
# más ozono: detrás hay una recta, ozono = 3 · temperatura + 10, con un poco de ruido.
temperature = torch.tensor([12.0, 15.0, 18.0, 21.0, 24.0, 27.0])
ozone = torch.tensor([47.0, 54.0, 65.0, 72.0, 83.0, 90.0])
print(f"{len(temperature)} horas · ozono de {ozone.min().item()} a {ozone.max().item()}")


# ============================================
# PASO 1: Una derivada, a mano y con autograd
# ============================================
# Descomenta las siguientes líneas:
# for start in [20.0, 30.0, 45.0]:
#     guess = torch.tensor(start, requires_grad=True)
#     loss = (guess - 30) ** 2
#     loss.backward()
#     by_hand = ((start + 0.001 - 30) ** 2 - (start - 30) ** 2) / 0.001
#     print(f"en {start}: autograd {guess.grad.item():6.1f} · a mano {by_hand:8.3f}")


# ============================================
# PASO 2: Los gradientes de una recta
# ============================================
# Descomenta las siguientes líneas:
# w = torch.tensor(2.0, requires_grad=True)
# b = torch.tensor(0.0, requires_grad=True)
# loss = ((w * temperature + b - ozone) ** 2).mean()
# loss.backward()
# print(f"pérdida {loss.item():.2f} · w.grad {w.grad.item():.2f} · b.grad {b.grad.item():.2f}")
# error = (w * temperature + b - ozone).detach()
# print(f"fórmula: {(2 * error * temperature).mean().item():.2f} · {(2 * error).mean().item():.2f}")


# ============================================
# PASO 3: La regla de la cadena y una neurona apagada
# ============================================
# Descomenta las siguientes líneas:
# for start in [1.5, -1.5]:
#     weight = torch.tensor(start, requires_grad=True)
#     output = torch.relu(weight * 2.0) * 3.0
#     output.backward()
#     print(f"peso {start:4}: salida {output.item():.1f} · gradiente {weight.grad.item():.1f}")


# ============================================
# PASO 4: Los gradientes se acumulan
# ============================================
# Descomenta las siguientes líneas:
# w = torch.tensor(2.0, requires_grad=True)
# for attempt in range(1, 4):
#     loss = ((w * temperature - ozone) ** 2).mean()
#     loss.backward()
#     print(f"backward {attempt}: w.grad {w.grad.item():.2f}")
# w.grad.zero_()
# print(f"tras zero_(): {w.grad.item()}")


# ============================================
# PASO 5: no_grad y detach
# ============================================
# Descomenta las siguientes líneas:
# with torch.no_grad():
#     predicted = w * temperature
# print("dentro de no_grad:", predicted.requires_grad)
# doubled = w * 2
# try:
#     doubled.numpy()
# except RuntimeError as error:
#     print(str(error).split(".")[0])
# print("con detach:", doubled.detach().numpy(), "· con item:", doubled.item())


# ============================================
# PASO 6: Bajar por la pendiente, a mano
# ============================================
# Descomenta las siguientes líneas:
# w = torch.tensor(2.0, requires_grad=True)
# b = torch.tensor(0.0, requires_grad=True)
# for step in range(1, 6):
#     loss = ((w * temperature + b - ozone) ** 2).mean()
#     loss.backward()
#     with torch.no_grad():
#         w -= 0.002 * w.grad
#         b -= 0.002 * b.grad
#     w.grad.zero_()
#     b.grad.zero_()
#     print(f"paso {step}: pérdida {loss.item():7.2f} · w {w.item():.3f} · b {b.item():.3f}")
