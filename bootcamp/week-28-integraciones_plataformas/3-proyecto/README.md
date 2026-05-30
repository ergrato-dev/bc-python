# Proyecto Semana 28 — studio-distributor

## Objetivo

Construir el módulo de distribución de Studio BC que:

1. Publica el render final en **YouTube** (upload resumable + thumbnail + playlist)
2. Publica en **Vimeo** (upload TUS + álbum)
3. Notifica a **Slack** con Block Kit (URLs, botones de acción)
4. Actualiza el registro en **Notion** (estado + URLs + nota)
5. Maneja errores por plataforma de forma independiente (un fallo no cancela el resto)

---

## Estructura

```
starter/
├── pyproject.toml
├── .env.example
├── src/
│   ├── __init__.py
│   ├── config.py              # DistributorConfig con pydantic-settings
│   ├── youtube_publisher.py   # YouTubePublisher
│   ├── vimeo_publisher.py     # VimeoPublisher
│   ├── notifier.py            # SlackNotifier + DiscordNotifier
│   ├── notion_updater.py      # NotionUpdater
│   ├── distributor.py         # Distributor: orchestrate all platforms
│   └── __main__.py            # Typer CLI: publish, notify, status
└── tests/
    ├── __init__.py
    ├── test_notifier.py
    └── test_notion_updater.py
```

---

## Comandos CLI

```bash
# Publicar en todas las plataformas
python -m src publish --path output/spot_verano_v3.mp4 \
  --title "Spot Verano 2024 — Canal 9" \
  --project "canal9/spot-verano" \
  --client-email "prod@canal9.com"

# Solo notificar (sin publicar)
python -m src notify --project "canal9/spot-verano" \
  --youtube-url "https://youtu.be/ID" \
  --vimeo-url "https://vimeo.com/ID"
```

---

## Configuración (.env)

```
YOUTUBE_CLIENT_SECRETS=client_secrets.json
YOUTUBE_TOKEN_PATH=youtube_token.json

VIMEO_TOKEN=...
VIMEO_KEY=...
VIMEO_SECRET=...

SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL=#distribuciones

DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

NOTION_TOKEN=secret_...
NOTION_DATABASE_ID=...
```

---

## Criterios de Aprobación

- [ ] YouTube + Vimeo: upload con metadata correcta
- [ ] Slack: Block Kit con URLs y botones
- [ ] Notion: actualización de estado + URLs
- [ ] Errores por plataforma independientes
- [ ] `mypy --strict` sin errores
