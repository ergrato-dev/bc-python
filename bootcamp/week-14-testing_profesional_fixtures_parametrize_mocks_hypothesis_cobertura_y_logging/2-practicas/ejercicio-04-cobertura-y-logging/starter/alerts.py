"""Alertas de una estación: el código que miden coverage y los tests. No lo cambies."""

import logging

# El logger de este módulo se llama "alerts", como el módulo.
logger = logging.getLogger(__name__)


def level(value: float | None, low: float, high: float) -> str:
    """El nivel de un valor: "sin dato", "bajo", "medio" o "alto"."""
    if value is None:
        return "sin dato"
    if value < low:
        return "bajo"
    if value > high:
        logger.warning("valor alto: %s", value)
        return "alto"
    return "medio"


def summary(values: list[float | None], low: float, high: float) -> dict[str, int]:
    """Cuántos valores hay de cada nivel."""
    counts: dict[str, int] = {}
    for value in values:
        name = level(value, low, high)
        counts[name] = counts.get(name, 0) + 1
    logger.info("%d valores clasificados", len(values))
    return counts


def describe(counts: dict[str, int]) -> str:
    """Los conteos en una línea, con un aviso si hay algún valor alto."""
    text = ", ".join(f"{name}: {count}" for name, count in sorted(counts.items()))
    if "alto" in counts:
        text += " (¡atención!)"
    return text
