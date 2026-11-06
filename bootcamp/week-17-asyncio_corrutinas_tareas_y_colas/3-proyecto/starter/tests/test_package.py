"""Tests de la forma del proyecto: el paquete core, su API pública, la versión y pyproject.toml.

No prueban qué calcula el Observatorio, sino cómo está organizado: si alguien mueve
un módulo o se olvida de exportar un nombre, fallan aquí antes que en otro sitio.
"""

import importlib.metadata
import importlib.util
import tomllib
from pathlib import Path

import observatorio
import observatorio.core
from observatorio.core import (
    batch,
    functional,
    live,
    model,
    record,
    schemas,
    sources,
    storage,
    streams,
    trends,
)

MODULES = [
    "analysis",
    "batch",
    "functional",
    "groups",
    "live",
    "model",
    "record",
    "report",
    "rules",
    "schemas",
    "sources",
    "storage",
    "streams",
    "trends",
]

# El pyproject.toml del proyecto: tests/ y pyproject.toml están en la misma raíz.
PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def read_pyproject() -> dict[str, object]:
    with PYPROJECT.open("rb") as file:
        return tomllib.load(file)


def test_version_is_0_17_0() -> None:
    assert observatorio.__version__ == "0.17.0"


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


def test_dev_tools_are_pinned() -> None:
    groups = read_pyproject()["dependency-groups"]
    assert isinstance(groups, dict)
    names = sorted(requirement.split("==")[0] for requirement in groups["dev"])
    assert names == ["coverage", "hypothesis", "mypy", "pytest", "ruff"]
    assert all("==" in requirement for requirement in groups["dev"])


def test_dependencies_are_pinned() -> None:
    project = read_pyproject()["project"]
    assert isinstance(project, dict)
    assert project["dependencies"] == ["pydantic==2.14.2", "rich==15.0.0", "typer==0.27.3"]


def test_the_command_runs_the_typer_application() -> None:
    project = read_pyproject()["project"]
    assert isinstance(project, dict)
    assert project["scripts"] == {"observatorio": "observatorio.cli:app"}


def test_cli_lives_outside_core() -> None:
    # La CLI usa core; core no sabe que existe la CLI.
    assert importlib.util.find_spec("observatorio.cli") is not None
    assert importlib.util.find_spec("observatorio.core.cli") is None


def test_ruff_line_length_is_100() -> None:
    tool = read_pyproject()["tool"]
    assert isinstance(tool, dict)
    assert tool["ruff"]["line-length"] == 100


def test_mypy_checks_src_and_tests() -> None:
    tool = read_pyproject()["tool"]
    assert isinstance(tool, dict)
    assert tool["mypy"]["files"] == ["src", "tests"]


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
