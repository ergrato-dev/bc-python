# Glosario — Semana 24: Procesamiento de Audio

## Conceptos de audio

**dBFS (Decibels Full Scale)**
Unidad de amplitud en audio digital. 0 dBFS es el nivel máximo sin clipping. Valores más negativos son más silenciosos. -14 dBFS es el estándar de loudness para plataformas de streaming (Spotify, YouTube, Apple Music).

**Sample rate (frecuencia de muestreo)**
Cantidad de muestras por segundo. CD audio = 44.100 Hz. Whisper trabaja nativamente a 16.000 Hz. Valores más altos = mayor fidelidad, mayor tamaño de archivo.

**Bit depth (profundidad de bits)**
Bits por muestra. 16-bit = 65.536 niveles de amplitud. 24-bit = 16.7 millones. Más bits = mayor rango dinámico. WAV 16-bit es suficiente para distribución; 24-bit para masterización.

**Mono / Stereo**
Mono: 1 canal. Stereo: 2 canales (izquierda + derecha). Whisper prefiere mono para transcripción — reduce datos redundantes a la mitad.

**Clipping**
Distorsión por saturación cuando la amplitud supera 0 dBFS. Los picos se recortan (`clip`). Irreversible en digital.

**Headroom**
Margen entre el nivel de señal más alto y 0 dBFS. Deja espacio para picos transitorios sin clipping.

---

## pydub

**AudioSegment**
Clase principal de pydub. Representa un fragmento de audio como bytes de muestras. Inmutable — cada operación retorna un nuevo `AudioSegment`.

**`audio.dBFS`**
Loudness media del audio en dBFS. Puede ser `-inf` para silencio absoluto.

**`audio.apply_gain(db)`**
Ajusta la ganancia por `db` decibeles. Positivo = más alto, negativo = más bajo.

**`split_on_silence()`**
Divide el audio en chunks en los puntos donde hay silencio continuo. Los parámetros `min_silence_len` y `silence_thresh` controlan qué se considera silencio.

**Overlay**
Mezcla de dos audios superpuestos en el tiempo. `base.overlay(other, position=ms)` superpone `other` sobre `base` a partir del `position` indicado.

---

## Whisper

**ASR (Automatic Speech Recognition)**
Tecnología para convertir voz en texto. Whisper es un modelo ASR de OpenAI basado en transformers.

**Modelo Whisper**
Pesos del modelo pre-entrenado. Se descarga automáticamente la primera vez. `tiny` (39M params) a `large` (1.55B params). Mayor modelo = mayor accuracy y mayor tiempo de inferencia.

**`result["segments"]`**
Lista de dicts con timestamps por fragmento de habla: `{"start": float, "end": float, "text": str}`. La base para generar subtítulos.

**`language="es"`**
Forzar el idioma de la transcripción. Más rápido y preciso que la autodetección cuando se conoce el idioma de antemano.

**`fp16=False`**
Usar precisión float32 en lugar de float16. Necesario en CPU — las CPUs no soportan fp16 nativo.

---

## Subtítulos

**SRT (SubRip Text)**
Formato de subtítulos más universal. Bloques numerados con timestamps `HH:MM:SS,mmm --> HH:MM:SS,mmm` y texto. Separados por líneas en blanco.

**WebVTT (Web Video Text Tracks)**
Estándar HTML5 para subtítulos. Similar a SRT: encabezado `WEBVTT`, timestamps con punto (`.`) en lugar de coma, compatible con `<video>` y YouTube.

**Timestamp**
Marca temporal que indica cuándo empieza y termina un subtítulo. Debe coincidir con los segmentos de la transcripción para que los subtítulos estén sincronizados.

**`textwrap.wrap()`**
Divide texto largo en líneas de ancho máximo. Los reproductores recomiendan ≤ 42 caracteres por línea y ≤ 2 líneas por bloque para legibilidad.

---

## Metadatos

**ID3**
Estándar de metadatos para archivos MP3. Contiene campos como TIT2 (título), TPE1 (artista), TALB (álbum), TBPM (BPM), TDRC (año).

**mutagen**
Librería Python para leer y escribir metadatos de audio: ID3 (MP3), Vorbis Comments (FLAC/OGG), MP4 tags (AAC/M4A).

**BPM (Beats Per Minute)**
Tempo de una pieza musical. Detectable con `librosa.beat.beat_track()`. Importante para música de fondo en spots publicitarios.
