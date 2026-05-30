# Rúbrica de Evaluación — Semana 23: Procesamiento de Imágenes

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica los modos de color de Pillow (RGB, RGBA, L, CMYK) y cuándo convertir entre ellos | 8 |
| Describe la diferencia entre `Image.thumbnail()` e `Image.resize()` en términos de proporciones | 7 |
| Explica qué es alpha compositing y cómo `Image.paste(logo, mask=logo)` aplica transparencia | 8 |
| Describe las ventajas de WebP frente a JPG y PNG en términos de tamaño y calidad | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Abre una imagen, la redimensiona a un tamaño fijo preservando proporciones y la guarda como WebP | 10 |
| Genera thumbnails en 3 resoluciones distintas (web, social, print) desde una imagen original | 10 |
| Aplica un watermark de logo PNG (con transparencia) sobre una imagen sin destruir el alpha del original | 10 |
| Procesa un lote de 20+ imágenes con `ThreadPoolExecutor` y muestra una barra de progreso con Rich | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| El pipeline `studio-art-pipeline` genera variantes web/social/thumb para cada imagen de `drop/` | 12 |
| Los thumbnails preservan proporciones y usan `LANCZOS` (sin pixelación visible) | 8 |
| El watermark se aplica correctamente a imágenes con y sin canal alpha | 5 |
| mypy --strict pasa sin errores en `src/` | 5 |
