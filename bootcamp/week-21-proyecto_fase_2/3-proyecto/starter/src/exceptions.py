"""Excepciones de dominio — nunca exponer excepciones de infraestructura a la CLI."""
from __future__ import annotations


class StudioError(Exception):
    """Base para todos los errores de dominio."""


class NotFoundError(StudioError):
    def __init__(self, entity: str, id: int) -> None:
        super().__init__(f"{entity} con id={id} no encontrado")
        self.entity = entity
        self.id = id


class ExternalServiceError(StudioError):
    """Falla al contactar un servicio externo."""


class DomainValidationError(StudioError):
    """Datos de negocio inválidos."""
