"""Ejercicio 01: herencia.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python inheritance_lab.py
"""


class Sensor:
    """La clase base de todo el ejercicio: un sensor con nombre, unidad y lecturas."""

    def __init__(self, name: str, unit: str) -> None:
        self.name = name
        self.unit = unit
        self.readings: list[float] = []

    def record(self, value: float) -> None:
        self.readings.append(value)

    def describe(self) -> str:
        return f"{self.name} ({self.unit})"


print("Ejercicio 01 · herencia")

# ============================================
# PASO 1: una subclase vacía ya sabe hacer cosas
# ============================================
# AirSensor hereda de Sensor: el __init__, record y describe vienen de la base.
# Descomenta las siguientes líneas:
# class AirSensor(Sensor):
#     pass
#
#
# pm25 = AirSensor("Centro", "µg/m³")
# pm25.record(18.5)
# print(pm25.describe(), "·", pm25.readings)
# print("¿Es un AirSensor?", isinstance(pm25, AirSensor), "· ¿Es un Sensor?", isinstance(pm25, Sensor))
# print("¿Un Sensor es un AirSensor?", isinstance(Sensor("Norte", "°C"), AirSensor))

# ============================================
# PASO 2: sustituir un método (override)
# ============================================
# Descomenta las siguientes líneas:
# class LabeledSensor(Sensor):
#     def describe(self) -> str:
#         return f"aire · {self.name} ({self.unit})"
#
#
# print(LabeledSensor("Centro", "µg/m³").describe())
# print(Sensor("Norte", "°C").describe())

# ============================================
# PASO 3: extender con super()
# ============================================
# Descomenta las siguientes líneas:
# class PollutantSensor(Sensor):
#     def __init__(self, name: str, unit: str, pollutant: str) -> None:
#         super().__init__(name, unit)
#         self.pollutant = pollutant
#
#     def describe(self) -> str:
#         return f"{super().describe()} · {self.pollutant}"
#
#
# class ForgetfulSensor(Sensor):
#     def __init__(self, name: str, unit: str, pollutant: str) -> None:
#         self.pollutant = pollutant
#
#
# pm10 = PollutantSensor("Centro", "µg/m³", "PM10")
# pm10.record(41.0)
# print(pm10.describe(), "·", pm10.readings)
# try:
#     ForgetfulSensor("Sur", "µg/m³", "NO2").record(3.0)
# except AttributeError as error:
#     print("Error:", error)

# ============================================
# PASO 4: la MRO y el polimorfismo
# ============================================
# Descomenta las siguientes líneas:
# print("MRO:", [cls.__name__ for cls in PollutantSensor.__mro__])
# print("¿bool hereda de int?", issubclass(bool, int), "· True + True =", True + True)
#
#
# def report(sensors: list[Sensor]) -> None:
#     for sensor in sensors:
#         print(" ", type(sensor).__name__, "->", sensor.describe())
#
#
# report([Sensor("Norte", "°C"), LabeledSensor("Este", "µg/m³"), PollutantSensor("Sur", "ppb", "O3")])

# ============================================
# PASO 5: una jerarquía de excepciones
# ============================================
# Descomenta las siguientes líneas:
# class DataFileError(Exception):
#     """Cualquier problema con un archivo de datos."""
#
#
# class HeaderError(DataFileError):
#     """La cabecera del CSV no es la esperada."""
#
#
# print("MRO:", [cls.__name__ for cls in HeaderError.__mro__])
# for problem in [HeaderError("cabecera inesperada: nombre;dato"), DataFileError("no existe medidas.csv")]:
#     try:
#         raise problem
#     except HeaderError as error:
#         print("Cabecera:", error)
#     except DataFileError as error:
#         print("Archivo:", error)
