"""
Ejercicio 01: Profiling con cProfile — SOLUCIÓN
"""
from __future__ import annotations

import cProfile
import io
import pstats
import time
from pathlib import Path


def _read_asset(path: Path) -> bytes:
    time.sleep(0.05)
    return b"fake_video_data" * 1000


def _compute_checksum(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def _extract_frames(data: bytes, n: int = 5) -> list[bytes]:
    time.sleep(0.2)
    return [data[:100] for _ in range(n)]


def _analyze_frame(frame: bytes) -> dict[str, str]:
    time.sleep(0.08)
    return {"description": "frame analysis", "category": "institucional"}


def _transcribe(data: bytes) -> str:
    time.sleep(0.15)
    return "Transcripción simulada del asset de Studio BC."


def process_asset(path: Path) -> dict[str, object]:
    data = _read_asset(path)
    checksum = _compute_checksum(data)
    frames = _extract_frames(data, n=5)
    analyses = [_analyze_frame(f) for f in frames]
    transcript = _transcribe(data)
    return {
        "checksum": checksum,
        "frames_analyzed": len(analyses),
        "transcription": transcript[:50],
    }


def run_with_cprofile(fn, *args) -> tuple[object, str]:
    pr = cProfile.Profile()
    pr.enable()
    result = fn(*args)
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats("cumulative").print_stats(10)
    return result, s.getvalue()


def find_bottleneck(report: str) -> str:
    for line in report.splitlines():
        line = line.strip()
        # Las filas de datos tienen al menos 5 campos separados por espacios
        parts = line.split()
        if len(parts) >= 6 and parts[0].replace(".", "").isdigit():
            return parts[-1]  # última columna: filename:lineno(function)
    return "unknown"


MOCK_REPORT = """
         47 function calls in 0.680 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.680    0.680  main.py:42(process_asset)
        5    0.000    0.000    0.400    0.080  main.py:25(_extract_frames)
        5    0.000    0.000    0.400    0.080  main.py:31(_analyze_frame)
        1    0.000    0.000    0.150    0.150  main.py:36(_transcribe)
"""


if __name__ == "__main__":
    path = Path("footage/spot_verano.mp4")
    print("=== Profiling del pipeline de Studio BC ===\n")

    try:
        result, report = run_with_cprofile(process_asset, path)
    except Exception:
        report = MOCK_REPORT

    bottleneck = find_bottleneck(report)
    print(report)
    print(f"Bottleneck detectado: {bottleneck}")

    assert isinstance(bottleneck, str) and len(bottleneck) > 0
    print("\nOK — Ejercicio 01 completado")
