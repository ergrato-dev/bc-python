"""
main.py — Orquestación del Asset Pipeline Async de Studio BC.
No modificar: es el punto de entrada que usa los módulos que debes implementar.
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone

import aiofiles

from src.downloader import MAX_CONCURRENT, download_asset
from src.models import AssetManifest, AssetResult, PipelineReport
from src.processor import process_assets_cpu
from src.reporter import write_report

MANIFEST_PATH = "manifest.json"
OUTPUT_PATH = "output/report.json"


async def load_manifest(path: str) -> AssetManifest:
    async with aiofiles.open(path, encoding="utf-8") as f:
        raw = await f.read()
    data = json.loads(raw)
    return AssetManifest(
        project_id=data["project_id"],
        assets=data["assets"],
    )


async def run_pipeline() -> None:
    manifest = await load_manifest(MANIFEST_PATH)
    print(f"▶ Pipeline: {manifest.project_id} ({len(manifest.assets)} assets)")

    sem = asyncio.Semaphore(MAX_CONCURRENT)
    started_at = datetime.now(tz=timezone.utc).isoformat()
    start = time.perf_counter()

    # Descarga con progreso en tiempo real (as_completed)
    download_coros = [
        download_asset(sem, a["name"], a["url"])
        for a in manifest.assets
    ]

    results: list[AssetResult] = []
    async for coro in asyncio.as_completed(download_coros):
        result = await coro
        elapsed = time.perf_counter() - start
        icon = "✅" if result.status == "ok" else "❌"
        print(f"  [{elapsed:.1f}s] {icon} {result.name}")
        results.append(result)

    # Generación de thumbnails CPU-bound
    asset_types = {a["name"]: a["type"] for a in manifest.assets}
    results = await process_assets_cpu(results, asset_types)

    finished_at = datetime.now(tz=timezone.utc).isoformat()

    report = PipelineReport(
        project_id=manifest.project_id,
        started_at=started_at,
        finished_at=finished_at,
        results=results,
    )

    await write_report(report, OUTPUT_PATH)

    summary = report.summary
    print(f"\n── Reporte ──")
    print(f"  ✅ ok: {summary.get('ok', 0)}")
    print(f"  ❌ failed: {summary.get('failed', 0)}")
    print(f"  ⏱ tiempo total: {time.perf_counter() - start:.2f}s")
    print(f"  💾 guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(run_pipeline())
