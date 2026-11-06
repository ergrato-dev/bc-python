"""Observatorio de datos: recoge, guarda, analiza y predice datos de un dominio."""

from importlib.metadata import version

# La versión se escribe una sola vez, en pyproject.toml; aquí se lee de los metadatos
# del paquete instalado. Así `observatorio --version` nunca se desfasa del proyecto.
__version__ = version("observatorio")
