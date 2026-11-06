from collections.abc import Iterator
from pathlib import Path
from typing import TextIO

import pytest

from readings import Station, load, parse


# ============================================
# PASO 1: Una fixture y dos tests que la piden por su nombre
# ============================================
# Descomenta las siguientes líneas:
# @pytest.fixture
# def station() -> Station:
#     return Station("Norte", [12.5, 8.0, 30.5])
#
#
# def test_mean(station: Station) -> None:
#     assert station.mean() == 17.0
#
#
# def test_add(station: Station) -> None:
#     station.add(55.1)
#     assert len(station.values) == 4


# ============================================
# PASO 2: Una fixture que usa otra, y una estación nueva en cada test
# ============================================
# Descomenta las siguientes líneas:
# @pytest.fixture
# def empty(station: Station) -> Station:
#     station.values.clear()
#     return station
#
#
# def test_empty_has_no_mean(empty: Station) -> None:
#     with pytest.raises(ValueError, match="sin lecturas"):
#         empty.mean()
#
#
# def test_station_is_new_in_each_test(station: Station) -> None:
#     assert len(station.values) == 3


# ============================================
# PASO 3: Una fixture con yield: lo de después del yield se ejecuta al terminar el test
# ============================================
# Descomenta las siguientes líneas:
# @pytest.fixture
# def opened(tmp_path: Path) -> Iterator[TextIO]:
#     path = tmp_path / "sur.txt"
#     path.write_text("Sur\n9,5\n", encoding="utf-8")
#     file = path.open(encoding="utf-8")
#     print("\n  abierto")
#     yield file
#     file.close()
#     print("\n  cerrado")
#
#
# def test_first_line_is_the_name(opened: TextIO) -> None:
#     assert opened.readline() == "Sur\n"


# ============================================
# PASO 4: Un test que usa la fixture de conftest.py, sin importarla
# ============================================
# Descomenta las siguientes líneas:
# def test_load_skips_missing_values(sample_file: Path) -> None:
#     station = load(sample_file)
#     assert station == Station("Norte", [12.5, 8.0])


# ============================================
# PASO 5: Un test, muchos casos
# ============================================
# Descomenta las siguientes líneas:
# @pytest.mark.parametrize(
#     ("text", "expected"),
#     [("12,5", 12.5), ("8", 8.0), (" 30.5 ", 30.5), ("NA", None), ("", None)],
# )
# def test_parse(text: str, expected: float | None) -> None:
#     assert parse(text) == expected


# ============================================
# PASO 6: Nombres para los casos y un fallo conocido
# ============================================
# Descomenta las siguientes líneas:
# @pytest.mark.parametrize(
#     "text",
#     [
#         pytest.param("abc", id="letras"),
#         pytest.param("12;5", id="punto-y-coma"),
#         pytest.param("nan", marks=pytest.mark.xfail(reason="float acepta nan")),
#     ],
# )
# def test_parse_rejects(text: str) -> None:
#     with pytest.raises(ValueError):
#         parse(text)


# ============================================
# PASO 7: Una fixture que se crea una vez por archivo, no una vez por test
# ============================================
# Descomenta las siguientes líneas:
# @pytest.fixture(scope="module")
# def stations() -> list[str]:
#     print("\n  creando la lista (cara)")
#     return ["Norte", "Sur", "Este"]
#
#
# @pytest.mark.parametrize("name", ["Norte", "Sur", "Este"])
# def test_known_station(stations: list[str], name: str) -> None:
#     assert name in stations
