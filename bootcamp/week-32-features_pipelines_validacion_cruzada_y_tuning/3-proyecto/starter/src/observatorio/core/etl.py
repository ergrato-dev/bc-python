"""Extraer de PostgreSQL, transformar con pandas y guardar una instantánea para analizar.

Qué: `extract` lee las medidas guardadas con una consulta de SQLAlchemy, `transform` añade
el nivel y pone los nombres de columna en español, y `write_snapshot` escribe un CSV y
devuelve su huella SHA-256.
Para qué: la base de datos cambia cada vez que alguien guarda o borra una carga; un análisis
que la lee directamente da otro resultado cada día. El notebook lee la instantánea, y la
huella demuestra que es la misma que se analizó.
Impacto: importa pandas, como frames.py: core/__init__.py no lo reexporta.
"""

import hashlib
from pathlib import Path

import pandas as pd
from sqlalchemy import Connection, select

from observatorio.core.database import Reading
from observatorio.core.frames import with_levels
from observatorio.core.model import Scale

# El tipo de cada columna, fijado: sin él, pandas lo deduce de las filas que lleguen, y una
# carga sin ningún valor tendría la columna `value` de tipo object en lugar de float64.
TYPES = {"load_id": "int64", "position": "int64", "label": "str", "value": "float64"}
# Los nombres de la instantánea, en el idioma del dominio, como los de medidas.csv.
SNAPSHOT_COLUMNS = {
    "load_id": "carga",
    "position": "posicion",
    "label": "etiqueta",
    "value": "valor",
    "level": "nivel",
}


def extract(connection: Connection, load_id: int | None = None) -> pd.DataFrame:
    """Las medidas de una carga, o de todas, en el orden en que se guardaron."""
    query = select(Reading.load_id, Reading.position, Reading.label, Reading.value).order_by(
        Reading.load_id, Reading.position
    )
    if load_id is not None:
        # El filtro va en el WHERE: PostgreSQL envía solo esas filas, no la tabla entera.
        query = query.where(Reading.load_id == load_id)
    return pd.read_sql(query, connection, dtype=TYPES)


def transform(frame: pd.DataFrame, scale: Scale) -> pd.DataFrame:
    """Una copia con el nivel de cada medida y las columnas en español."""
    return with_levels(frame, scale).rename(columns=SNAPSHOT_COLUMNS)


def write_snapshot(frame: pd.DataFrame, path: Path) -> str:
    """Escribe la tabla en CSV y devuelve la huella SHA-256 de los bytes escritos."""
    # lineterminator="\n": los mismos bytes en Linux, macOS y Windows, y la misma huella.
    data = frame.to_csv(index=False, lineterminator="\n").encode()
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()
