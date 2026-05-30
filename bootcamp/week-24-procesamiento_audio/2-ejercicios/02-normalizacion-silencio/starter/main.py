"""
Ejercicio 02 — Normalización y Detección de Silencio

Contexto: El estudio recibe grabaciones de entrevistas con volumen
inconsistente y pausas largas. Necesitamos normalizar y extraer
solo los segmentos con habla.

Instrucciones:
1. Completá `normalize_to_target()` — normaliza a un target dBFS
2. Completá `detect_speech_segments()` — retorna lista de (inicio_s, fin_s)
3. Completá `remove_silence()` — concatena solo los segmentos de habla
4. Completá `loudness_report()` — retorna stats básicos del audio
"""

from pydub import AudioSegment
from pydub.silence import detect_silence


def normalize_to_target(audio: AudioSegment, target_dbfs: float = -14.0) -> AudioSegment:
    """Normaliza audio al target dBFS dado."""
    # TODO: delta = target_dbfs - audio.dBFS; return audio.apply_gain(delta)
    raise NotImplementedError


def detect_speech_segments(
    audio: AudioSegment,
    min_silence_ms: int = 700,
    silence_thresh_db: float = -40.0,
) -> list[tuple[float, float]]:
    """
    Retorna lista de (inicio_s, fin_s) de los segmentos con habla.
    Usa detect_silence para encontrar los silencios y calcula los inversos.
    """
    # TODO:
    # 1. detect_silence(audio, min_silence_len, silence_thresh) → [(s, e), ...]
    # 2. Los segmentos de habla son los "huecos" entre silencios
    # 3. Incluir el inicio y el fin del audio si no son silencio
    # Retornar lista de (inicio_ms/1000, fin_ms/1000)
    raise NotImplementedError


def remove_silence(
    audio: AudioSegment,
    min_silence_ms: int = 700,
    silence_thresh_db: float = -40.0,
    padding_ms: int = 200,
) -> AudioSegment:
    """
    Concatena solo los segmentos con habla, con padding_ms de contexto en cada extremo.
    Usa split_on_silence.
    """
    # TODO: from pydub.silence import split_on_silence
    # chunks = split_on_silence(audio, min_silence_len, silence_thresh, keep_silence=padding_ms)
    # return sum(chunks, AudioSegment.empty())
    raise NotImplementedError


def loudness_report(audio: AudioSegment, chunk_ms: int = 1000) -> dict[str, float]:
    """
    Retorna dict con: mean_dbfs, min_dbfs, max_dbfs, duration_s.
    Omite chunks de -inf dBFS (silencio puro).
    """
    # TODO: calcular dBFS de cada chunk de chunk_ms ms
    # filtrar -inf, calcular media/min/max
    raise NotImplementedError


# ── Muestra ───────────────────────────────────────────────────────────────────
def make_speech_with_silence() -> AudioSegment:
    """Genera audio simulando habla con pausas largas."""
    import math, array as arr
    sample_rate = 44100

    def tone(freq: int, ms: int, vol: float) -> AudioSegment:
        n = int(sample_rate * ms / 1000)
        s = arr.array("h", [
            int(32767 * vol * math.sin(2 * math.pi * freq * i / sample_rate))
            for i in range(n)
        ])
        return AudioSegment(data=s.tobytes(), sample_width=2, frame_rate=sample_rate, channels=1)

    silence = AudioSegment.silent(duration=1500)  # 1.5s de silencio
    habla1 = tone(350, 2000, 0.15)  # 2s de "habla"
    habla2 = tone(380, 1500, 0.12)  # 1.5s de "habla"
    habla3 = tone(320, 2500, 0.18)  # 2.5s de "habla"

    return silence + habla1 + silence + habla2 + silence + habla3 + silence


if __name__ == "__main__":
    audio = make_speech_with_silence()
    print(f"Audio original: {len(audio)/1000:.1f}s, {audio.dBFS:.1f} dBFS")

    normalizado = normalize_to_target(audio, -14.0)
    print(f"Normalizado: {normalizado.dBFS:.1f} dBFS (objetivo: -14.0)")

    segments = detect_speech_segments(audio)
    print(f"Segmentos de habla: {segments}")

    limpio = remove_silence(audio)
    print(f"Sin silencios: {len(limpio)/1000:.1f}s (reducción: {(1 - len(limpio)/len(audio))*100:.0f}%)")

    report = loudness_report(audio)
    print(f"Reporte: {report}")
