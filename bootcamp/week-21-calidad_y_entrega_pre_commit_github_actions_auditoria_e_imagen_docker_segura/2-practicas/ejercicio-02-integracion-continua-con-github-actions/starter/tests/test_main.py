from main import level


def test_low() -> None:
    assert level(12.5) == "bajo"


def test_medium() -> None:
    assert level(30.0) == "medio"


# ============================================
# PASO 4: Un test que falla en el pull request
# ============================================
# "Alto desde HIGH": 50 tiene que ser alto.
# Descomenta las siguientes líneas:
# def test_high_starts_at_the_limit() -> None:
#     assert level(50.0) == "alto"
