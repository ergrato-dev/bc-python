"""Ejercicio 04 · Una API con PostgreSQL.

Una API de notas sobre SQLAlchemy: una sesión por petición, commit en la ruta que
escribe, 404 y 503, y al final tests que no dejan rastro en la base.

Antes de ejecutar, arranca el PostgreSQL de las prácticas: `docker compose up -d --wait`.
Cada ejecución borra y vuelve a crear la tabla: puedes repetir sin miedo.
"""

from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, create_engine, event, func, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

URL = "postgresql+psycopg://practicas:practicas@127.0.0.1:5433/practicas"

print("Ejercicio 04 · Una API con PostgreSQL")


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(200))


engine = create_engine(URL)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# ============================================
# PASO 1: La aplicación, su motor y una sesión por petición
# ============================================
# Descomenta las siguientes líneas:
# def database_unavailable(request: Request, problem: Exception) -> JSONResponse:
#     # Lo usa el paso 4. Un manejador se registra al crear la aplicación: una vez que
#     # ha atendido su primera petición, uno añadido después ya no se aplica.
#     return JSONResponse({"detail": "no se pudo conectar con PostgreSQL"}, status_code=503)
#
#
# def create_app(url: str) -> FastAPI:
#     @asynccontextmanager
#     async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#         app.state.engine = create_engine(url)
#         yield
#         app.state.engine.dispose()
#
#     app = FastAPI(lifespan=lifespan)
#     app.add_exception_handler(OperationalError, database_unavailable)
#     return app
#
#
# opened: list[Session] = []
#
#
# def get_session(request: Request) -> Iterator[Session]:
#     # Una sesión nueva en cada petición, cerrada al responder: nada se comparte.
#     with Session(request.app.state.engine) as session:
#         opened.append(session)
#         yield session
#
#
# SessionDep = Annotated[Session, Depends(get_session)]
# app = create_app(URL)
#
#
# @app.get("/notes/count")
# def count_notes(session: SessionDep) -> dict[str, object]:
#     return {"notes": session.scalar(select(func.count(Note.id)))}
#
#
# print("\n--- Paso 1: una sesión por petición ---")
# with TestClient(app) as client:
#     print("petición 1:", client.get("/notes/count").json())
#     print("petición 2:", client.get("/notes/count").json())
#     print("sesiones abiertas:", len(opened), "· ¿la misma?", opened[0] is opened[1])
#     print("conexiones abiertas en el pool:", app.state.engine.pool.checkedin())


# ============================================
# PASO 2: Escribir: modelo de entrada, commit y 201
# ============================================
# Descomenta las siguientes líneas:
# class NoteIn(BaseModel):
#     model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
#     text: Annotated[str, Field(min_length=1, max_length=200)]
#
#
# class NoteOut(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     id: int
#     text: str
#
#
# @app.post("/notes", status_code=status.HTTP_201_CREATED)
# def post_note(body: NoteIn, session: SessionDep, response: Response) -> NoteOut:
#     note = Note(text=body.text)
#     session.add(note)
#     # Sin commit, la sesión se cierra al responder y PostgreSQL deshace el INSERT.
#     session.commit()
#     response.headers["Location"] = f"/notes/{note.id}"
#     # from_attributes: el modelo se construye leyendo los atributos del objeto del ORM.
#     return NoteOut.model_validate(note)
#
#
# print("\n--- Paso 2: POST /notes ---")
# with TestClient(app) as client:
#     for text in ["comprar pilas", "  revisar el sensor del norte  ", ""]:
#         response = client.post("/notes", json={"text": text})
#         body = response.json()
#         shown = body if response.status_code == 201 else body["detail"][0]["msg"]
#         print(f"{text!r:<36} -> {response.status_code} {shown}")
#     print("total:", client.get("/notes/count").json()["notes"])


# ============================================
# PASO 3: Leer una, todas y el 404
# ============================================
# Descomenta las siguientes líneas:
# @app.get("/notes")
# def get_notes(session: SessionDep) -> list[NoteOut]:
#     notes = session.scalars(select(Note).order_by(Note.id))
#     return [NoteOut.model_validate(note) for note in notes]
#
#
# @app.get("/notes/{note_id}")
# def get_note(note_id: int, session: SessionDep) -> NoteOut:
#     note = session.get(Note, note_id)
#     if note is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la nota {note_id}")
#     return NoteOut.model_validate(note)
#
#
# print("\n--- Paso 3: GET ---")
# with TestClient(app) as client:
#     print("/notes   ->", client.get("/notes").json())
#     print("/notes/2 ->", client.get("/notes/2").json())
#     response = client.get("/notes/99")
#     print("/notes/99 ->", response.status_code, response.json())


# ============================================
# PASO 4: Sin PostgreSQL: 503, sin la contraseña
# ============================================
# Descomenta las siguientes líneas:
# broken_engine = create_engine("postgresql+psycopg://practicas:clave-secreta@127.0.0.1:1/practicas")
#
#
# def broken_session() -> Iterator[Session]:
#     with Session(broken_engine) as session:
#         yield session
#
#
# print("\n--- Paso 4: PostgreSQL en el puerto 1, donde no hay nadie ---")
# app.dependency_overrides[get_session] = broken_session
# with TestClient(app) as client:
#     response = client.get("/notes")
#     print("estado:", response.status_code, "· cuerpo:", response.json())
#     print("¿sale la contraseña?", "clave-secreta" in response.text)
# app.dependency_overrides.clear()


# ============================================
# PASO 5: Tests que no dejan rastro
# ============================================
# Descomenta las siguientes líneas:
# def test_session() -> Iterator[Session]:
#     # Una transacción por fuera; el commit de la ruta solo confirma un SAVEPOINT.
#     with engine.connect() as connection:
#         transaction = connection.begin()
#         session = Session(bind=connection, join_transaction_mode="create_savepoint")
#         yield session
#         session.close()
#         transaction.rollback()
#
#
# print("\n--- Paso 5: dependency_overrides con una transacción que se deshace ---")
# with TestClient(app) as client:
#     before = client.get("/notes/count").json()["notes"]
#     sessions = test_session()
#     session = next(sessions)
#     app.dependency_overrides[get_session] = lambda: session
#     client.post("/notes", json={"text": "nota de un test"})
#     client.post("/notes", json={"text": "otra nota de un test"})
#     print("dentro del test:", client.get("/notes/count").json()["notes"], "notas")
#     app.dependency_overrides.clear()
#     next(sessions, None)  # termina el generador: session.close() y el rollback
#     print("antes:", before, "· después del test:", client.get("/notes/count").json()["notes"])


# ============================================
# PASO 6: ¿Cuántas consultas cuesta cada petición?
# ============================================
# Descomenta las siguientes líneas:
# sent: list[str] = []
#
#
# def remember(conn: object, cursor: object, statement: str, *args: object) -> None:
#     sent.append(statement.split()[0])
#
#
# print("\n--- Paso 6: el SQL de cada petición ---")
# with TestClient(app) as client:
#     event.listen(app.state.engine, "before_cursor_execute", remember)
#     for method, path, body in [
#         ("GET", "/notes", None),
#         ("GET", "/notes/1", None),
#         ("POST", "/notes", {"text": "una más"}),
#     ]:
#         sent.clear()
#         client.request(method, path, json=body)
#         print(f"{method:<4} {path:<9} -> {sent}")
