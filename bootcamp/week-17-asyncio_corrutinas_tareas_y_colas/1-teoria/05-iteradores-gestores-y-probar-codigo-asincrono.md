# 05 · Iteradores, gestores y probar código asíncrono

⏱️ 50 min

## 🎯 Objetivos

- Escribir un generador asíncrono y recorrerlo con `async for`.
- Escribir un gestor de contexto asíncrono, con una clase o con `@asynccontextmanager`.
- Anotar con mypy iteradores, generadores y funciones de aviso (*callbacks*).
- Probar corrutinas con pytest, sin plugins y sin depender del tiempo.
- Saber qué aportan `pytest-asyncio` y AnyIO, y cuándo usarlos.

---

## 1. Generadores asíncronos

En la semana 11, un generador daba valores de uno en uno con `yield`, a medida que se le pedían. Un **generador asíncrono** es lo mismo, pero puede esperar con `await` entre valor y valor:

```python
async def replay(lines: Iterable[str], *, interval: float = 0.0) -> AsyncIterator[Measurement]:
    for measurement in iter_measurements(lines):
        await asyncio.sleep(interval)
        yield measurement
```

Una función `async def` con `yield` es un generador asíncrono; sin `yield`, una corrutina. Se recorre con **`async for`**:

```python
async for measurement in replay(lines, interval=0.5):
    series.add(measurement)
```

Cada vuelta llama a `await anext(...)`. Mientras el generador espera su `asyncio.sleep`, el bucle atiende a otras tareas. Es exactamente lo que hace `vigilar`: cada archivo es un generador que suelta una medida cada `interval` segundos, y varios se recorren a la vez.

Las mismas herramientas que con iteradores normales, en versión asíncrona:

| Normal | Asíncrono |
|---|---|
| `for x in it:` | `async for x in it:` |
| `[x for x in it]` | `[x async for x in it]` (solo dentro de `async def`) |
| `next(it)` | `await anext(it)` |
| `__iter__` / `__next__` | `__aiter__` / `__anext__` |
| `generador.close()` | `await generador.aclose()` |
| `contextlib.closing` | `contextlib.aclosing` |

Si sales antes de terminar (un `break`, una excepción), el generador queda a medias. `asyncio.run` cierra al final los que queden abiertos, pero si el generador tiene un recurso (una conexión), ciérralo tú con `aclose` o con `async with aclosing(generador)`.

## 2. Gestores de contexto asíncronos

Un gestor de contexto asíncrono es uno cuya entrada o salida tienen que **esperar**: abrir una conexión, cerrar una sesión HTTP, devolver un permiso del semáforo. Tiene `__aenter__` y `__aexit__`, que son corrutinas, y se usa con `async with`:

```python
class Station:
    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *problem: object) -> None:
        await self.disconnect()
```

O, como en la semana 7, con un generador y un decorador:

```python
@asynccontextmanager
async def connected(name: str) -> AsyncIterator[Station]:
    station = await connect(name)
    try:
        yield station
    finally:
        await station.disconnect()
```

Ya has usado varios: `asyncio.TaskGroup()`, `asyncio.timeout(...)`, `Semaphore` y `Lock`. En la semana 18, `httpx.AsyncClient()` será otro.

## 3. Tipos

| Qué es | Anotación |
|---|---|
| Una función `async def` que devuelve `T` | `async def f() -> T`; llamarla da un `Coroutine[Any, Any, T]` |
| Algo que se puede recorrer con `async for` | `AsyncIterable[T]` |
| Un iterador asíncrono | `AsyncIterator[T]` |
| Un generador asíncrono, si usas `aclose` o `asend` | `AsyncGenerator[T]` |
| Una función de aviso que recibe una ruta y una medida | `Callable[[Path, Measurement], None]` |
| Una función de aviso que es una corrutina | `Callable[[Path, Measurement], Awaitable[None]]` |

Fíjate en el alias de tu proyecto, `OnReading = Callable[[Path, Measurement], None]`. Es una función **normal**: `watch_file` la llama sin `await`, y por eso tiene que ser rápida. Escribir una línea en la terminal lo es. Si un día hiciera falta guardar cada medida en una base de datos, el aviso tendría que ser una corrutina.

## 4. Probar corrutinas con pytest

pytest no ejecuta funciones `async def` por sí solo. Si escribes un test así, pytest no lo ejecuta y lo da por fallido con `Failed: async def functions are not natively supported.`, seguido de una lista de plugins que lo harían. La solución más sencilla, sin dependencias, es la de tu proyecto: un test **normal** que arranca el bucle.

```python
def test_watch_file_summarizes_like_report_file(write_file: WriteFile) -> None:
    path = write_file("a.txt", "Norte;10\nSur;NA\n")
    assert asyncio.run(watch_file(path)) == report_file(path)
```

Para un generador asíncrono, una corrutina auxiliar que lo recoja:

```python
async def collect(stream: AsyncIterator[Measurement]) -> list[Measurement]:
    return [measurement async for measurement in stream]


def test_replay_gives_the_valid_measurements() -> None:
    assert asyncio.run(collect(replay(["Norte;10", "basura"]))) == [Measurement("Norte", 10.0)]
```

