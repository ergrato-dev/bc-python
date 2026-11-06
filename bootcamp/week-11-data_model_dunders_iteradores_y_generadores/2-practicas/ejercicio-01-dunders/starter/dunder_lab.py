"""Ejercicio 01: el data model y los dunders.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python dunder_lab.py
"""

from functools import total_ordering

print("Ejercicio 01 · Dunders")

# ============================================
# PASO 1: una clase sin dunders
# ============================================
# Una lectura con etiqueta y valor, escrita a mano (sin dataclass) y sin ningún dunder.
# Descomenta las siguientes líneas:
# class PlainReading:
#     def __init__(self, label: str, value: float) -> None:
#         self.label = label
#         self.value = value
#
#
# plain = PlainReading("Norte", 12.5)
# print("¿Se imprime bien?", "object at 0x" in str(plain))
# print("¿Iguales?", plain == PlainReading("Norte", 12.5))
# print("¿Tiene __eq__ propio?", "__eq__" in vars(PlainReading))

# ============================================
# PASO 2: __repr__ y __str__
# ============================================
# __repr__ es para quien programa; __str__, para quien lee el resultado.
# Descomenta las siguientes líneas:
# class Reading:
#     def __init__(self, label: str, value: float) -> None:
#         self.label = label
#         self.value = value
#
#     def __repr__(self) -> str:
#         return f"Reading({self.label!r}, {self.value!r})"
#
#     def __str__(self) -> str:
#         return f"{self.label}: {self.value} µg/m³"
#
#
# reading = Reading("Norte", 12.5)
# print(reading)
# print(f"En un f-string: {reading}")
# print("repr:", repr(reading))
# print("En una lista:", [reading, Reading("Sur", 8.0)])
# print("Con !r:", f"{reading!r}")

# ============================================
# PASO 3: __eq__ y __hash__
# ============================================
# Descomenta las siguientes líneas:
# class Station:
#     def __init__(self, code: str) -> None:
#         self.code = code
#
#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, Station):
#             return NotImplemented
#         return self.code == other.code
#
#
# print("¿Iguales?", Station("N-01") == Station("N-01"), "· ¿Igual a un str?", Station("N-01") == "N-01")
# print("__hash__ de Station:", Station.__hash__)
# try:
#     {Station("N-01")}
# except TypeError as error:
#     print("Error:", error)
#
#
# class HashableStation(Station):
#     def __hash__(self) -> int:
#         return hash(self.code)
#
#
# codes = {HashableStation("N-01"), HashableStation("N-01"), HashableStation("S-02")}
# print("En un set:", len(codes), "estaciones distintas")

# ============================================
# PASO 4: ordenar con __lt__ y total_ordering
# ============================================
# Descomenta las siguientes líneas:
# @total_ordering
# class Level:
#     NAMES = ("bajo", "medio", "alto")
#
#     def __init__(self, name: str) -> None:
#         self.name = name
#
#     def __repr__(self) -> str:
#         return f"Level({self.name!r})"
#
#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, Level):
#             return NotImplemented
#         return self.name == other.name
#
#     def __lt__(self, other: Level) -> bool:
#         return self.NAMES.index(self.name) < self.NAMES.index(other.name)
#
#
# levels = [Level("alto"), Level("bajo"), Level("medio")]
# print("Ordenados:", sorted(levels))
# print("¿alto >= medio?", Level("alto") >= Level("medio"), "· máximo:", max(levels))
# print("Métodos que añadió total_ordering:", sorted(set(vars(Level)) & {"__le__", "__gt__", "__ge__"}))

# ============================================
# PASO 5: operadores aritméticos y NotImplemented
# ============================================
# Descomenta las siguientes líneas:
# class Distance:
#     def __init__(self, km: float) -> None:
#         self.km = km
#
#     def __repr__(self) -> str:
#         return f"Distance({self.km})"
#
#     def __add__(self, other: Distance) -> Distance:
#         if not isinstance(other, Distance):
#             return NotImplemented
#         return Distance(self.km + other.km)
#
#     def __mul__(self, factor: float) -> Distance:
#         return Distance(self.km * factor)
#
#
# legs = [Distance(1.5), Distance(2.0), Distance(0.5)]
# print("Suma:", legs[0] + legs[1], "· Por 3:", legs[0] * 3)
# try:
#     legs[0] + 1
# except TypeError as error:
#     print("Error:", error)
# try:
#     sum(legs)
# except TypeError as error:
#     print("Error con sum:", error)
#
#
# class SummableDistance(Distance):
#     def __radd__(self, other: object) -> Distance:
#         if other == 0:
#             return self
#         return NotImplemented
#
#
# print("Con __radd__:", sum([SummableDistance(1.5), SummableDistance(2.0), SummableDistance(0.5)]))

# ============================================
# PASO 6: __bool__ y __len__ en un if
# ============================================
# Descomenta las siguientes líneas:
# class Inbox:
#     def __init__(self, messages: list[str]) -> None:
#         self.messages = messages
#
#     def __len__(self) -> int:
#         return len(self.messages)
#
#
# class Alarm:
#     def __init__(self, value: float, limit: float) -> None:
#         self.value = value
#         self.limit = limit
#
#     def __bool__(self) -> bool:
#         return self.value > self.limit
#
#
# for inbox in [Inbox([]), Inbox(["Norte sin dato"])]:
#     print(f"  Inbox con {len(inbox)}:", "hay avisos" if inbox else "vacía")
# print("¿Alarma con 55 sobre 50?", bool(Alarm(55, 50)), "· ¿Con 12?", bool(Alarm(12, 50)))
# print("¿Un objeto sin __bool__ ni __len__?", bool(PlainReading("Sur", 0.0)))
