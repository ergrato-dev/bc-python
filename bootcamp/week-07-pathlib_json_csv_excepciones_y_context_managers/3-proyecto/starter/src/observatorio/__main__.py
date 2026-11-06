"""Punto de entrada: `uv run observatorio "etiqueta;valor" ...` o `uv run observatorio < medidas.txt`.

Qué: lee las líneas, llama a la lógica y escribe el informe.
Para qué: es la única parte del Observatorio que toca la terminal; todo lo demás
son funciones puras que se prueban sin ella.
Impacto: si mañana las líneas llegan de una API o de PostgreSQL, solo cambia este archivo.
"""

import sys

from observatorio.analysis import count_level, process_lines, share
from observatorio.groups import distinct_labels, label_means, records_of, top, values_by_label
from observatorio.record import describe_record
from observatorio.report import longest_streak, summarize
from observatorio.trends import largest_jump, median, most_common_labels, moving_average, values_of

# Tu unidad y tus umbrales de la semana 2.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0

TOP = 3
WINDOW = 3

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
    args = sys.argv[1:] if argv is None else argv
    match args:
        case ["-h" | "--ayuda"]:
            print(USAGE)
            return 0
        case [option, *_] if option.startswith("-"):
            print(USAGE, file=sys.stderr)
            return 2
        case []:
            lines = list(sys.stdin)
        case _:
            lines = args
    rows, errors = process_lines(lines, UNIT, LOW, HIGH)
    for row in rows:
        print(row)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    print(summarize(rows))
    print(f"racha más larga en alto: {longest_streak(rows, 'alto')}")
    print(f"en alto: {share(count_level(rows, 'alto'), len(rows))}")
    records = records_of(lines)
    print(f"etiquetas distintas: {len(distinct_labels(records))}")
    print("medias más altas:")
    for label, mean in top(label_means(values_by_label(records)), TOP):
        print(f"  {describe_record(label, mean, UNIT)}")
    print("más frecuentes:")
    for label, count in most_common_labels(records, TOP):
        print(f"  {label}: {count}")
    values = values_of(records)
    if values:
        averages = " · ".join(f"{average:.1f}" for average in moving_average(values, WINDOW))
        print(f"mediana: {median(values):.1f} {UNIT}")
        print(f"media móvil ({WINDOW}): {averages}")
        print(f"mayor salto: {largest_jump(values):+.1f} {UNIT}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
