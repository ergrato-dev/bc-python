# Rúbrica de Evaluación — Semana 22: Automatización del Sistema de Archivos

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre `Path.glob()` y `Path.rglob()` y cuándo usar cada uno | 7 |
| Describe el modelo `Observer + Handler` de watchdog: qué corre en hilo separado y por qué | 8 |
| Explica qué es idempotencia en el contexto de procesamiento de archivos y cómo los checksums la garantizan | 8 |
| Distingue cuándo usar `shutil.move()` vs `Path.rename()` en términos de atomicidad y cross-device | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Implementa un `FileSystemEventHandler` que reacciona a `on_created` y filtra por extensión | 10 |
| Aplica una naming convention (regex + sustitución) a lotes de archivos sin colisión | 10 |
| Clasifica archivos en categorías (video/audio/imagen/doc) y los mueve a la carpeta destino correcta | 10 |
| Calcula checksum SHA-256 de un archivo y persiste el registro para saltar archivos ya procesados | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| El daemon `studio-ingest-daemon` observa `drop/`, clasifica y mueve a `organized/{tipo}/{fecha}/` | 12 |
| Se evita reprocesamiento: el daemon lee `.processed.json` al iniciar y lo actualiza al completar | 10 |
| El daemon maneja `KeyboardInterrupt` limpiamente (detiene el Observer antes de salir) | 5 |
| mypy --strict pasa sin errores en el módulo principal | 3 |
