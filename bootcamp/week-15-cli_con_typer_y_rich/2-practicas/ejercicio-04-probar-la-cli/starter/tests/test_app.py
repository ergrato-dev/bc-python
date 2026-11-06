"""Tests de app.py con CliRunner: la CLI se ejecuta dentro del test, sin otro proceso."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from app import app

runner = CliRunner()


# ============================================
# PASO 1: Ejecutar un comando y mirar el resultado
# ============================================
# Descomenta las siguientes líneas:
# def test_clasificar_one_value() -> None:
#     result = runner.invoke(app, ["clasificar", "30"])
#     assert result.exit_code == 0
#     assert result.stdout == "30 → medio\n"


# ============================================
# PASO 2: stderr y los códigos de salida
# ============================================
# Descomenta las siguientes líneas:
# def test_a_high_value_warns_on_stderr_with_code_1() -> None:
#     result = runner.invoke(app, ["clasificar", "12", "61"])
#     assert result.exit_code == 1
#     assert result.stdout == "12 → medio\n61 → alto\n"
#     assert result.stderr == "aviso: 1 valores altos\n"
#
#
# def test_a_value_that_is_not_a_number_is_a_usage_error() -> None:
#     result = runner.invoke(app, ["clasificar", "doce"])
#     assert result.exit_code == 2
#     assert "is not a valid float" in result.stderr
#     assert result.stdout == ""


# ============================================
# PASO 3: stdin con input=
# ============================================
# Descomenta las siguientes líneas:
# def test_clasificar_reads_stdin() -> None:
#     result = runner.invoke(app, ["clasificar"], input="5\n\n30\n")
#     assert result.exit_code == 0
#     assert result.stdout == "5 → bajo\n30 → medio\n"


# ============================================
# PASO 4: Archivos de verdad con tmp_path
# ============================================
# Descomenta las siguientes líneas:
# def test_contar_counts_lines_with_data(tmp_path: Path) -> None:
#     path = tmp_path / "medidas.txt"
#     path.write_text("12\n\n30\n61\n", encoding="utf-8")
#     result = runner.invoke(app, ["contar", str(path)])
#     assert result.stdout == "medidas.txt: 3 líneas con datos\n"
#
#
# def test_contar_a_missing_file(tmp_path: Path) -> None:
#     result = runner.invoke(app, ["contar", str(tmp_path / "no-existe.txt")])
#     assert result.exit_code == 2
#     assert "does not exist" in result.stderr


# ============================================
# PASO 5: Un caso por nivel
# ============================================
# Descomenta las siguientes líneas:
# @pytest.mark.parametrize(
#     ("value", "expected"), [("5", "bajo"), ("30", "medio"), ("61", "alto")]
# )
# def test_each_level(value: str, expected: str) -> None:
#     result = runner.invoke(app, ["clasificar", value])
#     assert result.stdout == f"{value} → {expected}\n"


# ============================================
# PASO 6: Los bordes, que el paso 5 no miraba
# ============================================
# Descomenta las siguientes líneas:
# @pytest.mark.parametrize(
#     ("value", "expected"),
#     [("9.9", "bajo"), ("10", "medio"), ("50", "medio"), ("50.1", "alto")],
# )
# def test_the_thresholds_are_medio(value: str, expected: str) -> None:
#     result = runner.invoke(app, ["clasificar", value])
#     assert result.stdout == f"{value} → {expected}\n"
