"""Punto de entrada: `uv run observatorio "etiqueta;valor" ...` o `uv run observatorio < medidas.txt`.

Qué: lee muchas líneas (argumentos o entrada estándar), escribe la fila de cada
una y termina con un resumen por niveles.
Para qué: procesar un archivo entero de medidas, no una sola línea.
Impacto: las líneas inválidas van a stderr con su número y no detienen el resto:
un error en la línea 900 no tira las 899 anteriores.
"""

import sys

from observatorio.report import is_data_line, longest_streak, summarize
from observatorio.rules import parse_line

# Tu unidad y tus umbrales de la semana 2.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0

USAGE = 'uso: observatorio ["etiqueta;valor" ...]  o  observatorio < archivo'


def main(argv: list[str] | None = None) -> int:
    """Procesa muchas líneas, escribe filas y resumen, y devuelve el código de salida.

    argv son los argumentos sin el nombre del programa; si es None, se toman de
    sys.argv[1:].
    - "-h" o "--ayuda" solo: USAGE en stdout y devuelve 0.
    - Otra opción que empiece por "-": USAGE en stderr y devuelve 2.
    - Sin argumentos: las líneas se leen de sys.stdin hasta que se acaben.
    - Con argumentos: cada argumento es una línea.
    Para cada línea, numerada desde 1 y sin espacios a los lados:
    - si no es una línea de datos, se salta;
    - si parse_line da None: "error: línea <n>: '<línea>'" en stderr;
    - si no, la fila en stdout.
    Al final, en stdout: summarize(filas) y "racha más larga en alto: <n>".
    Devuelve 1 si hubo alguna línea inválida y 0 si no.
    """
    raise NotImplementedError("Paso 8: implementa main")


if __name__ == "__main__":
    raise SystemExit(main())
