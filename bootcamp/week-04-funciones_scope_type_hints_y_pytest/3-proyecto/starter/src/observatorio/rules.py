"""Reglas del dominio: clasificar una medida y convertir una línea de texto en una fila.

Qué: nivel de cada medida según dos umbrales, y lectura de líneas "etiqueta;valor".
Para qué: la capa 0 leía una medida suelta; esta lee lo que escribe una persona o
lo que llega por una tubería, y lo deja listo para mostrar en columnas.
Impacto: los umbrales deciden qué se considera "alto" en tu dominio. En la fase 4
los informes cuentan registros por nivel, y en la fase 5 un modelo predice el nivel.
"""

from observatorio.record import parse_value


def classify(value: float | None, low: float, high: float) -> str:
    """Devuelve el nivel de value: "sin dato", "bajo", "medio" o "alto".

    "sin dato" si value es None; "bajo" si value < low; "medio" si value < high;
    "alto" en otro caso. Un valor igual a low ya es "medio"; igual a high, "alto".
    """
    if value is None:
        return "sin dato"
    elif value < low:
        return "bajo"
    elif value < high:
        return "medio"
    else:
        return "alto"


def format_row(label: str, value: float | None, unit: str, level: str) -> str:
    """Devuelve una fila de ancho fijo: etiqueta, valor con unidad y nivel.

    La etiqueta ocupa 16 caracteres alineada a la izquierda; el valor con unidad
    ("12.5 µg/m³", con 1 decimal) o "sin dato" ocupa 14 alineado a la derecha;
    después " | " y el nivel.
    Ejemplo: format_row("Norte", 12.54, "µg/m³", "medio")
    da "Norte               12.5 µg/m³ | medio".
    """
    value_text = "sin dato" if value is None else f"{value:.1f} {unit}"
    return f"{label:<16}{value_text:>14} | {level}"


def parse_line(line: str, unit: str, low: float, high: float) -> str | None:
    """Convierte "etiqueta;valor" en la fila de format_row, con su nivel.

    Quita los espacios de los lados a la etiqueta. Devuelve None si la línea no
    tiene exactamente un ";" o si la etiqueta queda vacía.
    Un valor no numérico ("abc") lanza ValueError: lo manejarás en la semana 7.
    """
    match line.split(";"):
        case [label, text] if label.strip():
            value = parse_value(text)
            return format_row(label.strip(), value, unit, classify(value, low, high))
        case _:
            return None
