"""La API HTTP del Observatorio: las cargas de PostgreSQL, servidas en JSON con FastAPI.

Qué: create_app(url) construye la aplicación con sus rutas (/health, /loads, /stats);
get_session presta una sesión por petición, y un error de conexión sale como 503.
Para qué: otros programas (un panel, un cuaderno, el móvil de alguien) leen y guardan
medidas sin instalar el Observatorio ni conocer PostgreSQL: solo HTTP y JSON.
Impacto: como la CLI, es un adaptador sobre core y no lee el entorno: la URL llega como
argumento. Las rutas son `def`, no `async def`: la sesión de SQLAlchemy es síncrona, y
FastAPI las ejecuta en su pool de hilos.
"""

from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from observatorio import __version__
from observatorio.core import (
    LabelStats,
    Load,
    LoadInfo,
    Measurement,
    MeasurementIn,
    Series,
    delete_load,
    label_stats,
    list_loads,
    load_series,
    make_engine,
    save_series,
)


class ReadingIn(MeasurementIn):
    """Una medida en el cuerpo de POST /loads: como en los JSON, con el límite de la tabla."""

    # String(100) en readings.label: sin este límite, una etiqueta más larga llegaría a
    # PostgreSQL, que la rechazaría con un error 500 en lugar de un 422.
    label: Annotated[str, Field(min_length=1, max_length=100)]


class LoadIn(BaseModel):
    """El cuerpo de POST /loads: de dónde vienen las medidas y la lista de medidas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source: Annotated[str, Field(min_length=1, max_length=500)]
    measurements: Annotated[list[ReadingIn], Field(min_length=1)]


class Health(BaseModel):
    """La respuesta de GET /health."""

    status: str
    version: str


def get_session(request: Request) -> Iterator[Session]:
    """Una sesión por petición, con el motor de la aplicación; se cierra al responder."""
    with Session(request.app.state.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()


@router.get("/health")
def health(session: SessionDep) -> Health:
    """Responde si la API está viva y PostgreSQL contesta."""
    session.execute(text("SELECT 1"))
    return Health(status="ok", version=__version__)


@router.get("/loads")
def get_loads(session: SessionDep) -> list[LoadInfo]:
    """Todas las cargas, de la más antigua a la más nueva, con cuántas medidas tiene cada una."""
    return list_loads(session)


@router.post("/loads", status_code=status.HTTP_201_CREATED)
def post_load(body: LoadIn, session: SessionDep, response: Response) -> LoadInfo:
    """Guarda una carga nueva con sus medidas y la devuelve con su número."""
    series = Series([reading.to_measurement() for reading in body.measurements])
    load = save_series(session, body.source, series)
    session.commit()
    response.headers["Location"] = f"/loads/{load.id}"
    return LoadInfo(load.id, load.source, load.created_at, len(series))


@router.get("/loads/{load_id}/measurements")
def get_measurements(load_id: int, session: SessionDep) -> list[Measurement]:
    """Las medidas de una carga, en su orden; 404 si no existe."""
    series = load_series(session, load_id)
    if series is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la carga {load_id}")
    return series.measurements


@router.delete("/loads/{load_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_load(load_id: int, session: SessionDep) -> None:
    """Borra una carga y sus medidas; 404 si no existe."""
    if not delete_load(session, load_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la carga {load_id}")
    session.commit()


@router.get("/stats")
def get_stats(session: SessionDep, load: int | None = None) -> list[LabelStats]:
    """Medidas, medidas con valor y media por etiqueta, de una carga (?load=N) o de todas."""
    if load is not None and session.get(Load, load) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la carga {load}")
    return label_stats(session, load)


def database_unavailable(request: Request, problem: Exception) -> JSONResponse:
    """503 sin el texto del error, que podría llevar el usuario o el servidor."""
    return JSONResponse(
        {"detail": "no se pudo conectar con PostgreSQL"},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


def create_app(url: str) -> FastAPI:
    """La aplicación de la API, con su motor para `url`, abierto al arrancar y cerrado al parar."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.engine = make_engine(url)
        yield
        app.state.engine.dispose()

    app = FastAPI(title="Observatorio", version=__version__, lifespan=lifespan)
    app.include_router(router)
    app.add_exception_handler(OperationalError, database_unavailable)
    return app
