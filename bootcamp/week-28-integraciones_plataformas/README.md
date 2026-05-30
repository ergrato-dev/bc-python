# Semana 28: Integraciones con Plataformas

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Subir videos a YouTube con la Data API v3: metadata, thumbnails y listas de reproducción
- Publicar en Vimeo usando upload chunked por protocolo TUS
- Enviar notificaciones ricas a Slack con Block Kit y adjuntar archivos
- Enviar embeds a Discord via webhooks con campos, color y thumbnails
- Actualizar bases de datos de Notion via API: propiedades y bloques de contenido

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [YouTube Data API v3](1-teoria/01-youtube-api.md) | Upload resumable, metadata, thumbnails, playlists |
| 02 | [Vimeo API](1-teoria/02-vimeo-api.md) | Upload TUS, privacidad, álbumes, embed settings |
| 03 | [Slack API](1-teoria/03-slack-api.md) | Webhooks, Block Kit, chat.postMessage, files.upload |
| 04 | [Discord Webhooks](1-teoria/04-discord-webhooks.md) | Embeds, campos, rate limiting, retry |
| 05 | [Notion API](1-teoria/05-notion-api.md) | Bases de datos, propiedades, bloques de contenido |

---

## Estructura de la Semana

```
week-28-integraciones_plataformas/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-youtube-upload/
│   ├── 02-vimeo-chunked/
│   ├── 03-slack-notificacion/
│   └── 04-notion-update/
├── 3-proyecto/
│   ├── README.md           # studio-distributor
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: YouTube + Vimeo | 1.5h |
| 2 | Teoría: Slack + Discord + Notion | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `google-api-python-client` | YouTube Data API v3 |
| `google-auth-oauthlib` | OAuth2 flow para YouTube |
| `PyVimeo` | Cliente oficial Vimeo con upload TUS |
| `slack-sdk` | Slack Web API y webhooks |
| `httpx` | Discord webhooks y Notion API (REST directo) |

---

## Navegación

← [Semana 27 — Arquitectura de Pipelines](../week-27-arquitectura_pipelines/README.md) · [Semana 29 — Monitoreo de Pipelines](../week-29-monitoreo_pipelines/README.md) →
