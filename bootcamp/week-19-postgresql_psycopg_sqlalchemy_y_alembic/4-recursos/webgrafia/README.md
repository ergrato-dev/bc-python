# Webgrafía — Semana 19

| Recurso | Para qué |
|---|---|
| [Tutorial de PostgreSQL](https://www.postgresql.org/docs/18/tutorial.html) (en inglés) | El tutorial oficial: tablas, consultas, `JOIN`, agregados y [transacciones](https://www.postgresql.org/docs/18/tutorial-transactions.html). El complemento de la teoría 01 |
| [Tipos de datos](https://www.postgresql.org/docs/18/datatype.html) y [restricciones](https://www.postgresql.org/docs/18/ddl-constraints.html) (en inglés) | Qué tipo elegir para cada columna, y todas las restricciones, `ON DELETE CASCADE` incluido |
| [`psql`](https://www.postgresql.org/docs/18/app-psql.html) (en inglés) | Todas las órdenes con `\`. Busca `\dt`, `\d` y `\x` |
| [SQLBolt](https://sqlbolt.com/) (en inglés) | Lecciones interactivas de SQL en el navegador, con un ejercicio en cada una. Si el SQL de la teoría 01 te supo a poco |
| [psycopg 3: uso básico](https://www.psycopg.org/psycopg3/docs/basic/usage.html) (en inglés) | Conexiones y cursores. Sigue con [parámetros](https://www.psycopg.org/psycopg3/docs/basic/params.html), [transacciones](https://www.psycopg.org/psycopg3/docs/basic/transactions.html) y [COPY](https://www.psycopg.org/psycopg3/docs/basic/copy.html): la teoría 02 y el ejercicio 01 |
| [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) (en inglés) | OWASP sobre la inyección de SQL: por qué los parámetros la impiden y qué hacer con lo que no puede ser parámetro |
| [Inyección SQL](https://es.wikipedia.org/wiki/Inyecci%C3%B3n_SQL) (en español) | La historia y los tipos de ataque, con ejemplos. Y la tira de [xkcd sobre Bobby Tables](https://xkcd.com/327/), que todo el mundo cita |
| [Tutorial unificado de SQLAlchemy](https://docs.sqlalchemy.org/en/21/tutorial/index.html) (en inglés) | El tutorial oficial de SQLAlchemy 2: Core y ORM juntos, en el mismo orden que los ejercicios 02 y 03 |
| [Cargar relaciones](https://docs.sqlalchemy.org/en/21/orm/queryguide/relationships.html) (en inglés) | Carga perezosa, `selectinload`, `joinedload` y el problema N+1: la teoría 03, sección 7 |
| [Transacciones de la sesión](https://docs.sqlalchemy.org/en/21/orm/session_transaction.html) (en inglés) | Cómo empieza y termina una transacción con la sesión; busca "Joining a Session into an External Transaction", la receta de la fixture `session` |
| [Tutorial de Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) (en inglés) | `init`, `revision`, `upgrade` y `downgrade`, paso a paso. Sigue con [autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html), que dice qué detecta y qué no |
| [Convenciones de nombres](https://alembic.sqlalchemy.org/en/latest/naming.html) (en inglés) | Por qué `naming_convention`, y qué pasa sin ella cuando toca borrar una restricción |
| [Recetario de Alembic](https://alembic.sqlalchemy.org/en/latest/cookbook.html) (en inglés) | Recetas: pasar una conexión a `env.py` (lo que hacen tus tests), migraciones de datos, varias bases |
| [La imagen `postgres`](https://hub.docker.com/_/postgres) (en inglés) | Las variables `POSTGRES_*`, el volumen y los scripts de arranque de la imagen oficial |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
