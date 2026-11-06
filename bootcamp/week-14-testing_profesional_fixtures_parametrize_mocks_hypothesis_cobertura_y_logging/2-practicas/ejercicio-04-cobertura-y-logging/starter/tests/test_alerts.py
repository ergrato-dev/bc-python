import logging

import pytest

from alerts import describe, level, summary


# ============================================
# PASO 1: Un solo test
# ============================================
# Descomenta las siguientes líneas:
# def test_level_medio() -> None:
#     assert level(30.0, 10.0, 50.0) == "medio"


# ============================================
# PASO 2: Un test por cada return de level, y summary
# ============================================
# Descomenta las siguientes líneas:
# @pytest.mark.parametrize(
#     ("value", "expected"),
#     [(None, "sin dato"), (5.0, "bajo"), (61.0, "alto")],
# )
# def test_level(value: float | None, expected: str) -> None:
#     assert level(value, 10.0, 50.0) == expected
#
#
# def test_summary_counts_each_level() -> None:
#     counts = summary([12.5, None, 61.0], 10.0, 50.0)
#     assert counts == {"medio": 1, "sin dato": 1, "alto": 1}
#
#
# def test_describe_warns_when_there_is_an_alto() -> None:
#     assert describe({"medio": 2, "alto": 1}) == "alto: 1, medio: 2 (¡atención!)"


# ============================================
# PASO 3: El camino que el informe de ramas echa en falta
# ============================================
# Descomenta las siguientes líneas:
# def test_describe_without_alto() -> None:
#     assert describe({"bajo": 1}) == "bajo: 1"


# ============================================
# PASO 6: Probar lo que se registra con caplog
# ============================================
# Descomenta las siguientes líneas:
# def test_level_logs_a_warning_for_alto(caplog: pytest.LogCaptureFixture) -> None:
#     level(61.0, 10.0, 50.0)
#     assert caplog.messages == ["valor alto: 61.0"]
#     assert caplog.records[0].levelname == "WARNING"
#
#
# def test_summary_logs_info_only_when_asked(caplog: pytest.LogCaptureFixture) -> None:
#     summary([12.5], 10.0, 50.0)
#     assert caplog.messages == []
#     caplog.set_level(logging.INFO, logger="alerts")
#     summary([12.5], 10.0, 50.0)
#     assert caplog.messages == ["1 valores clasificados"]
