# Tus tests de la semana 15: sustituye este ejemplo por al menos 6 tests tuyos (paso 14).
# Usa CliRunner con datos de tu dominio: un comando con éxito, uno con errores (código 1),
# un archivo que no existe (código 2), stdin con input=, --json y validar.
from typer.testing import CliRunner

from observatorio import cli


def test_example_version_starts_with_the_name() -> None:
    result = CliRunner().invoke(cli.app, ["--version"])
    assert result.stdout.startswith("observatorio ")
