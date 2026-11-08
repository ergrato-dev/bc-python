# Ejercicio 04 — Una API con PostgreSQL

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-dependencias-sesiones-y-ciclo-de-vida.md) y [05](../../1-teoria/05-probar-y-servir-una-api.md)

## Objetivo

Juntar lo de esta semana con lo de la semana 19: una API de notas guardadas en PostgreSQL, con la misma forma que la de tu proyecto:

- `create_app(url)` con su **lifespan**, y una **sesión por petición**;
- una ruta que **escribe**, con su modelo de entrada, su `commit`, su 201 y su `Location`;
- rutas que **leen**, con modelos de respuesta `from_attributes` y el 404;
- un **503** cuando PostgreSQL no contesta, sin enseñar la contraseña;
- **tests que no dejan rastro**: `dependency_overrides` con una transacción que se deshace;
- cuántas **consultas** cuesta cada petición.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

Este ejercicio trae su propio PostgreSQL, en el puerto 5433 para no chocar con el de tu proyecto:

```bash
cd bootcamp/week-20-fastapi_lo_justo_para_servir_tu_proyecto/2-practicas/ejercicio-04-una-api-con-postgresql/starter
docker compose up -d --wait
uv run python main.py
```

```
 Container practicas-semana-20-db-1  Healthy
Ejercicio 04 · Una API con PostgreSQL
```

`main.py` define el modelo `Note` y crea su tabla con `create_all`: en un ejercicio basta. En tu proyecto, las tablas las crean las migraciones.

## Pasos

### 1. La aplicación, su motor y una sesión por petición

Descomenta el **PASO 1** y ejecuta:

```
--- Paso 1: una sesión por petición ---
petición 1: {'notes': 0}
petición 2: {'notes': 0}
sesiones abiertas: 2 · ¿la misma? False
conexiones abiertas en el pool: 1
```

Es la forma de tu proyecto:

- `create_app(url)` construye la aplicación; su **lifespan** crea el motor al arrancar y lo cierra al parar (`dispose`);
- `get_session` abre una `Session` nueva **por petición** con ese motor, y el `with` la cierra al responder.

Dos peticiones, dos sesiones. Pero solo **una conexión** en el pool: la primera sesión la devolvió al cerrarse, y la segunda la volvió a usar. Abrir una conexión con PostgreSQL cuesta milisegundos; tomarla del pool, casi nada.

`database_unavailable` está registrado ya, aunque lo uses en el paso 4: lo explica su comentario.

### 2. Escribir: modelo de entrada, commit y 201

Descomenta el **PASO 2** y ejecuta:

```
--- Paso 2: POST /notes ---
'comprar pilas'                      -> 201 {'id': 1, 'text': 'comprar pilas'}
'  revisar el sensor del norte  '    -> 201 {'id': 2, 'text': 'revisar el sensor del norte'}
''                                   -> 422 String should have at least 1 character
total: 2
```

La ruta que escribe hace `commit`: es **quien decide** que el trabajo de la petición está terminado, como `guardar` en la CLI. Sin él, la sesión se cerraría al responder y PostgreSQL desharía el `INSERT`: la API respondería 201 y no habría nada guardado.

`NoteIn` dice lo que entra (`max_length=200`, el mismo límite que `String(200)`); `NoteOut`, lo que sale. `from_attributes=True` deja construir `NoteOut` desde un objeto del ORM, leyendo sus atributos.

### 3. Leer una, todas y el 404

Descomenta el **PASO 3** y ejecuta:

```
--- Paso 3: GET ---
/notes   -> [{'id': 1, 'text': 'comprar pilas'}, {'id': 2, 'text': 'revisar el sensor del norte'}]
/notes/2 -> {'id': 2, 'text': 'revisar el sensor del norte'}
/notes/99 -> 404 {'detail': 'no existe la nota 99'}
```

Las notas siguen ahí con otro `TestClient` y otras sesiones: están **confirmadas** en PostgreSQL. `session.get` devuelve `None` si no existe, y la ruta lo convierte en 404.

### 4. Sin PostgreSQL: 503, sin la contraseña

Descomenta el **PASO 4** y ejecuta:

```
--- Paso 4: PostgreSQL en el puerto 1, donde no hay nadie ---
estado: 503 · cuerpo: {'detail': 'no se pudo conectar con PostgreSQL'}
¿sale la contraseña? False
```

Sin el manejador, un `OperationalError` sería un **500** con la traza en el registro del servidor. `add_exception_handler(OperationalError, ...)` lo convierte en un **503** ("ahora no puedo, inténtalo luego"), con un mensaje que **no** copia el del error: ese texto puede llevar el usuario y el servidor de la base. Es el mismo cuidado que `database()` en la CLI.

El override del paso apunta la sesión a un motor sin servidor, solo durante el paso.

### 5. Tests que no dejan rastro

Descomenta el **PASO 5** y ejecuta:

```
--- Paso 5: dependency_overrides con una transacción que se deshace ---
dentro del test: 4 notas
antes: 2 · después del test: 2
```

Es la fixture `session` de tu proyecto (semana 19), aplicada a una API: una transacción por fuera y la sesión con `join_transaction_mode="create_savepoint"`. El `commit` de la ruta solo confirma un SAVEPOINT; al terminar, el `rollback` lo deshace todo. Dentro del "test" hay 4 notas; después, las 2 de antes.

`next(sessions, None)` hace avanzar el generador después de su `yield`: ejecuta `session.close()` y el `rollback`, como hace pytest al terminar un test.

### 6. ¿Cuántas consultas cuesta cada petición?

Descomenta el **PASO 6** y ejecuta:

```
--- Paso 6: el SQL de cada petición ---
GET  /notes    -> ['SELECT']
GET  /notes/1  -> ['SELECT']
POST /notes    -> ['INSERT', 'SELECT']
```

Cada `GET` cuesta **una** consulta. El `POST` cuesta dos: el `INSERT`, y un `SELECT` que no escribiste. Es `expire_on_commit` (semana 19, teoría 03): el commit caduca la nota, y `NoteOut.model_validate(note)` la vuelve a leer. Con una nota da igual; en tu proyecto, `post_load` apunta lo que necesita **antes** del commit.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `connection refused` en el puerto 5433 | Arranca el PostgreSQL del ejercicio: `docker compose up -d --wait` |
| `Bind for 127.0.0.1:5433 failed: port is already allocated` | Sigue arrancado el PostgreSQL de las prácticas de la semana 19: `docker compose -p practicas-semana-19 down` |
| El paso 3 no encuentra las notas del paso 2 | Falta `session.commit()` en `post_note` |
| El paso 4 da 500 en lugar de 503 | Falta `add_exception_handler` en `create_app`: tiene que estar antes de la primera petición |
| `AttributeError: 'State' object has no attribute 'engine'` | Usaste `TestClient(app)` sin `with`: el lifespan no se ejecutó |
| Después del paso 5 hay 4 notas | La sesión no está dentro de la transacción de fuera: revisa `bind=connection` y `join_transaction_mode` |

Al terminar, para el PostgreSQL del ejercicio: `docker compose down -v`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Dependencias y ciclo de vida](../ejercicio-03-dependencias-y-ciclo-de-vida/README.md) | **Ejercicio 04 · Una API con PostgreSQL** | [Proyecto · Observatorio, capa 19](../../3-proyecto/README.md) |
