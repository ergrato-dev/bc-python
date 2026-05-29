"""
Ejercicio 01: Protocols en Studio BC
Semana 15 — Python Moderno Avanzado
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable


# ============================================================
# PASO 1: Definir los Protocols base
# ============================================================
print("=== PASO 1: Protocols ===")

# Descomenta las siguientes líneas:
# class Nameable(Protocol):
#     @property
#     def name(self) -> str: ...
#
# class Timestamped(Protocol):
#     @property
#     def created_at(self) -> datetime: ...
#
# class Describable(Protocol):
#     @property
#     def description(self) -> str: ...
#
# print("Protocols definidos ✅")


# ============================================================
# PASO 2: Clases que satisfacen los Protocols (sin herencia)
# ============================================================
print("\n=== PASO 2: Entidades ===")

# Descomenta las siguientes líneas:
# @dataclass
# class Client:
#     name: str
#     email: str
#     created_at: datetime = field(default_factory=datetime.now)
#
# @dataclass
# class Project:
#     name: str
#     client_id: int
#     description: str = ""
#     created_at: datetime = field(default_factory=datetime.now)
#
# @dataclass
# class Asset:
#     name: str
#     file_path: str
#     description: str = ""
#     created_at: datetime = field(default_factory=datetime.now)
#
# client = Client(name="Acme Corp", email="contact@acme.com")
# project = Project(name="Campaña Navidad", client_id=1, description="Campaña Q4 2026")
# asset = Asset(name="video_hero.mp4", file_path="/media/video_hero.mp4", description="Video principal")
# print("Entidades creadas ✅")


# ============================================================
# PASO 3: Funciones que aceptan Protocols
# ============================================================
print("\n=== PASO 3: Funciones con Protocol ===")

# Descomenta las siguientes líneas:
# def display_name(item: Nameable) -> str:
#     return f"[{item.name}]"
#
# def show_info(item: Nameable & Timestamped) -> None:
#     print(f"{item.name} — creado: {item.created_at:%Y-%m-%d %H:%M}")
#
# print(display_name(client))   # funciona con Client
# print(display_name(project))  # funciona con Project
# print(display_name(asset))    # funciona con Asset
# print("display_name funciona con Client, Project y Asset ✅")


# ============================================================
# PASO 4: @runtime_checkable e isinstance
# ============================================================
print("\n=== PASO 4: runtime_checkable ===")

# Descomenta las siguientes líneas:
# @runtime_checkable
# class NameableRT(Protocol):
#     @property
#     def name(self) -> str: ...
#
# print(f"Client es Nameable en runtime: {isinstance(client, NameableRT)}")
# print(f"Asset es Nameable en runtime: {isinstance(asset, NameableRT)}")
# print(f"str no es Nameable en runtime: {isinstance('texto', NameableRT)}")
# print("@runtime_checkable ✅")
