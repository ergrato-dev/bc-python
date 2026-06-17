"""PipelineProfiler — wrapper de cProfile para el pipeline de Studio BC."""
from __future__ import annotations

import cProfile
import io
import pstats
from collections.abc import Callable
from typing import Any


class PipelineProfiler:
    def __init__(self, top_n: int = 20) -> None:
        self._top_n = top_n
        self._pr: cProfile.Profile | None = None

    def profile(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Ejecuta fn(*args, **kwargs) bajo cProfile y guarda los resultados.
        Retorna el valor de retorno de fn.

        TODO:
        - self._pr = cProfile.Profile()
        - self._pr.enable()
        - result = fn(*args, **kwargs)
        - self._pr.disable()
        - retornar result

        Referencia: teoría 01 — cProfile básico
        """
        raise NotImplementedError

    def report(self) -> str:
        """
        Genera el reporte de profiling como string.
        Retorna "No profile data. Call profile() first." si no hay datos.

        TODO:
        - Si self._pr es None: retornar el mensaje de error
        - s = io.StringIO()
        - ps = pstats.Stats(self._pr, stream=s)
        - ps.sort_stats("cumulative").print_stats(self._top_n)
        - retornar s.getvalue()

        Referencia: teoría 01 — pstats
        """
        raise NotImplementedError

    def top_functions(self, n: int = 5) -> list[tuple[str, float]]:
        """
        Retorna las N funciones con mayor cumtime como list[(nombre, cumtime)].
        Retorna [] si no hay datos de profiling.

        TODO:
        - Si self._pr es None: retornar []
        - stats = pstats.Stats(self._pr)
        - stats.sort_stats("cumulative")
        - Iterar stats.stats.items() para extraer (func_key, (cc, nc, tt, ct, callers))
        - Construir nombre: f"{func[2]}:{func[1]}:{func[0]}" (función:línea:archivo)
        - Retornar sorted por ct desc [:n]
        """
        raise NotImplementedError
