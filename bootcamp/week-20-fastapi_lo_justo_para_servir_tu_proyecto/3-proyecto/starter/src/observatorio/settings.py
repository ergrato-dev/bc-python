"""La configuración del Observatorio: variables OBSERVATORIO_* del entorno o de .env.

Qué: Settings lee y valida el token, el plazo, los reintentos y la URL de la base de datos.
Para qué: los valores que cambian de una máquina a otra, y los secretos, no van en el
código: van en el entorno o en un .env que nunca llega a Git.
Impacto: solo los programas (la CLI) crean Settings; el núcleo recibe los valores ya
leídos como argumentos y no sabe de dónde salieron.
"""

from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """OBSERVATORIO_TOKEN, _TIMEOUT, _RETRIES y _DATABASE_URL, validadas."""

    # env_prefix: `timeout` se lee de OBSERVATORIO_TIMEOUT, no de TIMEOUT, que podría
    # ser de otro programa. env_ignore_empty: `OBSERVATORIO_TOKEN=`, como en .env.example,
    # es "sin token", no un token vacío. extra="ignore": .env puede tener otras variables.
    model_config = SettingsConfigDict(
        env_prefix="OBSERVATORIO_",
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        frozen=True,
    )

    token: SecretStr | None = None
    timeout: Annotated[float, Field(gt=0)] = 10.0
    retries: Annotated[int, Field(ge=0, le=10)] = 3
    # SecretStr: la URL lleva la contraseña, y no debe salir en un registro ni en un error.
    database_url: SecretStr | None = None
