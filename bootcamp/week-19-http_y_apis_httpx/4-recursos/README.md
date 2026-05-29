# Recursos — Semana 19: HTTP y APIs con httpx

## Webgrafía esencial

- [httpx — Documentación oficial](https://www.python-httpx.org/)
- [httpx — Authentication](https://www.python-httpx.org/advanced/authentication/)
- [httpx — Timeouts](https://www.python-httpx.org/advanced/timeouts/)
- [httpx — Clients](https://www.python-httpx.org/advanced/clients/)
- [tenacity — Documentación](https://tenacity.readthedocs.io/)
- [Pydantic v2 — Validación de modelos](https://docs.pydantic.dev/latest/concepts/models/)
- [MDN — HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [RFC 6749 — OAuth2 Client Credentials](https://datatracker.ietf.org/doc/html/rfc6749#section-4.4)
- [Token Bucket Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Token_bucket)

## Videografía

- [ArjanCodes — httpx Tutorial (YouTube)](https://www.youtube.com/results?search_query=httpx+python+tutorial)
- [Tech With Tim — Python APIs with httpx](https://www.youtube.com/results?search_query=python+httpx+api+client)
- [Pydantic v2 — Full Course](https://www.youtube.com/results?search_query=pydantic+v2+python+tutorial)

## Lecturas complementarias

- [The Retry Pattern — Microsoft Azure Docs](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Circuit Breaker Pattern — Martin Fowler](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Exponential Backoff and Jitter — AWS Blog](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Rate Limiting Algorithms Compared](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)

## Herramientas de desarrollo

- [httpbin.org](https://httpbin.org) — servidor de prueba para requests HTTP
- [Hoppscotch](https://hoppscotch.io) — cliente HTTP alternativo a Postman (open source)
- [mitmproxy](https://mitmproxy.org) — proxy para inspeccionar tráfico HTTP
- [pytest-httpx](https://colin-b.github.io/pytest_httpx/) — mock de httpx en tests

## Librerías relacionadas

| Librería | Uso |
|----------|-----|
| `httpx` | Cliente HTTP sync/async |
| `tenacity` | Retry con backoff declarativo |
| `pydantic` | Validación de modelos de datos |
| `circuitbreaker` | Circuit breaker en producción |
| `limits` | Rate limiting avanzado con Redis |
| `authlib` | OAuth2 completo (incluye PKCE) |
