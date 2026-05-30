"""
Ejercicio 03 — Metadatos ID3 con mutagen

Contexto: Studio BC distribuye piezas de audio y necesita etiquetarlas
correctamente: título, artista, álbum, año, género y BPM.

Instrucciones:
1. Completá `read_mp3_info()` — retorna dict con propiedades técnicas
2. Completá `write_id3_tags()` — escribe tags ID3 en un MP3
3. Completá `read_id3_tags()` — lee los tags ID3 de un MP3
4. Completá `batch_tag()` — aplica tags a múltiples archivos con datos de un dict

Instalar: pip install mutagen
"""

from pathlib import Path


def read_mp3_info(path: Path) -> dict[str, object]:
    """
    Retorna dict con: duration_s, bitrate, channels, sample_rate.
    """
    from mutagen.mp3 import MP3
    # TODO: audio = MP3(str(path)); retornar audio.info.length, bitrate, channels, sample_rate
    raise NotImplementedError


def write_id3_tags(
    path: Path,
    title: str = "",
    artist: str = "",
    album: str = "",
    year: str = "",
    genre: str = "",
    bpm: str = "",
) -> None:
    """Escribe tags ID3 en el archivo MP3."""
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, TBPM
    # TODO:
    # tags = ID3()
    # if title: tags["TIT2"] = TIT2(encoding=3, text=title)
    # ... igual para TPE1 (artist), TALB (album), TDRC (year), TCON (genre), TBPM (bpm)
    # tags.save(str(path))
    raise NotImplementedError


def read_id3_tags(path: Path) -> dict[str, str]:
    """Lee y retorna los tags ID3 disponibles como dict de strings."""
    from mutagen.id3 import ID3
    # TODO: ID3(str(path)), extraer TIT2, TPE1, TALB, TDRC, TCON, TBPM
    # Usar str(tags.get("TIT2", "")) para evitar errores si no existe
    raise NotImplementedError


def batch_tag(files: list[Path], metadata: dict[str, dict[str, str]]) -> int:
    """
    Aplica tags a cada archivo.
    metadata es {filename: {title:, artist:, ...}}
    Retorna la cantidad de archivos etiquetados.
    """
    # TODO: iterar files, buscar path.name en metadata, llamar write_id3_tags
    raise NotImplementedError


# ── Muestra (genera un MP3 mínimo para tests) ─────────────────────────────────
def create_minimal_mp3(path: Path) -> None:
    from pydub import AudioSegment
    import math, array as arr
    sample_rate = 44100
    n = sample_rate  # 1 segundo
    samples = arr.array("h", [
        int(3276 * math.sin(2 * math.pi * 440 * i / sample_rate))
        for i in range(n)
    ])
    seg = AudioSegment(data=samples.tobytes(), sample_width=2, frame_rate=sample_rate, channels=1)
    seg.export(str(path), format="mp3", bitrate="128k")


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        mp3 = Path(tmp) / "track.mp3"
        create_minimal_mp3(mp3)

        info = read_mp3_info(mp3)
        print(f"Info técnica: {info}")

        write_id3_tags(
            mp3,
            title="Spot Verano Canal 9",
            artist="Studio BC",
            album="Producción 2024",
            year="2024",
            genre="Jingle",
            bpm="120",
        )
        print("Tags escritos.")

        tags = read_id3_tags(mp3)
        print(f"Tags leídos: {tags}")
        assert tags.get("title") == "Spot Verano Canal 9"
        assert tags.get("bpm") == "120"
        print("✓ Metadatos ID3 OK")
