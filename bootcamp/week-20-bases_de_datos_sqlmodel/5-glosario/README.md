# Glosario — Semana 20: Bases de Datos con SQLModel

## A

**Alembic**
Herramienta de migraciones de esquema para SQLAlchemy. Permite versionar y aplicar cambios de base de datos de forma incremental, como git para el esquema SQL.

**autogenerate** (Alembic)
Flag de `alembic revision` que compara los modelos Python actuales contra el esquema en la DB y genera automáticamente el diff como script de migración.

## B

**back_populates**
Parámetro de `Relationship()` que enlaza ambos extremos de una relación bidireccional. Debe apuntar al nombre del atributo en el modelo opuesto.

**BaseRepository**
Clase genérica que implementa CRUD básico reutilizable. Las subclases añaden queries específicas del dominio.

## C

**commit()**
Persiste todos los cambios pendientes de la sesión a la base de datos como una transacción atómica.

**connection pool**
Conjunto de conexiones a la base de datos reutilizables. SQLAlchemy gestiona el pool automáticamente a través del engine.

## D

**DetachedInstanceError**
Error que ocurre al acceder a un atributo lazy de un objeto SQLAlchemy después de que su sesión fue cerrada. Solución: usar eager loading o acceder dentro de la sesión.

**downgrade** (Alembic)
Revertir una o más migraciones aplicadas. Ejecuta el método `downgrade()` del script de migración.

## E

**eager loading**
Estrategia de carga que obtiene los objetos relacionados en la misma query (o en una segunda query optimizada). Evita el problema N+1. Ver `selectinload`.

**engine**
Objeto SQLAlchemy que representa la conexión a la base de datos. Gestiona el pool de conexiones y traduce el dialecto SQL.

## F

**Field()**
Función de SQLModel para configurar columnas: `primary_key`, `foreign_key`, `index`, `unique`, `ge`, `le`, `max_length`, etc.

**flush()**
Sincroniza el estado del objeto con la base de datos sin hacer commit. Útil para obtener IDs generados antes del commit final.

**foreign_key**
Campo que referencia la PK de otra tabla. En SQLModel: `Field(foreign_key="tabla.columna")`.

## G

**group_by()**
Cláusula SQL que agrupa filas con el mismo valor en una o más columnas, usada junto con funciones de aggregación.

## L

**lazy loading**
Estrategia de carga por defecto: los objetos relacionados se cargan solo cuando se accede al atributo. Puede causar el problema N+1.

**link_model**
Parámetro de `Relationship()` que especifica la tabla de asociación para relaciones many-to-many.

## M

**migration**
Script versionado que describe un cambio de esquema (crear tabla, añadir columna, crear índice) con una función `upgrade()` y su inversa `downgrade()`.

**many-to-many**
Relación donde múltiples registros de una tabla se asocian con múltiples de otra. Requiere tabla de asociación (link table).

## N

**N+1 Problem**
Anti-patrón donde se hace 1 query principal + N queries adicionales (una por cada objeto relacionado). Se resuelve con eager loading.

## O

**one-to-many**
Relación donde un registro de una tabla tiene múltiples registros asociados en otra. La FK vive en el lado "muchos".

**ORM** (Object-Relational Mapping)
Técnica que mapea tablas SQL a clases Python y filas a objetos. SQLAlchemy es el ORM subyacente de SQLModel.

## R

**refresh()**
Recarga el estado de un objeto desde la base de datos, actualizando atributos generados por el DB (ej: id autoincrementable).

**Relationship**
Descriptor de SQLModel que define la navegación entre modelos relacionados. No crea columna en la tabla — solo instala la lógica de ORM.

**Repository Pattern**
Patrón de diseño que abstrae el acceso a datos detrás de una interfaz. El dominio interactúa con el repositorio, no con la sesión directamente.

## S

**scalar_subquery()**
Subquery que retorna un único valor escalar, usable dentro de un `where()`.

**selectinload**
Estrategia de eager loading que emite una segunda SELECT con `IN` para cargar los relacionados. Eficiente para colecciones.

**Session**
Objeto SQLAlchemy que implementa el patrón Unit of Work: rastrea cambios, gestiona transacciones y hace flush/commit.

**SQLModel**
Librería creada por Sebastián Ramírez (creator of FastAPI) que une SQLAlchemy y Pydantic en una sola clase.

## T

**table=True**
Flag que convierte un `SQLModel` en una tabla SQL real. Sin él, el modelo es solo un schema Pydantic.

**transaction**
Unidad atómica de trabajo: o todas las operaciones se persisten (commit) o ninguna (rollback).

## U

**Unit of Work**
Patrón que agrupa múltiples operaciones de base de datos en una sola transacción. La `Session` de SQLAlchemy lo implementa.

**upgrade** (Alembic)
Aplicar una o más migraciones pendientes. `alembic upgrade head` aplica todas hasta la última.

## W

**where()**
Cláusula de filtro en queries SQLModel. Soporta comparaciones, `in_()`, `contains()`, `ilike()`, operadores `and_()`, `or_()`.
