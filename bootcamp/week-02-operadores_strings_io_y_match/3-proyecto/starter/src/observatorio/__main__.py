"""Punto de entrada: `uv run observatorio "etiqueta;valor"` o sin argumentos para escribir la línea.

Qué: lee una línea (argumento o teclado), la clasifica y escribe la fila.
Para qué: es la primera forma de usar el Observatorio desde la terminal y desde
otros programas (tuberías, scripts, Docker).
Impacto: el código de salida (0, 1 o 2) es lo que leen los scripts y el CI para
saber si la línea era válida.
"""

import sys

from observatorio.rules import parse_line

# Paso 4: cambia la unidad y los umbrales por los de tu dominio.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0

USAGE = 'uso: observatorio ["etiqueta;valor"]'


def main(argv: list[str] | None = None) -> int:
    """Lee una línea, escribe su fila y devuelve el código de salida.

    argv son los argumentos sin el nombre del programa; si es None, se toman de
    sys.argv[1:] (así lo llama `uv run observatorio`; los tests pasan una lista).
    - Sin argumentos: pide la línea con input("Registro (etiqueta;valor): ").
    - "-h" o "--ayuda": escribe USAGE en stdout y devuelve 0.
    - Un argumento: es la línea.
    - Más de uno: USAGE en stderr y devuelve 2.
    Si parse_line devuelve None: "error: línea inválida: '<línea>'" en stderr y
    devuelve 1. Si no, escribe la fila en stdout y devuelve 0.
    """
    raise NotImplementedError("Paso 7: implementa main")


if __name__ == "__main__":
    raise SystemExit(main())
