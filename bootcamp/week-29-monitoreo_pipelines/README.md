# Semana 29: Monitoreo de Pipelines

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Implementar structured logging con `structlog`: contexto por request, processors y JSON output
- Recolectar métricas de pipeline: tiempos por etapa, tasa de error, throughput y cola pendiente
- Configurar alertas automáticas con thresholds y notificaciones a Slack
- Implementar health checks con watchdog timers y endpoints de status JSON
- Construir un dashboard de terminal con `Rich Live` para monitoreo en tiempo real

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Structured Logging](1-teoria/01-structured-logging.md) | structlog, contexto, processors, JSON output |
| 02 | [Métricas de Pipeline](1-teoria/02-metricas-pipeline.md) | Tiempos, throughput, tasa de error, cola pendiente |
| 03 | [Alertas y Thresholds](1-teoria/03-alertas-thresholds.md) | Reglas de alerta, cooldown, notificaciones a Slack |
| 04 | [Health Checks](1-teoria/04-health-checks.md) | Watchdog timers, status endpoint, circuit breaker |
| 05 | [Dashboard Terminal](1-teoria/05-dashboard-terminal.md) | Rich Live, Layout, Table, Panel, Progress en tiempo real |

---

## Estructura de la Semana

```
week-29-monitoreo_pipelines/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-structlog-contexto/
│   ├── 02-metricas-coleccion/
│   ├── 03-alertas-slack/
│   └── 04-rich-live-dashboard/
├── 3-proyecto/
│   ├── README.md           # studio-monitor
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: structlog + métricas | 1.5h |
| 2 | Teoría: alertas + health checks + dashboard | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `structlog` | Logging estructurado con contexto y processors |
| `rich` | `Live`, `Layout`, `Table`, `Panel`, `Progress` para dashboard |
| `prometheus_client` | Contadores, histogramas y gauges (introducción básica) |
| `httpx` | Envío de alertas a Slack webhook |

---

## Navegación

← [Semana 28 — Integraciones con Plataformas](../week-28-integraciones_plataformas/README.md) · [Semana 30 — Proyecto Fase 3](../week-30-proyecto_fase_3/README.md) →
