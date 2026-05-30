from __future__ import annotations

import datetime
import httpx


class NotionUpdater:
    BASE = "https://api.notion.com/v1"
    VERSION = "2022-06-28"

    def __init__(self, token: str, database_id: str) -> None:
        self._db = database_id
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": self.VERSION,
            "Content-Type": "application/json",
        }

    def _post(self, path: str, body: dict[str, object]) -> dict[str, object]:
        resp = httpx.post(f"{self.BASE}{path}", headers=self._headers, json=body)
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def _patch(self, path: str, body: dict[str, object]) -> dict[str, object]:
        resp = httpx.patch(f"{self.BASE}{path}", headers=self._headers, json=body)
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def create_record(self, project: str, client: str) -> str:
        result = self._post("/pages", {
            "parent": {"database_id": self._db},
            "properties": {
                "Proyecto": {"title": [{"text": {"content": project}}]},
                "Cliente": {"rich_text": [{"text": {"content": client}}]},
                "Estado": {"select": {"name": "En proceso"}},
                "Fecha": {"date": {"start": datetime.date.today().isoformat()}},
            },
        })
        return str(result["id"])

    def update_status(
        self,
        page_id: str,
        status: str,
        youtube_url: str = "",
        vimeo_url: str = "",
    ) -> None:
        props: dict[str, object] = {"Estado": {"select": {"name": status}}}
        if youtube_url:
            props["YouTube URL"] = {"url": youtube_url}
        if vimeo_url:
            props["Vimeo URL"] = {"url": vimeo_url}
        self._patch(f"/pages/{page_id}", {"properties": props})

    def append_note(self, page_id: str, note: str, urls: list[str]) -> None:
        children: list[dict[str, object]] = [
            {"object": "block", "type": "heading_2",
             "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Entrega"}}]}},
            {"object": "block", "type": "paragraph",
             "paragraph": {"rich_text": [{"type": "text", "text": {"content": note}}]}},
        ]
        for url in urls:
            children.append({"object": "block", "type": "bookmark", "bookmark": {"url": url}})
        self._patch(f"/blocks/{page_id}/children", {"children": children})