Cada `asyncio.run` crea un bucle nuevo y lo cierra: un test no puede dejar tareas colgando para el siguiente.

## 5. Probar sin depender del tiempo

Las técnicas de la semana 16, en versión `asyncio`:

- **El orden de las tareas.** Con `asyncio.sleep(0)`, las tareas se turnan siempre igual. `test_replay_lets_other_tasks_run` comprueba que dos reproducciones se intercalan, `A1, B1, A2, B2...`: con un `time.sleep`, la primera iría entera antes.
- **Que corren a la vez.** Una `asyncio.Barrier(3)` solo se abre si tres tareas esperan en ella al mismo tiempo. Dentro de un `asyncio.timeout(5)`, para que, si falla, falle en 5 s en lugar de colgarse.
- **Cuántas a la vez.** Un contador `active` y su máximo `peak`, sin `Lock`, porque entre `active += 1` y `peak = max(...)` no hay ningún `await`.
- **Sustituir con `monkeypatch`.** `monkeypatch.setattr(live, "watch_file", falsa)` cambia la función que `watch_files` busca en su módulo. La falsa es otra corrutina que cede el turno o espera en la barrera.
- **Espiar el bucle.** `monkeypatch.setattr(asyncio, "sleep", espía)` apunta qué esperas se piden, sin esperar de verdad. El espía guarda el `asyncio.sleep` original para ceder el turno con él.

Y el tiempo, solo cuando es lo que se prueba, con margen: `vigilar -i 5 --tiempo 0.1` comprueba el plazo con un trabajo de segundos y un límite de una décima.

## 6. Plugins: `pytest-asyncio` y AnyIO

En un proyecto con muchos tests asíncronos, escribir `asyncio.run` en cada uno cansa. Dos plugins permiten escribir los tests directamente como `async def`:

- **`pytest-asyncio`** marca los tests con `@pytest.mark.asyncio` (o todos, con `asyncio_mode = "auto"` en la configuración) y ejecuta cada uno en un bucle. También permite *fixtures* asíncronas, por ejemplo un cliente HTTP abierto con `async with`.
- **AnyIO** trae su propio plugin de pytest (`@pytest.mark.anyio`). AnyIO es una capa sobre `asyncio` (y sobre Trio, otra biblioteca asíncrona) que usan httpx y FastAPI por debajo.

Tu proyecto no los necesita todavía: `asyncio.run` hace lo mismo con una línea, sin dependencias. Cuando lleguen las *fixtures* asíncronas, merecerá la pena.

## 7. Y las próximas semanas

`asyncio` es la base de lo que viene:

- **Semana 18**: `httpx.AsyncClient` hace peticiones HTTP con `await`. `vigilar` podrá consultar estaciones de verdad, con el mismo `TaskGroup`, el mismo `Semaphore` y el mismo `timeout`.
- **Semana 20**: FastAPI ejecuta cada petición como una corrutina en su propio bucle. Ahí no hay `asyncio.run`: el servidor ya lo arrancó, y tu código llamará a `watch_files` con `await`. Por eso `core` no tiene `asyncio.run`.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `TypeError: 'async_generator' object is not iterable` | Un `for` normal sobre un generador asíncrono | `async for`, dentro de `async def` |
| `TypeError: 'async for' requires an object with __aiter__ method, got coroutine` | La función `async def` no tiene `yield`: es una corrutina, no un generador | Añade el `yield`, o espérala con `await` |
| `SyntaxError: asynchronous comprehension outside of an asynchronous function` | `[x async for x in ...]` fuera de `async def` | Muévela a una corrutina |
| mypy: `"AsyncIterator[str]" has no attribute "aclose"` | La anotación es más general que el objeto | `AsyncGenerator[str]` |
| Un test `async def` sale como fallido sin ejecutarse | pytest no ejecuta corrutinas sin un plugin | Test normal con `asyncio.run`, o `pytest-asyncio` |
| Un test asíncrono se cuelga | Espera algo que nunca llega | Envuelve la espera del test en `asyncio.timeout` |

---

## ✅ Qué debes saber al terminar

- [ ] La diferencia entre una corrutina y un generador asíncrono, y cómo se recorre cada uno.
- [ ] Cuándo hace falta un gestor de contexto asíncrono, y las dos formas de escribirlo.
- [ ] Qué anotación lleva `replay`, `watch_file` y `on_reading`, y por qué.
- [ ] Cómo prueba tu proyecto sus corrutinas sin plugins.
- [ ] Las técnicas para probar orden, simultaneidad y límite sin medir tiempos.
- [ ] Qué aportan `pytest-asyncio` y AnyIO.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Coordinar tareas y no bloquear el bucle](04-coordinar-tareas-y-no-bloquear-el-bucle.md) | **05 · Iteradores, gestores y probar código asíncrono** | [Ejercicio 01 · Corrutinas y el bucle](../2-practicas/ejercicio-01-corrutinas-y-el-bucle/README.md) |
