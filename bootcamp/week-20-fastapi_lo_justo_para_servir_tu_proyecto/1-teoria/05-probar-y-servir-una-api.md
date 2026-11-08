# 05 · Probar y servir una API

⏱️ 1 h

## 🎯 Objetivos

- Probar una API con `TestClient`, con y sin su lifespan.
- Escribir la fixture `client`: la aplicación de verdad con la sesión de los tests.
- Decidir qué comprobar de cada respuesta: código, cuerpo, cabeceras, y lo que **no** debe salir.
- Probar que una ruta confirma lo que escribe, y que un error de la base no enseña secretos.
- Probar `observatorio servir` sin servir nada, y que la CLI no carga FastAPI hasta que la necesita.
- Servir la API en Docker, junto a PostgreSQL, con su *healthcheck*.

---

## 1. `TestClient`

```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/loads")
assert response.status_code == 200
assert response.json() == []
```

`TestClient` tiene la interfaz de un cliente HTTP (`get`, `post`, `delete`, `json=`, `params=`, `headers=`), pero no abre ningún puerto: construye la petición ASGI y llama a la aplicación directamente (teoría 01). Las respuestas son las mismas que daría uvicorn, sin red y en milisegundos.

Por dentro usa **httpx2**, el sucesor de `httpx`: Starlette 1.10 avisa con un `StarletteDeprecationWarning` si solo encuentra el `httpx` de siempre. Por eso `httpx2` va en el grupo `dev` de tu proyecto: lo usan los tests, no el programa. Tu `remote.py` sigue con `httpx==0.28.1`, que es lo que fija la semana 18.

Con un `with`, `TestClient` además **arranca y para** la aplicación: ejecuta el lifespan. Sin `with`, no lo ejecuta, y `app.state.engine` no existe.

---

## 2. La fixture `client`

```python
@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """Un cliente de la API cuyas peticiones usan la sesión del test."""
    app = api.create_app(TEST_URL)
    app.dependency_overrides[api.get_session] = lambda: session
    with TestClient(app) as client:
        yield client
```

Es la aplicación **de verdad**, la misma que sirve `observatorio servir`, con una sola diferencia: la sesión. `dependency_overrides` le da a cada ruta la sesión de la fixture `session` de `db_fixtures.py`, dentro de una transacción que se deshace al terminar el test (semana 19, teoría 05). El `commit` de `post_load` solo confirma un SAVEPOINT. Cada test empieza con la base vacía, y los tests no se pisan.

El `with` ejecuta el lifespan, que abre un motor que nadie usa: así el arranque y la parada también se prueban en cada test.

---

## 3. Qué comprobar de una respuesta

Una API es un **contrato** con programas que no conoces. Lo que pruebes es lo que prometes:

```python
def test_post_load_returns_201_and_the_new_load(client: TestClient) -> None:
    response = client.post("/loads", json=NORTE)
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"id", "source", "created_at", "measurements"}
    assert body["measurements"] == 3
```

- **El código** siempre: un 200 donde iba un 201 rompe a quien decide con él.
- **El cuerpo entero** cuando es corto (`== {"detail": "no existe la carga 999"}`), o sus claves exactas (`set(body) == {...}`): un campo de más también es un cambio de contrato, y puede ser un dato que no debía salir.
- **Las cabeceras** que prometes: `Location` en el 201, ninguna respuesta en el 204 (`response.content == b""`).
- **El `loc` de un 422**: dice que la validación falló **donde** debía, no por otra razón.
- **Lo que no debe salir**: `"secreto" not in response.text`.

Y una prueba que no parece de la API: que `/openapi.json` tenga exactamente tus rutas y sus métodos. Si alguien añade una ruta sin querer, o cambia un método, el test lo dice.

---

## 4. Lo que la sesión de los tests no puede probar

La fixture `client` tiene un punto ciego: como todo ocurre en una transacción que se ve a sí misma, una ruta **sin** `session.commit()` también pasaría. Los datos están en la sesión, aunque nunca se confirmen. Para eso hay tests con el **motor propio** de la aplicación, sin override:

```python
def test_own_engine_post_load_commits(db_env: Path) -> None:
    with TestClient(api.create_app(TEST_URL)) as client:
        load_id = post(client, NORTE)
    # Otra aplicación, otro motor, otras conexiones: solo ve lo confirmado.
    with TestClient(api.create_app(TEST_URL)) as client:
        assert [load["id"] for load in client.get("/loads").json()] == [load_id]
```

Escriben de verdad en la base de pruebas, así que usan `db_env`, que vacía las tablas antes. Son pocos y caros: solo los que necesitan confirmar.

De la misma manera se prueba el `dispose` del lifespan: con el motor propio, después de una petición el pool tiene una conexión guardada (`pool.checkedin() == 1`); después de salir del `with`, ninguna.

---

## 5. Sin PostgreSQL

```python
url = make_url(TEST_URL).set(port=1, password="secreto-de-prueba")
engine = make_engine(url.render_as_string(hide_password=False))
```

Una sesión con un motor que apunta al puerto 1, donde no hay nadie, y con una contraseña reconocible. El test comprueba dos cosas: que la respuesta es un **503** con su mensaje, y que `"secreto"` **no** aparece en ella. El segundo test es el importante: el primero lo pasaría también un manejador que copiara `str(problem)` en `detail`.

---

## 6. Probar `servir` sin servir

