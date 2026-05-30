# ffmpeg-python — Fundamentos

## Objetivos

- Entender el modelo de nodos y streams de ffmpeg-python
- Construir pipelines de procesamiento con la API fluent
- Ejecutar comandos con `ffmpeg.run()` y capturar errores
- Entender la diferencia entre usar ffmpeg-python y subprocess directo

---

## 1. Por qué ffmpeg-python

ffmpeg es la herramienta más potente para procesamiento de video, pero su CLI tiene una sintaxis compleja. `ffmpeg-python` expone la misma funcionalidad como un grafo de nodos Python:

```bash
# CLI equivalente:
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac -b:a 128k output.mp4
```

```python
# ffmpeg-python equivalente:
import ffmpeg

stream = ffmpeg.input("input.mp4")
stream = ffmpeg.output(stream, "output.mp4", vcodec="libx264", crf=23, acodec="aac", audio_bitrate="128k")
ffmpeg.run(stream)
```

---

## 2. Modelo de nodos

```python
import ffmpeg

# Input node
inp = ffmpeg.input("video.mp4")

# El input tiene streams de video y audio separables
video = inp.video
audio = inp.audio

# Aplicar filtro al video
scaled = video.filter("scale", 1280, 720)

# Reensamblar video + audio en output
out = ffmpeg.output(scaled, audio, "output.mp4")

# Ver el comando que se generaría sin ejecutar
print(ffmpeg.compile(out))

# Ejecutar
ffmpeg.run(out, overwrite_output=True)
```

---

## 3. Opciones comunes de input

```python
import ffmpeg

# Opciones de decodificación
inp = ffmpeg.input(
    "video.mp4",
    ss="00:01:30",      # seek a 1m30s antes de decodificar (rápido)
    t=30,               # leer solo 30 segundos
)

# Input desde URL
inp_url = ffmpeg.input("https://example.com/stream.m3u8")

# Imagen como video (slideshow)
inp_img = ffmpeg.input("frame_%04d.png", framerate=25)
```

---

## 4. Opciones comunes de output

```python
import ffmpeg

inp = ffmpeg.input("source.mp4")

out = ffmpeg.output(
    inp,
    "dest.mp4",
    # Video
    vcodec="libx264",
    crf=23,
    preset="slow",
    # Audio
    acodec="aac",
    audio_bitrate="128k",
    # Contenedor
    movflags="+faststart",   # optimizar para streaming web
)

ffmpeg.run(out, overwrite_output=True, quiet=True)
```

---

## 5. Capturar errores

```python
import ffmpeg
import subprocess

def run_ffmpeg(stream: ffmpeg.nodes.OutputStream) -> None:
    try:
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
    except ffmpeg.Error as e:
        # e.stderr contiene el log de ffmpeg
        stderr = e.stderr.decode("utf-8") if e.stderr else ""
        raise RuntimeError(f"ffmpeg falló:\n{stderr}") from e
```

---

## 6. Obtener el comando equivalente

Útil para debugging y logging:

```python
import ffmpeg

inp = ffmpeg.input("video.mp4")
out = ffmpeg.output(inp, "output.mp4", vcodec="libx264", crf=23)

# Lista de argumentos que se pasarían a ffmpeg
cmd = ffmpeg.compile(out)
print(" ".join(cmd))
# ffmpeg -i video.mp4 -crf 23 -vcodec libx264 output.mp4
```

---

## ✅ Resumen

| Concepto | API |
|---------|-----|
| Input | `ffmpeg.input(path, **options)` |
| Stream de video | `inp.video` o `inp["v"]` |
| Stream de audio | `inp.audio` o `inp["a"]` |
| Filtro | `.filter("nombre", args...)` |
| Output | `ffmpeg.output(streams..., path, **options)` |
| Ver comando | `ffmpeg.compile(output)` |
| Ejecutar | `ffmpeg.run(output, overwrite_output=True)` |
| Capturar error | `except ffmpeg.Error as e: e.stderr` |
