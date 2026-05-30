"""Tests de SlackNotifier y DiscordNotifier con mocks."""
from __future__ import annotations

from unittest.mock import MagicMock, patch
import pytest

from src.notifier import SlackNotifier, DiscordNotifier


@pytest.fixture
def slack(monkeypatch: pytest.MonkeyPatch) -> SlackNotifier:
    mock_client = MagicMock()
    mock_client.chat_postMessage.return_value = {"ts": "1234567890.123456"}
    with patch("slack_sdk.WebClient", return_value=mock_client):
        notifier = SlackNotifier("fake-token", "#test")
    notifier._client = mock_client
    return notifier


def test_slack_notify_delivery_returns_ts(slack: SlackNotifier) -> None:
    ts = slack.notify_delivery(
        project="canal9/spot",
        client="Canal 9",
        youtube_url="https://youtu.be/abc",
        vimeo_url="https://vimeo.com/123",
        file_count=3,
    )
    assert ts == "1234567890.123456"
    slack._client.chat_postMessage.assert_called_once()


def test_slack_notify_delivery_sends_blocks(slack: SlackNotifier) -> None:
    slack.notify_delivery("proj", "client", "https://yt.com", "https://vimeo.com")
    call_kwargs = slack._client.chat_postMessage.call_args.kwargs
    assert "blocks" in call_kwargs
    blocks = call_kwargs["blocks"]
    assert any(b.get("type") == "header" for b in blocks)
    assert any(b.get("type") == "actions" for b in blocks)


def test_slack_notify_error_sends_message(slack: SlackNotifier) -> None:
    slack.notify_error("proj", "export", "ConnectionError: timeout")
    slack._client.chat_postMessage.assert_called_once()
    call_kwargs = slack._client.chat_postMessage.call_args.kwargs
    assert "blocks" in call_kwargs


def test_discord_notifier_posts_embed(respx_mock=None) -> None:
    import httpx
    with patch("httpx.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=204)
        mock_post.return_value.raise_for_status = MagicMock()
        notifier = DiscordNotifier("https://discord.com/api/webhooks/test/token")
        notifier.notify_delivery("proj", "Canal 9", "https://yt.com", "https://vimeo.com")

    mock_post.assert_called_once()
    payload = mock_post.call_args.kwargs["json"]
    assert "embeds" in payload
    embed = payload["embeds"][0]
    assert "Canal 9" in str(embed.get("fields", []))
    assert embed["color"] == 0x3FB950
