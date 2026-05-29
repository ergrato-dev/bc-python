# Glosario — Semana 21: Proyecto Integrador Fase 2

## Arquitectura

**Arquitectura en capas (Layered Architecture)**
Organización del código en niveles con responsabilidades separadas: presentación, lógica de negocio, acceso a datos e infraestructura. Cada capa solo depende de la capa inmediatamente inferior.

**Capa de presentación (CLI)**
Capa que interactúa con el usuario. En este proyecto: comandos Typer + Rich. No contiene lógica de negocio, solo parseo de argumentos y renderizado de resultados.

**Capa de servicios (Service Layer)**
Coordina casos de uso orquestando repositorios y clientes HTTP. Aplica reglas de negocio y transforma errores de infraestructura en excepciones de dominio.

**Regla de dependencia (Dependency Rule)**
Principio que establece que las dependencias de código solo pueden apuntar hacia el centro (infraestructura), nunca hacia afuera. Un repositorio no puede importar un comando.

**Separación de responsabilidades (Separation of Concerns)**
Cada módulo o clase tiene una única razón para cambiar. Si cambiar la base de datos no debería modificar el código de la CLI, las responsabilidades están bien separadas.

---

## Patrones de diseño

**Repository Pattern**
Abstracción sobre la capa de persistencia que expone una interfaz orientada al dominio (`list_active`, `find_by_email`) en lugar de SQL directo. Los servicios usan repositorios; los repositorios usan la sesión.

**Inyección de dependencias (Dependency Injection)**
Técnica donde las dependencias se pasan desde afuera en lugar de construirse internamente. Ejemplo: `ExchangeService(client=FakeExchangeClient())` para tests.

**Context Manager como inyector de sesión**
Patrón `@contextmanager` + `yield` que entrega una sesión al consumidor y garantiza su cierre, sin que el consumidor gestione el ciclo de vida.

**Singleton de configuración**
Instancia única de `Settings` creada al importar `config.py`. Centraliza todas las variables de entorno y evita múltiples lecturas del archivo `.env`.

---

## Integración

**asyncio.run()**
Punto de entrada para ejecutar una coroutine desde código síncrono. Crea un nuevo event loop, ejecuta la coroutine hasta completarse y cierra el loop. Usado en la CLI para llamar clientes HTTP async.

**Bridge sync/async**
Patrón que envuelve llamadas `async` dentro de un método síncrono usando `asyncio.run()`. Permite que una CLI síncrona (Typer) use clientes HTTP asíncronos (httpx).

**pydantic-settings**
Extensión de Pydantic que carga configuración desde variables de entorno y archivos `.env`. La clase `BaseSettings` convierte automáticamente `DATABASE_URL` → `settings.database_url`.

**get_session_ctx()**
Context manager generador que abre una `Session` SQLModel, la cede al bloque `with`, y la cierra al salir. Usado por todos los comandos CLI.

---

## Testing

**Test de integración**
Test que verifica la interacción entre componentes reales (servicio + repositorio + base de datos). No mockea la base de datos — usa SQLite `:memory:` como sustituto real.

**Test unitario**
Test que verifica una unidad de código aislada, mockeando todas las dependencias externas. Los tests de `ExchangeService` con `FakeExchangeClient` son unitarios.

**SQLite `:memory:`**
Motor de base de datos que vive en RAM, descartado al cierre del proceso. Ideal para tests: crea tablas reales, acepta transacciones reales, sin archivos en disco.

**conftest.py**
Archivo especial de pytest que define fixtures compartidas para un directorio y sus subdirectorios. El `engine_fixture` y `session_fixture` viven aquí.

**Fixture de pytest**
Función decorada con `@pytest.fixture` que prepara (y opcionalmente destruye) el estado necesario para un test. El parámetro `scope` controla si se recrea por función, módulo o sesión.

**CliRunner (Typer/Click)**
Clase que simula la invocación de comandos CLI dentro de tests. Captura stdout/stderr y el código de salida sin abrir un proceso real.

---

## Errores de dominio

**StudioError**
Clase base de excepciones del proyecto. Todos los errores de dominio heredan de ella, permitiendo captura genérica en la CLI con `except StudioError`.

**NotFoundError**
Excepción que indica que una entidad solicitada no existe en la base de datos. Incluye el tipo de entidad y el ID buscado en el mensaje.

**ExternalServiceError**
Excepción que encapsula fallos al contactar APIs externas. Convierte `httpx.ConnectError` / `httpx.TimeoutException` en un error de dominio sin exponer detalles de transporte.

**DomainValidationError**
Excepción para reglas de negocio violadas (e.g., budget negativo, email duplicado). Distinta de `pydantic.ValidationError` que valida estructura de datos.

---

## Reportes

**Polars DataFrame**
Estructura de datos tabular de Polars. Inmutable, operaciones lazy, diseñada para alto rendimiento. En este proyecto se construye desde filas de SQLModel y se exporta a CSV/Parquet.

**write_csv() / write_parquet()**
Métodos de `polars.DataFrame` para serializar a disco. `write_csv` produce texto legible; `write_parquet` produce binario comprimido eficiente para análisis.

**group_by().agg()**
Operación Polars que agrupa filas por columna(s) y aplica funciones de agregación (`pl.sum`, `pl.mean`, `pl.count`) a las demás columnas.

**with_columns()**
Método Polars que añade o reemplaza columnas en un DataFrame sin modificar el original. Usado para calcular `budget_ars = budget * ars_rate`.
