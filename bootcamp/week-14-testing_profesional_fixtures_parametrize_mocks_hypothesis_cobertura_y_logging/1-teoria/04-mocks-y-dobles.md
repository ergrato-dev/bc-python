# 04 · Mocks y dobles

⏱️ 45 min

## 🎯 Objetivos

- Saber cuándo un test necesita un doble y cuándo no.
- Usar `Mock`: `return_value`, `side_effect` y las comprobaciones `assert_called_*`.
- Parchear con `patch` en el sitio correcto.
- Evitar dobles que mienten con `autospec`.
- Elegir entre `patch`, `monkeypatch` e inyectar la dependencia.

---

## 1. Lo que un test no controla

Un buen test es rápido, da siempre el mismo resultado y no depende del equipo en el que se ejecuta. Algunas cosas lo impiden:

| Qué | Problema en un test |
|---|---|
| La red: una API, un servicio web | Lenta, puede no estar, y responde distinto cada día |
| El reloj: `datetime.now()` | El resultado cambia cada minuto |
| El azar: `random` | Distinto en cada ejecución |
| Fallos del sistema: disco lleno, sin permiso | No se pueden provocar a voluntad en todos los equipos |

Para esos casos, el test sustituye la pieza real por un **doble**: un objeto que se comporta como ella, pero que controla el test. "Mock" es el nombre que se usa para casi todos, aunque hay varias clases:

| Doble | Qué hace | Ejemplo |
|---|---|---|
| *Stub* | Devuelve una respuesta fija | Un `urlopen` falso que siempre da `{"value": 12.5}` |
| *Fake* | Funciona de verdad, pero de forma simple | Un `BytesIO` en lugar de un archivo; una lista en lugar de una base de datos |
| *Mock* | Además, apunta cómo lo llamaron, para comprobarlo después | `fake.assert_called_once_with(url, timeout=5)` |

## 2. `Mock`

`unittest.mock` viene con Python. Un `Mock` acepta cualquier llamada y cualquier atributo:

```python
from unittest.mock import Mock

fake = Mock(return_value=12.5)
fake("Norte")                         # 12.5
fake.assert_called_once_with("Norte") # pasa
fake.call_args.args                   # ('Norte',)
fake.anything.at_all()                # otro Mock: se lo inventa
```

`return_value` es lo que devuelve al llamarlo. `side_effect` cambia ese comportamiento:

| `side_effect=` | Al llamarlo |
|---|---|
| Una excepción: `URLError("sin red")` | La lanza |
| Una lista: `[1.0, 2.0]` | Devuelve el primero, luego el segundo, luego `StopIteration` |
| Una función | La llama con los mismos argumentos y devuelve lo que ella devuelva |

Las comprobaciones más útiles: `assert_called_once_with(...)`, `assert_called_once()`, `assert_not_called()` y `call_count`. Un `MagicMock` es un `Mock` que además sabe hacer de contenedor, de iterador y de gestor de contexto (`with`).

## 3. `patch`: dónde se parchea

`patch("modulo.nombre", ...)` cambia `nombre` dentro de `modulo` por un `Mock` mientras dura el `with`, y lo deja como estaba al salir:

```python
from unittest.mock import patch

with patch("weather.urlopen", return_value=response('{"value": "12.5"}')) as fake:
    assert fetch_reading("Norte") == 12.5
fake.assert_called_once_with("http://observatorio.invalid/api/Norte", timeout=5)
```

La regla más importante: **parchea donde se usa, no donde se define**. `weather.py` hace `from urllib.request import urlopen`, y eso crea en `weather` un nombre `urlopen` propio que apunta a la función. Parchear `urllib.request.urlopen` cambia el original, pero `weather.urlopen` sigue apuntando a la función real. El test hace una petición de verdad.

| `weather.py` hace | Parchea |
|---|---|
| `from urllib.request import urlopen` | `"weather.urlopen"` |
| `import urllib.request` y llama a `urllib.request.urlopen(...)` | `"urllib.request.urlopen"` |

`patch.object(objeto, "atributo", ...)` parchea un atributo de un objeto que ya tienes, sin escribir su ruta como texto. Tu proyecto lo usa con una clase:

```python
with mock.patch.object(Path, "open", side_effect=PermissionError(13, "Permission denied")):
    ...
```

Mientras dura, **cualquier** `Path.open` lanza `PermissionError`, como si el sistema operativo negara el permiso. Así se prueba el `except PermissionError` de `read_lines` en cualquier equipo. Con `chmod 000` no valdría: `root`, que es como se ejecutan muchos contenedores, lee igual.

