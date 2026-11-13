"""Ejercicio 01 · Tensores: forma, tipo, memoria y broadcasting.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import torch

print("Ejercicio 01 · Tensores")

# Una semana de PM2.5, hora a hora, en tres sensores del Centro: 168 horas x 3 sensores.
# Sube en las horas punta (8 y 19) y el fin de semana baja. Generado con NumPy, en float64,
# como lo daría pandas.
rng = np.random.default_rng(34)
hour = np.arange(168) % 24
day = np.arange(168) // 24
rush = 18 * np.exp(-((hour - 8) ** 2) / 3) + 14 * np.exp(-((hour - 19) ** 2) / 3)
base = 14 + rush * np.where(day >= 5, 0.4, 1.0)
readings = (base[:, None] + rng.normal(0, 2, (168, 3)) + [0.0, 3.0, -2.0]).round(1)
print(f"readings: {type(readings).__name__} {readings.shape} {readings.dtype}")


# ============================================
# PASO 1: Del array al tensor
# ============================================
# Descomenta las siguientes líneas:
# week = torch.tensor(readings)
# print(week.shape, week.dtype, week.device)
# print(week[:2])
# light = week.float()
# print(light.dtype, f"{week.element_size()} bytes por número frente a {light.element_size()}")


# ============================================
# PASO 2: Copiar o compartir
# ============================================
# Descomenta las siguientes líneas:
# shared = torch.from_numpy(readings)
# copied = torch.tensor(readings)
# readings[0, 0] = 999.0
# print(f"compartido {shared[0, 0].item()} · copiado {copied[0, 0].item()}")
# readings[0, 0] = copied[0, 0].item()
# print(f"de vuelta: {shared[0, 0].item()}")


# ============================================
# PASO 3: La forma
# ============================================
# Descomenta las siguientes líneas:
# center = light[:, 0]
# by_day = center.reshape(7, 24)
# print(center.shape, "→", by_day.shape)
# print("martes a las 8:", by_day[1, 8].item())
# print("las 8 de cada día:", by_day[:, 8])
# print(
#     "como columna:",
#     center.unsqueeze(1).shape,
#     "· otra vez fila:",
#     center.reshape(-1, 1).squeeze(1).shape,
# )


# ============================================
# PASO 4: Reducir a lo largo de una dimensión
# ============================================
# Descomenta las siguientes líneas:
# daily = by_day.mean(dim=1)
# hourly = by_day.mean(dim=0)
# print("media de cada día:", daily.round(decimals=1))
# print("hora con la media más alta:", hourly.argmax().item(), f"({hourly.max().item():.1f})")
# print("media de cada sensor:", light.mean(dim=0).round(decimals=1))


# ============================================
# PASO 5: Broadcasting
# ============================================
# Descomenta las siguientes líneas:
# centered = by_day - by_day.mean(dim=1, keepdim=True)
# print(by_day.shape, "-", by_day.mean(dim=1, keepdim=True).shape, "=", centered.shape)
# print("el lunes, de media, tras centrar:", round(centered[0].mean().item(), 4))
# try:
#     by_day - by_day.mean(dim=1)
# except RuntimeError as error:
#     print("sin keepdim:", error)


# ============================================
# PASO 6: Multiplicar matrices
# ============================================
# Descomenta las siguientes líneas:
# weights = torch.tensor([[0.5], [0.25], [0.25]])
# combined = light @ weights
# print(light.shape, "@", weights.shape, "=", combined.shape)
# print("primeras tres horas:", combined[:3].squeeze(1))
# same = np.allclose(combined.squeeze(1).numpy(), readings @ [0.5, 0.25, 0.25], atol=1e-4)
# print("¿lo mismo que NumPy?", same)
