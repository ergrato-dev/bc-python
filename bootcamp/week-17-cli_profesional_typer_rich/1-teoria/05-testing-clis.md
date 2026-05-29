# Testing CLIs con Typer y CliRunner

## Objetivos

- Usar `typer.testing.CliRunner` para tests reproducibles
- Verificar exit codes, output y side effects
- Testear subcomandos, opciones y estados de error
- Integrar con pytest y fixtures

---

## 1. El problema de testear CLIs sin CliRunner

```python
# ❌ Malo — testea la función interna, no la CLI
def test_list_assets_bad():
    result = list_assets("my-project")   # llama directo a la función
    assert "intro.mp4" in result         # no verifica la salida de terminal

# ✅ Correcto — testea como lo haría un usuario real
def test_list_assets():
    runner = CliRunner()
    result = runner.invoke(app, ["assets", "list", "my-project"])
    assert result.exit_code == 0
    assert "intro.mp4" in result.output
```

`CliRunner` captura stdout, stderr y el exit code exactamente como lo vería un usuario en terminal.

---

## 2. Setup básico con pytest

```python
# tests/test_cli.py
import pytest
from typer.testing import CliRunner
from my_app.main import app   # el typer.Typer() raíz

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1" in result.output

def test_unknown_command():
    result = runner.invoke(app, ["nonexistent"])
    assert result.exit_code != 0
```

---

## 3. Testear argumentos y opciones

```python
from typer.testing import CliRunner
from my_app.main import app

runner = CliRunner()

def test_create_project_success():
    result = runner.invoke(app, ["projects", "create", "reel-2025", "--budget", "5000"])
    assert result.exit_code == 0
    assert "reel-2025" in result.output
    assert "5000" in result.output

def test_create_project_invalid_budget():
    result = runner.invoke(app, ["projects", "create", "reel-2025", "--budget", "-100"])
    assert result.exit_code != 0
    # typer/click incluye el error en output o en result.stderr (según versión)

def test_create_project_missing_required():
    result = runner.invoke(app, ["projects", "create"])
    assert result.exit_code != 0
    assert "Missing argument" in result.output or result.exit_code == 2

def test_create_project_invalid_id():
    result = runner.invoke(app, ["projects", "create", "invalid name!"])
    assert result.exit_code != 0
```

---

## 4. Testear con `env` y variables de entorno

```python
def test_uses_env_api_url():
    result = runner.invoke(
        app,
        ["status"],
        env={"BC_API_URL": "https://staging.studio.bc"},
    )
    assert result.exit_code == 0
    assert "staging" in result.output

def test_verbose_flag():
    result = runner.invoke(app, ["--verbose", "status"])
    assert result.exit_code == 0
    assert "Connecting to" in result.output   # solo aparece en verbose
```

---

## 5. Testear I/O de archivos con `mix_stderr` y `tmp_path`

```python
import pytest
from pathlib import Path
from typer.testing import CliRunner
from my_app.main import app

runner = CliRunner(mix_stderr=False)   # separa stderr de stdout

def test_process_file(tmp_path: Path):
    # Crea un archivo temporal de input
    input_file = tmp_path / "assets.json"
    input_file.write_text('[{"name": "intro.mp4", "type": "video"}]')

    result = runner.invoke(app, ["process", str(input_file), "--out", str(tmp_path)])
    assert result.exit_code == 0

    # Verifica que el output fue creado
    assert (tmp_path / "report.json").exists()

def test_process_missing_file():
    result = runner.invoke(app, ["process", "/nonexistent/file.json"])
    assert result.exit_code == 1
    # Con mix_stderr=False, los errores van a result.stderr
    # assert "not found" in result.stderr  (disponible con mix_stderr=False)
```

---

## 6. Fixtures para DRY tests

```python
import pytest
from typer.testing import CliRunner
from my_app.main import app

@pytest.fixture
def cli():
    return CliRunner()

@pytest.fixture
def sample_project(tmp_path):
    """Crea un proyecto temporal en disco para tests."""
    project_dir = tmp_path / "reel-2025"
    project_dir.mkdir()
    (project_dir / "manifest.json").write_text('{"project_id": "reel-2025", "assets": []}')
    return project_dir

def test_project_status(cli, sample_project):
    result = cli.invoke(app, ["projects", "status", str(sample_project)])
    assert result.exit_code == 0
    assert "reel-2025" in result.output

def test_add_asset(cli, sample_project):
    result = cli.invoke(app, [
        "assets", "add", "reel-2025",
        "intro.mp4", "--type", "video",
    ])
    assert result.exit_code == 0
```

---

## 7. Testear prompts interactivos

```python
def test_confirm_delete_yes():
    result = runner.invoke(app, ["projects", "delete", "reel-2025"], input="y\n")
    assert result.exit_code == 0
    assert "Deleted" in result.output

def test_confirm_delete_no():
    result = runner.invoke(app, ["projects", "delete", "reel-2025"], input="n\n")
    assert result.exit_code == 0
    assert "Cancelled" in result.output

def test_prompt_project_name():
    # Simula que el usuario escribe "my-new-project" + Enter
    result = runner.invoke(app, ["projects", "create-interactive"], input="my-new-project\n")
    assert result.exit_code == 0
    assert "my-new-project" in result.output
```

`input` es una cadena que simula la entrada del usuario línea por línea.

---

## ✅ Checklist para tests de CLI

- [ ] Test de `--help` en el comando raíz y cada subcomando
- [ ] Test de éxito con argumentos válidos y verificación de output
- [ ] Test de error con argumentos inválidos o faltantes (exit_code != 0)
- [ ] Test de variables de entorno relevantes
- [ ] Test de confirmaciones (prompts) con `input=`
- [ ] Test de creación/modificación de archivos con `tmp_path`
- [ ] `mix_stderr=False` si la app escribe errores a stderr

---

## Recursos Adicionales

- [Typer — Testing docs](https://typer.tiangolo.com/tutorial/testing/)
- [Click — Testing CLI applications](https://click.palletsprojects.com/testing/)
- [pytest — tmp_path fixture](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
