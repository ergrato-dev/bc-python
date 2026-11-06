"""Ejercicio 04: elegir el modelo.

La misma medida, "Norte" con 12.5, guardada de cinco formas.
Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python model_lab.py
"""

from dataclasses import dataclass
from typing import NamedTuple

print("Ejercicio 04 · Elegir el modelo")

# ============================================
# PASO 1: una tupla
# ============================================
# Descomenta las siguientes líneas:
# as_tuple = ("Norte", 12.5)
# label, value = as_tuple
# print("Tupla:", as_tuple, "· valor:", as_tuple[1], "· desempaquetada:", label, value)
# try:
#     as_tuple[1] = 13.0
# except TypeError as error:
#     print("Error:", error)

# ============================================
# PASO 2: un diccionario
# ============================================
# Descomenta las siguientes líneas:
# as_dict = {"label": "Norte", "value": 12.5}
# as_dict["value"] = 13.0
# as_dict["unti"] = "µg/m³"
# print("Diccionario:", as_dict)
# try:
#     print(as_dict["valor"])
# except KeyError as error:
#     print("Error: no existe la clave", error)

# ============================================
# PASO 3: una NamedTuple
# ============================================
# Descomenta las siguientes líneas:
# class NamedMeasurement(NamedTuple):
#     label: str
#     value: float | None
#
#
# named = NamedMeasurement("Norte", 12.5)
# print("NamedTuple:", named, "· valor:", named.value, "· también:", named[1])
# print("Desempaquetada:", *named)
# print("¿Igual a la tupla?", named == ("Norte", 12.5))
# try:
#     named.value = 13.0
# except AttributeError as error:
#     print("Error:", error)

# ============================================
# PASO 4: una dataclass
# ============================================
# Descomenta las siguientes líneas:
# @dataclass(frozen=True)
# class Measurement:
#     label: str
#     value: float | None
#
#
# measurement = Measurement("Norte", 12.5)
# print("dataclass:", measurement, "· valor:", measurement.value)
# print("¿Igual a la tupla?", measurement == ("Norte", 12.5))
# try:
#     label, value = measurement
# except TypeError as error:
#     print("Error:", error)

# ============================================
# PASO 5: slots
# ============================================
# Descomenta las siguientes líneas:
# @dataclass
# class Loose:
#     label: str
#     unit: str
#
#
# @dataclass(slots=True)
# class Slotted:
#     label: str
#     unit: str
#
#
# loose = Loose("Norte", "µg/m³")
# loose.unti = "°C"
# print("Sin slots:", loose, "· atributos:", vars(loose))
# slotted = Slotted("Norte", "µg/m³")
# try:
#     slotted.unti = "°C"
# except AttributeError as error:
#     print("Error:", error)
# print("¿Tiene __dict__?", hasattr(loose, "__dict__"), "·", hasattr(slotted, "__dict__"))
