"""El núcleo del Observatorio: modelo de registros, análisis y archivos.

Qué: reúne en un solo sitio los nombres públicos de los módulos de core.
Para qué: quien usa el paquete escribe `from observatorio.core import median` sin
saber en qué módulo vive cada función.
Impacto: los módulos se pueden reorganizar por dentro sin romper a quien importa de aquí.
"""

from observatorio.core.analysis import count_level, process_lines, ratio, share
from observatorio.core.batch import FileReport, report_file, report_files
from observatorio.core.functional import above, describe, rounded, skip_missing
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
from observatorio.core.live import replay, watch_file, watch_files
from observatorio.core.model import Measurement, Scale, Series
from observatorio.core.record import MISSING_MARKERS, describe_record, is_valid, parse_value
from observatorio.core.remote import (
    FetchError,
    download,
    download_all,
    get_text,
    make_client,
    target_of,
)
from observatorio.core.report import is_data_line, level_of, longest_streak, summarize
from observatorio.core.rules import classify, format_row, parse_line
from observatorio.core.schemas import (
    MeasurementIn,
    parse_measurements,
    read_measurements,
    read_scale,
)
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
    Summary,
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
    "FetchError",
    "FileReport",
    "FileSource",
    "LinesSource",
    "Measurement",
    "MeasurementIn",
    "Record",
    "Scale",
    "Series",
    "Source",
    "Summary",
    "TextFile",
    "above",
    "classify",
    "count_level",
    "describe",
    "describe_record",
    "distinct_labels",
    "download",
    "download_all",
    "format_row",
    "get_text",
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
    "make_client",
    "median",
    "most_common_labels",
    "moving_average",
    "open_file",
    "parse_line",
    "parse_measurements",
    "parse_record",
    "parse_value",
    "process_lines",
    "ratio",
    "read_csv",
    "read_data",
    "read_json",
    "read_lines",
    "read_measurements",
    "read_scale",
    "records_of",
    "replay",
    "report_file",
    "report_files",
    "rounded",
    "running_mean",
    "share",
    "skip_missing",
    "summarize",
    "summary_data",
    "target_of",
    "top",
    "values_by_label",
    "values_of",
    "watch_file",
    "watch_files",
    "write_json",
]
