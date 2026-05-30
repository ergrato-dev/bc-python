# Recursos — Semana 28: Integraciones con Plataformas

## Webgrafía

### Documentación oficial

| Recurso | URL | Por qué vale la pena |
|---------|-----|----------------------|
| YouTube Data API v3 | https://developers.google.com/youtube/v3/docs | Referencia completa de endpoints |
| YouTube — Upload a video | https://developers.google.com/youtube/v3/guides/uploading_a_video | Guía de upload resumable |
| Vimeo API Docs | https://developer.vimeo.com/api/reference | Referencia REST completa |
| PyVimeo — GitHub | https://github.com/vimeo/vimeo.py | Cliente oficial Python con TUS |
| Slack Block Kit | https://api.slack.com/block-kit | Builder visual + referencia |
| Slack Web API | https://api.slack.com/methods | Lista de métodos: chat, files, channels |
| Discord Webhooks | https://discord.com/developers/docs/resources/webhook | Embeds, rate limits |
| Notion API | https://developers.notion.com/reference | Pages, databases, blocks |

### Guías prácticas

| Recurso | Tema |
|---------|------|
| [Slack Block Kit Builder](https://app.slack.com/block-kit-builder) | Editor visual de Block Kit en tiempo real |
| [TUS Protocol Spec](https://tus.io/protocols/resumable-upload) | Especificación del protocolo de upload resumable |
| [Google OAuth2 Playground](https://developers.google.com/oauthplayground/) | Probar tokens OAuth2 de Google |
| [Notion API Postman Collection](https://developers.notion.com/reference/intro) | Colección lista para importar |

---

## Stack técnico de la semana

```
google-api-python-client    # YouTube Data API v3
google-auth-oauthlib        # OAuth2 flow para YouTube
PyVimeo                     # cliente oficial Vimeo con TUS
slack-sdk                   # Slack Web API y webhooks
httpx                       # Discord webhooks y Notion API (REST directo)
```

### Instalación rápida

```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
pip install PyVimeo
pip install slack-sdk
pip install httpx
```

---

## Configuración de credenciales

| Plataforma | Qué configurar |
|------------|----------------|
| YouTube | Google Cloud Console → OAuth2 credentials → `client_secrets.json` |
| Vimeo | developer.vimeo.com → Create App → Personal Access Token |
| Slack | api.slack.com → Create App → Bot Token Scopes: `chat:write`, `files:write` |
| Discord | Discord server → Channel → Integrations → Webhooks |
| Notion | notion.so/my-integrations → Create integration → share DB con la integración |

---

## Herramientas complementarias

| Herramienta | Uso |
|-------------|-----|
| [Slack Block Kit Builder](https://app.slack.com/block-kit-builder) | Diseñar mensajes Block Kit visualmente |
| [Postman](https://www.postman.com/) | Probar endpoints Notion/Discord directamente |
| [ngrok](https://ngrok.com/) | Exponer localhost para OAuth2 callbacks |
| [Discord Embed Visualizer](https://leovoel.github.io/embed-visualizer/) | Preview de embeds Discord |

---

## Navegación

← [Teoría](../1-teoria/) · [Proyecto](../3-proyecto/)
