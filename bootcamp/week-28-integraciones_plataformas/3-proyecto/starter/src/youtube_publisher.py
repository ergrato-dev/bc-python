from __future__ import annotations

import json
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]


def _get_credentials(secrets_path: Path, token_path: Path) -> Credentials:
    creds: Credentials | None = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_info(
            json.loads(token_path.read_text()), SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return creds


class YouTubePublisher:
    def __init__(self, secrets_path: Path, token_path: Path) -> None:
        creds = _get_credentials(secrets_path, token_path)
        self._service = build("youtube", "v3", credentials=creds)

    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str = "",
        tags: list[str] | None = None,
        privacy_status: str = "unlisted",
        category_id: str = "22",
    ) -> str:
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            },
        }
        media = MediaFileUpload(
            str(video_path), mimetype="video/mp4",
            resumable=True, chunksize=10 * 1024 * 1024,
        )
        request = self._service.videos().insert(
            part="snippet,status", body=body, media_body=media
        )
        response = None
        while response is None:
            _, response = request.next_chunk()
        return str(response["id"])

    def set_thumbnail(self, video_id: str, thumb_path: Path) -> None:
        media = MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
        self._service.thumbnails().set(videoId=video_id, media_body=media).execute()

    def add_to_playlist(self, video_id: str, playlist_title: str) -> str:
        resp = self._service.playlists().list(part="snippet", mine=True, maxResults=50).execute()
        for pl in resp.get("items", []):
            if pl["snippet"]["title"] == playlist_title:
                playlist_id = pl["id"]
                break
        else:
            result = self._service.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {"title": playlist_title},
                    "status": {"privacyStatus": "unlisted"},
                },
            ).execute()
            playlist_id = result["id"]

        self._service.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        ).execute()
        return str(playlist_id)
