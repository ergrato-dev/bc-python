"""La clase Sensor: un sensor con nombre, unidad y las lecturas que va guardando.

objects_lab.py la importa. Descomenta cada PASO de este archivo cuando el README
te lo pida.
"""


class Sensor:
    """Un sensor de una estación de medida."""

    # ============================================
    # PASO 4: atributos de clase
    # ============================================
    # Van dentro de la clase, fuera de los métodos: los comparten todos los sensores.
    # Descomenta las siguientes líneas:
    # kind = "aire"
    # created = 0

    # ============================================
    # PASO 2: __init__ y self
    # ============================================
    # __init__ se ejecuta al crear cada sensor; self es el sensor que se está creando.
    # Descomenta las siguientes líneas:
    # def __init__(self, name: str, unit: str) -> None:
    #     self.name = name
    #     self.unit = unit
    #     self.readings: list[float] = []
    #     print(f"  [creado el sensor {name}]")

    # ============================================
    # PASO 4: contar los sensores creados
    # ============================================
    # Descomenta la siguiente línea (va dentro de __init__, con su sangría):
    #     Sensor.created += 1

    # ============================================
    # PASO 3: métodos
    # ============================================
    # Un método es una función de la clase; recibe el sensor en self.
    # Descomenta las siguientes líneas:
    # def record(self, value: float) -> None:
    #     """Guarda una lectura."""
    #     self.readings.append(value)
    #
    # def mean(self) -> float:
    #     """La media de las lecturas, 0.0 si no hay ninguna."""
    #     if not self.readings:
    #         return 0.0
    #     return sum(self.readings) / len(self.readings)
    #
    # def summary(self) -> str:
    #     return f"{self.name}: {len(self.readings)} lecturas, media {self.mean():.1f} {self.unit}"


class SharedSensor:
    """Un sensor con un error: su lista de lecturas es un atributo de clase."""

    # ============================================
    # PASO 5: una lista compartida sin querer
    # ============================================
    # Descomenta las siguientes líneas:
    # readings: list[float] = []
    #
    # def __init__(self, name: str) -> None:
    #     self.name = name
    #
    # def record(self, value: float) -> None:
    #     self.readings.append(value)
