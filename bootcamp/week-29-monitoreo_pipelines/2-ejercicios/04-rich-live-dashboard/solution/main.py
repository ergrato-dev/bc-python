"""
Ejercicio 04 — Dashboard en Terminal con Rich Live — SOLUCIÓN
=============================================================
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


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


def _error_color(rate: float) -> str:
    if rate < 0.05:
        return "green"
    if rate < 0.15:
        return "yellow"
    return "red"


def _latency_color(p95: float) -> str:
    if p95 < 5.0:
        return "green"
    if p95 < 10.0:
        return "yellow"
    return "red"


def build_metrics_panel(stages: list[FakeMetrics]) -> Panel:
    table = Table(expand=True, show_header=True, header_style="bold cyan")
    table.add_column("Stage", style="cyan", width=14)
    table.add_column("Procesados", justify="right", width=12)
    table.add_column("Errores", justify="right", width=10)
    table.add_column("Error %", justify="right", width=10)
    table.add_column("P95 (s)", justify="right", width=10)

    for m in stages:
        er = m.error_rate
        ec = _error_color(er)
        lc = _latency_color(m.p95_s)
        table.add_row(
            m.stage,
            str(m.processed),
            str(m.errors),
            Text(f"{er:.1%}", style=ec),
            Text(f"{m.p95_s:.2f}", style=lc),
        )
    return Panel(table, title="Métricas por Stage", border_style="blue")


def build_status_panel(stages: list[FakeMetrics], uptime_s: float) -> Panel:
    total_processed = sum(m.processed for m in stages)
    total_errors = sum(m.errors for m in stages)
    global_error_rate = total_errors / max(total_processed, 1)

    if global_error_rate < 0.05:
        status_label, status_color = "OK", "green"
    elif global_error_rate < 0.15:
        status_label, status_color = "DEGRADADO", "yellow"
    else:
        status_label, status_color = "CRÍTICO", "red"

    minutes = int(uptime_s // 60)
    seconds = int(uptime_s % 60)

    text = Text()
    text.append("Estado: ", style="bold")
    text.append(f"{status_label}\n", style=f"bold {status_color}")
    text.append(f"Total procesados: {total_processed}\n")
    text.append(f"Total errores:    {total_errors}\n")
    text.append(f"Error rate:       {global_error_rate:.1%}\n")
    text.append(f"Uptime:           {minutes:02d}:{seconds:02d}")
    return Panel(text, title="Estado Global", border_style=status_color)


def build_layout(stages: list[FakeMetrics], uptime_s: float) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="upper", ratio=7),
        Layout(name="lower", ratio=3),
    )
    layout["upper"].update(build_metrics_panel(stages))
    layout["lower"].update(build_status_panel(stages, uptime_s))
    return layout


def run_dashboard(refresh_per_second: int = 1, max_ticks: int = 30) -> None:
    stages = make_fake_stages()
    start = time.time()

    with Live(screen=True, refresh_per_second=refresh_per_second) as live:
        for _ in range(max_ticks):
            for stage in stages:
                stage.tick()
            uptime = time.time() - start
            live.update(build_layout(stages, uptime))
            time.sleep(1 / refresh_per_second)


if __name__ == "__main__":
    run_dashboard()
