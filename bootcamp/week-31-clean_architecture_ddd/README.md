# Semana 31: Clean Architecture y DDD

> **Fase 4 — Arquitectura Master y Sistema de Producción** · _Senior → Master_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Aplicar la regla de dependencias de Clean Architecture: Domain → Application → Infrastructure
- Modelar el dominio con Entities, Value Objects y Aggregates (DDD básico)
- Implementar el Repository Pattern para abstraer acceso a datos y servicios externos
- Configurar Dependency Injection manual y con `dependency-injector`
- Refactorizar un módulo existente separando dominio de infraestructura

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Clean Architecture](1-teoria/01-clean-architecture.md) | Capas, regla de dependencias, boundaries |
| 02 | [DDD Básico](1-teoria/02-ddd-basico.md) | Entities, Value Objects, Aggregates, Domain Events |
| 03 | [Repository Pattern](1-teoria/03-repository-pattern.md) | Ports & adapters, Unit of Work |
| 04 | [Dependency Injection](1-teoria/04-dependency-injection.md) | DI manual, `dependency-injector` |
| 05 | [Refactoring Studio BC](1-teoria/05-refactoring-studio-bc.md) | Aplicar Clean Architecture al pipeline |

---

## Estructura de la Semana

```
week-31-clean_architecture_ddd/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de arquitectura
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-entidades-dominio/
│   ├── 02-value-objects/
│   ├── 03-repositorio-inmemory/
│   └── 04-inyeccion-dependencias/
├── 3-proyecto/
│   ├── README.md           # studio-refactored
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: Clean Architecture + DDD | 1.5h |
| 2 | Teoría: Repository + DI + Refactoring | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Herramienta | Rol |
|-------------|-----|
| `dependency-injector` | Container de DI con providers declarativos |
| `abc.ABC` / `Protocol` | Definir interfaces de repositorios (ports) |
| `dataclasses(frozen=True)` | Value Objects inmutables |
| `pytest` | Tests de domain y application en aislamiento total |

---

## Navegación

← [Semana 30 — Proyecto Fase 3](../week-30-proyecto_fase_3/README.md) · [Semana 32 — IA Aplicada a Media](../week-32-ia_aplicada_media/README.md) →
