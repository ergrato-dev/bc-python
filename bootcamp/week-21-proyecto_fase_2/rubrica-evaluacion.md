# Rúbrica de Evaluación — Semana 21: Proyecto Integrador Fase 2

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Arquitectura y Diseño (25 pts)

| Indicador | Puntos |
|-----------|--------|
| El proyecto tiene capas claramente separadas: CLI → Servicios → Repositorios → DB/APIs | 10 |
| No hay queries SQL ni llamadas httpx directamente en los comandos Typer | 8 |
| La configuración (DB URL, API keys) se lee de variables de entorno o `Settings`, no hardcodeada | 7 |

## Integración Técnica (45 pts)

| Indicador | Puntos |
|-----------|--------|
| SQLModel: modelos con relaciones, sesiones gestionadas por capa de servicio | 10 |
| Typer + Rich: al menos 3 subcomandos funcionales con salida tabulada | 10 |
| httpx async: al menos una llamada a API externa con retry y timeout | 10 |
| Polars: al menos un reporte con aggregaciones exportado a CSV | 10 |
| mypy --strict pasa sin errores en `src/` | 5 |

## Calidad (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Tests de integración con DB en memoria — al menos 5 tests que pasan | 12 |
| Manejo de errores: mensajes claros ante fallo de red o registro no encontrado | 10 |
| README del proyecto con instrucciones de instalación y uso de cada comando | 8 |
