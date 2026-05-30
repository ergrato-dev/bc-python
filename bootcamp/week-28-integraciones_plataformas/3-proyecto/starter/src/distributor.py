from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("studio.distributor")


@dataclass
class DistributionResult:
    project: str
    youtube_url: str = ""
    vimeo_url: str = ""
    slack_ts: str = ""
    notion_page_id: str = ""
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return not self.errors

    @property
    def partial_success(self) -> bool:
        return bool(self.youtube_url or self.vimeo_url) and bool(self.errors)


class Distributor:
    def __init__(
        self,
        youtube_publisher=None,   # type: ignore[assignment]
        vimeo_publisher=None,     # type: ignore[assignment]
        slack_notifier=None,      # type: ignore[assignment]
        discord_notifier=None,    # type: ignore[assignment]
        notion_updater=None,      # type: ignore[assignment]
    ) -> None:
        self._yt = youtube_publisher
        self._vimeo = vimeo_publisher
        self._slack = slack_notifier
        self._discord = discord_notifier
        self._notion = notion_updater

    def distribute(
        self,
        video_path: Path,
        title: str,
        project: str,
        client: str,
        description: str = "",
        thumbnail_path: Path | None = None,
    ) -> DistributionResult:
        result = DistributionResult(project=project)

        # 1. YouTube
        if self._yt:
            try:
                video_id = self._yt.upload_video(video_path, title, description)
                if thumbnail_path and thumbnail_path.exists():
                    self._yt.set_thumbnail(video_id, thumbnail_path)
                result.youtube_url = f"https://youtu.be/{video_id}"
                logger.info("[%s] YouTube OK — %s", project, result.youtube_url)
            except Exception as e:
                result.errors["youtube"] = str(e)
                logger.error("[%s] YouTube FALLO: %s", project, e)

        # 2. Vimeo
        if self._vimeo:
            try:
                video_id = self._vimeo.publish(video_path, title, description)
                result.vimeo_url = f"https://vimeo.com/{video_id}"
                logger.info("[%s] Vimeo OK — %s", project, result.vimeo_url)
            except Exception as e:
                result.errors["vimeo"] = str(e)
                logger.error("[%s] Vimeo FALLO: %s", project, e)

        # 3. Notion (crear/actualizar registro)
        if self._notion:
            try:
                page_id = self._notion.create_record(project, client)
                self._notion.update_status(
                    page_id, "Entregado",
                    youtube_url=result.youtube_url,
                    vimeo_url=result.vimeo_url,
                )
                result.notion_page_id = page_id
                logger.info("[%s] Notion OK — %s", project, page_id)
            except Exception as e:
                result.errors["notion"] = str(e)
                logger.error("[%s] Notion FALLO: %s", project, e)

        # 4. Slack
        if self._slack and (result.youtube_url or result.vimeo_url):
            try:
                ts = self._slack.notify_delivery(
                    project, client,
                    youtube_url=result.youtube_url or "N/A",
                    vimeo_url=result.vimeo_url or "N/A",
                )
                result.slack_ts = ts
                logger.info("[%s] Slack OK — ts=%s", project, ts)
            except Exception as e:
                result.errors["slack"] = str(e)
                logger.error("[%s] Slack FALLO: %s", project, e)

        # 5. Discord
        if self._discord and (result.youtube_url or result.vimeo_url):
            try:
                self._discord.notify_delivery(
                    project, client,
                    youtube_url=result.youtube_url or "N/A",
                    vimeo_url=result.vimeo_url or "N/A",
                )
                logger.info("[%s] Discord OK", project)
            except Exception as e:
                result.errors["discord"] = str(e)
                logger.error("[%s] Discord FALLO: %s", project, e)

        return result
