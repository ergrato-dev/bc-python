"""
Ejercicio 04 — Validar respuestas de API con Pydantic
=======================================================
Aprende a nunca confiar ciegamente en response.json(). Valida siempre.

API: https://jsonplaceholder.typicode.com

Tareas:
  1. [Post / PostList]         Definir modelos Pydantic para /posts
  2. [User]                    Modelo con sub-modelo anidado (Address, Geo)
  3. [parse_response]          Función genérica de parseo con manejo de ValidationError
  4. [detect_schema_mismatch]  Detectar cuando la API responde con un schema inesperado
  5. [validate_partial]        Manejar campos opcionales y validación parcial

Ejecutar: python main.py
"""
from __future__ import annotations

from typing import TypeVar
from pydantic import BaseModel, Field, ValidationError, model_validator
import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"
T = TypeVar("T", bound=BaseModel)


# ── Tarea 1 — Modelos para /posts ─────────────────────────────────────────────

class Post(BaseModel):
    """
    Modelo para un post de jsonplaceholder.
    Campos: id (int), userId (int), title (str), body (str)
    Agrega validaciones:
      - title: no puede estar vacío
      - body: mínimo 10 caracteres
    """
    # TODO: definir los 4 campos con Field() donde corresponda
    pass


class PostList(BaseModel):
    """Lista de posts paginada (wrapper que añade metadatos)."""
    items: list[Post]
    count: int = 0

    @model_validator(mode="after")
    def set_count(self) -> "PostList":
        # Autocalcular count a partir de items
        self.count = len(self.items)
        return self


# ── Tarea 2 — Modelo anidado User ─────────────────────────────────────────────

class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    """
    Modelo para un usuario de jsonplaceholder.
    Campos: id, name, username, email, address (Address), company (Company)
    """
    # TODO: definir los 6 campos
    pass


# ── Tarea 3 — Función genérica de parseo ──────────────────────────────────────

def parse_response(response: httpx.Response, model: type[T]) -> T:
    """
    Parsea y valida una respuesta HTTP con el modelo dado.

    1. Llama a response.raise_for_status()
    2. Verifica que Content-Type sea application/json
    3. Llama a model.model_validate(response.json())
    4. Si falla con ValidationError, lanza ValueError con mensaje descriptivo
    """
    # TODO: implementar los 4 pasos
    raise NotImplementedError


# ── Tarea 4 — Detectar schema inesperado ──────────────────────────────────────

class StrictPost(BaseModel):
    """
    Post estricto: rechaza campos extra y exige que el body tenga al menos 3 palabras.
    """
    model_config = {"extra": "forbid"}

    id: int
    userId: int
    title: str
    body: str

    @model_validator(mode="after")
    def body_has_words(self) -> "StrictPost":
        # TODO: verificar que body tiene al menos 3 palabras
        # TODO: si no, lanzar ValueError("body muy corto")
        return self


def fetch_and_validate_strict(client: httpx.Client, post_id: int) -> StrictPost | None:
    """
    Intenta parsear el post como StrictPost.
    Si falla ValidationError, imprime el error y retorna None.
    """
    # TODO: GET /posts/{post_id}
    # TODO: Intenta StrictPost.model_validate(data)
    # TODO: Captura ValidationError, imprime los errores, retorna None
    raise NotImplementedError


# ── Tarea 5 — Campos opcionales ───────────────────────────────────────────────

class PartialPost(BaseModel):
    """
    Post con campos opcionales para manejar APIs que omiten campos en algunos endpoints.
    - id: requerido
    - title: requerido
    - body: opcional, default=""
    - userId: opcional, default=None
    - tags: lista de strings, default=[]
    """
    # TODO: definir los 5 campos con valores por defecto donde corresponda
    pass


def fetch_partial(client: httpx.Client, post_id: int) -> PartialPost:
    """Obtiene un post y lo parsea como PartialPost (tolerando campos faltantes)."""
    # TODO: GET /posts/{post_id}
    # TODO: return PartialPost.model_validate(response.json())
    raise NotImplementedError


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=== Tarea 1: Post + PostList ===")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        response = client.get("/posts", params={"_limit": 3})
        try:
            post_list = PostList(items=response.json())
            print(f"  Posts: {post_list.count} items")
            for p in post_list.items:
                print(f"    [{p.id}] {p.title[:40]}")
        except (ValidationError, NotImplementedError) as e:
            print(f"  Tarea 1: {e}")

    print("\n=== Tarea 2: User anidado ===")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        response = client.get("/users/1")
        try:
            user = User.model_validate(response.json())
            print(f"  Usuario: {user.name} ({user.username})")
            print(f"  Ciudad: {user.address.city}")
            print(f"  Empresa: {user.company.name}")
        except (ValidationError, NotImplementedError, AttributeError) as e:
            print(f"  Tarea 2: {e}")

    print("\n=== Tarea 3: parse_response ===")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        try:
            post = parse_response(client.get("/posts/1"), Post)
            print(f"  Post: [{post.id}] {post.title[:40]}")
        except NotImplementedError:
            print("  Tarea 3 no implementada aún")

    print("\n=== Tarea 4: schema estricto ===")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        try:
            post = fetch_and_validate_strict(client, 1)
            if post:
                print(f"  StrictPost: [{post.id}] {post.title[:40]}")
        except NotImplementedError:
            print("  Tarea 4 no implementada aún")

    print("\n=== Tarea 5: campos opcionales ===")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        try:
            partial = fetch_partial(client, 1)
            print(f"  PartialPost id={partial.id}, userId={partial.userId}")
            print(f"  tags (vacío por defecto): {partial.tags}")
        except NotImplementedError:
            print("  Tarea 5 no implementada aún")


if __name__ == "__main__":
    main()
