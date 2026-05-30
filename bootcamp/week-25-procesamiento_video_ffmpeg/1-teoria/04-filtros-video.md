# Filtros de Video

## Objetivos

- Aplicar filtros de escala, recorte y framerate
- Agregar texto y logos sobre video
- Encadenar múltiples filtros
- Entender el filter_complex para operaciones avanzadas

---

## 1. Filtro scale

```python
import ffmpeg

inp = ffmpeg.input("video.mp4")

# Escalar a 1280×720
scaled = inp.video.filter("scale", 1280, 720)

# Preservar aspect ratio (ancho fijo, alto calculado)
scaled_w = inp.video.filter("scale", 1280, -2)  # -2: par más cercano

# Reducir a 50%
half = inp.video.filter("scale", "iw/2", "ih/2")

# Escalar si es mayor que 1920×1080, no tocar si es menor
capped = inp.video.filter("scale", "min(1920,iw)", -2)
```

---

## 2. Filtro fps (cambiar framerate)

```python
import ffmpeg

inp = ffmpeg.input("video_60fps.mp4")

# Reducir a 25 fps (para difusión PAL)
v25 = inp.video.filter("fps", fps=25)

# Reducir a 24 fps (cine)
v24 = inp.video.filter("fps", fps=24)

ffmpeg.output(v24, inp.audio, "output_24fps.mp4").run(overwrite_output=True)
```

---

## 3. Filtro crop

```python
import ffmpeg

inp = ffmpeg.input("video.mp4")

# crop(width, height, x, y)
# Recortar un cuadrado central de 1080×1080 de un video 1920×1080
cropped = inp.video.filter("crop", 1080, 1080, "(iw-1080)/2", 0)

# Usar variables de ffmpeg: iw=input width, ih=input height
# Centrado
center_crop = inp.video.filter(
    "crop",
    "min(iw,ih)",   # lado del cuadrado
    "min(iw,ih)",
    "(iw-min(iw,ih))/2",
    "(ih-min(iw,ih))/2",
)
```

---

## 4. Filtro drawtext (watermark de texto)

```python
import ffmpeg

inp = ffmpeg.input("video.mp4")

# Texto en esquina inferior derecha
v = inp.video.filter(
    "drawtext",
    text="© Studio BC 2024",
    fontsize=28,
    fontcolor="white@0.7",      # blanco con 70% opacidad
    x="w-text_w-20",            # 20px desde el borde derecho
    y="h-text_h-20",            # 20px desde el borde inferior
    shadowx=2,
    shadowy=2,
    shadowcolor="black@0.5",
)

# Timecode dinámico (frame counter)
v_tc = inp.video.filter(
    "drawtext",
    text="%{pts\\:hms}",        # timestamp del frame
    fontsize=24,
    fontcolor="white",
    x=10, y=10,
    box=1,
    boxcolor="black@0.6",
    boxborderw=5,
)
```

---

## 5. Overlay de logo

```python
import ffmpeg

base = ffmpeg.input("video.mp4")
logo = ffmpeg.input("logo.png")

# Posicionar logo en esquina inferior derecha (con margen 20px)
overlay = ffmpeg.filter(
    [base.video, logo],
    "overlay",
    x="W-w-20",   # W=ancho del base, w=ancho del logo
    y="H-h-20",   # H=alto del base, h=alto del logo
)

out = ffmpeg.output(overlay, base.audio, "output.mp4", vcodec="libx264", crf=20)
out.run(overwrite_output=True, quiet=True)
```

---

## 6. Encadenar múltiples filtros

```python
import ffmpeg
from pathlib import Path

def process_for_web(src: Path, dest: Path, watermark_text: str = "© Studio BC") -> None:
    inp = ffmpeg.input(str(src))

    # Cadena de filtros: escalar → cambiar fps → watermark
    v = (
        inp.video
        .filter("scale", 1280, -2)      # 720p
        .filter("fps", fps=25)          # 25 fps
        .filter(
            "drawtext",
            text=watermark_text,
            fontsize=24,
            fontcolor="white@0.6",
            x="w-text_w-15",
            y="h-text_h-15",
        )
    )

    (
        ffmpeg.output(v, inp.audio, str(dest), vcodec="libx264", crf=23, preset="fast",
                      acodec="aac", audio_bitrate="128k", movflags="+faststart")
        .run(overwrite_output=True, quiet=True)
    )
```

---

## ✅ Resumen

| Filtro | Uso | Ejemplo |
|--------|-----|---------|
| `scale` | Redimensionar | `filter("scale", 1280, -2)` |
| `fps` | Cambiar framerate | `filter("fps", fps=25)` |
| `crop` | Recortar región | `filter("crop", w, h, x, y)` |
| `drawtext` | Texto superpuesto | `filter("drawtext", text="...", x=, y=)` |
| `overlay` | Logo superpuesto | `ffmpeg.filter([base, logo], "overlay", x=, y=)` |
