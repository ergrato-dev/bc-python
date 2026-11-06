import platform

from main import greet, python_summary


def test_greet_uses_the_name() -> None:
    assert greet("Ana") == "Hola, Ana"


def test_greet_without_name_says_hello_world() -> None:
    assert greet("") == "Hola, mundo"


def test_greet_with_only_spaces_says_hello_world() -> None:
    assert greet("   ") == "Hola, mundo"


def test_python_summary_matches_the_interpreter() -> None:
    assert python_summary() == f"Python {platform.python_version()}"


def test_python_is_the_pinned_version() -> None:
    # .python-version fija 3.14.10: si falla, uv está usando otro intérprete.
    assert platform.python_version() == "3.14.10"
