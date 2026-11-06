import pytest

from report import current_user, inside_container, is_root, python_version


def test_python_version_is_the_pinned_one() -> None:
    assert python_version() == "3.14.10"


def test_current_user_is_not_empty() -> None:
    assert current_user() != ""


def test_is_root_returns_a_bool() -> None:
    assert isinstance(is_root(), bool)


@pytest.mark.skipif(not inside_container(), reason="solo aplica dentro del contenedor")
def test_container_does_not_run_as_root() -> None:
    # Un proceso root dentro del contenedor tiene más permisos de los que necesita.
    assert not is_root(), "Paso 6: añade un usuario sin privilegios al Dockerfile"
