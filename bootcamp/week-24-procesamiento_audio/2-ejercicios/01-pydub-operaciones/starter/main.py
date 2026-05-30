"""
Ejercicio 01 — pydub: Operaciones básicas de audio

Contexto: Studio BC recibe audios crudos y necesita:
- Extraer el primer y último minuto de una entrevista
- Agregar intro y outro musicales con fade
- Exportar el resultado final a MP3 192k

Instrucciones:
1. Completá `extract_segment()` — extrae un segmento entre start_ms y end_ms
2. Completá `add_intro_outro()` — concatena intro + contenido + outro con fades
3. Completá `mix_with_background()` — mezcla voz con música de fondo más baja
4. Completá `export_mp3()` — exporta a MP3 con bitrate dado

Nota: los audios se generan sintéticamente (tonos puros) para no requerir archivos reales.
"""

from pathlib import Path
from pydub import AudioSegment


def extract_segment(audio: AudioSegment, start_ms: int, end_ms: int) -> AudioSegment:
    """Extrae el segmento entre start_ms y end_ms."""
    # TODO: usar slicing de pydub: audio[start_ms:end_ms]
    raise NotImplementedError


def add_intro_outro(
    content: AudioSegment,
    intro: AudioSegment,
    outro: AudioSegment,
    fade_ms: int = 1000,
) -> AudioSegment:
    """
    Concatena: intro (con fade out) + content + outro (con fade in).
    Retorna el audio completo.
    """
    # TODO:
    # 1. intro_faded = intro.fade_out(fade_ms)
    # 2. outro_faded = outro.fade_in(fade_ms)
    # 3. retornar intro_faded + content + outro_faded
    raise NotImplementedError


def mix_with_background(
    voice: AudioSegment,
    music: AudioSegment,
    music_volume_db: float = -18.0,
) -> AudioSegment:
    """
    Mezcla voice con music a music_volume_db dB por debajo de su nivel actual.
    La música se repite si es más corta que la voz.
    """
    # TODO:
    # 1. music_low = music + music_volume_db (ajustar ganancia)
    # 2. voice.overlay(music_low, loop=True)
    raise NotImplementedError


def export_mp3(audio: AudioSegment, output: Path, bitrate: str = "192k") -> Path:
    """Exporta audio a MP3 con el bitrate dado."""
    # TODO: audio.export(str(output), format="mp3", bitrate=bitrate)
    raise NotImplementedError


# ── Helpers de muestra ────────────────────────────────────────────────────────
def make_tone(freq_hz: int = 440, duration_ms: int = 3000, volume_db: float = -20.0) -> AudioSegment:
    """Genera un tono puro (sine wave) para pruebas."""
    import math, array as arr
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    samples = arr.array("h", [
        int(32767 * (10 ** (volume_db / 20)) * math.sin(2 * math.pi * freq_hz * i / sample_rate))
        for i in range(n_samples)
    ])
    return AudioSegment(
        data=samples.tobytes(),
        sample_width=2,
        frame_rate=sample_rate,
        channels=1,
    )


if __name__ == "__main__":
    import tempfile

    voz = make_tone(220, 5000, -15.0)    # 5 segundos, voz baja
    intro = make_tone(440, 2000, -20.0)  # 2 segundos, intro
    outro = make_tone(330, 2000, -20.0)  # 2 segundos, outro
    musica = make_tone(880, 3000, -10.0) # 3 segundos, música

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)

        seg = extract_segment(voz, 1000, 4000)
        print(f"Segmento extraído: {len(seg)} ms (esperado ~3000)")

        completo = add_intro_outro(voz, intro, outro)
        print(f"Con intro/outro: {len(completo)} ms (esperado ~9000)")

        mezclado = mix_with_background(voz, musica)
        print(f"Con fondo musical: {len(mezclado)} ms")

        mp3_path = export_mp3(mezclado, out / "final.mp3")
        print(f"MP3 exportado: {mp3_path.stat().st_size} bytes")
        print("✓ Ejercicio completado")
