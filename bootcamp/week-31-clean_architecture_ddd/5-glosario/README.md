# Glosario — Semana 31: Clean Architecture y DDD

## Clean Architecture

| Término | Definición |
|---------|------------|
| **Clean Architecture** | Arquitectura en capas donde las dependencias apuntan siempre hacia adentro |
| **Regla de dependencias** | Código externo puede depender de interno, nunca al revés: infra → app → domain |
| **Capa Domain** | Lógica de negocio pura: Entities, Value Objects, reglas — sin imports externos |
| **Capa Application** | Use Cases que orquestan el dominio — sin conocer infraestructura concreta |
| **Capa Infrastructure** | Adapters concretos: S3, Slack, SQLite — implementan ports del dominio |
| **Capa Presentation** | CLI, API, UI — llama al application layer via DI, sin lógica de negocio |
| **Boundary** | Línea entre capas; cruzarla siempre con una interface (Protocol o ABC) |

## Domain-Driven Design (DDD)

| Término | Definición |
|---------|------------|
| **Entity** | Objeto con identidad única (`id`); dos entities con mismo id son el mismo objeto |
| **Value Object** | Sin identidad, inmutable (`frozen=True`); igualdad por valor, no por referencia |
| **Aggregate** | Grupo de Entities y VOs como unidad transaccional; tiene un Aggregate Root |
| **Domain Event** | Hecho inmutable que ya ocurrió (`JobCreated`, `JobFailed`) |
| **Invariante** | Regla de negocio siempre verdadera (ej. solo se puede iniciar un job PENDING) |
| **Ubiquitous Language** | Vocabulario compartido técnico/negocio; los nombres del código reflejan el dominio |

## Repository Pattern

| Término | Definición |
|---------|------------|
| **Repository** | Abstracción que simula una colección de Entities sin exponer el mecanismo de persistencia |
| **Port** | Interface (Protocol) definida en domain/application — el "qué" |
| **Adapter** | Implementación concreta de un Port en infrastructure — el "cómo" |
| **InMemoryRepository** | Adapter en memoria para tests — sin base de datos ni credenciales |

## Dependency Injection

| Término | Definición |
|---------|------------|
| **Dependency Injection** | Pasar las dependencias al objeto desde afuera, no crearlas internamente |
| **Constructor Injection** | Pasar dependencias por el `__init__` — forma más simple de DI |
| **DI Container** | Objeto que sabe cómo construir y conectar todas las dependencias |
| **Singleton Provider** | Una sola instancia por container — para repositorios y connections |
| **Factory Provider** | Nueva instancia en cada llamada — para use cases |
| **Override** | Reemplazar un provider en tests sin modificar código de producción |
| **Inversion of Control** | El use case no crea sus dependencias — las recibe; control invertido |
