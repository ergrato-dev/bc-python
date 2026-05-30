"""
DistributeStage — notifica al equipo vía Slack webhook.

Requiere:
    pip install httpx
    SLACK_WEBHOOK_URL en entorno o .env
"""
from __future__ import annotations

from .base import Stage, StageResult


class DistributeStage:
    name = "distribute"

    def __init__(self, slack_webhook_url: str = "", dry_run: bool = True) -> None:
        self._webhook = slack_webhook_url
        self._dry_run = dry_run

    def process(self, data: dict[str, object]) -> StageResult:
        project = str(data.get("project", "unknown"))
        stem = str(data.get("stem", "archivo"))
        web_url = str(data.get("s3_web_url", ""))
        thumb_url = str(data.get("s3_thumb_url", ""))

        try:
            self._notify_slack(project, stem, web_url, thumb_url)
        except Exception as e:
            return StageResult(success=False, data=data, error=f"Distribute error: {e}")

        return StageResult(success=True, data={**data, "distributed": True})

    def _notify_slack(
        self,
        project: str,
        stem: str,
        web_url: str,
        thumb_url: str,
    ) -> None:
        """
        Envía un mensaje Block Kit a Slack con el resultado del pipeline.

        TODO si dry_run=True: imprimir "[DRY-RUN] Slack: proyecto={project} stem={stem} url={web_url}"
        TODO si dry_run=False:
            import httpx
            blocks = [
                {"type": "header", "text": {"type": "plain_text", "text": f"Pipeline OK: {project}"}},
                {"type": "section", "fields": [
                    {"type": "mrkdwn", "text": f"*Archivo:*\n{stem}"},
                    {"type": "mrkdwn", "text": f"*Web URL:*\n<{web_url}|Ver>"},
                ]},
            ]
            httpx.post(
                self._webhook,
                json={"text": f"Pipeline OK: {project}/{stem}", "blocks": blocks},
                timeout=5.0,
            ).raise_for_status()

        Referencia: semana 28 — DistributeStage / notifier.py
                    semana 29 — AlertManager._send_slack()
        """
        raise NotImplementedError
