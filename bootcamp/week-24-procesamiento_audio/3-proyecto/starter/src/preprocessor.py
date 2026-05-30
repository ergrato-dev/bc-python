"""Normalización y pre-procesado de audio para Whisper."""

import tempfile
from pathlib import Path

from pydub import AudioSegment
from pydub.effects import normalize


def normalize_audio(audio: AudioSegment, target_dbfs: float = -14.0) -> AudioSegment:
    """Normaliza audio al target dBFS."""
    # TODO: delta = target_dbfs - audio.dBFS; return audio.apply_gain(delta)
    raise NotImplementedError


def to_wav_mono_16k(src: Path) -> Path:
    """
    Convierte audio a WAV mono 16kHz (formato nativo de Whisper).
    Retorna path a un archivo temporal — el llamador es responsable de eliminarlo.
    """
    # TODO:
    # 1. AudioSegment.from_file(str(src))
    # 2. set_channels(1), set_frame_rate(16000)
    # 3. normalize_audio(audio)
    # 4. Exportar a NamedTemporaryFile(suffix=".wav", delete=False)
    # 5. Retornar Path(tmp.name)
    raise NotImplementedError


def preprocess(src: Path, dest_dir: Path) -> Path:
    """
    Normaliza audio y guarda en dest_dir/normalized/.
    Retorna el path del archivo normalizado.
    """
    out_dir = dest_dir / "normalized"
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / src.name

    audio = AudioSegment.from_file(str(src))
    norm = normalize_audio(audio)
    norm.export(str(dest), format=src.suffix.lstrip("."))
    return dest
