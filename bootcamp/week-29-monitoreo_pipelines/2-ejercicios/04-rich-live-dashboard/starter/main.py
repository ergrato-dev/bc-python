"""
Ejercicio 04 — Dashboard en Terminal con Rich Live

Objetivo: construir un dashboard en vivo con Rich que muestre métricas
de pipeline actualizadas en tiempo real cada segundo.

Pasos:
1. Completar build_metrics_panel() con una Table de Rich
2. Completar build_status_panel() con el estado global
3. Completar build_layout() ensamblando ambos paneles
4. Completar run_dashboard() con el loop Rich Live
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field


try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:
    raise SystemExit("Instala rich: pip install rich")


# ─── Datos simulados ─────────────────────────────────────────────────────────

@dataclass
class FakeMetrics:
    stage: str
    processed: int = 0
    errors: int = 0
    p95_s: float = 0.0
    _base_rate: float = field(default_factory=lambda: random.uniform(0.5, 2.0))

    def tick(self) -> None:
        new = random.randint(1, 5)
        self.processed += new
        if random.random() < 0.05:
            self.errors += 1
        self.p95_s = round(random.uniform(0.1, 12.0), 2)

    @property
    def error_rate(self) -> float:
        return self.errors / max(self.processed, 1)


def make_fake_stages() -> list[FakeMetrics]:
    return [
        FakeMetrics("ingest"),
        FakeMetrics("transcode"),
        FakeMetrics("distribute"),
        FakeMetrics("notify"),
    ]


# ─── Constructores de paneles ─────────────────────────────────────────────────

def build_metrics_panel(stages: list[FakeMetrics]) -> Panel:
    """
    Construye un Panel con una Table que muestra por cada stage:
    - Stage (nombre)
    - Procesados (int)
    - Errores (int)
    - Error % (coloreado: verde <5%, amarillo <15%, rojo ≥15%)
    - P95 (s) (coloreado: verde <5s, amarillo <10s, rojo ≥10s)

    TODO: crear Table con columnas y filas, envolver en Panel(title="Métricas por Stage")
    """
    # TODO: implementar
    raise NotImplementedError


def build_status_panel(stages: list[FakeMetrics], uptime_s: float) -> Panel:
    """
    Construye un Panel con resumen global:
    - Total procesados (suma de todos los stages)
    - Total errores
    - Tasa de error global
    - Uptime formateado (MM:SS)
    - Estado general: "OK" (verde) si error_rate < 0.05, "DEGRADADO" (amarillo) < 0.15,
      "CRÍTICO" (rojo) en caso contrario

    TODO: construir Text con cada línea, envolver en Panel(title="Estado Global")
    """
    # TODO: implementar
    raise NotImplementedError


def build_layout(stages: list[FakeMetrics], uptime_s: float) -> Layout:
    """
    Ensambla el layout:
    - Fila superior (70%): build_metrics_panel
    - Fila inferior (30%): build_status_panel

    TODO: crear Layout, split_column con dos hijos (ratio 7 y 3)
    """
    # TODO: implementar
    raise NotImplementedError


# ─── Loop principal ───────────────────────────────────────────────────────────

def run_dashboard(refresh_per_second: int = 1, max_ticks: int = 30) -> None:
    """
    Ejecuta el dashboard en vivo durante max_ticks iteraciones.

    TODO:
    1. Inicializar stages y start_time
    2. Usar `with Live(screen=True, refresh_per_second=refresh_per_second) as live:`
    3. En cada tick: llamar stage.tick() en todos los stages, calcular uptime,
       llamar live.update(build_layout(stages, uptime)), dormir 1/refresh_per_second
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    run_dashboard()
