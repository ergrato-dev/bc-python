"""Ejercicio 01: clases y objetos.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python objects_lab.py
"""

from sensor import SharedSensor, Sensor

print("Ejercicio 01 · Clases y objetos")

# ============================================
# PASO 1: una clase vacía y sus objetos
# ============================================
# Una clase es un tipo nuevo; cada llamada a la clase crea un objeto distinto.
# Descomenta las siguientes líneas:
# class Station:
#     """Una estación de medida, todavía sin nada dentro."""
#
#
# north = Station()
# south = Station()
# print("Tipo de north:", type(north).__name__)
# print("¿north es una Station?", isinstance(north, Station))
# print("¿north y south son el mismo objeto?", north is south)
# north.city = "Lima"
# print("Atributos de north:", vars(north))
# print("Atributos de south:", vars(south))

# ============================================
# PASO 2: __init__ y self
# ============================================
# Descomenta el PASO 2 de sensor.py y después estas líneas:
# north = Sensor("Norte", "µg/m³")
# south = Sensor("Sur", "µg/m³")
# print("Nombre de north:", north.name)
# print("Atributos de south:", vars(south))
# print("¿Iguales?", Sensor("Este", "°C") == Sensor("Este", "°C"))

# ============================================
# PASO 3: métodos
# ============================================
# Descomenta el PASO 3 de sensor.py y después estas líneas:
# north.record(12.5)
# north.record(48.9)
# south.record(8.0)
# south.record(9.0)
# print(north.summary())
# print(south.summary())
# print("Lo mismo, llamado desde la clase:", Sensor.mean(north))

# ============================================
# PASO 4: atributos de clase
# ============================================
# Descomenta los dos bloques del PASO 4 de sensor.py y después estas líneas:
# print("Sensores creados:", Sensor.created)
# print("Clase de medida de north:", north.kind, "· de south:", south.kind)
# north.kind = "agua"
# print("Tras cambiar north.kind:", north.kind, "·", south.kind, "·", Sensor.kind)
# print("¿kind está en vars(north)?", "kind" in vars(north), "· ¿y en vars(south)?", "kind" in vars(south))

# ============================================
# PASO 5: una lista compartida sin querer
# ============================================
# Descomenta el PASO 5 de sensor.py y después estas líneas:
# east = SharedSensor("Este")
# west = SharedSensor("Oeste")
# east.record(20.0)
# print("Lecturas de west:", west.readings)
# print("¿La misma lista?", east.readings is west.readings)
