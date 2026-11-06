"""Ejercicio 03: dataclasses.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python dataclasses_lab.py
"""

import json
from dataclasses import FrozenInstanceError, asdict, dataclass, field, fields, replace

print("Ejercicio 03 · dataclasses")

# ============================================
# PASO 1: @dataclass escribe los métodos por ti
# ============================================
# Solo declaras los campos, con su tipo; @dataclass genera __init__, __repr__ y __eq__.
# Descomenta las siguientes líneas:
# @dataclass
# class Station:
#     name: str
#     city: str
#     altitude: int
#
#
# north = Station("Norte", "Lima", 154)
# print(north)
# print("¿Iguales?", north == Station("Norte", "Lima", 154))
# print("Campos:", [f.name for f in fields(Station)])
# north.altitude = 160
# print("Tras cambiarla:", north.altitude)

# ============================================
# PASO 2: valores por defecto
# ============================================
# Descomenta las siguientes líneas:
# @dataclass
# class Sensor:
#     name: str
#     unit: str = "µg/m³"
#     active: bool = True
#
#
# print(Sensor("PM2.5"))
# print(Sensor("Temperatura", "°C", active=False))
#
# try:
#
#     @dataclass
#     class Broken:
#         unit: str = "µg/m³"
#         name: str
#
# except TypeError as error:
#     print("Error:", error)

# ============================================
# PASO 3: una lista por defecto
# ============================================
# Descomenta las siguientes líneas:
# try:
#
#     @dataclass
#     class SharedRoute:
#         stops: list[str] = []
#
# except ValueError as error:
#     print("Error:", error)
#
#
# @dataclass
# class Route:
#     name: str
#     stops: list[str] = field(default_factory=list)
#
#
# morning = Route("Mañana")
# evening = Route("Tarde")
# morning.stops.append("Norte")
# print(morning)
# print(evening)

# ============================================
# PASO 4: __post_init__
# ============================================
# Se ejecuta justo después del __init__ generado: para validar y para calcular campos.
# Descomenta las siguientes líneas:
# @dataclass
# class Reading:
#     label: str
#     value: float
#     level: str = field(init=False)
#
#     def __post_init__(self) -> None:
#         if self.value < 0:
#             raise ValueError(f"lectura negativa en {self.label}: {self.value}")
#         self.level = "alto" if self.value >= 50 else "normal"
#
#
# print(Reading("Norte", 48.9))
# print(Reading("Centro", 61.2))
# try:
#     Reading("Sur", -3.0)
# except ValueError as error:
#     print("Error:", error)

# ============================================
# PASO 5: frozen, order, replace y asdict
# ============================================
# Descomenta las siguientes líneas:
# @dataclass(frozen=True, order=True)
# class Version:
#     major: int
#     minor: int
#     patch: int
#
#
# current = Version(0, 8, 0)
# try:
#     current.minor = 9
# except FrozenInstanceError as error:
#     print("Error:", error)
# following = replace(current, minor=9)
# print("Siguiente:", following, "· la de antes sigue:", current)
# print("Ordenadas:", sorted([Version(1, 0, 0), Version(0, 10, 0), following]))
# print("En un set:", {current, Version(0, 8, 0)})
# print("Como JSON:", json.dumps(asdict(following)))
