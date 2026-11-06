"""Pide la última lectura de una estación a un servicio web: el código que prueban los tests.

El servicio no existe (".invalid" es un dominio reservado que nunca resuelve): los
tests no pueden llamarlo de verdad, y no deben. No cambies este archivo.
"""

import json
from datetime import UTC, datetime
from urllib.error import URLError
from urllib.request import urlopen

BASE_URL = "http://observatorio.invalid/api"


class ReadingError(Exception):
    """La lectura no llegó: el servicio no responde."""


def fetch_reading(station: str) -> float:
    """Pide {"value": ...} a BASE_URL/<station> y devuelve el valor como float.

    Si el servicio no responde, lanza ReadingError("sin respuesta de <station>").
    """
    try:
        with urlopen(f"{BASE_URL}/{station}", timeout=5) as response:
            data = json.load(response)
    except URLError as error:
        raise ReadingError(f"sin respuesta de {station}") from error
    return float(data["value"])


def stamp(value: float) -> str:
    """El valor con la hora actual en UTC: "12.5 a las 08:30"."""
    return f"{value} a las {datetime.now(UTC):%H:%M}"
