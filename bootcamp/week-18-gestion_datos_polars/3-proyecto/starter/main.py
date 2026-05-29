"""main.py — Studio BC KPI Dashboard."""
from __future__ import annotations

from src.pipeline import build_kpi_pipeline, save_outputs
from src.reporter import print_kpi_table, print_alerts

DATA_DIR   = "data"
OUTPUT_DIR = "output"


def main() -> None:
    print("Building KPI pipeline...")
    kpi, trend = build_kpi_pipeline(DATA_DIR)

    print_kpi_table(kpi)
    print_alerts(kpi)

    save_outputs(kpi, trend, OUTPUT_DIR)
    print(f"\nSaved: {OUTPUT_DIR}/kpi_report.parquet · {OUTPUT_DIR}/kpi_report.json")


if __name__ == "__main__":
    main()
