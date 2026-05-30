"""
Ejercicio 03: Slack API — Block Kit y Notificaciones — SOLUCIÓN
===============================================================
"""
from __future__ import annotations

import os
from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
CHANNEL = os.getenv("SLACK_CHANNEL", "#general")


def send_delivery_notification(
    project: str,
    client: str,
    youtube_url: str,
    vimeo_url: str,
    file_count: int = 0,
) -> str:
    slack = WebClient(token=SLACK_TOKEN)
    blocks: list[dict[str, object]] = [
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
                    "text": {"type": "plain_text", "text": "YouTube"},
                    "url": youtube_url,
                    "style": "primary",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Vimeo"},
                    "url": vimeo_url,
                },
            ],
        },
    ]

    try:
        resp = slack.chat_postMessage(
            channel=CHANNEL,
            text=f"Entrega lista: {project}",
            blocks=blocks,
        )
        return str(resp["ts"])
    except SlackApiError as e:
        raise RuntimeError(f"Slack error: {e.response['error']}") from e


def send_error_notification(project: str, stage: str, error: str) -> None:
    slack = WebClient(token=SLACK_TOKEN)
    blocks: list[dict[str, object]] = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":red_circle: *Pipeline fallido*\n*Proyecto:* {project}\n*Etapa:* `{stage}`",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"```{error[:500]}```"},
        },
    ]
    slack.chat_postMessage(
        channel=CHANNEL,
        text=f"Error en {project}",
        blocks=blocks,
    )


def upload_report_file(file_path: str, title: str = "") -> None:
    slack = WebClient(token=SLACK_TOKEN)
    path = Path(file_path)
    with path.open("rb") as f:
        slack.files_upload_v2(
            channel=CHANNEL,
            file=f,
            filename=path.name,
            title=title or path.stem,
        )


if __name__ == "__main__":
    if not SLACK_TOKEN:
        print("Configurar SLACK_BOT_TOKEN en variables de entorno")
        raise SystemExit(1)

    print("1. Enviando notificación de entrega...")
    ts = send_delivery_notification(
        project="canal9/spot-verano-2024",
        client="Canal 9",
        youtube_url="https://youtu.be/dQw4w9WgXcQ",
        vimeo_url="https://vimeo.com/12345678",
        file_count=3,
    )
    print(f"   Mensaje enviado. ts={ts}")

    print("2. Enviando notificación de error...")
    send_error_notification(
        project="canal9/spot-verano-2024",
        stage="export",
        error="ConnectionError: S3 bucket not accessible\n  at s3_uploader.py:42",
    )
    print("   Notificación de error enviada")

    print("OK — Ejercicio 03 completado")
