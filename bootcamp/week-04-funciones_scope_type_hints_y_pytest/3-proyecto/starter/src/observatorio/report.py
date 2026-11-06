"""Informe de muchas filas: qué líneas cuentan, cuántas hay por nivel y la racha más larga.

Qué: funciones que recorren con un bucle las líneas o las filas ya clasificadas.
Para qué: la capa 1 clasificaba una línea; esta resume un archivo entero de medidas.
Impacto: el resumen por niveles es el primer "análisis" del Observatorio. En la
fase 4 lo hará pandas en una línea; aquí ves qué hay debajo: un bucle y contadores.
"""


def is_data_line(line: str) -> bool:
    """True si la línea trae un registro: no está vacía y no es un comentario.

    Una línea con solo espacios cuenta como vacía. Un comentario empieza por "#",
    aunque tenga espacios delante ("  # nota").
    """
    text = line.strip()
    return text != "" and not text.startswith("#")


def level_of(row: str) -> str:
    """Devuelve el nivel de una fila de format_row: lo que va después de " | ".

    Ejemplo: level_of("Norte               12.5 µg/m³ | medio") da "medio".
    """
    return row.rpartition(" | ")[2]


def summarize(rows: list[str]) -> str:
    """Cuenta las filas por nivel y devuelve una línea de resumen.

    Formato: "registros: 4 | bajo: 1 | medio: 2 | alto: 1 | sin dato: 0".
    Con una lista vacía, todos los contadores son 0.
    """
    low = medium = high = missing = 0
    for row in rows:
        level = level_of(row)
        if level == "bajo":
            low += 1
        elif level == "medio":
            medium += 1
        elif level == "alto":
            high += 1
        else:
            missing += 1
    return (
        f"registros: {len(rows)} | bajo: {low} | medio: {medium} "
        f"| alto: {high} | sin dato: {missing}"
    )


def longest_streak(rows: list[str], level: str) -> int:
    """Devuelve la mayor cantidad de filas seguidas con ese nivel.

    Ejemplo: con niveles alto, alto, medio, alto, longest_streak(rows, "alto") da 2.
    Si ninguna fila tiene ese nivel, da 0.
    """
    best = current = 0
    for row in rows:
        if level_of(row) == level:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best
