# Glosario — Semana 19: HTTP y APIs con httpx

## A

**API Key**
Credencial estática que se envía como header (`X-API-Key`) o query param para identificar al cliente. Simple pero no permite scopes ni expiración automática.

**AsyncClient** (httpx)
Versión asíncrona de `httpx.Client`. Requiere `async with` y `await` en cada llamada. Permite concurrencia con `asyncio.gather`.

## B

**Backoff exponencial**
Estrategia de espera entre reintentos donde el tiempo crece exponencialmente: 1s, 2s, 4s, 8s... Evita saturar el servidor con reintentos inmediatos.

**Bearer Token**
Esquema de autenticación HTTP donde el cliente envía `Authorization: Bearer <token>`. Común con JWT y OAuth2.

## C

**Circuit Breaker**
Patrón que detiene completamente las llamadas a un servicio cuando detecta N fallos consecutivos. Después de un cooldown, prueba de nuevo (half-open).

**Client Credentials Flow** (OAuth2)
Flujo OAuth2 para autenticación server-to-server sin usuario: intercambia `client_id + client_secret` por un `access_token`.

**Connection Pool**
Conjunto de conexiones TCP reutilizables que mantiene `httpx.Client`. Evita el overhead de abrir/cerrar TCP en cada request.

**ConnectError** (httpx)
Excepción lanzada cuando no se puede establecer conexión TCP al servidor (sin ruta, DNS fallido, etc.).

**ConnectTimeout** (httpx)
Subtipo de `TimeoutException`: el servidor no respondió durante el handshake TCP.

## H

**httpx**
Librería HTTP moderna para Python con API sync y async, HTTP/2, timeouts granulares y transports intercambiables.

**HTTPStatusError** (httpx)
Excepción lanzada por `response.raise_for_status()` cuando el status code es 4xx o 5xx.

## J

**Jitter**
Variación aleatoria añadida al tiempo de espera en backoff exponencial. Evita el thundering herd cuando múltiples clientes reintentan al mismo tiempo.

**JWT** (JSON Web Token)
Token compacto y autosuficiente que contiene claims firmados digitalmente. Común como Bearer Token en APIs modernas.

## O

**OAuth2**
Framework de autorización estándar (RFC 6749) que permite a una aplicación obtener acceso limitado a recursos en nombre de un usuario o de sí misma.

## P

**Pydantic**
Librería de validación de datos para Python basada en type hints. Permite definir modelos con validación automática al parsear JSON.

## R

**Rate Limit**
Límite al número de requests que un cliente puede hacer en una ventana de tiempo. Violarlo devuelve `429 Too Many Requests`.

**ReadTimeout** (httpx)
El servidor comenzó a responder pero tardó demasiado en enviar todos los datos.

**Retry-After**
Header HTTP que indica cuántos segundos esperar antes de volver a intentar (en respuestas 429 o 503).

## S

**Sliding Window**
Algoritmo de rate limiting que cuenta las llamadas en una ventana temporal que avanza continuamente, más preciso que ventanas fijas.

## T

**tenacity**
Librería de retry para Python. Permite declarar políticas de reintento con decoradores: stop, wait, retry conditions, logging.

**Thundering Herd**
Problema donde múltiples clientes reintentan simultáneamente después de un fallo, saturando aún más el servidor. Se evita con jitter.

**Token Bucket**
Algoritmo de rate limiting: un bucket acumula tokens a una tasa fija. Cada llamada consume un token. Permite ráfagas hasta la capacidad máxima.

**Transport** (httpx)
Capa de bajo nivel que maneja la comunicación real. Permite mockear llamadas en tests (`MockTransport`, `WSGITransport`, `ASGITransport`).

## V

**ValidationError** (Pydantic)
Excepción con detalles estructurados sobre qué campos fallaron la validación y por qué.
