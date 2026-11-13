"""Tests de la forma del proyecto: el paquete core, su API pública, la versión y pyproject.toml.

No prueban qué calcula el Observatorio, sino cómo está organizado: si alguien mueve
un módulo o se olvida de exportar un nombre, fallan aquí antes que en otro sitio.
"""

import importlib.metadata
import importlib.util
import subprocess
import sys
import tomllib
from pathlib import Path

import observatorio
import observatorio.core
from observatorio.core import (
    batch,
    database,
    functional,
    live,
    model,
    record,
    remote,
    schemas,
    sources,
    storage,
    streams,
    trends,
)

MODULES = [
    "analysis",
    "arrays",
    "batch",
    "charts",
    "clustering",
    "columnar",
    "database",
    "ensembles",
    "etl",
    "findings",
    "frames",
    "functional",
    "groups",
    "inference",
    "learning",
    "live",
    "model",
    "record",
    "remote",
    "report",
    "rules",
    "schemas",
    "sources",
    "storage",
    "streams",
    "summaries",
    "trends",
    "validation",
]

# El pyproject.toml del proyecto: tests/ y pyproject.toml están en la misma raíz.
PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def read_pyproject() -> dict[str, object]:
    with PYPROJECT.open("rb") as file:
        return tomllib.load(file)


def test_version_is_0_33_0() -> None:
    assert observatorio.__version__ == "0.33.0"


def test_version_comes_from_the_installed_metadata() -> None:
    assert observatorio.__version__ == importlib.metadata.version("observatorio")


def test_core_is_a_package() -> None:
    assert hasattr(observatorio.core, "__path__")


def test_every_module_lives_in_core() -> None:
    missing = [
        name for name in MODULES if importlib.util.find_spec(f"observatorio.core.{name}") is None
    ]
    assert missing == []


def test_no_module_is_left_outside_core() -> None:
    left = [
        name for name in MODULES if importlib.util.find_spec(f"observatorio.{name}") is not None
    ]
    assert left == []


def test_core_all_has_no_duplicates() -> None:
    assert len(observatorio.core.__all__) == len(set(observatorio.core.__all__))


def test_every_name_in_core_all_exists() -> None:
    missing = [name for name in observatorio.core.__all__ if not hasattr(observatorio.core, name)]
    assert missing == []


def test_core_all_exports_the_public_api() -> None:
    expected = {
        "DataFileError",
        "Measurement",
        "Record",
        "Scale",
        "Series",
        "Source",
        "TextFile",
        "CsvFile",
        "FileSource",
        "LinesSource",
        "open_file",
        "iter_lines",
        "iter_measurements",
        "running_mean",
        "above",
        "skip_missing",
        "rounded",
        "describe",
        "MeasurementIn",
        "Summary",
        "read_measurements",
        "read_scale",
        "level_counts",
        "median",
        "parse_value",
        "process_lines",
        "read_data",
        "records_of",
        "summary_data",
        "write_json",
        "FileReport",
        "report_file",
        "report_files",
        "replay",
        "watch_file",
        "watch_files",
        "parse_measurements",
        "FetchError",
        "make_client",
        "get_text",
        "target_of",
        "download",
        "download_all",
        "Base",
        "Load",
        "Reading",
        "LoadInfo",
        "LabelStats",
        "make_engine",
        "save_series",
        "load_series",
        "list_loads",
        "label_stats",
        "delete_load",
    }
    assert expected <= set(observatorio.core.__all__)


def test_core_reexports_the_same_objects() -> None:
    assert observatorio.core.parse_value is record.parse_value
    assert observatorio.core.median is trends.median
    assert observatorio.core.DataFileError is storage.DataFileError
    assert observatorio.core.Series is model.Series
    assert observatorio.core.Source is sources.Source
    assert observatorio.core.running_mean is streams.running_mean
    assert observatorio.core.describe is functional.describe
    assert observatorio.core.read_scale is schemas.read_scale
    assert observatorio.core.report_files is batch.report_files
    assert observatorio.core.watch_files is live.watch_files
    assert observatorio.core.download_all is remote.download_all
    assert observatorio.core.save_series is database.save_series


