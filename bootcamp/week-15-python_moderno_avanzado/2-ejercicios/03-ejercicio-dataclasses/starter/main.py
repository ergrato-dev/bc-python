"""
Ejercicio 03: Dataclasses Avanzadas
Semana 15 — Python Moderno Avanzado
"""

from __future__ import annotations
import sys
from dataclasses import dataclass, field, KW_ONLY
from datetime import datetime


# ============================================================
# PASO 1: field() — defaults seguros
# ============================================================
print("=== PASO 1: field() ===")

# Descomenta las siguientes líneas:
# @dataclass
# class Client:
#     name: str
#     email: str
#     tags: list[str] = field(default_factory=list)
#     created_at: datetime = field(default_factory=datetime.now, repr=False, compare=False)
#
# c1 = Client(name="Acme Corp", email="contact@acme.com")
# c2 = Client(name="Beta Studio", email="hello@beta.com")
# c1.tags.append("vip")
# c1.tags.append("activo")
#
# print(f"Client 1 tags: {c1.tags}")
# print(f"Client 2 tags: {c2.tags}     ← listas independientes ✅")


# ============================================================
# PASO 2: __post_init__ — validación y normalización
# ============================================================
print("\n=== PASO 2: __post_init__ ===")

# Descomenta las siguientes líneas:
# @dataclass
# class ClientValidated:
#     name: str
#     email: str
#     tags: list[str] = field(default_factory=list)
#
#     def __post_init__(self) -> None:
#         if "@" not in self.email or "." not in self.email:
#             raise ValueError(f"invalid email: {self.email!r}")
#         self.email = self.email.lower().strip()
#
# cv = ClientValidated(name="Acme Corp", email="  Contact@ACME.com  ")
# print(f"Email normalizado: {cv.email}")
#
# try:
#     ClientValidated(name="Bad Corp", email="no-es-email")
# except ValueError as e:
#     print(f"ValueError capturado: {e}  ✅")


# ============================================================
# PASO 3: KW_ONLY — keyword-only arguments
# ============================================================
print("\n=== PASO 3: KW_ONLY ===")

# Descomenta las siguientes líneas:
# @dataclass
# class Asset:
#     name: str
#     _: KW_ONLY
#     file_path: str
#     asset_type: str
#     size_mb: float = 0.0
#
# a = Asset("video_hero.mp4", file_path="/media/hero.mp4", asset_type="video", size_mb=245.0)
# print(f"Asset: {a.name} → {a.file_path} ({a.asset_type}, {a.size_mb} MB)")
#
# try:
#     Asset("video.mp4", "/media/v.mp4", "video")   # posicionales → error
# except TypeError as e:
#     print(f"TypeError capturado: Asset no acepta posicionales después de KW_ONLY ✅")


# ============================================================
# PASO 4: slots=True — memoria eficiente
# ============================================================
print("\n=== PASO 4: slots ===")

# Descomenta las siguientes líneas:
# @dataclass
# class AssetNormal:
#     name: str
#     file_path: str
#     asset_type: str
#
# @dataclass(slots=True)
# class AssetSlots:
#     name: str
#     file_path: str
#     asset_type: str
#
# normal = AssetNormal("video.mp4", "/media/video.mp4", "video")
# slotted = AssetSlots("video.mp4", "/media/video.mp4", "video")
#
# print(f"__dict__ de AssetNormal: ~{sys.getsizeof(normal.__dict__)} bytes")
# print(f"AssetSlots no tiene __dict__ ✅" if not hasattr(slotted, "__dict__") else "")
