"""Tests del grupo assets."""
import pytest
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()


def test_assets_list_no_filter():
    result = runner.invoke(app, ["assets", "list"])
    assert result.exit_code == 0

def test_assets_list_by_project():
    result = runner.invoke(app, ["assets", "list", "reel-2025"])
    assert result.exit_code == 0
    assert "reel-2025" in result.output or "intro.mp4" in result.output

def test_assets_add_success():
    result = runner.invoke(app, ["assets", "add", "reel-2025", "test.mp4", "--type", "video"])
    assert result.exit_code == 0

def test_assets_add_invalid_project():
    result = runner.invoke(app, ["assets", "add", "nonexistent", "test.mp4"])
    assert result.exit_code != 0

# TODO: añade al menos 2 tests más:
# - assets list con --type filtra correctamente
# - assets remove con confirmación "y" elimina el asset
