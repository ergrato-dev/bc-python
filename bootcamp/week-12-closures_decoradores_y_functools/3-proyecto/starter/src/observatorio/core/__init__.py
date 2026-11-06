"""El núcleo del Observatorio: modelo de registros, análisis y archivos.

Qué: reúne en un solo sitio los nombres públicos de los módulos de core.
Para qué: quien usa el paquete escribe `from observatorio.core import median` sin
saber en qué módulo vive cada función.
Impacto: los módulos se pueden reorganizar por dentro sin romper a quien importa de aquí.
"""

from observatorio.core.analysis import count_level, process_lines, ratio, share
from observatorio.core.groups import (
    LEVELS,
    Record,
    distinct_labels,
    label_means,
    level_counts,
    parse_record,
    records_of,
    top,
    values_by_label,
)
from observatorio.core.model import Measurement, Scale, Series
from observatorio.core.record import MISSING_MARKERS, describe_record, is_valid, parse_value
from observatorio.core.report import is_data_line, level_of, longest_streak, summarize
from observatorio.core.rules import classify, format_row, parse_line
from observatorio.core.sources import (
    CsvFile,
    FileSource,
    LinesSource,
    Source,
    TextFile,
    open_file,
)
from observatorio.core.storage import (
    HEADER,
    DataFileError,
    read_csv,
    read_data,
    read_json,
    read_lines,
    summary_data,
    write_json,
)
from observatorio.core.streams import iter_lines, iter_measurements, running_mean
from observatorio.core.trends import (
    jumps,
    largest_jump,
    median,
    most_common_labels,
    moving_average,
    values_of,
)

# Lo que exporta `from observatorio.core import *` y la lista oficial de la API pública.
__all__ = [
    "HEADER",
    "LEVELS",
    "MISSING_MARKERS",
    "CsvFile",
    "DataFileError",
    "FileSource",
    "LinesSource",
    "Measurement",
    "Record",
    "Scale",
    "Series",
    "Source",
    "TextFile",
    "classify",
    "count_level",
    "describe_record",
    "distinct_labels",
    "format_row",
    "is_data_line",
    "is_valid",
    "iter_lines",
    "iter_measurements",
    "jumps",
    "label_means",
    "largest_jump",
    "level_counts",
    "level_of",
    "longest_streak",
    "median",
    "most_common_labels",
    "moving_average",
    "open_file",
    "parse_line",
    "parse_record",
    "parse_value",
    "process_lines",
    "ratio",
    "read_csv",
    "read_data",
    "read_json",
    "read_lines",
    "records_of",
    "running_mean",
    "share",
    "summarize",
    "summary_data",
    "top",
    "values_by_label",
    "values_of",
    "write_json",
]
