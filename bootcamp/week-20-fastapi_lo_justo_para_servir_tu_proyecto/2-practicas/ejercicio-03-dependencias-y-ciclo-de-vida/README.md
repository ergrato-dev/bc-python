# Ejercicio 03 — Dependencias y ciclo de vida

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-dependencias-sesiones-y-ciclo-de-vida.md) y [04](../../1-teoria/04-def-o-async-def-concurrencia-en-el-servidor.md)

## Objetivo

Entender las tres piezas con las que tu API abrirá una sesión de PostgreSQL por petición, y la decisión de escribir `def` o `async def`:

- una **dependencia** con `Depends`, compartida por varias rutas;
- una dependencia con **`yield`**, que prepara algo antes de la ruta y lo recoge después;
- dependencias que usan otras, y la **caché por petición**;
- **`dependency_overrides`**, para cambiar una dependencia en los tests;
- el **lifespan**, que abre lo que dura toda la vida de la aplicación;
- cinco peticiones a la vez contra rutas `def`, `async def` que bloquea y `async def` que espera.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-20-fastapi_lo_justo_para_servir_tu_proyecto/2-practicas/ejercicio-03-dependencias-y-ciclo-de-vida/starter
uv run python main.py
```

```
Ejercicio 03 · Dependencias y ciclo de vida
```

## Pasos

### 1. Una dependencia

Descomenta el **PASO 1** y ejecuta:

```
--- Paso 1: Depends ---
/stations              -> {'page': {'limit': 10, 'offset': 0}}
/readings?limit=500    -> {'page': {'limit': 100, 'offset': 0}}
/readings?offset=uno   -> 422
```

Una **dependencia** es una función que FastAPI llama **antes** de la ruta y cuyo resultado le pasa como argumento. `Depends(pagination)` dice cuál; el alias `Pagination` evita repetirlo en cada ruta. La dependencia tiene sus propios parámetros, que FastAPI lee de la petición como los de una ruta: `limit` y `offset` vienen de la consulta, con su 422 si no son números. Las dos rutas comparten la regla de los 100 como máximo, escrita una vez.

### 2. Una dependencia con `yield`

Descomenta el **PASO 2** y ejecuta:

```
--- Paso 2: yield ---
sesión 1 -> ['abre sesión 1', 'la ruta usa sesión 1', 'cierra sesión 1']
sesión 2 -> ['abre sesión 2', 'la ruta usa sesión 2', 'cierra sesión 2']
```

Con `yield`, la dependencia tiene dos mitades: lo de antes del `yield` se ejecuta antes de la ruta; lo de después, cuando la ruta ha terminado. Es un `with` repartido en el tiempo, y el `finally` cierra aunque la ruta falle. Cada petición tiene **la suya**: sesión 1, sesión 2. Así abrirá tu API una sesión de SQLAlchemy por petición.

### 3. Una dependencia que usa otra, una vez por petición

Descomenta el **PASO 3** y ejecuta:

```
--- Paso 3: dependencias encadenadas ---
{'user': 'ana', 'session': 'sesión 3'} -> ['abre sesión 3', 'get_user con sesión 3', 'cierra sesión 3']
```

`get_user` pide una sesión, y la ruta también. Pero solo se abre **una**: dentro de una petición, FastAPI guarda el resultado de cada dependencia y lo reutiliza. Por eso `get_user` y la ruta trabajan con la misma sesión, y lo que una escribe la otra lo ve.

### 4. Sustituir una dependencia en los tests

Descomenta el **PASO 4** y ejecuta:

```
--- Paso 4: dependency_overrides ---
/loads -> sesión de pruebas · ['la ruta usa sesión de pruebas']
/me    -> {'user': 'ana', 'session': 'sesión de pruebas'}
sin override -> sesión 4
```

`app.dependency_overrides[get_session] = ...` le dice a FastAPI: donde se pida `get_session`, llama a esta otra función. La ruta no cambia, ni `get_user`, que también recibe la sesión de pruebas. Es lo que harán los tests de tu proyecto: la sesión de `db_fixtures.py`, dentro de una transacción que se deshace (teoría 05). Con `clear()`, todo vuelve a ser como antes.

### 5. El lifespan: abrir al arrancar, cerrar al parar

Descomenta el **PASO 5** y ejecuta:

```
--- Paso 5: lifespan ---
  arranca: abro el motor (una vez)
  petición 1: motor de PostgreSQL
  petición 2: motor de PostgreSQL
  para: cierro el motor
  fuera del with: el motor ya está cerrado
```

Hay cosas que no se abren en cada petición: el **motor** de SQLAlchemy y su pool de conexiones se crean una vez y se reutilizan. El **lifespan** es un gestor de contexto: lo de antes del `yield` se ejecuta al arrancar el servidor, y lo de después al pararlo. Lo que guardas en `app.state` lo leen las rutas con `request.app.state`.

`TestClient(...)` dentro de un `with` arranca y para la aplicación como un servidor: ejecuta el lifespan. Sin `with`, no lo ejecuta.

### 6. `def` o `async def`

Descomenta el **PASO 6** y ejecuta:

```
--- Paso 6: cinco peticiones a la vez, de 0,2 s cada una ---
/def             0.20 s
/async-blocking  1.01 s
/async           0.20 s
```

Cinco peticiones a la vez, y cada ruta tarda 0,2 s:

- **`def`**: FastAPI la ejecuta en un **hilo** de su pool. `time.sleep` bloquea ese hilo, no los demás: las cinco a la vez, 0,2 s.
- **`async def` con `time.sleep`**: se ejecuta en el **bucle de eventos**, y `time.sleep` lo bloquea entero. Nadie más avanza: una detrás de otra, 1 s. Es el error más caro de una API.
- **`async def` con `await asyncio.sleep`**: espera devolviendo el control al bucle (semana 17), que atiende a las demás: 0,2 s.

La regla: `async def` solo si **todo** lo que hace por dentro espera con `await`. SQLAlchemy con su sesión normal bloquea, como `time.sleep`: por eso las rutas de tu proyecto son `def` (teoría 04). `httpx2.ASGITransport` llama a la aplicación sin red, como `TestClient`, pero desde código `async`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `AttributeError: 'State' object has no attribute 'engine'` | Usaste `TestClient(app_with_life)` sin `with`: el lifespan no se ejecutó |
| El paso 2 no apunta `cierra ...` | Falta el `finally`, o el `yield` está fuera del `try` |
| El paso 3 abre dos sesiones | Escribiste `Depends(get_session)` con una función distinta en cada lado: tiene que ser la misma |
| El override del paso 4 no se aplica | La clave tiene que ser la función original, `get_session`, no `SessionDep` |
| En el paso 6, `/def` tarda 1 s | Tu máquina tiene un solo núcleo libre o mucha carga: vuelve a ejecutar; lo que importa es la diferencia con `/async-blocking` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Cuerpos y respuestas con Pydantic](../ejercicio-02-cuerpos-y-respuestas-con-pydantic/README.md) | **Ejercicio 03 · Dependencias y ciclo de vida** | [Ejercicio 04 · Una API con PostgreSQL](../ejercicio-04-una-api-con-postgresql/README.md) |
