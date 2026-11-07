# 05 · Probar clientes HTTP y validar lo que llega

⏱️ 50 min

## 🎯 Objetivos

- Probar código que hace peticiones sin salir a Internet.
- Responder con `httpx.MockTransport` y comprobar qué peticiones se hicieron.
- Levantar un servidor de verdad en `127.0.0.1` dentro de un test.
- Probar reintentos y esperas sin esperar.
- Tratar lo que llega por la red como datos que no son de fiar, y pedirlo con educación.

---

## 1. Por qué los tests no salen a Internet

Un test que pide datos a un servidor de verdad:

- **falla sin que tu código cambie**: el servidor está caído, la red de la cafetería no funciona, la API cambió un campo;
- es **lento**: cada petición, decenas o cientos de milisegundos;
- no puede probar **los fallos**: no puedes pedirle a una API real que te dé un `503` justo ahora;
- **gasta** tu cuota y, si lleva token, lo expone en tu máquina de CI.

La regla: los tests de tu proyecto **no salen de tu máquina**. Hay dos formas de conseguirlo, y tu proyecto usa las dos.

## 2. `httpx.MockTransport`: respuestas sin red

Por dentro, un cliente de httpx tiene un **transporte**: la pieza que de verdad abre conexiones y manda bytes. `MockTransport` es un transporte falso, que en lugar de usar la red llama a **tu función** con la petición y devuelve lo que ella devuelva:

```python
def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/norte.json":
        return httpx.Response(200, json=[{"label": "Norte", "value": 10}])
    return httpx.Response(404)


transport = httpx.MockTransport(handler)
async with make_client(transport=transport) as client:
    text = await get_text(client, "http://estaciones.test/norte.json")
```

Con eso pruebas todo: el código de estado (`httpx.Response(503)`), el cuerpo (`json=`, `text=`), las cabeceras (`headers={"Retry-After": "2"}`) y los fallos de red, **lanzando** la excepción desde el *handler*:

```python
def handler(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("fallo de prueba", request=request)
```

Y como el *handler* recibe la petición, puedes **guardarla** y comprobar qué mandó tu código: la URL, el `User-Agent`, el `Authorization`. Los tests de tu proyecto usan una pequeña fábrica, `replies(...)`, que contesta en orden con una lista de respuestas y apunta cada petición: `replies(httpx.Response(503), httpx.Response(200))` es "falla una vez y después va bien".

El *handler* también puede ser una corrutina (`async def`). Así se prueba la concurrencia, con lo que ya conoces de la semana 17: una `asyncio.Barrier` que solo se abre si tres descargas esperan a la vez, o un contador `active` con su máximo.

Para que esto funcione, tu código tiene que **dejar cambiar el transporte**. Por eso `make_client` tiene un parámetro `transport`, que fuera de los tests nadie usa. Es una costura (*seam*): un punto por donde el test entra sin tocar el resto.

## 3. Un servidor de verdad, en `127.0.0.1`

`MockTransport` no prueba que tu código hable HTTP de verdad: no hay conexión, ni cabeceras en bytes, ni redirecciones del sistema operativo. Para eso, un servidor **real** en tu máquina. La biblioteca estándar trae uno:

```bash
uv run python -m http.server 8000 --bind 127.0.0.1 --directory datos
```

sirve los archivos de `datos/` en `http://127.0.0.1:8000/`. Es el que usarás en el proyecto para probar `descargar` a mano. Dentro de un test, lo arrancas en un hilo:

```python
httpd = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=web))
Thread(target=httpd.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{httpd.server_address[1]}"
...
httpd.shutdown()
```

El puerto `0` le pide al sistema uno libre: dos tests a la vez no chocan. `127.0.0.1` no sale de tu máquina, así que funciona sin red, también en Docker. Úsalo para pocos tests: los que comprueban que todo encaja de verdad. Los casos raros, con `MockTransport`.

`http.server` es **solo para pruebas**: la documentación de Python avisa de que no es seguro para producción.

## 4. Probar los reintentos sin esperar

Tus reintentos esperan 0,5 + 1 + 2 s. Diez tests de reintentos serían más de medio minuto. La técnica es la de la semana 17: cambiar `asyncio.sleep` por un **espía** que apunta cuánto le pidieron esperar y cede el turno sin esperar:

```python
@pytest.fixture
def waits(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    asked: list[float] = []
    real_sleep = asyncio.sleep

    async def spy(delay: float) -> None:
        asked.append(delay)
        await real_sleep(0)

    monkeypatch.setattr(asyncio, "sleep", spy)
    return asked
```

Ahora un test comprueba **las esperas exactas**, sin esperar ninguna: `assert waits == [0.5, 1.0, 2.0]`. Y otro, que un `404` no espera nada: `assert waits == []`.

## 5. Probar la CLI sin red y sin tus variables

