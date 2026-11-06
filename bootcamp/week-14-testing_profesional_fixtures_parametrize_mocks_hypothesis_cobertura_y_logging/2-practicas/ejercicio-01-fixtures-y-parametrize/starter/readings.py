"""Lecturas de una estación: el código que prueban los tests del ejercicio.

No lo cambies: el ejercicio está en tests/.
"""

from dataclasses import dataclass, field
from pathlib import Path


def parse(text: str) -> float | None:
    """Convierte el texto de una lectura: "12,5" da 12.5; "NA" o "" dan None.

    Lanza ValueError si el texto no es un número.
    """
    text = text.strip()
    if text in ("", "NA"):
        return None
    return float(text.replace(",", "."))


@dataclass
class Station:
    """Una estación con sus lecturas, en orden de llegada."""

    name: str
    values: list[float] = field(default_factory=list)

    def add(self, value: float) -> None:
        self.values.append(value)

    def mean(self) -> float:
        """La media de las lecturas. Lanza ValueError si no hay ninguna."""
        if not self.values:
            raise ValueError("sin lecturas")
        return sum(self.values) / len(self.values)


def load(path: Path) -> Station:
    """Lee un archivo: la primera línea es el nombre y las demás, lecturas (salta los NA)."""
    name, *rows = path.read_text(encoding="utf-8").splitlines()
    station = Station(name)
    for row in rows:
        value = parse(row)
        if value is not None:
            station.add(value)
    return station
