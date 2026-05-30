"""FrameAnalyzer — analiza frames de video con GPT-4o Vision."""
from __future__ import annotations

import base64
import json
import subprocess
import tempfile
from pathlib import Path

from openai import OpenAI

from .config import AIConfig

client = OpenAI()

MOCK_FRAME_ANALYSIS: dict[str, object] = {
    "description": "Estudio de producción audiovisual con equipo de iluminación profesional.",
    "topic": "producción de video",
    "category": "institucional",
    "mood": "profesional",
    "suggested_tags": ["studio", "produccion", "video", "iluminacion", "profesional"],
}


class FrameAnalyzer:
    def __init__(self, config: AIConfig | None = None) -> None:
        self._cfg = config or AIConfig()

    def extract_frames(self, video_path: Path, n: int = 5) -> list[Path]:
        """
        Extrae N frames distribuidos a lo largo del video.
        En dry_run, devuelve lista vacía.

        TODO:
        - Si dry_run: return []
        - Usar ffprobe para obtener la duración del video:
              ffprobe -v quiet -print_format json -show_streams video_path
        - Calcular timestamps de frames distribuidos uniformemente
        - Usar ffmpeg para extraer cada frame:
              ffmpeg -ss {ts} -i video_path -vframes 1 -q:v 2 frame_path.jpg
        - Devolver lista de paths extraídos

        Referencia: teoría 01 — extract_frames()
        """
        if self._cfg.dry_run:
            return []
        raise NotImplementedError

    def analyze_frame(self, image_path: Path) -> dict[str, object]:
        """
        Analiza un frame con GPT-4o Vision.

        TODO:
        - Si dry_run: return MOCK_FRAME_ANALYSIS
        - encode_image(image_path) → base64
        - Prompt que pide JSON con description, topic, category, mood, suggested_tags
        - client.chat.completions.create con model=cfg.vision_model,
          response_format={"type": "json_object"}
        - Parsear y retornar JSON

        Referencia: ejercicio 01 — analyze_frame()
        """
        if self._cfg.dry_run:
            return MOCK_FRAME_ANALYSIS
        raise NotImplementedError

    def analyze_video(self, video_path: Path) -> list[dict[str, object]]:
        """
        Extrae frames y los analiza. Devuelve lista de análisis por frame.
        En dry_run devuelve [MOCK_FRAME_ANALYSIS].
        """
        if self._cfg.dry_run:
            return [MOCK_FRAME_ANALYSIS]
        frames = self.extract_frames(video_path, self._cfg.max_frames)
        return [self.analyze_frame(f) for f in frames]
