# Rúbrica de Evaluación — Semana 31: Clean Architecture y DDD

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la regla de dependencias de Clean Architecture y por qué el dominio no puede importar infraestructura | 8 |
| Describe la diferencia entre Entity y Value Object: identidad vs igualdad por valor | 7 |
| Explica qué problema resuelve el Repository Pattern y cómo un `IJobRepository` desacopla la capa de aplicación del storage | 8 |
| Describe cómo Dependency Injection permite cambiar implementaciones sin modificar los consumers | 7 |

---

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Implementa `Asset` como Entity con identidad `asset_id` y comportamiento de dominio | 10 |
| Implementa `ProjectSlug` como Value Object inmutable (`frozen=True`) con validación | 10 |
| Implementa `IJobRepository` (Protocol) y `InMemoryJobRepository` que lo cumple | 10 |
| Configura un container de DI con `dependency-injector` que inyecta el repositorio en un use case | 10 |

---

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `studio-refactored` tiene estructura `domain/`, `application/`, `infrastructure/`, `presentation/` | 10 |
| `ProcessAssetUseCase` en `application/` solo depende de interfaces del dominio, nunca de infraestructura | 10 |
| `pytest tests/domain/ tests/application/` pasa sin importar boto3, httpx ni ffmpeg | 7 |
| `mypy --strict src/` pasa sin errores | 3 |
