# Rúbrica de Evaluación — Semana 26: Cloud Storage y Assets

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre un bucket S3 y un objeto, y qué es una presigned URL y cuándo usarla | 8 |
| Describe el flujo de autenticación con Service Account de Google (JSON key → credentials → service) | 7 |
| Distingue entre hot storage (S3 Standard), cold storage (Glacier) y cuándo aplicar cada uno | 8 |
| Explica cómo ETag de S3 se usa para detectar cambios y cuándo NO coincide con SHA-256 | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Sube y descarga un archivo a S3 con `boto3`, pasando metadata personalizada como `ExtraArgs` | 10 |
| Genera una presigned URL para descarga con expiración configurable | 10 |
| Sube un archivo a Google Drive en una carpeta específica usando Service Account | 10 |
| Implementa sync incremental: compara checksums locales vs remotos y solo sube lo modificado | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| El daemon `studio-cloud-backup` sube assets de `output/` a S3 con estructura `{proyecto}/{tipo}/{fecha}/` | 12 |
| El mismo daemon sube a Drive la carpeta de entrega del cliente con permisos de lectura configurados | 10 |
| El backup es incremental: lee `.sync_state.json` y omite archivos sin cambios | 5 |
| mypy --strict pasa sin errores en el módulo principal | 3 |
