"""
Ejercicio 04: TypeGuard y Narrowing
Semana 15 — Python Moderno Avanzado
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import TypeGuard


# ============================================================
# PASO 1: El problema sin TypeGuard
# ============================================================
print("=== PASO 1: Sin TypeGuard — narrowing manual ===")

# Descomenta las siguientes líneas:
# @dataclass
# class Asset:
#     name: str
#     file_path: str
#     asset_type: str
#
# def process_no_guard(items: list[object]) -> None:
#     for item in items:
#         if hasattr(item, "name") and hasattr(item, "file_path"):
#             # mypy reportaría: error: "object" has no attribute "name"
#             # porque hasattr no le informa al type checker del tipo exacto
#             print(getattr(item, "name"))   # usamos getattr para evitar el error en runtime
#
# print("sin TypeGuard, mypy no puede verificar el tipo dentro del if")


# ============================================================
# PASO 2: TypeGuard — narrowing explícito
# ============================================================
print("\n=== PASO 2: Con TypeGuard ===")

# Descomenta las siguientes líneas:
# def is_asset(obj: object) -> TypeGuard[Asset]:
#     return (
#         hasattr(obj, "name")
#         and hasattr(obj, "file_path")
#         and hasattr(obj, "asset_type")
#         and isinstance(getattr(obj, "name"), str)
#         and isinstance(getattr(obj, "file_path"), str)
#     )
#
# mixed_items: list[object] = [
#     Asset("video_hero.mp4", "/media/hero.mp4", "video"),
#     "un string cualquiera",
#     42,
#     Asset("banner.png", "/media/banner.png", "image"),
#     Asset("jingle.mp3", "/media/jingle.mp3", "audio"),
# ]
#
# valid_assets = [item for item in mixed_items if is_asset(item)]
# print(f"Procesando {len(valid_assets)} assets válidos de {len(mixed_items)} objetos")
# for asset in valid_assets:
#     print(f"name: {asset.name:<20} | path: {asset.file_path}")  # ✅ mypy OK


# ============================================================
# PASO 3: TypeGuard para discriminar tipos de Asset
# ============================================================
print("\n=== PASO 3: TypeGuard para discriminar tipos ===")

# Descomenta las siguientes líneas:
# @dataclass
# class VideoAsset:
#     name: str
#     file_path: str
#     asset_type: str = "video"
#     codec: str = "h264"
#
# @dataclass
# class ImageAsset:
#     name: str
#     file_path: str
#     asset_type: str = "image"
#     width: int = 0
#     height: int = 0
#
# type StudioAsset = VideoAsset | ImageAsset
#
# def is_video(asset: StudioAsset) -> TypeGuard[VideoAsset]:
#     return isinstance(asset, VideoAsset)
#
# def is_image(asset: StudioAsset) -> TypeGuard[ImageAsset]:
#     return isinstance(asset, ImageAsset)
#
# def route_to_pipeline(asset: StudioAsset) -> str:
#     if is_video(asset):
#         return f"video pipeline: {asset.codec}"          # ✅ VideoAsset aquí
#     if is_image(asset):
#         return f"image pipeline: {asset.width}x{asset.height}"  # ✅ ImageAsset aquí
#     return "default pipeline"
#
# assets: list[StudioAsset] = [
#     VideoAsset("hero.mp4", "/media/hero.mp4", codec="h264"),
#     ImageAsset("banner.png", "/media/banner.png", width=1920, height=1080),
# ]
# for a in assets:
#     print(route_to_pipeline(a))


# ============================================================
# PASO 4: TypeGuard con validación compleja
# ============================================================
print("\n=== PASO 4: TypeGuard con validación compleja ===")

# Descomenta las siguientes líneas:
# def is_uploadable(obj: object) -> TypeGuard[Asset]:
#     if not (hasattr(obj, "asset_type") and hasattr(obj, "file_path") and hasattr(obj, "name")):
#         return False
#     file_path = getattr(obj, "file_path")
#     return isinstance(file_path, str) and len(file_path) > 0 and file_path.startswith("/")
#
# candidates: list[object] = [
#     Asset("video.mp4", "/media/video.mp4", "video"),
#     Asset("image.png", "", "image"),          # file_path vacío → no uploadable
#     Asset("audio.mp3", "/media/audio.mp3", "audio"),
# ]
#
# uploadable = [obj for obj in candidates if is_uploadable(obj)]
# print(f"{len(uploadable)} de {len(candidates)} objetos son uploadables ✅")
# for asset in uploadable:
#     print(f"  → {asset.name}")
