"""
Ejercicio 03: Slack API — Block Kit y Notificaciones
====================================================
Envía mensajes Block Kit a Slack con botones, campos y notificación de error.

Requisitos:
    pip install slack-sdk

Variables de entorno:
    SLACK_BOT_TOKEN=xoxb-...
    SLACK_CHANNEL=#distribuciones

Ejecutar:
    python main.py
"""
from __future__ import annotations

import os


SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
CHANNEL = os.getenv("SLACK_CHANNEL", "#general")


def send_delivery_notification(
    project: str,
    client: str,
    youtube_url: str,
    vimeo_url: str,
    file_count: int = 0,
) -> str:
    """
    Envía un mensaje Block Kit de entrega exitosa.
    Devuelve el timestamp del mensaje (ts).
    """
    # TODO: importar WebClient de slack_sdk
    # TODO: construir blocks con header, divider, section (fields), actions (botones)
    # TODO: slack.chat_postMessage(channel=CHANNEL, text=fallback, blocks=blocks)
    # TODO: capturar SlackApiError y relanzar como RuntimeError
    raise NotImplementedError


def send_error_notification(project: str, stage: str, error: str) -> None:
    """Envía un mensaje de error en rojo con el traceback."""
    # TODO: section con mrkdwn + code block del error (500 chars max)
    raise NotImplementedError


def upload_report_file(file_path: str, title: str = "") -> None:
    """Sube un archivo PDF/CSV al canal de Slack."""
    # TODO: WebClient.files_upload_v2(channel=CHANNEL, file=..., title=...)
    raise NotImplementedError


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
