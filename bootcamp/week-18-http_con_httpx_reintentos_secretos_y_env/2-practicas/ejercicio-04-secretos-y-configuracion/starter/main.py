"""Ejercicio 04 · Secretos y configuración: variables de entorno, .env y pydantic-settings.

Ejecuta cada paso con la orden que dice el README: algunas ponen una variable delante
(`EJERCICIO_RETRIES=0 uv run python main.py`) o cargan el archivo .env.
El token de este ejercicio es inventado: nunca pongas aquí uno de verdad.
"""

import os
from pathlib import Path
from typing import Annotated

from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

print("Ejercicio 04 · Secretos y configuración")


# ============================================
# PASO 1: Leer una variable de entorno
# ============================================
# Descomenta las siguientes líneas:
# print("get:", os.environ.get("EJERCICIO_TOKEN"))
# try:
#     print("corchetes:", os.environ["EJERCICIO_TOKEN"])
# except KeyError as problem:
#     print("KeyError:", problem)


# ============================================
# PASO 2: Todo es texto
# ============================================
# Descomenta las siguientes líneas:
# retries = os.environ.get("EJERCICIO_RETRIES", "3")
# print(f"reintentos: {retries!r} · ¿reintenta? {bool(retries)}")


# ============================================
# PASO 3: Un archivo .env
# ============================================
# Descomenta las siguientes líneas:
# names = sorted(name for name in os.environ if name.startswith("EJERCICIO_"))
# print("variables EJERCICIO_*:", names)


# ============================================
# PASO 4: pydantic-settings
# ============================================
# Descomenta las siguientes líneas:
# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_prefix="EJERCICIO_",
#         env_file=".env",
#         env_ignore_empty=True,
#         extra="ignore",
#     )
#
#     token: SecretStr | None = None
#     timeout: Annotated[float, Field(gt=0)] = 10.0
#     retries: Annotated[int, Field(ge=0, le=10)] = 3
#
#
# settings = Settings()
# print(settings)
# print("¿reintenta?", settings.retries > 0)


# ============================================
# PASO 5: Un valor que no vale
# ============================================
# Descomenta las siguientes líneas:
# os.environ["EJERCICIO_TIMEOUT"] = "rápido"
# try:
#     Settings()
# except ValidationError as problem:
#     first = problem.errors()[0]
#     print(f"EJERCICIO_{str(first['loc'][0]).upper()}: {first['msg']}")
# del os.environ["EJERCICIO_TIMEOUT"]


# ============================================
# PASO 6: ¿Quién gana, el entorno o .env?
# ============================================
# Descomenta las siguientes líneas:
# print("solo .env:", Settings().retries)
# os.environ["EJERCICIO_RETRIES"] = "7"
# print("entorno y .env:", Settings().retries)
# del os.environ["EJERCICIO_RETRIES"]


# ============================================
# PASO 7: SecretStr
# ============================================
# Descomenta las siguientes líneas:
# print("print:", settings.token)
# print("repr:", repr(settings.token))
# print("JSON:", settings.model_dump_json())
# if settings.token is not None:
#     secret = settings.token.get_secret_value()
#     print("para la cabecera:", len(secret), "caracteres, empieza por", secret[:3])


# ============================================
# PASO 8: Lo que SecretStr no protege
# ============================================
# Descomenta las siguientes líneas:
# class Leaky(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_prefix="EJERCICIO_", env_file=".env", extra="ignore"
#     )
#     token: str | None = None
#
#
# print("con str:", Leaky())
# ignored = Path(".gitignore").read_text(encoding="utf-8").splitlines()
# print("¿.env en .gitignore?", ".env" in ignored)