def test_dev_tools_are_pinned() -> None:
    groups = read_pyproject()["dependency-groups"]
    assert isinstance(groups, dict)
    names = sorted(requirement.split("==")[0] for requirement in groups["dev"])
    assert names == [
        "coverage",
        "httpx2",
        "hypothesis",
        "mypy",
        "pandas-stubs",
        "pre-commit",
        "py-spy",
        "pytest",
        "pyyaml",
        "ruff",
        "scipy-stubs",
        "types-pyyaml",
    ]
    assert all("==" in requirement for requirement in groups["dev"])


def test_dependencies_are_pinned() -> None:
    project = read_pyproject()["project"]
    assert isinstance(project, dict)
    assert project["dependencies"] == [
        "alembic==1.20.1",
        "duckdb==2.0.0",
        "fastapi==0.162.0",
        "httpx==0.28.1",
        "matplotlib==3.11.2",
        "numpy==2.5.4",
        "pandas==3.1.0",
        "polars==2.1.0",
        "psycopg[binary]==3.3.6",
        "pydantic==2.14.2",
        "pydantic-settings==2.16.1",
        "rich==15.0.0",
        "scikit-learn==1.9.1",
        "scipy==1.18.1",
        "sqlalchemy==2.1.6",
        "typer==0.27.3",
        "uvicorn==0.54.0",
    ]


def test_the_command_runs_the_typer_application() -> None:
    project = read_pyproject()["project"]
    assert isinstance(project, dict)
    assert project["scripts"] == {"observatorio": "observatorio.cli:app"}


def test_cli_lives_outside_core() -> None:
    # La CLI usa core; core no sabe que existe la CLI.
    assert importlib.util.find_spec("observatorio.cli") is not None
    assert importlib.util.find_spec("observatorio.core.cli") is None


def test_api_lives_outside_core() -> None:
    # La API, como la CLI, es un programa sobre core.
    assert importlib.util.find_spec("observatorio.api") is not None
    assert importlib.util.find_spec("observatorio.core.api") is None


def test_core_does_not_import_fastapi() -> None:
    # core no sabe que la sirve HTTP: se puede usar sin FastAPI.
    code = "import sys, observatorio.core; print('fastapi' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False\n"


def test_settings_live_outside_core() -> None:
    # La configuración la leen los programas (la CLI, la API de la semana 20), no core.
    assert importlib.util.find_spec("observatorio.settings") is not None
    assert importlib.util.find_spec("observatorio.core.settings") is None


def test_ruff_line_length_is_100() -> None:
    tool = read_pyproject()["tool"]
    assert isinstance(tool, dict)
    assert tool["ruff"]["line-length"] == 100


def test_mypy_checks_src_tests_and_migrations() -> None:
    tool = read_pyproject()["tool"]
    assert isinstance(tool, dict)
    assert tool["mypy"]["files"] == ["src", "tests", "migrations"]


def test_mypy_is_strict() -> None:
    tool = read_pyproject()["tool"]
    assert isinstance(tool, dict)
    assert tool["mypy"]["strict"] is True
    assert tool["mypy"]["plugins"] == ["pydantic.mypy"]


def test_coverage_measures_branches_with_a_floor() -> None:
    tool = read_pyproject()["tool"]
    assert isinstance(tool, dict)
    assert tool["coverage"]["run"]["source_pkgs"] == ["observatorio"]
    assert tool["coverage"]["run"]["branch"] is True
    assert tool["coverage"]["report"]["fail_under"] >= 95


def test_migrations_live_outside_the_package() -> None:
    # Alembic las ejecuta desde la raíz del proyecto; no se instalan con el paquete.
    root = PYPROJECT.parent
    assert (root / "alembic.ini").is_file()
    assert (root / "migrations" / "env.py").is_file()
    assert importlib.util.find_spec("observatorio.migrations") is None
