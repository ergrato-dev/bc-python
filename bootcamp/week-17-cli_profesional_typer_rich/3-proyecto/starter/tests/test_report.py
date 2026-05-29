"""Tests del grupo report."""
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()


def test_report_generate_table():
    result = runner.invoke(app, ["report", "generate", "reel-2025", "--format", "table"])
    assert result.exit_code == 0

def test_report_generate_json():
    result = runner.invoke(app, ["report", "generate", "reel-2025", "--format", "json"])
    assert result.exit_code == 0

def test_report_generate_invalid_format():
    result = runner.invoke(app, ["report", "generate", "reel-2025", "--format", "xml"])
    assert result.exit_code != 0

def test_report_nonexistent_project():
    result = runner.invoke(app, ["report", "generate", "nonexistent"])
    assert result.exit_code != 0
