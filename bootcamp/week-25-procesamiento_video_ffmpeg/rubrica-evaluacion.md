# Rúbrica de Evaluación — Semana 25: Procesamiento de Video con FFmpeg

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre CRF y bitrate fijo en H.264/H.265 y cuándo usar cada uno | 8 |
| Describe qué es un proxy y por qué facilita la edición no destructiva | 7 |
| Explica el concepto de filtro en ffmpeg (filter_complex) y la diferencia entre filtros simples y complejos | 8 |
| Describe qué información proporciona ffprobe y cómo usarlo desde Python | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Transcodifica un video a H.264 con CRF 23, preset slow y audio AAC 128k | 10 |
| Extrae un clip entre dos timecodes y un thumbnail en el segundo 5 de un video | 10 |
| Aplica un filtro `scale` + `drawtext` a un video manteniendo aspect ratio | 10 |
| Lee metadata completa de un video (codec, resolución, framerate, duración) con ffprobe | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| El pipeline genera proxy (720p H.264) + thumbnail + web encode para cada video de `drop/` | 12 |
| El proxy mantiene el audio original y tiene exactamente 25% de la resolución original | 8 |
| La metadata del video original se escribe en un JSON junto a los outputs | 7 |
| mypy --strict pasa sin errores en `src/` | 3 |
