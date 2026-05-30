# Proyecto Semana 29: `studio-monitor`

> Daemon de monitoreo en tiempo real para el pipeline audiovisual de Studio BC

---

## Descripción

`studio-monitor` observa el pipeline de producción de Studio BC y provee:

- **Métricas** por stage: throughput, error rate, latencias P50/P95
- **Alertas** con umbral + cooldown enviadas a Slack
- **Health checks** de componentes: disco, Redis, archivo de estado
- **Watchdog** que reinicia el daemon si se cuelga
- **Dashboard Rich** en terminal con actualización en vivo

Se integra con el `SyncState` de la semana 26 y el `StateStore` de la semana 27.

---

## Estructura

```
starter/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── config.py         # Settings desde env vars
│   ├── metrics.py        # MetricsCollector, StageMetrics
│   ├── alerts.py         # AlertRule, AlertManager → Slack
│   ├── health.py         # HealthChecker, WatchdogTimer
│   ├── dashboard.py      # Rich Live dashboard
│   └── __main__.py       # CLI: monitor / status
└── tests/
    ├── __init__.py
    ├── test_metrics.py
    └── test_alerts.py
```

---

## Comandos

```bash
# Arrancar el dashboard en vivo
python -m src monitor --state-file .sync_state.json

# Ver estado sin dashboard (JSON)
python -m src status --state-file .sync_state.json

# Ejecutar tests
pytest tests/ -v
```

---

## Tareas del Estudiante

### `metrics.py`
- [ ] `StageMetrics.record()`: acumular duration y success/error
- [ ] `MetricsCollector.throughput`: jobs por segundo desde inicio
- [ ] `MetricsCollector.snapshot()`: dict con p95, error_rate, throughput por stage

### `alerts.py`
- [ ] `AlertRule.should_fire()`: comparación + cooldown
- [ ] `AlertManager._send_slack()`: POST al webhook o dry_run print
- [ ] `AlertManager.check()`: evaluar todas las reglas

### `health.py`
- [ ] `HealthChecker.check_all()`: ejecutar los tres checks y retornar dict
- [ ] `WatchdogTimer.reset()`: reiniciar el timer sin duplicar

### `dashboard.py`
- [ ] `build_metrics_table()`: Rich Table con columnas coloreadas
- [ ] `build_layout()`: Layout con métricas + status + health

---

## Criterios de Aceptación

- [ ] `mypy --strict src/` pasa sin errores
- [ ] `pytest tests/` — 8+ tests en verde
- [ ] El dashboard se actualiza cada segundo con datos reales del state file
- [ ] Una alerta se dispara cuando error_rate > 5 % y no vuelve a dispararse hasta que pasa el cooldown
- [ ] El watchdog reinicia el monitor si no recibe `reset()` en N segundos
