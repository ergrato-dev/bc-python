"""Punto de entrada: `uv run observatorio` o `uv run python -m observatorio`."""

from observatorio.record import describe_record, parse_value


def main() -> None:
    # Paso 8: cambia estos tres registros por datos reales de tu dominio.
    print(describe_record("Ejemplo A", parse_value("12,5"), "unidad"))
    print(describe_record("Ejemplo B", parse_value("7"), "unidad"))
    print(describe_record("Ejemplo C", parse_value("NA"), "unidad"))


if __name__ == "__main__":
    main()
