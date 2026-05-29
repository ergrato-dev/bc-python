# Rúbrica de Evaluación — Semana 19: HTTP y APIs con httpx

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre `httpx.get()` (one-shot) y `httpx.Client` (session) y cuándo usar cada uno | 8 |
| Describe por qué el retry con jitter aleatorio evita el thundering herd | 7 |
| Distingue `ConnectTimeout`, `ReadTimeout` y `HTTPStatusError` y cómo manejar cada uno | 8 |
| Explica el OAuth2 client credentials flow: qué se envía, qué se recibe, cómo se usa el token | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Implementa `httpx.Auth` personalizado para Bearer Token o API Key | 10 |
| Usa `tenacity.retry` con `stop_after_attempt`, `wait_exponential` y `retry_if_exception_type` | 10 |
| Maneja correctamente `HTTPStatusError` (4xx vs 5xx) y `ConnectError` sin crashear | 10 |
| Valida una respuesta JSON de API con un modelo Pydantic y maneja `ValidationError` | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `studio-api-client` tiene al menos 2 proveedores integrados con auth distinta | 10 |
| Todas las llamadas tienen timeout configurado y retry en errores de red | 8 |
| Respuestas validadas con Pydantic — nunca se accede a `response.json()` sin validar | 7 |
| mypy --strict pasa sin errores | 5 |
