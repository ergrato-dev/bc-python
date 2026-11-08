# Glosario — Semana 20

| Término | Definición |
|---|---|
| **API HTTP** | Un conjunto de rutas que otros programas llaman por HTTP, con un contrato: qué esperan y qué devuelven, casi siempre en JSON |
| **`APIRouter`** | Un grupo de rutas de FastAPI que se añade a una aplicación con `include_router`. Las rutas de tu API viven en uno, a nivel de módulo |
| **`app.state`** | Un espacio de la aplicación para guardar lo que dura toda su vida, como el motor. Las rutas lo leen con `request.app.state` |
| **ASGI** | *Asynchronous Server Gateway Interface*: el contrato entre un servidor y una aplicación de Python. La aplicación es una corrutina que recibe `scope`, `receive` y `send` |
| **Bucle de eventos** | El hilo de asyncio que reparte el tiempo entre corrutinas cada vez que una espera con `await`. Si algo lo bloquea, nada más avanza |
| **Cabecera** | Un par nombre-valor de una petición o una respuesta, como `content-type: application/json` o `location: /loads/7` |
| **Código de estado** | El número de tres cifras que resume una respuesta: 2xx bien, 4xx culpa de quien llama, 5xx culpa del servidor |
| **Consulta (*query string*)** | Lo que va detrás del `?` en una URL: `?load=3&limit=10`. En FastAPI, los parámetros sencillos que no están en la ruta |
| **Contrato** | Lo que una API promete: rutas, métodos, lo que acepta y lo que devuelve, con sus códigos. Cambiarlo rompe a quien la usa |
| **`create_app`** | La función que construye la aplicación de tu API con la URL de la base. Así importar `api.py` no depende del entorno |
| **Cuerpo (*body*)** | Los datos que viajan después de las cabeceras. En un `POST` de tu API, un JSON que se valida con `LoadIn` |
| **`curl`** | El cliente HTTP de la terminal. `-i` enseña las cabeceras, `-X` cambia el método, `-d` envía un cuerpo |
| **`def` o `async def`** | Cómo se declara una ruta. FastAPI ejecuta una `def` en un hilo de su pool y una `async def` en el bucle de eventos |
| **Dependencia** | Una función que FastAPI llama antes de la ruta para darle algo que necesita, declarada con `Depends`. Se resuelve una vez por petición |
| **Dependencia con `yield`** | Una dependencia con dos mitades: lo de antes del `yield` prepara (abre la sesión) y lo de después recoge (la cierra) |
| **`dependency_overrides`** | El diccionario de una aplicación FastAPI que sustituye una dependencia por otra. Lo usan los tests para dar su sesión |
| **`detail`** | La clave del cuerpo de error de FastAPI: un texto con `HTTPException`, o la lista de problemas en un 422 |
| ***Endpoint*** | Una ruta con su método: `GET /loads` y `POST /loads` son dos *endpoints* de la misma ruta |
| **FastAPI** | El *framework* web de Python que usa las anotaciones de tipo para validar, convertir y documentar. Está construido sobre Starlette y Pydantic |
| ***Healthcheck*** | Una comprobación periódica de que un servicio funciona. El de tu API pregunta a `/health`, que pregunta a PostgreSQL |
| **`HTTPException`** | La excepción de FastAPI que corta una ruta y responde con un código y un `detail` |
| **httpx2** | El sucesor de `httpx`. `TestClient` lo usa por dentro; en tu proyecto, solo en el grupo `dev` |
| **Lifespan** | Un gestor de contexto que FastAPI ejecuta al arrancar (antes del `yield`) y al parar (después). Abre y cierra el motor |
| **`Location`** | La cabecera de un 201 que dice dónde está lo que se acaba de crear: `/loads/7` |
| **`loc`** | En un 422, dónde está el problema: `["body", "measurements", 1, "label"]` es la etiqueta de la segunda medida |
| **Manejador de excepciones** | Una función que convierte una excepción en una respuesta para todas las rutas. El tuyo convierte `OperationalError` en un 503 |
| **Método** | El verbo de una petición: `GET` lee, `POST` crea, `DELETE` borra, `PUT` y `PATCH` cambian |
| **OpenAPI** | El formato estándar que describe una API: rutas, parámetros, cuerpos y respuestas. FastAPI lo genera en `/openapi.json` |
| **Parámetro de ruta** | Un hueco de la ruta, como `{load_id}` en `/loads/{load_id}`, que la función recibe convertido a su tipo |
| **Petición** | Lo que envía un cliente: método, ruta, consulta, cabeceras y cuerpo |
| **Pool de hilos** | Los hilos que FastAPI (con AnyIO) tiene preparados para ejecutar las rutas `def` sin bloquear el bucle de eventos. Son 40 por defecto |
| **Recurso** | Lo que nombra una ruta: `/loads` es la colección de cargas y `/loads/7` es una de ellas. Las rutas son sustantivos |
| **Respuesta** | Lo que devuelve el servidor: código, cabeceras y cuerpo |
| **Ruta** | La parte de la URL que elige qué se pide (`/loads/7/measurements`), y la función que la atiende |
| **Servidor** | El programa que acepta conexiones y responde peticiones. En tu proyecto, uvicorn |
| **`SessionDep`** | El alias `Annotated[Session, Depends(get_session)]`, para no repetirlo en cada ruta |
| **Starlette** | La biblioteca ASGI sobre la que está FastAPI: peticiones, respuestas, rutas, manejadores y `TestClient` |
| **Swagger UI** | La página de `/docs`: lee el OpenAPI de tu API y te deja probar cada ruta desde el navegador |
| **`TestClient`** | El cliente de pruebas de FastAPI: llama a la aplicación por ASGI, sin red. Dentro de un `with`, ejecuta el lifespan |
| **Tipo de retorno** | La anotación `-> ...` de una ruta: FastAPI convierte, valida y filtra la respuesta con ella |
| **uvicorn** | El servidor ASGI que usa tu proyecto: abre el puerto, habla HTTP y llama a la aplicación |
| **Validación** | Comprobar que los datos que llegan cumplen el contrato antes de usarlos. En FastAPI, la hace Pydantic con tus anotaciones |
| ***Workers*** | Procesos completos del servidor, cada uno con su aplicación y su pool de conexiones: `uvicorn --workers 4` |
| **`0.0.0.0`** | La dirección que significa "todas las interfaces". Un servidor que escucha en ella acepta conexiones de fuera; dentro de un contenedor es necesaria, en tu portátil es peligrosa |
| **`127.0.0.1`** | La dirección de tu propia máquina (*localhost*). Un servidor que solo escucha en ella no es alcanzable desde la red |
| **201 Created** | Creado. Va con `Location`. Lo responde `POST /loads` |
| **204 No Content** | Hecho, sin cuerpo. Lo responde `DELETE /loads/{id}` |
| **404 Not Found** | Lo que se pide no existe: una carga que no está, o una ruta que no hay |
| **422 Unprocessable Content** | La petición se entiende, pero sus datos no cumplen el contrato. FastAPI lo responde antes de llamar a tu función |
| **503 Service Unavailable** | El servidor no puede ahora, por algo de lo que depende. Lo responde tu API si PostgreSQL no contesta |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
