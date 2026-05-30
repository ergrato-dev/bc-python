"""AssetTranscriber — transcribe audio/video con Whisper."""
from __future__ import annotations

import subprocess
from pathlib import Path

from openai import OpenAI

from .config import AIConfig

client = OpenAI()

MOCK_TRANSCRIPT: dict[str, object] = {
    "text": "Bienvenidos a Studio BC. Somos un estudio de producción audiovisual con más de 10 años de experiencia.",
    "language": "es",
    "duration": 8.4,
    "segments": [
        {"id": 0, "start": 0.0, "end": 4.2, "text": "Bienvenidos a Studio BC."},
        {"id": 1, "start": 4.2, "end": 8.4, "text": "Somos un estudio con más de 10 años de experiencia."},
    ],
}


class AssetTranscriber:
    def __init__(self, config: AIConfig | None = None) -> None:
        self._cfg = config or AIConfig()

    def extract_audio(self, video_path: Path) -> Path:
        """Extrae el audio de un video en MP3 con ffmpeg."""
        out = video_path.with_suffix(".mp3")
        subprocess.run([
            "ffmpeg", "-i", str(video_path), "-vn",
            "-acodec", "libmp3lame", "-q:a", "4",
            str(out), "-y",
        ], check=True, capture_output=True)
        return out

    def transcribe(self, audio_path: Path) -> dict[str, object]:
        """
        Transcribe el audio con Whisper verbose_json.

        TODO:
        - Si dry_run: return MOCK_TRANSCRIPT
        - client.audio.transcriptions.create con:
              model="whisper-1"
              response_format="verbose_json"
              timestamp_granularities=["segment"]
              language="es" (o sin language para detección automática)
        - Retornar dict con text, language, duration, segments [{id,start,end,text}]

        Referencia: ejercicio 02 — transcribe_with_segments()
        """
        if self._cfg.dry_run:
            return MOCK_TRANSCRIPT
        raise NotImplementedError

    def transcribe_video(self, video_path: Path) -> dict[str, object]:
        """Extrae audio y lo transcribe. En dry_run devuelve mock."""
        if self._cfg.dry_run:
            return MOCK_TRANSCRIPT
        audio_path = self.extract_audio(video_path)
        return self.transcribe(audio_path)

    @staticmethod
    def to_srt(segments: list[dict[str, object]]) -> str:
        """Convierte segmentos a formato SRT."""
        def fmt(s: float) -> str:
            h, m = int(s // 3600), int((s % 3600) // 60)
            sec, ms = int(s % 60), int((s % 1) * 1000)
            return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

        lines: list[str] = []
        for i, seg in enumerate(segments, 1):
            s, e = float(str(seg["start"])), float(str(seg["end"]))
            lines.append(f"{i}\n{fmt(s)} --> {fmt(e)}\n{seg['text']}\n")
        return "\n".join(lines)
