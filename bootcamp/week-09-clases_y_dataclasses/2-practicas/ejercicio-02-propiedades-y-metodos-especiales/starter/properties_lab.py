"""Ejercicio 02: propiedades y métodos especiales.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python properties_lab.py
"""

from thermometer import Thermometer

print("Ejercicio 02 · Propiedades y métodos especiales")

kitchen = Thermometer("Cocina", 21.5)

# ============================================
# PASO 1: __repr__ y __str__
# ============================================
# Descomenta las siguientes líneas:
# print(kitchen)
# print(repr(kitchen))
# print([kitchen, Thermometer("Patio", 14.0)])
# print(f"En un f-string: {kitchen} · con !r: {kitchen!r}")

# ============================================
# PASO 2: __eq__
# ============================================
# Descomenta el PASO 2 de thermometer.py y después estas líneas:
# print("¿Iguales?", Thermometer("Patio", 14.0) == Thermometer("Patio", 14.0))
# print("¿Igual a un texto?", kitchen == "Cocina")
# try:
#     print({kitchen})
# except TypeError as error:
#     print("Error:", error)

# ============================================
# PASO 3: una propiedad calculada
# ============================================
# Descomenta el PASO 3 de thermometer.py y después estas líneas:
# print("En Fahrenheit:", kitchen.fahrenheit)
# kitchen.celsius = 30.0
# print("Tras calentarse:", kitchen.fahrenheit)
# try:
#     kitchen.fahrenheit = 100.0
# except AttributeError as error:
#     print("Error:", error)

# ============================================
# PASO 4: una propiedad que valida
# ============================================
# Descomenta el PASO 4 de thermometer.py y después estas líneas:
# print("Atributos de kitchen:", vars(kitchen))
# try:
#     kitchen.celsius = -300.0
# except ValueError as error:
#     print("Error:", error)
# try:
#     Thermometer("Polo", -500.0)
# except ValueError as error:
#     print("Error:", error)
# print("Sigue igual:", kitchen)

# ============================================
# PASO 5: método de clase y método estático
# ============================================
# Descomenta el PASO 5 de thermometer.py y después estas líneas:
# visitor = Thermometer.from_fahrenheit("Houston", 98.6)
# print(visitor)
# print("212 °F son", Thermometer.to_celsius(212.0), "°C")