El comando `descargar` crea su propio cliente con `make_client`. El test lo sustituye con `monkeypatch.setattr(cli, "make_client", falso)`, donde `falso` llama al de verdad con un `MockTransport`. Funciona porque `cli.py` busca `make_client` en su módulo cada vez que lo llama, como `live.watch_file` en la semana 17.

Y hay algo nuevo: tu máquina tiene **su** configuración. Si exportaste `OBSERVATORIO_TOKEN`, o tienes un `.env` en la carpeta, los tests lo leerían. La *fixture* `clean_env` lo evita: cambia a una carpeta temporal vacía (sin `.env`) y borra las variables `OBSERVATORIO_*` con `monkeypatch.delenv`. Cada test pone las suyas con `monkeypatch.setenv`, y `monkeypatch` las deshace al terminar.

Y un test comprueba lo más importante de la teoría 04: con `-v` y un token, **el token no aparece** en ninguna salida ni en el registro.

## 6. Lo que llega no es de fiar

Un servidor que no es tuyo puede mandarte cualquier cosa: un campo de menos, un texto donde iba un número, una página HTML de mantenimiento con `200`, un archivo de 2 GB. Tu código trata la respuesta como **datos externos**, igual que un archivo que te mandó otra persona (semana 13):

- **valida** antes de usar: `parse_measurements` pasa el texto por `MeasurementIn`. Si no valida, la descarga es un error, y **no se guarda** nada a medias;
- **no ejecutes** nada de lo que llega: nunca `eval`, nunca `pickle.loads` de datos de la red;
- **no confíes en los nombres**: tu Observatorio guarda cada descarga como `<nombre>.txt` usando solo el último trozo de la ruta de la URL (`PurePosixPath(...).stem`). Una URL como `http://x/../../etc/passwd` da `passwd.txt` dentro de tu carpeta, no un archivo fuera de ella;
- **limita el tamaño** si la fuente no es tuya: httpx descarga el cuerpo entero en memoria con `.text`. Para archivos grandes, `client.stream(...)` y leer por trozos. No lo necesitas con unas pocas medidas.

## 7. Pedir con educación

Una API pública es de alguien que paga el servidor. Un buen cliente:

- se **identifica** con su `User-Agent` (`observatorio/0.18.0`), para que el dueño sepa quién pide;
- tiene un **límite de peticiones a la vez** (`--limite`) y respeta `429` y `Retry-After`;
- **reintenta con espera**, nunca en bucle cerrado;
- **lee los términos de uso**: algunos datos abiertos piden citar la fuente, otros prohíben descargas masivas;
- **no pide lo que ya tiene**: si vas a usar los mismos datos muchas veces, descárgalos una vez y trabaja con el archivo. Es exactamente lo que hace `descargar`.

## 8. Otras herramientas

| Herramienta | Qué hace | ¿Cuándo? |
|---|---|---|
| `respx` | Simula respuestas de httpx con reglas por URL y método | Muchos tests con muchas rutas |
| `pytest-httpx` | Una *fixture* que intercepta todas las peticiones de httpx | Igual, al estilo pytest |
| VCR (`vcrpy`, `pytest-recording`) | Graba respuestas reales una vez y las reproduce | Probar contra la forma real de una API compleja |

`MockTransport` viene con httpx y te basta para este proyecto: es una función, sin magia que aprender.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| Un test pasa en tu máquina y falla en CI | Lee tu `.env` o tus variables | Una *fixture* como `clean_env`, con `monkeypatch.chdir` y `delenv` |
| Un test de reintentos tarda segundos | Espera de verdad | Espía `asyncio.sleep` |
| `httpx.ConnectError` en un test | El test salió a la red de verdad | Pasa un `MockTransport`, o arranca el servidor en `127.0.0.1` |
| Un test se queda colgado | El *handler* espera algo que nunca llega | Envuelve la espera en `asyncio.timeout(5)` |
| `OSError: [Errno 98] Address already in use` | Un puerto fijo que otro proceso ya usa | Puerto `0` y lee `server_address` |

---

## ✅ Qué debes saber al terminar

- [ ] Por qué los tests no salen a Internet.
- [ ] Cómo responder y comprobar peticiones con `MockTransport`, incluidos los fallos de red.
- [ ] Para qué sirve el parámetro `transport` de `make_client`.
- [ ] Cuándo usar un servidor de verdad en `127.0.0.1`, y cómo arrancarlo en un test.
- [ ] Cómo probar los reintentos sin esperar.
- [ ] Por qué los tests de la CLI empiezan con `clean_env`.
- [ ] Qué haces con lo que llega de un servidor que no es tuyo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Secretos y configuración con `.env`](04-secretos-y-configuracion-con-env.md) | **05 · Probar clientes HTTP y validar lo que llega** | [Ejercicio 01 · Peticiones con httpx](../2-practicas/ejercicio-01-peticiones-con-httpx/README.md) |
