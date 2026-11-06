"""Punto de entrada: `uv run observatorio "etiqueta;valor" ...`, `uv run observatorio < medidas.txt`
o `uv run observatorio -f medidas.csv -j resumen.json`.

Qué: lee las líneas, llama a la lógica y escribe el informe.
Para qué: es la única parte del Observatorio que toca la terminal; todo lo demás
son funciones puras que se prueban sin ella.
Impacto: si mañana las líneas llegan de una API o de PostgreSQL, solo cambia este archivo.
"""

import sys
from pathlib import Path

from observatorio import __version__
from observatorio.core import (
    DataFileError,
    count_level,
    describe_record,
    distinct_labels,
    label_means,
    largest_jump,
    longest_streak,
    median,
    most_common_labels,
    moving_average,
    process_lines,
    read_data,
    records_of,
    share,
    summarize,
    summary_data,
    top,
    values_by_label,
    values_of,
    write_json,
)

# Tu unidad y tus umbrales de la semana 2.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0

TOP = 3
WINDOW = 3

USAGE = 'uso: observatorio ["etiqueta;valor" ...]  o  observatorio < archivo  o  observatorio -f archivo [-j resumen.json]  o  observatorio --version'


def main(argv: list[str] | None = None) -> int:
    """Lee las líneas, escribe filas, errores e informe, y devuelve el código de salida.

    Las opciones y el origen de las líneas son los de la semana 3:
    - "-h" o "--ayuda" solo: USAGE en stdout y devuelve 0.
    - "-V" o "--version" solo (semana 8): "observatorio <versión>" en stdout y devuelve 0.
    - Otra opción que empiece por "-": USAGE en stderr y devuelve 2.
    - Sin argumentos, las líneas son sys.stdin; con argumentos, los argumentos.
    Y los de la semana 7:
    - "-f RUTA" o "--archivo RUTA": las líneas salen de read_data(Path(RUTA)).
    - Detrás, "-j RUTA" o "--json RUTA": al final guarda summary_data(registros) con
      write_json y escribe "resumen guardado en <RUTA>".
    - Una DataFileError, al leer o al escribir: "error: <mensaje>" en stderr y devuelve 2.
    Con process_lines(lines, UNIT, LOW, HIGH):
    - cada fila, en stdout;
    - cada error, en stderr con el prefijo "error: ";
    - después, en stdout: summarize(filas), "racha más larga en alto: <n>" y
      "en alto: <share de las filas en alto sobre el total de filas>".
    Devuelve 1 si hubo errores y 0 si no.
    """
    args = sys.argv[1:] if argv is None else argv
    source: Path | None = None
    output: Path | None = None
    match args:
        case ["-h" | "--ayuda"]:
            print(USAGE)
            return 0
        case ["-V" | "--version"]:
            print(f"observatorio {__version__}")
            return 0
        case ["-f" | "--archivo", name]:
            source = Path(name)
        case ["-f" | "--archivo", name, "-j" | "--json", summary]:
            source, output = Path(name), Path(summary)
        case [option, *_] if option.startswith("-"):
            print(USAGE, file=sys.stderr)
            return 2
        case []:
            lines = list(sys.stdin)
        case _:
            lines = args
    if source is not None:
        try:
            lines = read_data(source)
        except DataFileError as problem:
            print(f"error: {problem}", file=sys.stderr)
            return 2
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
    if output is not None:
        try:
            write_json(summary_data(records), output)
        except DataFileError as problem:
            print(f"error: {problem}", file=sys.stderr)
            return 2
        print(f"resumen guardado en {output}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
