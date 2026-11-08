# Webgrafía — Semana 20

| Recurso | Para qué |
|---|---|
| [Tutorial de FastAPI](https://fastapi.tiangolo.com/es/tutorial/) (en español) | El tutorial oficial, paso a paso. Esta semana: [parámetros de ruta](https://fastapi.tiangolo.com/es/tutorial/path-params/), [cuerpo](https://fastapi.tiangolo.com/es/tutorial/body/), [modelo de respuesta](https://fastapi.tiangolo.com/es/tutorial/response-model/) y [manejo de errores](https://fastapi.tiangolo.com/es/tutorial/handling-errors/): la teoría 02 y los ejercicios 01 y 02 |
| [Dependencias con `yield`](https://fastapi.tiangolo.com/es/tutorial/dependencies/dependencies-with-yield/) (en español) | Qué se ejecuta antes y después del `yield`, y qué pasa con las excepciones. La teoría 03 |
| [Eventos de lifespan](https://fastapi.tiangolo.com/es/advanced/events/) (en español) | El lifespan, con un ejemplo de algo que se carga una vez al arrancar |
| [Concurrencia y async / await](https://fastapi.tiangolo.com/es/async/) (en español) | La explicación de FastAPI de cuándo `def` y cuándo `async def`, con hamburguesas. La teoría 04 |
| [Testing](https://fastapi.tiangolo.com/es/tutorial/testing/) y [dependencias en los tests](https://fastapi.tiangolo.com/es/advanced/testing-dependencies/) (en español) | `TestClient` y `dependency_overrides`: la teoría 05 |
| [Bases de datos SQL](https://fastapi.tiangolo.com/es/tutorial/sql-databases/) (en español) | Una API con base de datos según FastAPI, con SQLModel. Compárala con la tuya: misma sesión por petición, otra biblioteca para los modelos |
| [Sesión: cuándo crearla, confirmarla y cerrarla](https://docs.sqlalchemy.org/en/21/orm/session_basics.html) (en inglés) | Busca "When do I construct a Session, when do I commit it, and when do I close it?": la regla de una sesión por petición, explicada por SQLAlchemy |
| [uvicorn](https://uvicorn.dev/) (en inglés) | Las opciones del servidor. Sigue con [despliegue](https://uvicorn.dev/deployment/): procesos, `--workers` y qué poner delante |
| [Starlette](https://starlette.dev/) (en inglés) | La biblioteca sobre la que está FastAPI: peticiones, respuestas, rutas y `TestClient` |
| [Introducción a ASGI](https://asgi.readthedocs.io/en/latest/introduction.html) (en inglés) | El contrato entre el servidor y la aplicación: `scope`, `receive` y `send`. La teoría 01, sección 3 |
| [Códigos de estado HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Reference/Status) (en español) | MDN, uno por uno. Y la cabecera [`Location`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Location) (en inglés) |
| [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) (en inglés) | La definición oficial de métodos, códigos y cabeceras. Para consultar, no para leer de corrido: busca "201 Created" o "Idempotent Methods" |
| [Especificación OpenAPI](https://spec.openapis.org/oas/latest.html) (en inglés) | Lo que hay dentro de tu `/openapi.json` |
| [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) (en inglés) | Las reglas de diseño de API de una empresa grande: nombres de recursos, códigos, errores, paginación. Para cuando tu API crezca |
| [httpx2](https://github.com/pydantic/httpx2) (en inglés) | El sucesor de `httpx` que usa `TestClient` |
| [bc-fastapi](https://github.com/ergrato-dev/bc-fastapi) (en español) | El bootcamp de FastAPI: autenticación, arquitectura por capas, WebSockets, seguridad y despliegue. La continuación de esta semana |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
