"""
Excepciones personalizadas para la API.

Este módulo define excepciones específicas para el manejo
de errores de la API de OpenWeatherMap.
"""


class APIError(Exception):
    """Excepción base para errores de API."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """
        Inicializa APIError.

        Args:
            message: Mensaje de error descriptivo.
            status_code: Código HTTP opcional.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        """Representación string del error."""
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class CityNotFoundError(APIError):
    """Excepción cuando no se encuentra la ciudad."""

    def __init__(self, city: str) -> None:
        """
        Inicializa CityNotFoundError.

        Args:
            city: Nombre de la ciudad no encontrada.
        """
        self.city = city
        super().__init__(
            f'Ciudad "{city}" no encontrada.',
            status_code=404,
        )


class InvalidAPIKeyError(APIError):
    """Excepción cuando la API key es inválida."""

    def __init__(self) -> None:
        """Inicializa InvalidAPIKeyError."""
        super().__init__(
            "API key inválida o no configurada.",
            status_code=401,
        )


class ConnectionError(APIError):
    """Excepción cuando hay problemas de conexión."""

    def __init__(self, detail: str = "") -> None:
        """
        Inicializa ConnectionError.

        Args:
            detail: Detalle adicional del error.
        """
        message = "No se pudo conectar al servicio de clima."
        if detail:
            message += f" {detail}"
        super().__init__(message)


class RateLimitError(APIError):
    """Excepción cuando se excede el límite de requests."""

    def __init__(self) -> None:
        """Inicializa RateLimitError."""
        super().__init__(
            "Se ha excedido el límite de solicitudes. Intenta más tarde.",
            status_code=429,
        )
