# Semana 22: Automatización del Sistema de Archivos

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Usar `pathlib` para operaciones masivas: glob, rename, árbol de directorios
- Monitorear directorios en tiempo real con `watchdog` (`Observer` + `FileSystemEventHandler`)
- Aplicar convenciones de nomenclatura para archivos de producción audiovisual
- Construir un clasificador de archivos basado en reglas con movimiento automático
- Implementar idempotencia con checksums `hashlib` para evitar reprocesamiento

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [pathlib Avanzado](1-teoria/01-pathlib-avanzado.md) | Glob, tree walk, bulk rename, operaciones atómicas |
| 02 | [watchdog — Fundamentos](1-teoria/02-watchdog-fundamentos.md) | Observer, FileSystemEventHandler, tipos de evento |
| 03 | [Naming Conventions](1-teoria/03-naming-conventions.md) | Estándares de nomenclatura audiovisual, regex, auto-rename |
| 04 | [Organización Automática](1-teoria/04-organizacion-automatica.md) | Clasificador de archivos, reglas, move/copy seguro |
| 05 | [Idempotencia y Checksums](1-teoria/05-idempotencia-checksums.md) | hashlib MD5/SHA256, registro de procesados, lock files |

---

## Estructura de la Semana

```
week-22-automatizacion_sistema_archivos/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-pathlib-glob-masivo/
│   ├── 02-watchdog-monitor/
│   ├── 03-renombrador-automatico/
│   └── 04-checksum-deduplicacion/
├── 3-proyecto/
│   ├── README.md           # studio-ingest-daemon
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: pathlib + watchdog | 1.5h |
| 2 | Teoría: naming + organización + idempotencia | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `pathlib` | Operaciones de sistema de archivos tipadas |
| `watchdog` | Monitoreo de directorios en tiempo real |
| `hashlib` | Checksums para idempotencia |
| `shutil` | Operaciones de copia/movimiento seguras |
| `re` | Patrones de nomenclatura y extracción |

---

## Navegación

← [Semana 21 — Proyecto Fase 2](../week-21-proyecto_fase_2/README.md) · [Semana 23 — Procesamiento de Imágenes](../week-23-procesamiento_imagenes/README.md) →
