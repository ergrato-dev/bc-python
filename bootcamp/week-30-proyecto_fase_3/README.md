# Semana 30: Proyecto Fase 3 — Pipeline de Producción

> **Fase 3 — Automatización y Pipelines de Media** · _Semana integradora_

## Descripción

Esta semana no tiene teoría ni ejercicios guiados: es la semana de **integración y entrega** de la Fase 3.

El proyecto `studio-production-pipeline` une todo lo construido en las semanas 22–29 en un único sistema operativo end-to-end para Studio BC:

```
drop/   →  Ingest  →  Validate  →  Transcode  →  Cloud Upload
                                                    ↓
                                               Distribute
                                           (YouTube · Vimeo)
                                                    ↓
                                                 Notify
                                             (Slack · Discord)
                                                    ↓
                                             Dashboard Live
                                         (Rich terminal monitor)
```

---

## Objetivos

Al terminar esta semana, el estudiante habrá demostrado que puede:

- Integrar watchdog, ffmpeg, boto3, Drive API, YouTube, Vimeo, Slack y Rich en un pipeline cohesivo
- Diseñar etapas con el `Stage Protocol` y manejar fallos con DLQ y retry
- Desplegar un daemon que procesa archivos nuevos y registra su estado en JSON
- Escribir tests de integración que cubren el flujo completo sin credenciales reales
- Defender técnicamente las decisiones de diseño

---

## Estructura

```
week-30-proyecto_fase_3/
├── README.md
├── rubrica-evaluacion.md
├── 3-proyecto/
│   ├── README.md           # Descripción del proyecto + TODOs
│   ├── starter/            # Scaffolding para el estudiante
│   └── solution/           # Solo instructores
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Leer README del proyecto + planificar integración | 0.5h |
| 2 | Implementar las 3 etapas con TODOs | 2.5h |
| 3 | Escribir tests de integración + watcher | 1.5h |
| 4 | Demo en vivo + dashboard + refinamiento | 1.5h |

---

## Criterios de Aprobación

- Pipeline procesa un video de `drop/` de punta a punta sin intervención manual
- `pytest tests/ -v` pasa con cobertura > 80 %
- `mypy --strict src/` pasa sin errores
- Demo en vivo ejecutándose en terminal con dashboard visible

---

## Navegación

← [Semana 29 — Monitoreo de Pipelines](../week-29-monitoreo_pipelines/README.md) · [Semana 31 — Clean Architecture y DDD](../week-31-clean_architecture_ddd/README.md) →
