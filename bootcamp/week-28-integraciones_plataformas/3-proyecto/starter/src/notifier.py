from __future__ import annotations

from datetime import datetime, timezone

import httpx


class SlackNotifier:
    def __init__(self, token: str, channel: str) -> None:
        from slack_sdk import WebClient
        self._client = WebClient(token=token)
        self._channel = channel

    def notify_delivery(
        self,
        project: str,
        client: str,
        youtube_url: str,
        vimeo_url: str,
        file_count: int = 0,
    ) -> str:
        blocks: list[dict[str, object]] = [
            {"type": "header", "text": {"type": "plain_text", "text": f"Entrega lista: {project}"}},
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Cliente:*\n{client}"},
                    {"type": "mrkdwn", "text": f"*Archivos:*\n{file_count}"},
                    {"type": "mrkdwn", "text": f"*YouTube:*\n<{youtube_url}|Ver>"},
                    {"type": "mrkdwn", "text": f"*Vimeo:*\n<{vimeo_url}|Ver>"},
                ],
            },
            {
                "type": "actions",
                "elements": [
                    {"type": "button", "text": {"type": "plain_text", "text": "YouTube"}, "url": youtube_url, "style": "primary"},
                    {"type": "button", "text": {"type": "plain_text", "text": "Vimeo"}, "url": vimeo_url},
                ],
            },
        ]
        from slack_sdk.errors import SlackApiError
        try:
            resp = self._client.chat_postMessage(
                channel=self._channel,
                text=f"Entrega lista: {project}",
                blocks=blocks,
            )
            return str(resp["ts"])
        except SlackApiError as e:
            raise RuntimeError(f"Slack error: {e.response['error']}") from e

    def notify_error(self, project: str, stage: str, error: str) -> None:
        blocks: list[dict[str, object]] = [
            {
                "type": "section",
                "text": {"type": "mrkdwn",
                         "text": f":red_circle: *Pipeline fallido*\n*Proyecto:* {project}\n*Etapa:* `{stage}`"},
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": f"```{error[:500]}```"}},
        ]
        self._client.chat_postMessage(
            channel=self._channel, text=f"Error en {project}", blocks=blocks
        )


class DiscordNotifier:
    def __init__(self, webhook_url: str) -> None:
        self._url = webhook_url

    def notify_delivery(
        self,
        project: str,
        client: str,
        youtube_url: str,
        vimeo_url: str,
    ) -> None:
        embed: dict[str, object] = {
            "title": f"Entrega lista: {project}",
            "color": 0x3FB950,
            "fields": [
                {"name": "Cliente", "value": client, "inline": True},
                {"name": "YouTube", "value": f"[Ver]({youtube_url})", "inline": True},
                {"name": "Vimeo", "value": f"[Ver]({vimeo_url})", "inline": True},
            ],
            "footer": {"text": "Studio BC Pipeline"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        resp = httpx.post(self._url, json={"username": "Studio BC", "embeds": [embed]})
        if resp.status_code == 429:
            import time
            time.sleep(float(resp.json().get("retry_after", 1.0)))
            httpx.post(self._url, json={"username": "Studio BC", "embeds": [embed]}).raise_for_status()
        else:
            resp.raise_for_status()
