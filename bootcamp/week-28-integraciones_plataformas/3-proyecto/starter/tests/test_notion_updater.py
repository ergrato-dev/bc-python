"""Tests de NotionUpdater con httpx mocks."""
from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest

from src.notion_updater import NotionUpdater


@pytest.fixture
def notion() -> NotionUpdater:
    return NotionUpdater(token="secret_test", database_id="db-id-123")


def test_create_record_calls_post(notion: NotionUpdater) -> None:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"id": "page-id-abc"}

    with patch("httpx.post", return_value=mock_resp) as mock_post:
        page_id = notion.create_record("canal9/spot", "Canal 9")

    assert page_id == "page-id-abc"
    mock_post.assert_called_once()
    body = mock_post.call_args.kwargs["json"]
    assert body["parent"]["database_id"] == "db-id-123"
    assert body["properties"]["Proyecto"]["title"][0]["text"]["content"] == "canal9/spot"


def test_update_status_patches_page(notion: NotionUpdater) -> None:
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"id": "page-id-abc"}

    with patch("httpx.patch", return_value=mock_resp) as mock_patch:
        notion.update_status(
            "page-id-abc",
            "Entregado",
            youtube_url="https://youtu.be/abc",
            vimeo_url="https://vimeo.com/123",
        )

    mock_patch.assert_called_once()
    props = mock_patch.call_args.kwargs["json"]["properties"]
    assert props["Estado"]["select"]["name"] == "Entregado"
    assert props["YouTube URL"]["url"] == "https://youtu.be/abc"


def test_update_status_omits_empty_urls(notion: NotionUpdater) -> None:
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {}

    with patch("httpx.patch", return_value=mock_resp) as mock_patch:
        notion.update_status("page-id", "En proceso")

    props = mock_patch.call_args.kwargs["json"]["properties"]
    assert "YouTube URL" not in props
    assert "Vimeo URL" not in props
