#!/usr/bin/env python3
"""
Ejercicio 3: Crear un Paquete Completo
=======================================
Aprende a estructurar un paquete Python distribuible.

Este archivo contiene las instrucciones y código de ejemplo.
Tu tarea es crear la estructura real del paquete.
"""

print("=== Crear Paquete text-tools ===\n")


# ============================================
# PASO 1: Crear Estructura de Carpetas
# ============================================
print("--- Paso 1: Crear estructura ---")
print("""
Ejecuta estos comandos para crear la estructura:

mkdir -p text-tools/src/text_tools text-tools/tests
cd text-tools
touch pyproject.toml README.md
touch src/text_tools/__init__.py
touch src/text_tools/core.py
touch src/text_tools/transformers.py
touch src/text_tools/cli.py
touch tests/__init__.py tests/test_core.py tests/test_transformers.py
""")


# ============================================
# PASO 2: Contenido de pyproject.toml
# ============================================
print("\n--- Paso 2: pyproject.toml ---")
print("""
Copia este contenido a text-tools/pyproject.toml:

[project]
name = "text-tools"
version = "0.1.0"
description = "Herramientas de transformación de texto"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Tu Nombre", email = "tu@email.com"}
]

dependencies = [
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
]

[project.scripts]
text-tools = "text_tools.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/text_tools"]
""")


# ============================================
# PASO 3: Contenido de __init__.py
# ============================================
print("\n--- Paso 3: src/text_tools/__init__.py ---")
print('''
Copia este contenido:

"""Text Tools - Herramientas de transformación de texto."""

from .core import TextProcessor
from .transformers import (
    to_uppercase,
    to_lowercase,
    reverse_text,
    count_words,
    count_chars,
)

__version__ = "0.1.0"
__all__ = [
    "TextProcessor",
    "to_uppercase",
    "to_lowercase",
    "reverse_text",
    "count_words",
    "count_chars",
]
''')


# ============================================
# PASO 4: Contenido de core.py
# ============================================
print("\n--- Paso 4: src/text_tools/core.py ---")
print('''
Copia este contenido:

"""Funcionalidad principal de text-tools."""

from typing import Callable

class TextProcessor:
    """Procesador de texto con transformaciones encadenables."""

    def __init__(self, text: str = ""):
        self._text = text
        self._history: list[str] = []

    @property
    def text(self) -> str:
        """Texto actual."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Establece nuevo texto."""
        self._text = value
        self._history.append(value)

    def apply(self, transform: Callable[[str], str]) -> "TextProcessor":
        """Aplica una transformación y retorna self para encadenar."""
        self._text = transform(self._text)
        self._history.append(self._text)
        return self

    def reset(self, text: str = "") -> "TextProcessor":
        """Reinicia el procesador con nuevo texto."""
        self._text = text
        self._history = [text] if text else []
        return self

    @property
    def history(self) -> list[str]:
        """Historial de transformaciones."""
        return self._history.copy()

    def __str__(self) -> str:
        return self._text

    def __repr__(self) -> str:
        return f"TextProcessor(text={self._text!r})"
''')


# ============================================
# PASO 5: Contenido de transformers.py
# ============================================
print("\n--- Paso 5: src/text_tools/transformers.py ---")
print('''
Copia este contenido:

"""Funciones de transformación de texto."""

def to_uppercase(text: str) -> str:
    """Convierte texto a mayúsculas."""
    return text.upper()

def to_lowercase(text: str) -> str:
    """Convierte texto a minúsculas."""
    return text.lower()

def reverse_text(text: str) -> str:
    """Invierte el texto."""
    return text[::-1]

def capitalize_words(text: str) -> str:
    """Capitaliza cada palabra."""
    return text.title()

def remove_spaces(text: str) -> str:
    """Elimina espacios."""
    return text.replace(" ", "")

def count_words(text: str) -> int:
    """Cuenta palabras en el texto."""
    return len(text.split())

def count_chars(text: str) -> int:
    """Cuenta caracteres (sin espacios)."""
    return len(text.replace(" ", ""))

def snake_case(text: str) -> str:
    """Convierte a snake_case."""
    return text.lower().replace(" ", "_")

def kebab_case(text: str) -> str:
    """Convierte a kebab-case."""
    return text.lower().replace(" ", "-")
''')