`uvicorn.run` sirve hasta que pulsas Ctrl+C: un test que lo llamara no terminaría nunca. Se sustituye con `monkeypatch` (semana 14) por una función que apunta con qué se la llamó:

```python
def fake_run(app: FastAPI, *, host: str, port: int) -> None:
    calls.update(app=app, host=host, port=port)

monkeypatch.setattr(uvicorn, "run", fake_run)
```

Y el test comprueba que `servir` crea una aplicación FastAPI, con el host y el puerto que tocan. Un test más le hace peticiones a esa aplicación con `TestClient`: así se sabe que `servir` sirve **tus** rutas, con la URL de `OBSERVATORIO_DATABASE_URL`.

---

## 7. Importar tarde

```python
@app.command()
def servir(...) -> None:
    url = database_url()
    # Importar aquí: FastAPI y uvicorn solo se cargan al servir, no en cada comando.
    import uvicorn

    from observatorio.api import create_app

    uvicorn.run(create_app(url), host=host, port=puerto)
```

Importar FastAPI, Starlette y uvicorn cuesta tiempo cada vez que arranca el programa. Medido en Docker, importar la CLI tarda 0,87 s, y con la API y uvicorn, 1,06 s: un 22 % más en **cada** `--version`, `informe` o `guardar`, que no los usan. Importándolos dentro de `servir`, solo paga quien sirve.

Un test lo vigila desde otro proceso, porque en el de pytest FastAPI ya está importado:

```python
code = "import sys, observatorio.cli; print('fastapi' in sys.modules)"
result = subprocess.run([sys.executable, "-c", code], check=False, capture_output=True, text=True)
assert result.stdout == "False\n"
```

Otro test igual comprueba que `core` tampoco importa FastAPI: `core` no sabe que lo sirve HTTP.

---

## 8. Servir en Docker

La API usa la **misma imagen** que `app`, con otra orden:

```yaml
  api:
    image: local/observatorio:week-20
    command: ["observatorio", "servir", "--host", "0.0.0.0"]
    environment:
      OBSERVATORIO_DATABASE_URL: postgresql+psycopg://observatorio:observatorio@db:5432/observatorio
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
```

- **`--host 0.0.0.0`** dentro del contenedor: con `127.0.0.1`, uvicorn solo se oiría a sí mismo, y Docker no podría llevarle las peticiones;
- **`127.0.0.1:8000:8000`** fuera: solo tu máquina llega al puerto. La API no comprueba quién llama (teoría 01, sección 7);
- **el *healthcheck*** pregunta a `/health`, que a su vez hace `SELECT 1` en PostgreSQL. `docker compose up --wait` espera a que conteste 200. La imagen no trae `curl`, pero trae Python;
- **las migraciones** no las aplica la API al arrancar: se aplican antes, una vez, con `docker compose run --rm app alembic upgrade head`. Si varias copias de la API arrancaran a la vez, todas intentarían migrar.

---

## 9. Probar a mano

```bash
curl -i http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/loads \
     -H 'content-type: application/json' \
     -d '{"source": "curl", "measurements": [{"label": "Norte", "value": "12,5"}]}'
curl -s 'http://127.0.0.1:8000/stats?load=1'
curl -s -X DELETE -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/loads/1
```

`-i` enseña el código y las cabeceras; `-w '%{http_code}'`, solo el código. Y <http://127.0.0.1:8000/docs> en el navegador hace lo mismo con botones. Es **explorar**, no probar: lo que descubras a mano, escríbelo como test.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated` | Falta `httpx2` | `uv add --dev httpx2==2.16.0` |
| Un test que escribe deja datos para el siguiente | Usa el motor propio sin `db_env` | `db_env` vacía las tablas antes |
| Los tests pasan sin `session.commit()` en la ruta | Solo prueban con la sesión de la fixture | Un test con el motor propio y dos aplicaciones |
| El test de `servir` no termina | Llama al `uvicorn.run` de verdad | `monkeypatch.setattr(uvicorn, "run", ...)` |
| `curl: (7) Failed to connect to 127.0.0.1 port 8000` | La API no está arrancada, o escucha en `127.0.0.1` dentro del contenedor | `docker compose ps`; `--host 0.0.0.0` en `command` |
| `/health` da 503 en Docker | La API arrancó antes que PostgreSQL | `depends_on` con `condition: service_healthy` |
| Las rutas dan 500 y el registro dice `relation "loads" does not exist` | No se aplicaron las migraciones | `docker compose run --rm app alembic upgrade head` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué hace `TestClient`, y qué cambia con `with`.
- [ ] Por qué la fixture `client` usa la aplicación de verdad y solo cambia la sesión.
- [ ] Qué comprobar de una respuesta, y por qué las claves exactas.
- [ ] Qué no puede probar la sesión de los tests, y cómo se prueba el `commit`.
- [ ] Cómo se prueba que un 503 no enseña la contraseña.
- [ ] Cómo se prueba `servir` sin servir, y por qué la CLI importa FastAPI tarde.
- [ ] Por qué `0.0.0.0` dentro, `127.0.0.1` fuera, y las migraciones antes de arrancar.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · def o async def: concurrencia en el servidor](04-def-o-async-def-concurrencia-en-el-servidor.md) | **05 · Probar y servir una API** | [Ejercicio 01 · Tu primera API](../2-practicas/ejercicio-01-primera-api/README.md) |
