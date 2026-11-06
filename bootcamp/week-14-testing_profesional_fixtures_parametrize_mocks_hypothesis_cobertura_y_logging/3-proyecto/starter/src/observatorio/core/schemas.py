"""La frontera del Observatorio: validar con Pydantic los datos que llegan en JSON.

Qué: el esquema de una medida en JSON (MeasurementIn) y dos lectores, read_measurements y
read_scale, que convierten un archivo JSON en una Series o en una Scale validadas.
Para qué: un JSON puede traer cualquier cosa (claves de más, textos donde iban números,
etiquetas vacías); se comprueba una vez, al entrar, y el resto del programa confía en
sus tipos sin volver a mirar.
Impacto: el modelo no importa este módulo ni sabe que Pydantic existe; los errores de
validación salen como DataFileError, como cualquier otro fallo de archivo.
"""

from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError, field_validator

from observatorio.core.model import Measurement, Scale, Series
from observatorio.core.record import parse_value
from observatorio.core.storage import DataFileError, read_lines


class MeasurementIn(BaseModel):
    """Una medida tal como llega en JSON: {"label": "Norte", "value": "12,5"}.

    La etiqueta, sin espacios a los lados y no vacía; el valor, un número, null o un
    texto con las reglas de parse_value ("12,5", "NA"). Una clave de más es un error.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    label: Annotated[str, Field(min_length=1)]
    # strict: sin él, Pydantic convierte true en 1.0. Los textos ya llegan convertidos
    # por parse_text, que se ejecuta antes (mode="before").
    value: Annotated[float | None, Field(strict=True)]

    @field_validator("value", mode="before")
    @classmethod
    def parse_text(cls, value: object) -> object:
        """Convierte un texto con parse_value antes de validar el tipo; lo demás, tal cual."""
        if isinstance(value, str):
            return parse_value(value)
        return value

    def to_measurement(self) -> Measurement:
        """La medida del modelo, ya sin nada de Pydantic."""
        return Measurement(self.label, self.value)


# Se crean una vez, al importar: construir el validador es lo caro, usarlo es rápido.
_MEASUREMENTS = TypeAdapter(list[MeasurementIn])
# Scale es una dataclass del modelo: Pydantic valida sus campos y ejecuta su __post_init__,
# así que la regla de los umbrales no se repite aquí.
_SCALE = TypeAdapter(Scale)


def _invalid(path: Path, error: ValidationError) -> DataFileError:
    """DataFileError con el primer error: "datos no válidos en <path>: <dónde>: <qué>"."""
    first = error.errors()[0]
    where = ".".join(str(part) for part in first["loc"])
    prefix = f"{where}: " if where else ""
    return DataFileError(f"datos no válidos en {path}: {prefix}{first['msg']}")


def read_measurements(path: Path) -> Series:
    """La serie de un archivo JSON con una lista de medidas, validadas con MeasurementIn.

    Los fallos de archivo, como en read_lines. Si el texto no es JSON o alguna medida no
    es válida, DataFileError("datos no válidos en <path>: ...") con el primer error.
    """
    text = "\n".join(read_lines(path))
    try:
        items = _MEASUREMENTS.validate_json(text)
    except ValidationError as error:
        raise _invalid(path, error) from error
    return Series([item.to_measurement() for item in items])


def read_scale(path: Path) -> Scale:
    """La escala de un archivo JSON {"unit": ..., "low": ..., "high": ...}, validada.

    Los errores, como en read_measurements; también los umbrales imposibles de Scale.
    """
    text = "\n".join(read_lines(path))
    try:
        return _SCALE.validate_json(text)
    except ValidationError as error:
        raise _invalid(path, error) from error