# ============================================
# PASO 6: Contenido de cli.py
# ============================================
print("\n--- Paso 6: src/text_tools/cli.py ---")
print('''
Copia este contenido:

"""Interfaz de línea de comandos para text-tools."""

import click
from . import transformers

@click.group()
@click.version_option()
def main():
    """Text Tools - Herramientas de transformación de texto."""
    pass

@main.command()
@click.argument("text")
def upper(text: str):
    """Convierte texto a mayúsculas."""
    click.echo(transformers.to_uppercase(text))

@main.command()
@click.argument("text")
def lower(text: str):
    """Convierte texto a minúsculas."""
    click.echo(transformers.to_lowercase(text))

@main.command()
@click.argument("text")
def reverse(text: str):
    """Invierte el texto."""
    click.echo(transformers.reverse_text(text))

@main.command()
@click.argument("text")
def count(text: str):
    """Cuenta caracteres y palabras."""
    chars = transformers.count_chars(text)
    words = transformers.count_words(text)
    click.echo(f"Characters: {chars}, Words: {words}")

@main.command()
@click.argument("text")
@click.option("--style", "-s", type=click.Choice(["snake", "kebab"]), default="snake")
def convert(text: str, style: str):
    """Convierte texto a snake_case o kebab-case."""
    if style == "snake":
        result = transformers.snake_case(text)
    else:
        result = transformers.kebab_case(text)
    click.echo(result)

if __name__ == "__main__":
    main()
''')


# ============================================
# PASO 7: Contenido de tests
# ============================================
print("\n--- Paso 7: tests/test_core.py ---")
print('''
Copia este contenido:

"""Tests para el módulo core."""

import pytest
from text_tools.core import TextProcessor
from text_tools import transformers

class TestTextProcessor:
    def test_init_empty(self):
        proc = TextProcessor()
        assert proc.text == ""

    def test_init_with_text(self):
        proc = TextProcessor("hello")
        assert proc.text == "hello"

    def test_apply_transform(self):
        proc = TextProcessor("hello")
        proc.apply(transformers.to_uppercase)
        assert proc.text == "HELLO"

    def test_chained_transforms(self):
        proc = TextProcessor("Hello World")
        result = proc.apply(transformers.to_lowercase).apply(transformers.reverse_text)
        assert result.text == "dlrow olleh"

    def test_history(self):
        proc = TextProcessor("a")
        proc.apply(transformers.to_uppercase)
        proc.apply(transformers.reverse_text)
        assert len(proc.history) == 3  # original + 2 transforms

    def test_reset(self):
        proc = TextProcessor("hello")
        proc.apply(transformers.to_uppercase)
        proc.reset("new text")
        assert proc.text == "new text"
        assert len(proc.history) == 1
''')

print('''
--- tests/test_transformers.py ---

"""Tests para transformers."""

from text_tools import transformers

def test_to_uppercase():
    assert transformers.to_uppercase("hello") == "HELLO"

def test_to_lowercase():
    assert transformers.to_lowercase("HELLO") == "hello"

def test_reverse_text():
    assert transformers.reverse_text("abc") == "cba"

def test_count_words():
    assert transformers.count_words("hello world") == 2
    assert transformers.count_words("one") == 1

def test_count_chars():
    assert transformers.count_chars("hello world") == 10  # sin espacio

def test_snake_case():
    assert transformers.snake_case("Hello World") == "hello_world"

def test_kebab_case():
    assert transformers.kebab_case("Hello World") == "hello-world"
''')


# ============================================
# PASO 8: Instalar y probar
# ============================================
print("\n--- Paso 8: Instalar y probar ---")
print("""
Ejecuta estos comandos dentro de la carpeta text-tools/:

# Instalar dependencias
uv add click
uv add --dev pytest

# Instalar paquete en modo editable
uv pip install -e .

# Probar CLI
text-tools --help
text-tools upper "hello world"
text-tools reverse "python"
text-tools count "hello world"
text-tools convert "Hello World" --style snake

# Ejecutar tests
uv run pytest -v
""")


# ============================================
# DEMOSTRACIÓN (usando código inline)
# ============================================
print("\n--- Demostración inline ---")

# Simular el funcionamiento del paquete
from typing import Callable

class TextProcessor:
    def __init__(self, text: str = ""):
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    def apply(self, transform: Callable[[str], str]) -> "TextProcessor":
        self._text = transform(self._text)
        return self

def to_uppercase(text: str) -> str:
    return text.upper()

def reverse_text(text: str) -> str:
    return text[::-1]

# Usar el procesador
proc = TextProcessor("hello world")
result = proc.apply(to_uppercase).apply(reverse_text)
print(f"Original: 'hello world'")
print(f"Uppercase -> Reverse: '{result.text}'")


# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 50)
print("✅ Ejercicio completado!")
print("=" * 50)
print("""
Conceptos aprendidos:
1. Estructura src/ layout para paquetes distribuibles
2. pyproject.toml como configuración estándar
3. Entry points [project.scripts] para comandos CLI
4. hatchling como build backend moderno
5. uv pip install -e . para desarrollo
6. Tests con pytest para verificar funcionalidad
""")
