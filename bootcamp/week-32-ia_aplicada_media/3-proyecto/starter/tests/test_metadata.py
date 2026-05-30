"""
Tests del studio-ai-tagger — sin OPENAI_API_KEY, usando dry_run.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from src.config import AIConfig
from src.tagger import AutoTagger, MOCK_TAGS, MOCK_CATEGORY
from src.metadata import MetadataGenerator, MOCK_TITLE, MOCK_DESC, MOCK_CHAPTERS
from src.transcriber import AssetTranscriber, MOCK_TRANSCRIPT
from src.analyzer import AssetAnalyzer


@pytest.fixture
def dry_config() -> AIConfig:
    cfg = AIConfig()
    cfg.dry_run = True
    return cfg


class TestAutoTagger:
    def test_dry_run_returns_mock_tags(self, dry_config: AIConfig) -> None:
        tags = AutoTagger(dry_config).generate_tags("descripción de prueba")
        assert tags == MOCK_TAGS

    def test_dry_run_returns_mock_category(self, dry_config: AIConfig) -> None:
        category = AutoTagger(dry_config).classify("descripción de prueba")
        assert category == MOCK_CATEGORY


class TestMetadataGenerator:
    def test_dry_run_title_max_70_chars(self, dry_config: AIConfig) -> None:
        title = MetadataGenerator(dry_config).generate_title("desc de prueba")
        assert len(title) <= 70

    def test_dry_run_description_has_snippet(self, dry_config: AIConfig) -> None:
        result = MetadataGenerator(dry_config).generate_description("desc de prueba")
        assert "snippet" in result
        assert len(result["snippet"]) > 0

    def test_dry_run_chapters_have_timestamp(self, dry_config: AIConfig) -> None:
        segments: list[dict[str, object]] = list(MOCK_TRANSCRIPT["segments"])  # type: ignore[arg-type]
        chapters = MetadataGenerator(dry_config).generate_chapters(segments)
        assert all("timestamp" in ch for ch in chapters)


class TestAssetTranscriber:
    def test_dry_run_returns_mock_transcript(self, dry_config: AIConfig) -> None:
        result = AssetTranscriber(dry_config).transcribe(Path("any.mp3"))
        assert result["text"] == MOCK_TRANSCRIPT["text"]

    def test_to_srt_format(self) -> None:
        segments: list[dict[str, object]] = list(MOCK_TRANSCRIPT["segments"])  # type: ignore[arg-type]
        srt = AssetTranscriber.to_srt(segments)
        assert "-->" in srt


class TestAssetAnalyzer:
    def test_dry_run_full_analysis(self, dry_config: AIConfig, tmp_path: Path) -> None:
        fake_path = tmp_path / "mock.mp4"
        fake_path.write_bytes(b"fake")
        result = AssetAnalyzer(dry_config).analyze(fake_path)
        assert result.title == MOCK_TITLE
        assert len(result.tags) > 0
        assert result.category == MOCK_CATEGORY

    def test_to_dict_has_required_keys(self, dry_config: AIConfig, tmp_path: Path) -> None:
        fake_path = tmp_path / "mock.mp4"
        fake_path.write_bytes(b"fake")
        result = AssetAnalyzer(dry_config).analyze(fake_path)
        data = result.to_dict()
        required = {"title", "tags", "category", "transcription", "chapters"}
        assert required.issubset(data.keys())
