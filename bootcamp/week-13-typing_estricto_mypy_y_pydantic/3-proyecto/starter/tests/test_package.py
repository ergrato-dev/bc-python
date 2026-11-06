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
    functional,
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
    "functional",
    "groups",
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


def test_version_is_0_13_0() -> None:
    assert observatorio.__version__ == "0.13.0"


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


def test_dev_tools_are_pinned() -> None:
    groups = read_pyproject()["dependency-groups"]
    assert isinstance(groups, dict)
    names = sorted(requirement.split("==")[0] for requirement in groups["dev"])
    assert names == ["mypy", "pytest", "ruff"]
    assert all("==" in requirement for requirement in groups["dev"])


def test_pydantic_is_the_only_pinned_dependency() -> None:
    project = read_pyproject()["project"]
    assert isinstance(project, dict)
    assert project["dependencies"] == ["pydantic==2.14.2"]


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
