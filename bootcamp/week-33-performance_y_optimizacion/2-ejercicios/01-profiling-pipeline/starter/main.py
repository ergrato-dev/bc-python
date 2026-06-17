"""
Ejercicio 01: Profiling con cProfile
=====================================
Perfila un pipeline simulado de Studio BC con cProfile.
Identifica la función más lenta y propone una optimización.

Ejecutar: python main.py
"""
from __future__ import annotations

import cProfile
import io
import pstats
import time
from pathlib import Path


# ── Pipeline simulado de Studio BC ───────────────────────────────────────────

def _read_asset(path: Path) -> bytes:
    """Simula leer un archivo de video grande."""
    time.sleep(0.05)
    return b"fake_video_data" * 1000


def _compute_checksum(data: bytes) -> str:
    """Calcula checksum del asset."""
    import hashlib
    return hashlib.sha256(data).hexdigest()


def _extract_frames(data: bytes, n: int = 5) -> list[bytes]:
    """Simula extracción de N frames con ffmpeg."""
    time.sleep(0.2)  # ← bottleneck principal
    return [data[:100] for _ in range(n)]


def _analyze_frame(frame: bytes) -> dict[str, str]:
    """Simula análisis de un frame con GPT-4o Vision."""
    time.sleep(0.08)
    return {"description": "frame analysis", "category": "institucional"}


def _transcribe(data: bytes) -> str:
    """Simula transcripción con Whisper."""
    time.sleep(0.15)
    return "Transcripción simulada del asset de Studio BC."


def process_asset(path: Path) -> dict[str, object]:
    """Pipeline completo de procesamiento de un asset."""
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


# ── Funciones a implementar ───────────────────────────────────────────────────

def run_with_cprofile(fn, *args) -> tuple[object, str]:
    """
    Ejecuta fn(*args) bajo cProfile y devuelve (result, report_str).

    TODO:
    1. Crear cProfile.Profile()
    2. pr.enable() → ejecutar fn(*args) → pr.disable()
    3. Usar io.StringIO() + pstats.Stats(pr, stream=s)
    4. Ordenar por "cumulative", imprimir top 10
    5. Retornar (result, s.getvalue())
    """
    raise NotImplementedError


def find_bottleneck(report: str) -> str:
    """
    A partir del reporte de cProfile, extrae el nombre de la función
    con mayor cumtime (la primera línea de stats después del header).

    TODO: parsear el reporte (str.splitlines) y extraer el nombre de función
    de la primera fila de datos.
    """
    raise NotImplementedError


# ── Mock para dry-run ─────────────────────────────────────────────────────────

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
        bottleneck = find_bottleneck(report)
        print(report)
        print(f"Bottleneck detectado: {bottleneck}")
    except NotImplementedError:
        print("(dry-run — usando mock)")
        bottleneck = find_bottleneck(MOCK_REPORT)
        print(MOCK_REPORT)
        print(f"Bottleneck detectado: {bottleneck}")

    assert isinstance(bottleneck, str) and len(bottleneck) > 0
    print("\nOK — Ejercicio 01 completado")
