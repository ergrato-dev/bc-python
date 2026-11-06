"""Conversión de unidades: el módulo que importa imports_lab.py.

Un módulo es esto: un archivo .py. Su nombre, sin la extensión, es el nombre del módulo.
"""

# Esta línea se ejecuta cada vez que el archivo se CARGA, no cada vez que se importa.
print(f"  [cargando units.py, __name__ = {__name__!r}]")

KM_PER_MILE = 1.609344


def miles_to_km(miles: float) -> float:
    """Convierte millas a kilómetros."""
    return miles * KM_PER_MILE


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convierte grados Celsius a Fahrenheit."""
    return celsius * 9 / 5 + 32


# Solo cuando ejecutas `uv run python units.py`, no cuando otro archivo lo importa.
if __name__ == "__main__":
    print("units.py ejecutado directamente: prueba rápida")
    print(f"  1 milla = {miles_to_km(1):.3f} km")
