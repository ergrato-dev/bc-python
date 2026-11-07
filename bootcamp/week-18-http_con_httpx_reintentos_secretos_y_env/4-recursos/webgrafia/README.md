# Webgrafía — Semana 18

| Recurso | Para qué |
|---|---|
| [Generalidades del protocolo HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Guides/Overview) (en español) | El diálogo de petición y respuesta, contado por MDN, con dibujos. El complemento de la teoría 01 |
| [Códigos de estado de respuesta HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Status) (en español) | Qué significa cada código, uno por uno. Ten la página abierta mientras haces el ejercicio 01 |
| [`Retry-After`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After) (en inglés) | Las dos formas de la cabecera, segundos o fecha, del paso 6 del ejercicio 03 |
| [httpx](https://www.python-httpx.org/) (en inglés) | La documentación oficial. Lee sobre todo [Clients](https://www.python-httpx.org/advanced/clients/), [Timeouts](https://www.python-httpx.org/advanced/timeouts/), [Resource Limits](https://www.python-httpx.org/advanced/resource-limits/) y [Exceptions](https://www.python-httpx.org/exceptions/): la teoría 02 |
| [Transports](https://www.python-httpx.org/advanced/transports/) (en inglés) | `MockTransport` y los reintentos de `HTTPTransport(retries=...)`: la teoría 05 y el paso 8 del ejercicio 03 |
| [Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) (en inglés) | El artículo clásico de AWS que compara reintentos con y sin *jitter*, con gráficas de cuánto trabajo le cuesta al servidor cada estrategia |
| [stamina](https://stamina.hynek.me/en/stable/) (en inglés) | Reintentos listos para producción, con buenos valores por defecto. Lee "Motivation": explica cada decisión de tu bucle de reintentos |
| [Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) (en inglés) | `pydantic-settings` entero: prefijos, `.env`, prioridades y fuentes. La teoría 04 |
| [Twelve-Factor App: Configuración](https://12factor.net/es/config) (en español) | Por qué la configuración va en el entorno y no en el código, en una página |
| [Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) (en inglés) | OWASP sobre secretos: dónde guardarlos, cómo rotarlos y qué hacer si se filtran. Más de lo que necesitas hoy, y lo que vas a necesitar mañana |
| [Acerca del escaneo de secretos](https://docs.github.com/es/code-security/secret-scanning/introduction/about-secret-scanning) (en español) | Cómo detecta GitHub tokens en tus *commits* y qué hace la protección de *push* |
| [`http.server`](https://docs.python.org/es/3.14/library/http.server.html) (en español) | El servidor de la biblioteca estándar que usas en el proyecto y en los tests, con su aviso de seguridad |
| [`uv run`](https://docs.astral.sh/uv/reference/cli/#uv-run) (en inglés) | Todas las opciones, `--env-file` incluida |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
