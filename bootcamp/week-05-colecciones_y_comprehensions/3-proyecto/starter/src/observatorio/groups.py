"""Colecciones del Observatorio: registros como tuplas, conteos y grupos como diccionarios.

Qué: funciones puras que convierten las líneas en registros (etiqueta, valor) y los
agrupan por nivel y por etiqueta.
Para qué: hasta ahora cada fila era un texto ya formateado y el número se perdía;
con los registros puedes calcular medias por etiqueta y ordenar etiquetas.
Impacto: values_by_label es un "group by" escrito a mano. En la semana 24 pandas
lo hace con df.groupby("label")["value"].mean(), y sabrás qué hay debajo.
"""

from collections.abc import Iterable

from observatorio.record import parse_value
from observatorio.report import is_data_line, level_of

# Una tupla y no una lista: los niveles no cambian mientras corre el programa.
LEVELS = ("bajo", "medio", "alto", "sin dato")

# Un registro es una pareja (etiqueta, valor); el valor es None si falta el dato.
Record = tuple[str, float | None]


def parse_record(line: str) -> Record | None:
    """Convierte "etiqueta;valor" en la tupla (etiqueta, valor).

    Mismas reglas que parse_line: quita los espacios de los lados a la etiqueta y
    devuelve None si la línea no tiene exactamente un ";" o si la etiqueta queda vacía.
    Ejemplo: parse_record(" Norte ;12,5") da ("Norte", 12.5); parse_record("Sur;NA")
    da ("Sur", None).
    """
    raise NotImplementedError("Paso 4: implementa parse_record")


def records_of(lines: Iterable[str]) -> list[Record]:
    """Devuelve los registros de las líneas de datos válidas, en orden.

    Salta las líneas que no son de datos (is_data_line) y las inválidas
    (parse_record da None). Quita los espacios de los lados de cada línea.
    """
    raise NotImplementedError("Paso 5: implementa records_of")


def level_counts(rows: list[str]) -> dict[str, int]:
    """Cuenta las filas por nivel: {"bajo": 2, "medio": 2, "alto": 2, "sin dato": 1}.

    Las claves son siempre las de LEVELS, en ese orden, aunque valgan 0.
    """
    raise NotImplementedError("Paso 6: implementa level_counts")


def values_by_label(records: list[Record]) -> dict[str, list[float]]:
    """Agrupa los valores por etiqueta: {"Norte": [12.5, 48.9], "Sur": [8.0, 9.5]}.

    Los valores None no se guardan; una etiqueta que solo tiene None no aparece.
    Las etiquetas quedan en el orden en que aparecen por primera vez.
    """
    raise NotImplementedError("Paso 7: implementa values_by_label")


def label_means(groups: dict[str, list[float]]) -> dict[str, float]:
    """Devuelve la media de cada grupo: {"Norte": 30.7, "Sur": 8.75}.

    Cada lista de groups tiene al menos un valor (así las deja values_by_label).
    """
    raise NotImplementedError("Paso 8: implementa label_means")


def top(means: dict[str, float], n: int) -> list[tuple[str, float]]:
    """Las n parejas (etiqueta, media) con la media más alta, de mayor a menor.

    Con medias iguales, va primero la etiqueta que va antes en orden alfabético.
    Si hay menos de n etiquetas, devuelve todas.
    """
    raise NotImplementedError("Paso 9: implementa top")


def distinct_labels(records: list[Record]) -> set[str]:
    """El conjunto de etiquetas distintas, también las que solo tienen None."""
    raise NotImplementedError("Paso 10: implementa distinct_labels")