## 4. `autospec`: dobles que no mienten

Un `Mock` acepta cualquier cosa, y eso es un peligro: si mañana `fetch_reading` pasa a pedir dos argumentos, el `Mock` seguirá aceptando uno y el test seguirá en verde.

```python
loose = Mock(return_value=12.5)
loose("Norte", "Sur", 3)                 # 12.5: no sabe nada del original

strict = create_autospec(fetch_reading, return_value=12.5)
strict("Norte", "Sur", 3)                # TypeError: too many positional arguments
```

`create_autospec`, o `patch(..., autospec=True)`, copia la firma del original: los argumentos, y en una clase, los métodos y atributos. Tu proyecto lo usa para espiar `write_json` desde `main`:

```python
with mock.patch.object(entry, "write_json", autospec=True) as fake:
    assert entry.main(["-f", str(path), "-j", str(output)]) == 0
fake.assert_called_once()
data, where = fake.call_args.args
```

El test comprueba qué recibió `write_json` sin escribir ningún archivo.

## 5. `monkeypatch` y la inyección

Para un doble sencillo no hace falta `Mock`. La fixture `monkeypatch` de pytest cambia un atributo por cualquier cosa y lo deshace al terminar el test:

```python
def test_fetch_reading_with_monkeypatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(weather, "urlopen", lambda url, timeout: response('{"value": 8}'))
    assert fetch_reading("Sur") == 8.0
```

Y muchas veces lo mejor es no parchear nada: **inyectar** la dependencia, es decir, recibirla como parámetro.

```python
def stamp(value: float, now: Callable[[], datetime] = lambda: datetime.now(UTC)) -> str:
    return f"{value} a las {now():%H:%M}"


def test_stamp() -> None:
    assert stamp(12.5, now=lambda: datetime(2026, 11, 6, 8, 30)) == "12.5 a las 08:30"
```

Es lo que hace tu `main` desde la semana 3: recibe `argv` como parámetro en lugar de leer `sys.argv`, y por eso sus tests no parchean nada. El `Source` de la semana 10 es la misma idea: `main` no sabe si las líneas vienen de un archivo o de una lista.

| Herramienta | Cuándo |
|---|---|
| Inyectar la dependencia | Código tuyo que puedes diseñar así: lo más simple de probar |
| `monkeypatch.setattr` | Un doble simple en código que no recibe la dependencia |
| `patch` / `patch.object` | Hace falta `side_effect`, contar llamadas o `autospec` |

## 6. No abuses

Un mock prueba que tu código **llama** a algo, no que funcione. Un test lleno de mocks se rompe cada vez que reorganizas el código, aunque el comportamiento no cambie, y puede pasar con un programa roto.

- Usa dobles para lo que no controlas: red, reloj, azar, fallos del sistema.
- **No** los uses para tu propia lógica: si para probar `median` parcheas `sorted`, no estás probando `median`.
- Un archivo de verdad en `tmp_path` es mejor que un mock de `open`, salvo para provocar un fallo imposible.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| El test hace una petición de verdad o lee un archivo real | El parche está donde se define el nombre, no donde se usa | `patch("tu_modulo.nombre")` |
| `TypeError: cannot set 'now' attribute of immutable type 'datetime.datetime'` | `patch("datetime.datetime.now")` | Parchea el nombre `datetime` del módulo que lo usa, o inyecta el reloj |
| El test sigue en verde tras cambiar la firma de la función | Un `Mock` sin `autospec` acepta cualquier llamada | `autospec=True` |
| `AttributeError: 'assert_called_once_wiht' is not a valid assertion` | Una errata en una comprobación | Corrígela: Python rechaza los nombres raros que empiezan por `assert` |
| Un parche "se queda" en otros tests | Se aplicó sin `with` ni fixture | Usa siempre `with patch(...)` o `monkeypatch`, que deshacen el cambio |

---

## ✅ Qué debes saber al terminar

- [ ] Qué partes de un programa conviene sustituir por un doble y cuáles no.
- [ ] Qué hacen `return_value` y `side_effect`.
- [ ] Por qué se parchea donde se usa el nombre y no donde se define.
- [ ] Qué evita `autospec`.
- [ ] Por qué inyectar una dependencia ahorra el mock.
- [ ] Por qué el permiso de lectura se prueba con un mock y no con `chmod`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Hypothesis](03-hypothesis.md) | **04 · Mocks y dobles** | [05 · Cobertura y logging](05-cobertura-y-logging.md) |
