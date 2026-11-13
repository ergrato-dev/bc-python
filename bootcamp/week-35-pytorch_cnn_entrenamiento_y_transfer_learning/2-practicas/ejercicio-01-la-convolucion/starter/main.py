"""Ejercicio 01 · La convolución: filtros que se deslizan.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import torch
import torch.nn.functional as F
from sklearn.datasets import load_digits
from torch import nn

print("Ejercicio 01 · La convolución")

# Un día de PM2.5, hora a hora: sube por la mañana, baja a mediodía, sube por la tarde.
# fmt: off
day = torch.tensor(
    [12, 11, 10, 10, 11, 14, 22, 35, 41, 33, 25, 20,
     18, 17, 18, 21, 27, 36, 39, 31, 24, 19, 15, 13],
    dtype=torch.float32,
)
# fmt: on
print(f"un día: {tuple(day.shape)} valores")

# Un dígito escrito a mano: 8 x 8 píxeles, de 0 (blanco) a 16 (negro).
digit = torch.tensor(load_digits().images[0], dtype=torch.float32)


def draw(image: torch.Tensor) -> None:
    """Una imagen en la terminal: '#' lo muy positivo, '-' lo muy negativo."""
    top = image.abs().max()
    for row in image:
        print(" ".join("#" if v > top / 2 else "-" if v < -top / 2 else "." for v in row))


# ============================================
# PASO 1: Un filtro que se desliza
# ============================================
# Descomenta las siguientes líneas:
# La media de cada tres horas seguidas, a mano: el filtro [1/3, 1/3, 1/3] se desliza.
# kernel = torch.tensor([1 / 3, 1 / 3, 1 / 3])
# by_hand = torch.stack([(day[i : i + 3] * kernel).sum() for i in range(len(day) - 2)])
# print(f"a mano:  {tuple(by_hand.shape)} · {[round(v, 1) for v in by_hand[:5].tolist()]}")

# Lo mismo con conv1d: pide (lotes, canales, longitud) y el filtro (salidas, entradas, tamaño).
# with_torch = F.conv1d(day.reshape(1, 1, -1), kernel.reshape(1, 1, -1))
# print(
#     f"conv1d:  {tuple(with_torch.shape)} · {[round(v, 1) for v in with_torch[0, 0, :5].tolist()]}"
# )
# print(f"¿iguales? {torch.allclose(by_hand, with_torch[0, 0])}")


# ============================================
# PASO 2: Un filtro que detecta subidas
# ============================================
# Descomenta las siguientes líneas:
# [-1, 0, 1]: la hora siguiente menos la anterior. Positivo si sube, negativo si baja.
# rise = F.conv1d(day.reshape(1, 1, -1), torch.tensor([[[-1.0, 0.0, 1.0]]]))[0, 0]
# print(f"subidas: {rise.tolist()}")
# print(f"sube más a las {rise.argmax().item() + 1} h · baja más a las {rise.argmin().item() + 1} h")


# ============================================
# PASO 3: Relleno y paso
# ============================================
# Descomenta las siguientes líneas:
# signal = day.reshape(1, 1, -1)
# for padding, stride in [(0, 1), (1, 1), (0, 2), (1, 3)]:
#     shape = F.conv1d(signal, kernel.reshape(1, 1, -1), padding=padding, stride=stride).shape
#     print(f"padding={padding} stride={stride}: {shape[-1]} valores")


# ============================================
# PASO 4: En dos dimensiones
# ============================================
# Descomenta las siguientes líneas:
# draw(digit)
# vertical = torch.tensor([[-1.0, 0.0, 1.0]] * 3)
# horizontal = vertical.T
# edges = F.conv2d(digit.reshape(1, 1, 8, 8), torch.stack([vertical, horizontal]).unsqueeze(1))
# print(f"bordes: {tuple(edges.shape)}")
# print("verticales:")
# draw(edges[0, 0])
# print("horizontales:")
# draw(edges[0, 1])


# ============================================
# PASO 5: Una capa: muchos filtros que aprende sola
# ============================================
# Descomenta las siguientes líneas:
# torch.manual_seed(35)
# layer = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1)
# maps = layer(digit.reshape(1, 1, 8, 8))
# pooled = nn.MaxPool2d(2)(maps)
# print(f"filtros: {tuple(layer.weight.shape)} · sesgos: {tuple(layer.bias.shape)}")
# print(f"parámetros: {sum(p.numel() for p in layer.parameters())}")
# print(f"mapas: {tuple(maps.shape)} · tras MaxPool2d(2): {tuple(pooled.shape)}")


# ============================================
# PASO 6: Los mismos pesos en todas partes
# ============================================
# Descomenta las siguientes líneas:
# Una capa lineal que diera una salida por píxel: un peso por cada par de píxeles, más
# un sesgo por salida. Se calcula, no se crea: con 224 x 224 no cabría en tu memoria.
# for side in [8, 28, 224]:
#     image = torch.zeros(1, 1, side, side)
#     pixels = side * side
#     print(
#         f"{side:3d} x {side:<3d} · conv: {tuple(layer(image).shape[1:])},"
#         f" {sum(p.numel() for p in layer.parameters())} parámetros"
#         f" · lineal: {pixels * pixels + pixels} parámetros"
#     )
