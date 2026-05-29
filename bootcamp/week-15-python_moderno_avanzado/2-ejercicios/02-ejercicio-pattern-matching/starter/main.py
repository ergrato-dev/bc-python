"""
Ejercicio 02: Pattern Matching en Studio BC
Semana 15 — Python Moderno Avanzado
"""

from __future__ import annotations
from dataclasses import dataclass


# ============================================================
# PASO 1: Routing de comandos con literales y OR patterns
# ============================================================
print("=== PASO 1: Routing de comandos ===")

# Descomenta las siguientes líneas:
# def handle_command(command: str) -> str:
#     match command:
#         case "help" | "h" | "--help":
#             return "Comandos: list, add, remove, status"
#         case "list":
#             return "Listando proyectos..."
#         case "add":
#             return "Agregando proyecto..."
#         case "remove":
#             return "Eliminando proyecto..."
#         case "status":
#             return "Estado: 3 proyectos activos"
#         case _:
#             return f"Comando desconocido: {command!r}"
#
# for cmd in ["list", "help", "xyz"]:
#     print(f"{cmd:<6}→ {handle_command(cmd)}")


# ============================================================
# PASO 2: Guards — condiciones adicionales
# ============================================================
print("\n=== PASO 2: Guards ===")

# Descomenta las siguientes líneas:
# def classify_file(filename: str, size_mb: float) -> str:
#     match filename:
#         case name if name.endswith((".mp4", ".mov", ".avi")) and size_mb > 500:
#             return f"video pesado: {name}"
#         case name if name.endswith((".mp4", ".mov", ".avi")):
#             return f"video liviano: {name}"
#         case name if name.endswith((".jpg", ".png", ".webp")):
#             return f"imagen: {name}"
#         case name if name.endswith((".mp3", ".wav", ".flac")):
#             return f"audio: {name}"
#         case _:
#             return f"desconocido: {filename}"
#
# test_files = [
#     ("produccion_final.mp4", 1024.0),
#     ("thumbnail.jpg", 0.5),
#     ("notes.txt", 0.1),
# ]
# for fname, size in test_files:
#     print(classify_file(fname, size))


# ============================================================
# PASO 3: Class patterns con dataclasses
# ============================================================
print("\n=== PASO 3: Class patterns ===")

# Descomenta las siguientes líneas:
# @dataclass
# class VideoAsset:
#     name: str
#     duration_s: float
#     codec: str = "h264"
#
# @dataclass
# class ImageAsset:
#     name: str
#     width: int
#     height: int
#
# @dataclass
# class AudioAsset:
#     name: str
#     duration_s: float
#     bitrate_kbps: int = 128
#
# type StudioAsset = VideoAsset | ImageAsset | AudioAsset
#
# def describe_asset(asset: StudioAsset) -> str:
#     match asset:
#         case VideoAsset(name=n, duration_s=d) if d > 3600:
#             return f"video largo: {n} ({d/3600:.1f}h)"
#         case VideoAsset(name=n, codec="h265"):
#             return f"video HEVC: {n}"
#         case VideoAsset(name=n):
#             return f"video: {n}"
#         case ImageAsset(name=n, width=w, height=h):
#             return f"imagen {w}×{h}: {n}"
#         case AudioAsset(name=n, bitrate_kbps=b) if b >= 320:
#             return f"audio lossless: {n}"
#         case AudioAsset(name=n):
#             return f"audio: {n}"
#
# assets: list[StudioAsset] = [
#     VideoAsset("documental.mp4", duration_s=7560.0),
#     VideoAsset("campana_hevc.mp4", duration_s=30.0, codec="h265"),
#     ImageAsset("banner.png", width=1920, height=1080),
# ]
# for a in assets:
#     print(describe_asset(a))


# ============================================================
# PASO 4: Mapping patterns — eventos del pipeline
# ============================================================
print("\n=== PASO 4: Mapping patterns (pipeline events) ===")

# Descomenta las siguientes líneas:
# def handle_pipeline_event(event: dict[str, object]) -> None:
#     match event:
#         case {"type": "upload_complete", "file": str(path), "size_mb": float(mb)}:
#             print(f"upload OK: {path} ({mb:.1f} MB)")
#         case {"type": "transcode_complete", "output": str(out), **rest}:
#             print(f"transcode OK: {out}, metadata: {rest}")
#         case {"type": "transcode_failed", "error": str(err)}:
#             print(f"transcode error: {err}")
#         case {"type": str(unknown)}:
#             print(f"evento no manejado: {unknown}")
#
# events: list[dict[str, object]] = [
#     {"type": "upload_complete", "file": "/media/raw/video.mp4", "size_mb": 1024.0},
#     {"type": "transcode_failed", "error": "codec not supported"},
#     {"type": "health_check", "status": "ok"},
# ]
# for event in events:
#     handle_pipeline_event(event)
