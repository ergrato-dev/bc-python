# Tus tests de la semana 22: sustituye este ejemplo por al menos 6 tests tuyos (paso 16).
# Usa las funciones de test_performance.py (calls_of, profiled_informe, lines_of,
# table_rows): que informe pinte las filas de --filas y no más, que analice cada línea una
# vez también con errores, que Series.parse dé lo mismo que process_lines con tus datos,
# que el generador ponga algún "NA" (el mutante que sobrevive)...
from test_performance import calls_of, lines_of, profiled_informe

from observatorio.core import parse_record


def test_example_informe_reads_each_line_once_with_five_rows() -> None:
    result, profiler = profiled_informe(["-n", "5", *lines_of(30)])
    assert result.exit_code == 0
    assert calls_of(profiler, parse_record) == 30
