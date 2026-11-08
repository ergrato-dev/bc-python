"""Ejercicio 03 · Auditar y actualizar dependencias.

El programa no usa sus dependencias: las mira. Escribe qué hay instalado en el entorno
y quién pide qué, para que compares con `uv tree` antes y después de actualizar.
"""

from importlib import metadata

print("Ejercicio 03 · Auditar dependencias")

# ============================================
# PASO 1: Lo que hay instalado
# ============================================
# Cada paquete instalado deja sus metadatos (nombre, versión, dependencias) en el
# entorno. importlib.metadata los lee.
# Descomenta las siguientes líneas:
# print("\n--- Paso 1: lo instalado ---")
# for dist in sorted(metadata.distributions(), key=lambda d: d.metadata["Name"].lower()):
#     print(f"{dist.metadata['Name']:<20} {dist.version}")

# ============================================
# PASO 2: Quién pide qué
# ============================================
# Lo que cada dependencia directa pide, sin los extras opcionales: así llega urllib3.
# Descomenta las siguientes líneas:
# print("\n--- Paso 2: quién pide qué ---")
# for name in ("jinja2", "requests"):
#     required = [req for req in metadata.requires(name) or [] if "extra ==" not in req]
#     print(f"{name} pide: {', '.join(required)}")
