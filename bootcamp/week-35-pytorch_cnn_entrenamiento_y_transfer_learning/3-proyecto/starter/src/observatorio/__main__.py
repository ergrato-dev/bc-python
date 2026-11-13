"""`python -m observatorio ...` hace lo mismo que el comando `observatorio ...`."""

from observatorio.cli import app

if __name__ == "__main__":
    app(prog_name="observatorio")
