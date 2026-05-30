"""Transcripción de audio con Whisper."""

from pathlib import Path
from typing import Any


def load_model(model_name: str = "base") -> Any:
    """
    Carga el modelo Whisper. Si no está instalado, retorna None.
    Cachear el modelo para no recargarlo en cada llamada.
    """
    try:
        import whisper
        return whisper.load_model(model_name)
    except ImportError:
        return None


def transcribe(audio_path: Path, model: Any = None, language: str = "es") -> list[dict[str, Any]]:
    """
    Transcribe audio_path y retorna lista de segmentos:
    [{"start": float, "end": float, "text": str}, ...]

    Si model es None (Whisper no disponible), retorna segmentos de muestra.
    """
    if model is None:
        # Stub para cuando Whisper no está instalado
        return [
            {"start": 0.0,  "end": 3.5,  "text": "Audio procesado por Studio BC."},
            {"start": 4.0,  "end": 7.2,  "text": "Transcripción no disponible sin Whisper."},
        ]

    # TODO:
    # 1. from src.preprocessor import to_wav_mono_16k
    # 2. tmp = to_wav_mono_16k(audio_path)
    # 3. result = model.transcribe(str(tmp), language=language, fp16=False)
    # 4. tmp.unlink()
    # 5. return result["segments"]
    raise NotImplementedError
