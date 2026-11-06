"""Funciones pequeñas con bugs escondidos: el código que prueban los tests del ejercicio.

Solo cambiarás la línea que te indique el README en el paso 4.
"""


def to_line(label: str, value: float) -> str:
    """Escribe una medida como línea "etiqueta;valor"."""
    return f"{label};{value}"


def from_line(line: str) -> tuple[str, float]:
    """Lee una línea "etiqueta;valor": la inversa de to_line."""
    label, text = line.split(";")
    return label, float(text)


def chunks(items: list[int], size: int) -> list[list[int]]:
    """Parte items en trozos de size elementos; el último puede ser más corto."""
    return [items[start : start + size] for start in range(0, len(items) - size, size)]


def mean(values: list[float]) -> float:
    """La media de una lista no vacía."""
    return sum(values) / len(values)
