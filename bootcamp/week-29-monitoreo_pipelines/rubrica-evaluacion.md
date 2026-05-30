# Rúbrica de Evaluación — Semana 29: Monitoreo de Pipelines

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre logging estructurado (structlog JSON) y logging clásico de texto plano | 8 |
| Describe qué es un histograma de tiempos de etapa y cómo calcular percentil 95 desde una lista | 7 |
| Explica el concepto de cooldown en alertas y por qué es necesario para evitar spam | 8 |
| Describe cómo funciona un watchdog timer: qué lo resetea y qué ocurre si expira | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Configura structlog con processor de timestamp, nivel y output JSON; usa `bind()` para agregar contexto | 10 |
| Implementa un `MetricsCollector` que registra duración por etapa y calcula throughput y p95 | 10 |
| Implementa una regla de alerta con threshold y cooldown que envía notificación a Slack webhook | 10 |
| Construye un panel Rich Live que muestra tabla de jobs, métricas y estado de salud en tiempo real | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `studio-monitor` lee `.pipeline_state.json` y muestra un dashboard con estado de jobs actualizado cada 2s | 12 |
| Las alertas se disparan cuando la tasa de error supera el threshold y no se repiten durante el cooldown | 10 |
| El health check detecta si el pipeline lleva más de N minutos sin procesar ningún job (watchdog) | 5 |
| mypy --strict pasa sin errores en el módulo principal | 3 |
