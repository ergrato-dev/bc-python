"""Análisis de un lote de líneas: separar filas y errores, contar y calcular proporciones.

Qué: funciones puras (no leen ni escriben nada) que trabajan con las líneas y las filas.
Para qué: main queda reducido a leer y escribir; toda la lógica se prueba con
llamadas normales, sin capturar la salida.
Impacto: process_lines es la pieza que reutilizarán la lectura de CSV (semana 7),
la CLI con Typer (semana 15) y la API (semana 20): ninguna de ellas usa print.
"""

from collections.abc import Iterable

from observatorio.core.groups import level_counts
from observatorio.core.report import is_data_line
from observatorio.core.rules import parse_line


def process_lines(
    lines: Iterable[str], unit: str, low: float, high: float
) -> tuple[list[str], list[str]]:
    """Clasifica muchas líneas y devuelve (filas, errores), sin imprimir nada.

    Numera las líneas desde 1, contando también las que se saltan. Quita los
    espacios de los lados y salta las que no son líneas de datos. Cada línea válida
    da su fila de parse_line; cada inválida, un error "línea <n>: '<línea>'".
    Ejemplo: process_lines(["# x", "Norte;12,5", "malo"], "u", 10.0, 50.0)
    da ([fila de Norte], ["línea 3: 'malo'"]).
    """
    rows: list[str] = []
    errors: list[str] = []
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not is_data_line(line):
            continue
        row = parse_line(line, unit, low, high)
        if row is None:
            errors.append(f"línea {number}: {line!r}")
        else:
            rows.append(row)
    return rows, errors


def count_level(rows: list[str], level: str) -> int:
    """Cuántas filas tienen ese nivel."""
    return level_counts(rows).get(level, 0)


def ratio(part: int, total: int) -> float:
    """Devuelve part / total, entre 0 y 1. Si total es 0, devuelve 0.0.

    Lanza ValueError si part o total son negativos, o si part es mayor que total:
    una proporción así no tiene sentido y es mejor fallar que devolver un número falso.
    """
    if part < 0 or total < 0 or part > total:
        raise ValueError(f"proporción imposible: {part} de {total}")
    if total == 0:
        return 0.0
    return part / total


def share(part: int, total: int, *, decimals: int = 1) -> str:
    """Devuelve la proporción como porcentaje con texto: share(2, 7) da "28.6 %".

    decimals solo se puede pasar por nombre: share(2, 7, decimals=2) da "28.57 %".
    Los errores de ratio llegan tal cual a quien llama.
    """
    return f"{ratio(part, total) * 100:.{decimals}f} %"
