# Rúbrica de Evaluación — Semana 28: Integraciones con Plataformas

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica el flujo OAuth2 de YouTube: authorization URL → código → token → refresh | 8 |
| Describe qué es el protocolo TUS y por qué Vimeo lo usa para uploads grandes | 7 |
| Explica la diferencia entre un Incoming Webhook y usar `chat.postMessage` de Slack SDK | 8 |
| Describe cómo Notion API estructura una base de datos: database_id, properties, page | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Sube un video a YouTube con título, descripción, tags y estado `unlisted` | 10 |
| Envía un mensaje Block Kit a Slack con sección, campos y enlace de acción | 10 |
| Envía un embed a Discord con color, título, fields y thumbnail | 10 |
| Actualiza una fila de base de datos en Notion con estado y URL de entrega | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `studio-distributor publish` sube a YouTube y Vimeo con metadata del proyecto | 12 |
| Después del upload, notifica a Slack y actualiza el registro en Notion | 10 |
| Los errores de plataforma se manejan individualmente: un fallo no cancela las demás plataformas | 5 |
| mypy --strict pasa sin errores en el módulo principal | 3 |
