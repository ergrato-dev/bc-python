# Libros y Documentación — Semana 30: Proyecto Fase 3

Esta es una semana de integración. Las lecturas recomendadas son las que ayudan a pensar en el sistema como un todo.

## Arquitectura de software

| Recurso | Descripción |
|---------|-------------|
| [Architecture Patterns with Python](https://www.cosmicpython.com/) | Libro gratuito online — Repository, Service Layer, Event-Driven; directamente aplicable |
| [Python Design Patterns](https://python-patterns.guide/) | Catálogo de patrones con ejemplos Python modernos — Strategy, Decorator, Facade |
| [Refactoring.Guru — Chain of Responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility) | Patrón GoF base del Stage Protocol con ejemplos Python |

## Testing y calidad

| Recurso | Descripción |
|---------|-------------|
| [pytest Documentation](https://docs.pytest.org/en/stable/) | Referencia completa — fixtures, marcadores, plugins |
| [Python Testing with pytest (libro, cap. gratuitos)](https://pragprog.com/titles/bopytest2/python-testing-with-pytest-second-edition/) | El libro de pytest — fixtures, parametrize, conftest |
| [Test-Driven Development with Python (OBEYT)](https://www.obeythetestinggoat.com/) | Libro gratuito online — TDD con Python de punta a punta |

## Operaciones y producción

| Recurso | Descripción |
|---------|-------------|
| [The Twelve-Factor App](https://12factor.net/) | 12 principios para apps de producción — config, logs, procesos, builds |
| [Site Reliability Engineering (Google)](https://sre.google/sre-book/table-of-contents/) | Cap. 6 (Monitoring) y Cap. 18 (Software Engineering in SRE) — directamente aplicables |

## Checklist de entrega

Antes de hacer la demo, verificar:

```
✅ pytest tests/ -v --cov=src --cov-report=term-missing (cobertura ≥ 80 %)
✅ mypy --strict src/ (cero errores)
✅ .env.example actualizado con todas las variables
✅ README del proyecto con comandos de instalación y ejecución
✅ .pipeline_state.json vacío (o eliminado) antes de la demo
✅ Carpeta drop/ vacía
✅ ffmpeg instalado: ffmpeg -version
```

> **Destacado:** [Architecture Patterns with Python](https://www.cosmicpython.com/) (Harry Percival & Bob Gregory) es de lectura obligatoria para entender por qué el diseño en capas que usamos es la base de software de producción mantenible.
