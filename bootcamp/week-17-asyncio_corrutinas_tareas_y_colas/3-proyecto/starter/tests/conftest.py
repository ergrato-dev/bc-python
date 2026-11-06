"""Fixtures compartidas: pytest las encuentra solo, sin importarlas, en cualquier test de tests/.

Qué: los datos de prueba que se repetían en muchos archivos, escritos una vez.
Para qué: un test pide lo que necesita por el nombre de su parámetro.
Impacto: si cambia cómo se crea una serie de prueba, cambia aquí y no en veinte tests.
"""

from collections.abc import Callable
from pathlib import Path

import pytest

from observatorio.core import Scale, Series


@pytest.fixture
def scale() -> Scale:
    """La escala de los tests: unidad, 10 y 50."""
    return Scale("unidad", 10.0, 50.0)


@pytest.fixture
def lines() -> list[str]:
    """Cinco líneas: un comentario, tres medidas válidas y una inválida."""
    return ["# medidas", "Norte;12,5", "Sur;NA", "malo", "Este;55,1"]


@pytest.fixture
def series(lines: list[str]) -> Series:
    """La serie de las líneas de `lines`: Norte, Sur y Este. Nueva en cada test."""
    return Series.from_lines(lines)


@pytest.fixture
def write_file(tmp_path: Path) -> Callable[[str, str], Path]:
    """Una fábrica: write_file(nombre, texto) crea el archivo en tmp_path y da su ruta."""

    def write(name: str, text: str) -> Path:
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        return path

    return write
