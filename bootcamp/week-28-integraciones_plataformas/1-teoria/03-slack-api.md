# Slack API

## 1. Dos formas de enviar mensajes

| Método | Cuándo |
|--------|--------|
| **Incoming Webhook** | URL fija por canal; simple, sin SDK, sin permisos complejos |
| **Web API (`chat.postMessage`)** | Enviar a cualquier canal, historial, adjuntar archivos, bot token |

---

## 2. Incoming Webhook

```python
import httpx


SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T.../B.../..."


def notify_webhook(message: str, webhook_url: str = SLACK_WEBHOOK_URL) -> None:
    resp = httpx.post(webhook_url, json={"text": message})
    resp.raise_for_status()
```

---

## 3. Block Kit — Mensajes Enriquecidos

Block Kit es el sistema de componentes de Slack para mensajes estructurados.

```python
def build_delivery_message(
    project: str,
    client: str,
    youtube_url: str,
    vimeo_url: str,
    file_count: int,
) -> list[dict[str, object]]:
    return [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"Entrega lista: {project}"},
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Cliente:*\n{client}"},
                {"type": "mrkdwn", "text": f"*Archivos:*\n{file_count}"},
                {"type": "mrkdwn", "text": f"*YouTube:*\n<{youtube_url}|Ver en YouTube>"},
                {"type": "mrkdwn", "text": f"*Vimeo:*\n<{vimeo_url}|Ver en Vimeo>"},
            ],
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Abrir en YouTube"},
                    "url": youtube_url,
                    "style": "primary",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Abrir en Vimeo"},
                    "url": vimeo_url,
                },
            ],
        },
    ]
```

---

## 4. Enviar con `slack-sdk`

```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def send_delivery_notification(
    token: str,
    channel: str,
    project: str,
    client_name: str,
    youtube_url: str,
    vimeo_url: str,
    file_count: int = 0,
) -> str:
    slack = WebClient(token=token)
    blocks = build_delivery_message(project, client_name, youtube_url, vimeo_url, file_count)

    try:
        resp = slack.chat_postMessage(
            channel=channel,
            text=f"Entrega lista: {project}",  # fallback para notificaciones
            blocks=blocks,
        )
        return str(resp["ts"])  # timestamp del mensaje
    except SlackApiError as e:
        raise RuntimeError(f"Slack error: {e.response['error']}") from e
```

---

## 5. Subir Archivos

```python
from pathlib import Path


def upload_file_to_slack(
    token: str,
    channel: str,
    file_path: Path,
    title: str = "",
    comment: str = "",
) -> None:
    slack = WebClient(token=token)
    with file_path.open("rb") as f:
        slack.files_upload_v2(
            channel=channel,
            file=f,
            filename=file_path.name,
            title=title or file_path.stem,
            initial_comment=comment,
        )
```

`files_upload_v2` reemplaza al deprecated `files_upload` y usa el nuevo endpoint de upload en dos pasos.

---

## 6. Notificación de Error

```python
def notify_error(
    token: str,
    channel: str,
    project: str,
    stage: str,
    error_message: str,
) -> None:
    slack = WebClient(token=token)
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":red_circle: *Pipeline fallido*\n*Proyecto:* {project}\n*Etapa:* `{stage}`",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"```{error_message[:500]}```"},
        },
    ]
    slack.chat_postMessage(channel=channel, text=f"Error en {project}", blocks=blocks)
```

---

## Resumen

| Operación | Herramienta |
|-----------|-------------|
| Mensaje simple | Incoming Webhook + `httpx.post` |
| Mensaje estructurado | `WebClient.chat_postMessage(blocks=[...])` |
| Subir archivo | `WebClient.files_upload_v2(channel, file, filename)` |
| Block Kit | Header, Section, Divider, Actions, Image |
| Error handling | `SlackApiError` con `e.response["error"]` |
