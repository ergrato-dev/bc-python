"""Ejercicio 03 · Dependencias, ciclo de vida y def o async def.

Las dependencias (Depends) preparan lo que una ruta necesita y lo recogen al terminar;
el lifespan abre y cierra lo que dura toda la vida de la aplicación. Al final, cinco
peticiones a la vez enseñan qué pasa si una ruta `async def` bloquea.
"""

import asyncio
import time
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import Annotated

import httpx2
from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient

print("Ejercicio 03 · Dependencias y ciclo de vida")

app = FastAPI()
client = TestClient(app)

# Lo que va pasando, en orden: cada dependencia y cada ruta apuntan aquí.
log: list[str] = []


# ============================================
# PASO 1: Una dependencia
# ============================================
# Descomenta las siguientes líneas:
# def pagination(limit: int = 10, offset: int = 0) -> dict[str, int]:
#     # Una dependencia recibe parámetros como una ruta: limit y offset son de la consulta.
#     return {"limit": min(limit, 100), "offset": offset}
#
#
# Pagination = Annotated[dict[str, int], Depends(pagination)]
#
#
# @app.get("/stations")
# def get_stations(page: Pagination) -> dict[str, object]:
#     return {"page": page}
#
#
# @app.get("/readings")
# def get_readings(page: Pagination) -> dict[str, object]:
#     return {"page": page}
#
#
# print("\n--- Paso 1: Depends ---")
# print("/stations              ->", client.get("/stations").json())
# print("/readings?limit=500    ->", client.get("/readings?limit=500").json())
# print("/readings?offset=uno   ->", client.get("/readings?offset=uno").status_code)


# ============================================
# PASO 2: Una dependencia con yield
# ============================================
# Descomenta las siguientes líneas:
# class FakeSession:
#     """Hace de sesión de base de datos: solo apunta cuándo se abre y se cierra."""
#
#     count = 0
#
#     def __init__(self) -> None:
#         FakeSession.count += 1
#         self.name = f"sesión {FakeSession.count}"
#
#
# def get_session() -> Iterator[FakeSession]:
#     session = FakeSession()
#     log.append(f"abre {session.name}")
#     try:
#         yield session  # aquí se ejecuta la ruta
#     finally:
#         log.append(f"cierra {session.name}")
#
#
# SessionDep = Annotated[FakeSession, Depends(get_session)]
#
#
# @app.get("/loads")
# def get_loads(session: SessionDep) -> str:
#     log.append(f"la ruta usa {session.name}")
#     return session.name
#
#
# print("\n--- Paso 2: yield ---")
# for _ in range(2):
#     log.clear()
#     print(client.get("/loads").json(), "->", log)


# ============================================
# PASO 3: Una dependencia que usa otra, una vez por petición
# ============================================
# Descomenta las siguientes líneas:
# def get_user(session: SessionDep) -> str:
#     log.append(f"get_user con {session.name}")
#     return "ana"
#
#
# @app.get("/me")
# def get_me(user: Annotated[str, Depends(get_user)], session: SessionDep) -> dict[str, str]:
#     return {"user": user, "session": session.name}
#
#
# print("\n--- Paso 3: dependencias encadenadas ---")
# log.clear()
# print(client.get("/me").json(), "->", log)


# ============================================
# PASO 4: Sustituir una dependencia en los tests
# ============================================
# Descomenta las siguientes líneas:
# class TestSession(FakeSession):
#     def __init__(self) -> None:
#         self.name = "sesión de pruebas"
#
#
# test_session = TestSession()
# app.dependency_overrides[get_session] = lambda: test_session
# print("\n--- Paso 4: dependency_overrides ---")
# log.clear()
# print("/loads ->", client.get("/loads").json(), "·", log)
# print("/me    ->", client.get("/me").json())
# app.dependency_overrides.clear()
# print("sin override ->", client.get("/loads").json())


# ============================================
# PASO 5: El lifespan: abrir al arrancar, cerrar al parar
# ============================================
# Descomenta las siguientes líneas:
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#     print("  arranca: abro el motor (una vez)")
#     app.state.engine = "motor de PostgreSQL"
#     yield
#     print("  para: cierro el motor")
#
#
# app_with_life = FastAPI(lifespan=lifespan)
#
#
# @app_with_life.get("/engine")
# def get_engine(request: Request) -> str:
#     return str(request.app.state.engine)
#
#
# print("\n--- Paso 5: lifespan ---")
# with TestClient(app_with_life) as life_client:
#     print("  petición 1:", life_client.get("/engine").json())
#     print("  petición 2:", life_client.get("/engine").json())
# print("  fuera del with: el motor ya está cerrado")


# ============================================
# PASO 6: def o async def
# ============================================
# Descomenta las siguientes líneas:
# slow = FastAPI()
#
#
# @slow.get("/def")
# def with_def() -> str:
#     time.sleep(0.2)  # bloquea, pero en un hilo del pool de FastAPI
#     return "def"
#
#
# @slow.get("/async-blocking")
# async def async_blocking() -> str:
#     time.sleep(0.2)  # bloquea el bucle de eventos: nadie más avanza
#     return "async def con time.sleep"
#
#
# @slow.get("/async")
# async def async_waiting() -> str:
#     await asyncio.sleep(0.2)  # espera sin bloquear: el bucle atiende a los demás
#     return "async def con await"
#
#
# async def five_at_once(path: str) -> float:
#     transport = httpx2.ASGITransport(app=slow)
#     async with httpx2.AsyncClient(transport=transport, base_url="http://test") as http:
#         start = time.perf_counter()
#         await asyncio.gather(*(http.get(path) for _ in range(5)))
#         return time.perf_counter() - start
#
#
# print("\n--- Paso 6: cinco peticiones a la vez, de 0,2 s cada una ---")
# for path in ["/def", "/async-blocking", "/async"]:
#     print(f"{path:<16} {asyncio.run(five_at_once(path)):.2f} s")
