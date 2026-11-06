"""Un registro del dominio: una medida con su etiqueta y su unidad.

Qué: lectura y presentación de una sola medida.
Para qué: es la pieza más pequeña del Observatorio; las semanas siguientes leen
miles de registros, los guardan en PostgreSQL y los analizan.
Impacto: si una medida vacía se lee como 0 en vez de None, todos los promedios
de la fase 4 salen mal sin dar error.
"""

MISSING_MARKERS = ("", "NA", "N/A", "-")


def parse_value(text: str) -> float | None:
    """Convierte el texto de una medida en float.

    Ignora espacios a los lados y acepta coma decimal ("12,5" da 12.5).
    Devuelve None si el texto es uno de MISSING_MARKERS (dato faltante).
    """
    raise NotImplementedError("Paso 5: implementa parse_value")


def describe_record(label: str, value: float | None, unit: str) -> str:
    """Devuelve "<label>: <value con 1 decimal> <unit>", o "<label>: sin dato" si value es None.

    Ejemplo: describe_record("Estación Norte", 12.54, "µg/m³") da "Estación Norte: 12.5 µg/m³".
    """
    raise NotImplementedError("Paso 6: implementa describe_record")


def is_valid(value: float | None, minimum: float, maximum: float) -> bool:
    """True si value no es None y está entre minimum y maximum, ambos incluidos."""
    raise NotImplementedError("Paso 7: implementa is_valid")
