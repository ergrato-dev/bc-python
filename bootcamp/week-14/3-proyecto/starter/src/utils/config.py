"""
Configuración de la aplicación.

Este módulo gestiona la configuración cargada desde
variables de entorno y archivo .env.
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """
    Configuración de la aplicación.

    Attributes:
        api_key: API key de OpenWeatherMap.
        base_url: URL base de la API.
        timeout: Timeout para requests.
        data_dir: Directorio de datos.
        log_level: Nivel de logging.
    """

    api_key: str
    base_url: str = "https://api.openweathermap.org/data/2.5"
    timeout: int = 10
    data_dir: str = "data"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "Config":
        """
        Carga configuración desde variables de entorno.

        Args:
            env_file: Ruta al archivo .env (opcional).

        Returns:
            Instancia de Config con valores cargados.

        Raises:
            ValueError: Si falta OPENWEATHER_API_KEY.
        """
        # TODO: Implementar
        # 1. Cargar archivo .env si existe
        # 2. Leer variables de entorno
        # 3. Validar que api_key existe
        # 4. Crear y retornar Config
        pass

    @staticmethod
    def _load_env_file(path: str) -> None:
        """
        Carga variables desde archivo .env.

        Args:
            path: Ruta al archivo .env.
        """
        # TODO: Implementar parser simple de .env
        # Formato: KEY=value (ignorar líneas vacías y comentarios #)
        pass

    def validate(self) -> bool:
        """
        Valida que la configuración sea correcta.

        Returns:
            True si es válida.

        Raises:
            ValueError: Si hay valores inválidos.
        """
        # TODO: Implementar validaciones
        # 1. api_key no vacío
        # 2. timeout > 0
        # 3. base_url válida
        pass
