"""Un registro del dominio: una medida con su etiqueta y su unidad.

Qué: lectura y presentación de una sola medida.
Para qué: es la pieza más pequeña del Observatorio; las semanas siguientes leen
miles de registros, los guardan en PostgreSQL y los analizan.
Impacto: si una medida vacía se lee como 0 en vez de None, todos los promedios
de la fase 4 salen mal sin dar error.
"""

import math

MISSING_MARKERS = ("", "NA", "N/A", "-")


def parse_value(text: str) -> float | None:
    """Convierte el texto de una medida en float.

    Ignora espacios a los lados y acepta coma decimal ("12,5" da 12.5).
    Devuelve None si el texto es uno de MISSING_MARKERS (dato faltante).
    Lanza ValueError si no es un número o si no es finito ("nan", "inf"): float los
    acepta, pero una medida infinita no existe y un nan estropea medianas y medias.
    """
    text = text.strip()
    if text in MISSING_MARKERS:
        return None
    value = float(text.replace(",", "."))
    if not math.isfinite(value):
        raise ValueError(f"valor no finito: {text!r}")
    return value


def describe_record(label: str, value: float | None, unit: str) -> str:
    """Devuelve "<label>: <value con 1 decimal> <unit>", o "<label>: sin dato" si value es None.

    Ejemplo: describe_record("Estación Norte", 12.54, "µg/m³") da "Estación Norte: 12.5 µg/m³".
    """
    if value is None:
        return f"{label}: sin dato"
    return f"{label}: {value:.1f} {unit}"


def is_valid(value: float | None, minimum: float, maximum: float) -> bool:
    """True si value no es None y está entre minimum y maximum, ambos incluidos."""
    return value is not None and minimum <= value <= maximum
