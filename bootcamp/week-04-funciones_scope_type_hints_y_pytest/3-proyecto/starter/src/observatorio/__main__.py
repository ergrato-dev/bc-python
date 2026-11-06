"""Punto de entrada: `uv run observatorio "etiqueta;valor" ...` o `uv run observatorio < medidas.txt`.

Qué: lee las líneas, llama a la lógica y escribe el informe.
Para qué: es la única parte del Observatorio que toca la terminal; todo lo demás
son funciones puras que se prueban sin ella.
Impacto: si mañana las líneas llegan de una API o de PostgreSQL, solo cambia este archivo.
"""

import sys

from observatorio.analysis import count_level, process_lines, share
from observatorio.report import longest_streak, summarize

# Tu unidad y tus umbrales de la semana 2.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0

USAGE = 'uso: observatorio ["etiqueta;valor" ...]  o  observatorio < archivo'


def main(argv: list[str] | None = None) -> int:
    """Lee las líneas, escribe filas, errores e informe, y devuelve el código de salida.

    Las opciones y el origen de las líneas son los de la semana 3:
    - "-h" o "--ayuda" solo: USAGE en stdout y devuelve 0.
    - Otra opción que empiece por "-": USAGE en stderr y devuelve 2.
    - Sin argumentos, las líneas son sys.stdin; con argumentos, los argumentos.
    Con process_lines(lines, UNIT, LOW, HIGH):
    - cada fila, en stdout;
    - cada error, en stderr con el prefijo "error: ";
    - después, en stdout: summarize(filas), "racha más larga en alto: <n>" y
      "en alto: <share de las filas en alto sobre el total de filas>".
    Devuelve 1 si hubo errores y 0 si no.
    """
    raise NotImplementedError("Paso 8: implementa main")


if __name__ == "__main__":
    raise SystemExit(main())
