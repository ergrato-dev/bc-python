# Glosario — Semana 18

| Término | Definición |
|---|---|
| **`.env`** | Archivo con las variables de configuración de **tu** máquina, una `NOMBRE=valor` por línea. Puede tener secretos: nunca va a Git ni a la imagen Docker |
| **`.env.example`** | La plantilla de `.env`: las mismas claves, sin valores de verdad. Va a Git, para que quien clone el repositorio sepa qué configurar |
| **`AsyncClient`** | El cliente asíncrono de httpx: se abre con `async with` y cada petición se espera con `await`. Reutiliza conexiones entre peticiones |
| **`Authorization`** | Cabecera de la petición que dice quién eres. Con un token: `Authorization: Bearer <token>` |
| **Backoff (espera exponencial)** | Esperar cada vez más antes de cada reintento: `backoff`, el doble, el doble otra vez. Con 0,5 s y 3 reintentos: 0,5 + 1 + 2 |
| **Cabecera** | Una línea `Nombre: valor` de una petición o una respuesta, antes del cuerpo. Los nombres no distinguen mayúsculas |
| **Cliente** | El programa que manda la petición. En httpx, también el objeto (`Client`, `AsyncClient`) que guarda las conexiones y lo que comparten todas las peticiones |
| **Código de estado** | El número de tres cifras de la respuesta. `2xx` bien, `3xx` en otro sitio, `4xx` error de la petición, `5xx` error del servidor |
| **Configuración** | Lo que cambia de una máquina a otra (un token, un plazo, una dirección) y por eso va fuera del código, en el entorno |
| **Costura (*seam*)** | Un punto por donde un test puede cambiar una pieza sin tocar el resto. En tu proyecto, el parámetro `transport` de `make_client` |
| **Cuerpo** | Lo que va después de las cabeceras: el JSON de una respuesta, los datos de un `POST`. Son solo bytes, y se validan |
| **Entorno (variables de)** | El diccionario de textos que cada proceso recibe de quien lo arranca. En Python, `os.environ`. Gana a `.env` |
| **`FetchError`** | La excepción de tu proyecto para una descarga que no salió bien, después de los reintentos que tocaban |
| **`follow_redirects`** | Opción de httpx para seguir solo las respuestas `3xx` hasta la URL final. Por defecto, no las sigue |
| **HTTP** | El protocolo de petición y respuesta de la web y de casi todas las API |
| **HTTPS** | HTTP sobre una conexión cifrada con TLS, en la que además el cliente comprueba el certificado del servidor. El único sitio por donde viaja un token |
| **`HTTPStatusError`** | La excepción de `raise_for_status()`: hubo respuesta, y su código es `4xx` o `5xx` |
| **httpx** | Biblioteca de clientes HTTP para Python, síncrona y asíncrona, con plazos por defecto y `MockTransport` para los tests |
| **Idempotente** | Una petición que, repetida, deja el servidor igual que hecha una vez: `GET`, `PUT`, `DELETE`. Solo esas se reintentan sin miedo |
| ***Jitter*** | Un poco de azar en cada espera de reintento, para que muchos clientes que fallaron a la vez no vuelvan a la vez |
| **`Limits`** | `httpx.Limits(max_connections=...)`: cuántas conexiones abre como mucho un cliente. Por defecto, 100 |
| **Método** | Lo que pides hacer con un recurso: `GET` leer, `POST` crear, `PUT` sustituir, `DELETE` borrar... |
| **`MockTransport`** | Transporte de httpx que, en lugar de usar la red, llama a tu función con cada petición y devuelve lo que ella devuelva. Para tests |
| **Petición** | Lo que manda el cliente: método, URL, cabeceras y, a veces, cuerpo |
| **Plazo (*timeout*)** | Cuánto se espera antes de dar por perdida una operación. En httpx, por fases (`connect`, `read`, `write`, `pool`); para un total, `asyncio.timeout` |
| **`pydantic-settings`** | Extensión de Pydantic con `BaseSettings`: un modelo que se rellena solo con el entorno y `.env`, convertido y validado |
| **`raise_for_status`** | Método de la respuesta de httpx que lanza `HTTPStatusError` si el código es `4xx` o `5xx`; si no, no hace nada |
| **Reintento** | Repetir una petición que falló por algo pasajero. Solo los fallos de red, los `429` y los `5xx`, con espera y con tope |
| **Respuesta** | Lo que devuelve el servidor: código de estado, cabeceras y cuerpo |
| **`Retry-After`** | Cabecera con la que el servidor dice cuánto esperar antes de volver, con un `429` o un `503` |
| **Revocar** | Anular un token en la web de la API, para que deje de valer. Lo único que arregla un secreto filtrado |
| **Secreto** | Un dato que da acceso a algo: un token, una contraseña, una clave. No va en el código, ni en Git, ni en los registros |
| **`SecretStr`** | Tipo de Pydantic para secretos: se imprime como `'**********'`, y el valor solo sale con `get_secret_value()` |
| **Servidor** | El programa que recibe las peticiones y contesta. `python -m http.server` es uno, solo para pruebas |
| **`Settings`** | La clase de tu proyecto, en `settings.py`, que lee `OBSERVATORIO_TOKEN`, `OBSERVATORIO_TIMEOUT` y `OBSERVATORIO_RETRIES` |
| **Token (*API key*)** | Un texto largo que te identifica ante una API. Quien lo tiene es tú para esa API |
| **Transporte** | La pieza de un cliente de httpx que de verdad abre conexiones y manda bytes. Se puede cambiar por `MockTransport` |
| **`TransportError`** | La familia de excepciones de httpx para "no hubo respuesta": `ConnectError`, `ReadTimeout`, `UnsupportedProtocol`... |
| **URL** | La dirección de un recurso: esquema, servidor, puerto, ruta y consulta |
| **`User-Agent`** | Cabecera de la petición que dice qué programa pide. La tuya: `observatorio/0.18.0` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
