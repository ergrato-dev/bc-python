# Glosario — Semana 19

| Término | Definición |
|---|---|
| **ACID** | Lo que promete una transacción: atomicidad (todo o nada), consistencia (se cumplen las restricciones), aislamiento (otras conexiones no ven lo no confirmado) y durabilidad (lo confirmado sobrevive a un apagón) |
| **Alembic** | La herramienta de migraciones de SQLAlchemy: genera, aplica y deshace los cambios del esquema |
| **`alembic_version`** | La tabla donde Alembic apunta, en cada base, por qué revisión va. Así sabe qué migraciones le faltan |
| **`--autogenerate`** | Opción de `alembic revision` que compara los modelos con la base y escribe un borrador de migración. No detecta renombrados ni cambios de datos: se lee siempre |
| **Carga perezosa (*lazy loading*)** | Cargar una relación la primera vez que se toca, con su propia consulta. Es la de por defecto, y la causa del problema N+1 |
| **Clave foránea (*foreign key*)** | Una columna que apunta a la clave primaria de otra tabla. La base no deja guardar un valor que no exista allí |
| **Clave primaria (*primary key*)** | La columna que identifica cada fila: única y nunca vacía. Casi siempre un `id` que numera la base |
| **`COMMIT`** | Confirmar una transacción: sus cambios pasan a ser definitivos y visibles para las demás conexiones |
| **`COPY`** | La orden de PostgreSQL para cargar o sacar datos en bloque. Mucho más rápida que un `INSERT` por fila |
| **Core** | La capa de SQLAlchemy que describe tablas en Python y construye SQL por partes (`select`, `insert`...) |
| **`create_all`** | Crea las tablas de un `MetaData` que no existan. No cambia las que ya existen: en un proyecto, las tablas las crean las migraciones |
| **Cursor** | La posición en el resultado de una consulta. `fetchone` avanza una fila; `fetchall` trae las que quedan |
| **`downgrade`** | La mitad de una migración que la deshace; y la orden de Alembic que retrocede en la cadena |
| ***Driver*** | La biblioteca que habla el protocolo de una base de datos. psycopg 3 es el de PostgreSQL |
| **DSN** | La URL de conexión: usuario, contraseña, máquina, puerto y base. Es un secreto, porque lleva la contraseña |
| **`expire_on_commit`** | La sesión marca sus objetos como caducados al confirmar, y los vuelve a leer en el siguiente acceso. Está activado por defecto |
| **`flush`** | Enviar a la base los cambios pendientes de la sesión **sin** confirmar la transacción. Con él, PostgreSQL asigna los `id` |
| ***Healthcheck*** | La orden con la que Docker comprueba si un servicio está listo. En PostgreSQL, `pg_isready` |
| **`head`** | La última migración de la cadena. `alembic upgrade head` aplica todas las que faltan |
| **Índice** | Una estructura aparte que hace rápidas las búsquedas por una columna, como el índice de un libro |
| **Inyección de SQL** | Un ataque en el que un dato que alguien escribe se convierte en SQL porque se pegó en el texto de la consulta. Los parámetros lo impiden |
| **`JOIN`** | Unir las filas de dos tablas por una condición, casi siempre la clave foránea. `LEFT JOIN` conserva también las de la izquierda sin pareja |
| **Mapa de identidad** | El registro de la sesión con un solo objeto por fila: dos `get` de la misma clave devuelven el mismo objeto |
| **`Mapped`** | La anotación de SQLAlchemy 2 que declara una columna con su tipo de Python: `Mapped[float \| None]` es una columna que admite `NULL` |
| **Migración** | Un archivo que lleva el esquema de la base de un estado al siguiente, y sabe volver. Va a Git y se aplica en orden |
| **Modelo** | Una clase del ORM que describe una tabla; cada instancia es una fila |
| **N+1** | Hacer una consulta para una lista y otra más por cada elemento. Se arregla con `selectinload` o con un `GROUP BY` |
| ***Naming convention*** | Plantillas para los nombres de restricciones e índices (`fk_readings_load_id_loads`), para que sean los mismos en todas las bases |
| **`NULL`** | El valor que falta. No es igual a nada, ni a otro `NULL`: se pregunta con `IS NULL`. `count(columna)` y `avg` lo ignoran |
| **ORM** | *Object Relational Mapper*: convierte filas en objetos y cambios en objetos en SQL |
| **Parámetro** | Un valor que viaja aparte del texto del SQL (`%s`, `:nombre`). Nunca se convierte en SQL |
| **Pool de conexiones** | El almacén de conexiones abiertas de un motor, que se prestan y se devuelven en lugar de abrirse cada vez |
| **PostgreSQL** | La base de datos relacional, libre, que usa el bootcamp. Es un servidor: los programas se conectan a él |
| **psql** | El cliente de PostgreSQL en la terminal. `\dt` lista las tablas, `\d tabla` describe una |
| **psycopg** | El *driver* de PostgreSQL para Python. La versión 3 se instala como `psycopg`, con el extra `[binary]` |
| **Restricción** | Una regla que la base comprueba siempre: `NOT NULL`, `UNIQUE`, `CHECK`, clave primaria o foránea |
| **Revisión** | El identificador de una migración (`0001`). Cada una apunta a la anterior con `down_revision` |
| **`ROLLBACK`** | Deshacer una transacción: nada de lo que hizo queda en la base |
| **SAVEPOINT** | Un punto dentro de una transacción al que se puede volver sin deshacerla entera. La fixture `session` los usa |
| **`selectinload`** | Opción del ORM que carga una relación de muchos objetos en una sola consulta extra (`WHERE id IN (...)`) |
| **`server_default`** | Un valor por defecto que pone la base de datos, no Python. Rellena las filas que ya existían al añadir una columna |
| **Sesión (`Session`)** | El espacio de trabajo del ORM: recuerda los objetos cargados, apunta los cambios y los envía en el `flush` |
| **SQL** | El lenguaje de las bases de datos relacionales: dices **qué** quieres y la base decide cómo |
| **SQLAlchemy** | La biblioteca de bases de datos de Python más usada: Core, ORM, motor y pool |
| **Tabla** | Filas con las mismas columnas, cada una de un tipo |
| **Transacción** | Un grupo de operaciones que se aplican todas o ninguna, entre un `BEGIN` y un `COMMIT` o `ROLLBACK` |
| **`TRUNCATE`** | Vaciar tablas enteras de golpe. Con `RESTART IDENTITY`, la numeración de los `id` vuelve a empezar |
| **Unidad de trabajo** | La sesión decide el SQL a partir de los cambios en los objetos: cambias un atributo y ella envía el `UPDATE` |
| **`upgrade`** | La mitad de una migración que la aplica; y la orden de Alembic que avanza en la cadena |
| **Volumen** | El almacenamiento de Docker que vive fuera del contenedor. Los datos de PostgreSQL sobreviven a `down`, no a `down -v` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
