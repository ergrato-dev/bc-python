from __future__ import annotations

from pathlib import Path


class VimeoPublisher:
    def __init__(self, token: str, key: str, secret: str, album_name: str = "Studio BC") -> None:
        import vimeo
        self._client = vimeo.VimeoClient(token=token, key=key, secret=secret)
        self._album_name = album_name

    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str = "",
        privacy: str = "unlisted",
    ) -> str:
        uri: str = self._client.upload(
            str(video_path),
            data={
                "name": title,
                "description": description,
                "privacy": {"view": privacy, "embed": "private", "download": False},
            },
        )
        return uri.split("/")[-1]

    def _get_or_create_album(self) -> str:
        resp = self._client.get("/users/me/albums", params={"per_page": 100})
        for album in resp.json().get("data", []):
            if album["name"] == self._album_name:
                return str(album["uri"].split("/")[-1])
        resp = self._client.post(
            "/users/me/albums",
            data={"name": self._album_name, "privacy": "unlisted"},
        )
        return str(resp.json()["uri"].split("/")[-1])

    def publish(self, video_path: Path, title: str, description: str = "") -> str:
        video_id = self.upload_video(video_path, title, description)
        album_id = self._get_or_create_album()
        self._client.put(f"/users/me/albums/{album_id}/videos/{video_id}")
        return video_id
