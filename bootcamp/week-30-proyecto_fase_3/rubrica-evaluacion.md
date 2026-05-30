# Rúbrica de Evaluación — Semana 30: Proyecto Fase 3

## Puntaje Total: 200 puntos · Mínimo para aprobar: 140 pts · Demo en vivo obligatoria

---

## Conocimiento (60 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica el rol de cada etapa del pipeline y cómo se conectan mediante el `Stage Protocol` | 15 |
| Describe la estrategia de manejo de errores: retry, DLQ y cómo se decide si un job pasa a `failed` | 15 |
| Explica cómo el daemon watchdog detecta archivos nuevos y los encola sin duplicados (idempotencia) | 15 |
| Describe qué información registra el `StateStore` y cómo el dashboard lo lee en tiempo real | 15 |

---

## Desempeño (80 pts)

| Indicador | Puntos |
|-----------|--------|
| El daemon detecta un `.mp4` copiado a `drop/` e inicia el pipeline automáticamente | 20 |
| La etapa `TranscodeStage` genera proxy (25% res), thumbnail (frame 5s) y web encode (1080p máx) | 20 |
| La etapa `CloudStage` sube a S3 con clave `{project}/{type}/{date}/{file}` | 20 |
| La etapa `DistributeStage` envía notificación a Slack con las URLs generadas | 20 |

---

## Producto (60 pts)

| Indicador | Puntos |
|-----------|--------|
| El pipeline procesa 3 videos de punta a punta en demo en vivo sin errores | 20 |
| `pytest tests/ -v` pasa — todos los tests en verde con cobertura ≥ 80 % | 15 |
| El dashboard Rich muestra estado de jobs, métricas y health checks actualizándose cada segundo | 15 |
| `mypy --strict src/` pasa sin errores | 5 |
| `.sync_state.json` registra correctamente todos los jobs procesados con timestamps | 5 |

---

## Defensa Técnica (bonus: hasta +20 pts si aplica)

| Indicador | Puntos |
|-----------|--------|
| El estudiante explica una decisión de diseño no trivial y la justifica | +10 |
| El estudiante identifica una mejora posible y describe cómo la implementaría | +10 |
