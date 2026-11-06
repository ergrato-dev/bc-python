"""La clase Thermometer: un termómetro con nombre y temperatura en grados Celsius.

properties_lab.py la importa. Descomenta cada PASO de este archivo cuando el README
te lo pida.
"""

# El cero absoluto: no hay temperaturas más bajas.
ABSOLUTE_ZERO = -273.15


class Thermometer:
    """Un termómetro de una casa o una estación."""

    def __init__(self, name: str, celsius: float) -> None:
        self.name = name
        self.celsius = celsius

    # ============================================
    # PASO 1: __repr__ y __str__
    # ============================================
    # __repr__ es para quien programa; __str__, para quien lee el resultado.
    # Descomenta las siguientes líneas:
    # def __repr__(self) -> str:
    #     return f"Thermometer({self.name!r}, {self.celsius!r})"
    #
    # def __str__(self) -> str:
    #     return f"{self.name}: {self.celsius} °C"

    # ============================================
    # PASO 2: __eq__
    # ============================================
    # Dos termómetros son iguales si tienen el mismo nombre y la misma temperatura.
    # Descomenta las siguientes líneas:
    # def __eq__(self, other: object) -> bool:
    #     if not isinstance(other, Thermometer):
    #         return NotImplemented
    #     return (self.name, self.celsius) == (other.name, other.celsius)

    # ============================================
    # PASO 3: una propiedad calculada
    # ============================================
    # Se lee como un atributo, pero cada vez ejecuta el método.
    # Descomenta las siguientes líneas:
    # @property
    # def fahrenheit(self) -> float:
    #     return round(self.celsius * 9 / 5 + 32, 1)

    # ============================================
    # PASO 4: una propiedad que valida
    # ============================================
    # El valor de verdad se guarda en self._celsius; el guion bajo dice "es interno".
    # Descomenta las siguientes líneas:
    # @property
    # def celsius(self) -> float:
    #     return self._celsius
    #
    # @celsius.setter
    # def celsius(self, value: float) -> None:
    #     if value < ABSOLUTE_ZERO:
    #         raise ValueError(f"temperatura imposible: {value} °C (mínimo {ABSOLUTE_ZERO})")
    #     self._celsius = value

    # ============================================
    # PASO 5: método de clase y método estático
    # ============================================
    # Descomenta las siguientes líneas:
    # @classmethod
    # def from_fahrenheit(cls, name: str, fahrenheit: float) -> Thermometer:
    #     """Otra forma de crear un termómetro: a partir de grados Fahrenheit."""
    #     return cls(name, cls.to_celsius(fahrenheit))
    #
    # @staticmethod
    # def to_celsius(fahrenheit: float) -> float:
    #     """Convierte grados Fahrenheit a Celsius. No usa ni self ni cls."""
    #     return round((fahrenheit - 32) * 5 / 9, 1)
