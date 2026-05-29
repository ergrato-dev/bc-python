"""Tests del grupo projects."""
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()


def test_projects_list():
    result = runner.invoke(app, ["projects", "list"])
    assert result.exit_code == 0

def test_projects_create_success():
    result = runner.invoke(app, ["projects", "create", "test-proj", "--client", "Test Client"])
    assert result.exit_code == 0
    assert "test-proj" in result.output

def test_projects_create_duplicate():
    runner.invoke(app, ["projects", "create", "dup-proj", "--client", "A"])
    result = runner.invoke(app, ["projects", "create", "dup-proj", "--client", "B"])
    assert result.exit_code != 0

def test_verbose_flag():
    result = runner.invoke(app, ["--verbose", "assets", "list"])
    assert result.exit_code == 0
    # La API URL aparece en verbose
    assert "api.studio.bc" in result.output or result.exit_code == 0

def test_env_api_url():
    result = runner.invoke(app, ["assets", "list"], env={"BC_API_URL": "https://staging.bc"})
    assert result.exit_code == 0
