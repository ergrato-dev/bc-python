"""AssetAnalyzer — orquesta vision, transcripción, tagging y metadata."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .config import AIConfig
from .metadata import MetadataGenerator
from .tagger import AutoTagger
from .transcriber import AssetTranscriber
from .vision import FrameAnalyzer


@dataclass
class AssetAnalysis:
    asset_path: str
    title: str = ""
    snippet: str = ""
    full_description: str = ""
    call_to_action: str = ""
    tags: list[str] = field(default_factory=list)
    category: str = ""
    transcription: str = ""
    language: str = "es"
    segments: list[dict[str, object]] = field(default_factory=list)
    chapters: list[dict[str, object]] = field(default_factory=list)
    visual_analyses: list[dict[str, object]] = field(default_factory=list)
    srt: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "asset_path": self.asset_path,
            "title": self.title,
            "snippet": self.snippet,
            "full_description": self.full_description,
            "call_to_action": self.call_to_action,
            "tags": self.tags,
            "category": self.category,
            "transcription": self.transcription,
            "language": self.language,
            "chapters": self.chapters,
            "visual_analyses": self.visual_analyses,
        }

    def youtube_description(self) -> str:
        gen = MetadataGenerator()
        return gen.format_youtube_description(
            {"full_description": self.full_description, "call_to_action": self.call_to_action},
            self.chapters,
        )


class AssetAnalyzer:
    def __init__(self, config: AIConfig | None = None) -> None:
        self._cfg = config or AIConfig()
        self._vision = FrameAnalyzer(self._cfg)
        self._transcriber = AssetTranscriber(self._cfg)
        self._tagger = AutoTagger(self._cfg)
        self._metadata = MetadataGenerator(self._cfg)

    def analyze(self, asset_path: Path) -> AssetAnalysis:
        result = AssetAnalysis(asset_path=str(asset_path))
        suffix = asset_path.suffix.lower()

        # 1. Análisis visual (solo video e imagen)
        if suffix in {".mp4", ".mov", ".mxf", ".jpg", ".png"}:
            if suffix in {".jpg", ".png"}:
                result.visual_analyses = [self._vision.analyze_frame(asset_path)]
            else:
                result.visual_analyses = self._vision.analyze_video(asset_path)

        # 2. Transcripción (video y audio)
        if suffix in {".mp4", ".mov", ".mxf", ".mp3", ".wav", ".flac"}:
            transcript_data = self._transcriber.transcribe_video(asset_path)
            result.transcription = str(transcript_data.get("text", ""))
            result.language = str(transcript_data.get("language", "es"))
            result.segments = list(transcript_data.get("segments", []))  # type: ignore[arg-type]
            result.srt = AssetTranscriber.to_srt(result.segments)

        # 3. Descripción consolidada para tagging
        visual_desc = " ".join(
            str(a.get("description", "")) for a in result.visual_analyses
        )
        combined = f"{visual_desc} {result.transcription}".strip()

        # 4. Tags + categoría
        result.tags = self._tagger.generate_tags(combined)
        result.category = self._tagger.classify(combined)

        # 5. Título y descripción
        result.title = self._metadata.generate_title(combined, result.tags)
        desc_data = self._metadata.generate_description(combined, result.transcription)
        result.snippet = str(desc_data.get("snippet", ""))
        result.full_description = str(desc_data.get("full_description", ""))
        result.call_to_action = str(desc_data.get("call_to_action", ""))

        # 6. Capítulos
        if result.segments:
            result.chapters = self._metadata.generate_chapters(result.segments)

        return result
