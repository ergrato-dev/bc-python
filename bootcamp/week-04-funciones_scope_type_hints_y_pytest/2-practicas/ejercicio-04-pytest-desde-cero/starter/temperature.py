"""Funciones de temperatura para practicar tests. Dos tienen un error a propósito: los tests te dirán cuáles."""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convierte grados Celsius a Fahrenheit: F = C * 9 / 5 + 32."""
    return celsius * 9 / 5 + 32


def average(values: list[float]) -> float:
    """Promedio de values. Lanza ValueError si la lista está vacía."""
    if len(values) == 0:
        raise ValueError("lista vacía: no hay promedio")
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def classify_temperature(celsius: float) -> str:
    """ "frío" por debajo de 15; "templado" desde 15 y por debajo de 25; "calor" desde 25."""
    if celsius < 15:
        return "frío"
    if celsius <= 25:
        return "templado"
    return "calor"


def parse_celsius(text: str) -> float:
    """Convierte "21,5 °C" (o "21.5") en 21.5. Un texto no numérico lanza ValueError."""
    return float(text.removesuffix("°C").strip().replace(",", "."))
