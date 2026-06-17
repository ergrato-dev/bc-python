"""Tests de MetadataCache y AssetStreamer — sin Redis, usando dry_run."""
from __future__ import annotations

from pathlib import Path

import pytest

from src.cache import MetadataCache, MOCK_CACHE
from src.config import AppConfig
from src.streamer import AssetStreamer


@pytest.fixture(autouse=True)
def clear_mock_cache() -> None:
    MOCK_CACHE.clear()
    yield
    MOCK_CACHE.clear()


@pytest.fixture
def dry_cfg() -> AppConfig:
    cfg = AppConfig()
    cfg.dry_run = True
    return cfg


# ── MetadataCache ─────────────────────────────────────────────────────────────

class TestMetadataCache:
    def test_miss_returns_none(self, dry_cfg: AppConfig) -> None:
        cache = MetadataCache(dry_cfg)
        assert cache.get("nonexistent-key") is None

    def test_set_and_get_roundtrip(self, dry_cfg: AppConfig) -> None:
        cache = MetadataCache(dry_cfg)
        data = {"title": "Test Asset", "tags": ["a", "b", "c"]}
        cache.set("key1", data)
        result = cache.get("key1")
        assert result == data

    def test_delete_removes_entry(self, dry_cfg: AppConfig) -> None:
        cache = MetadataCache(dry_cfg)
        cache.set("key2", {"x": 1})
        cache.delete("key2")
        assert cache.get("key2") is None

    def test_delete_nonexistent_does_not_raise(self, dry_cfg: AppConfig) -> None:
        cache = MetadataCache(dry_cfg)
        cache.delete("no-existe")  # no debe lanzar excepción

    def test_overwrite_value(self, dry_cfg: AppConfig) -> None:
        cache = MetadataCache(dry_cfg)
        cache.set("k", {"v": 1})
        cache.set("k", {"v": 2})
        assert cache.get("k") == {"v": 2}

    def test_stats_keys_count(self, dry_cfg: AppConfig) -> None:
        cache = MetadataCache(dry_cfg)
        cache.set("a", {"x": 1})
        cache.set("b", {"x": 2})
        stats = cache.stats()
        assert stats["keys"] == 2

    def test_stats_has_backend_field(self, dry_cfg: AppConfig) -> None:
        cache = MetadataCache(dry_cfg)
        stats = cache.stats()
        assert "backend" in stats


# ── AssetStreamer ─────────────────────────────────────────────────────────────

class TestAssetStreamer:
    def test_checksum_is_deterministic(self, dry_cfg: AppConfig, tmp_path: Path) -> None:
        path = tmp_path / "asset.bin"
        path.write_bytes(b"Studio BC test data" * 1000)
        streamer = AssetStreamer(dry_cfg)
        sha1 = streamer.checksum(path)
        sha2 = streamer.checksum(path)
        assert sha1 == sha2
        assert len(sha1) == 64  # SHA-256 hex

    def test_checksum_differs_for_different_content(self, dry_cfg: AppConfig, tmp_path: Path) -> None:
        path_a = tmp_path / "a.bin"
        path_b = tmp_path / "b.bin"
        path_a.write_bytes(b"contenido A")
        path_b.write_bytes(b"contenido B")
        streamer = AssetStreamer(dry_cfg)
        assert streamer.checksum(path_a) != streamer.checksum(path_b)

    def test_file_stats_has_required_keys(self, dry_cfg: AppConfig, tmp_path: Path) -> None:
        path = tmp_path / "sample.bin"
        path.write_bytes(b"x" * 1024)
        streamer = AssetStreamer(dry_cfg)
        stats = streamer.file_stats(path)
        assert "size_bytes" in stats
        assert "size_mb" in stats
        assert "checksum" in stats
        assert stats["size_bytes"] == 1024

    def test_iter_json_records(self, dry_cfg: AppConfig, tmp_path: Path) -> None:
        import json
        path = tmp_path / "assets.jsonl"
        records = [{"id": i, "title": f"Asset {i}"} for i in range(10)]
        path.write_text("\n".join(json.dumps(r) for r in records) + "\n")
        streamer = AssetStreamer(dry_cfg)
        loaded = list(streamer.iter_json_records(path))
        assert len(loaded) == 10
        assert loaded[0]["id"] == 0
        assert loaded[-1]["id"] == 9
