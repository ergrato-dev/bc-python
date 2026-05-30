"""
Ejercicio 04 — Transcripción y Generación de Subtítulos

Contexto: Studio BC necesita generar subtítulos SRT y VTT automáticamente
para todos los audios de entrevistas.

Instrucciones:
1. Completá `seconds_to_srt_time()` — convierte segundos a "HH:MM:SS,mmm"
2. Completá `seconds_to_vtt_time()` — convierte segundos a "HH:MM:SS.mmm"
3. Completá `generate_srt()` — genera archivo .srt desde lista de segmentos
4. Completá `generate_vtt()` — genera archivo .vtt desde lista de segmentos
5. (Opcional) Completá `transcribe_with_whisper()` si tenés whisper instalado

Los segmentos tienen formato: [{"start": float, "end": float, "text": str}]

Instalar Whisper: pip install openai-whisper (modelo ~150MB se descarga automáticamente)
"""

from pathlib import Path


def seconds_to_srt_time(seconds: float) -> str:
    """Convierte segundos a formato SRT: HH:MM:SS,mmm"""
    # TODO:
    # total_ms = int(seconds * 1000)
    # ms = total_ms % 1000
    # s = (total_ms // 1000) % 60
    # m = (total_ms // 60000) % 60
    # h = total_ms // 3600000
    # return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    raise NotImplementedError


def seconds_to_vtt_time(seconds: float) -> str:
    """Convierte segundos a formato VTT: HH:MM:SS.mmm (punto, no coma)"""
    # TODO: reutilizar seconds_to_srt_time y reemplazar la coma
    raise NotImplementedError


def generate_srt(segments: list[dict[str, object]], output: Path) -> Path:
    """
    Genera un archivo .srt desde la lista de segmentos.
    Cada segmento tiene: {"start": float, "end": float, "text": str}
    """
    # TODO:
    # Para cada segmento (i empezando en 1):
    #   línea número, timestamps (start --> end), texto, línea en blanco
    # output.write_text(content, encoding="utf-8")
    raise NotImplementedError


def generate_vtt(segments: list[dict[str, object]], output: Path) -> Path:
    """Genera un archivo .vtt desde la lista de segmentos."""
    # TODO: igual que SRT pero empezar con "WEBVTT\n\n" y usar punto en timestamps
    raise NotImplementedError


def transcribe_with_whisper(audio_path: Path, model_name: str = "base") -> list[dict[str, object]]:
    """
    (Opcional) Transcribe audio con Whisper y retorna la lista de segmentos.
    Si Whisper no está disponible, retorna segmentos de muestra.
    """
    try:
        import whisper
        model = whisper.load_model(model_name)
        result = model.transcribe(str(audio_path), language="es", fp16=False)
        return result["segments"]  # type: ignore[index]
    except ImportError:
        # Whisper no instalado — retornar segmentos de muestra para probar las funciones
        return [
            {"start": 1.28, "end": 4.72, "text": "Bienvenidos a Studio BC."},
            {"start": 5.10, "end": 8.34, "text": "Hoy presentamos nuestro nuevo spot para Canal 9."},
            {"start": 9.00, "end": 13.50, "text": "Este proyecto fue desarrollado en tiempo récord."},
        ]


if __name__ == "__main__":
    import tempfile

    segments = transcribe_with_whisper(Path("dummy.wav"))  # usa muestra si no hay whisper

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)

        srt = generate_srt(segments, out / "subtitulos.srt")
        vtt = generate_vtt(segments, out / "subtitulos.vtt")

        print("=== SRT ===")
        print(srt.read_text())

        print("=== VTT ===")
        print(vtt.read_text())

        # Validaciones
        srt_content = srt.read_text()
        assert "00:00:01,280 --> 00:00:04,720" in srt_content
        assert "Bienvenidos a Studio BC." in srt_content

        vtt_content = vtt.read_text()
        assert vtt_content.startswith("WEBVTT")
        assert "00:00:01.280 --> 00:00:04.720" in vtt_content

        print("✓ SRT y VTT generados correctamente")
