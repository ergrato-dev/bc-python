# Ejercicio 03 — Reintentos con espera

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-reintentos-y-espera-exponencial.md)

## Objetivo

Escribir, paso a paso, el bucle de reintentos de tu proyecto, y ver por qué es así:

- un fallo que se arregla solo si repites la petición;
- reintentar sin esperar, y por qué no basta;
- la espera exponencial y cuánto suma;
- qué se reintenta y qué no: un `404` no, un fallo de conexión sí;
- la variación aleatoria (*jitter*) y la cabecera `Retry-After`;
- un tope de tiempo total, y lo que trae httpx de serie.

La función `fetch` del paso 4 es casi la `get_text` de tu proyecto. Las peticiones van al servidor de prueba de `servidor.py`, como en los ejercicios anteriores. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-18-http_con_httpx_reintentos_secretos_y_env/2-practicas/ejercicio-03-reintentos-con-espera/starter
uv run python main.py
```

```
Ejercicio 03 · Reintentos con espera
```

La ruta `/inestable?id=X&fallos=N` contesta `503` las primeras `N` veces que le pides ese `id`, y `200` a partir de ahí. Cada paso usa un `id` distinto, para que no se pisen.

## Pasos

### 1. Un fallo pasajero

Descomenta el **PASO 1** y ejecuta:

```
503 {'error': 'servidor saturado'}
503 {'error': 'servidor saturado'}
200 {'intentos': 3}
```

La misma petición, tres veces: falla, falla y sale bien. Es lo que pasa con un servidor que se está reiniciando o que está saturado un momento. Si tu programa se rindiera al primer `503`, perdería una descarga que a la tercera habría salido.

### 2. Reintentar sin esperar

Descomenta el **PASO 2** y ejecuta:

```
  intento 1: 503
  intento 2: 503
  intento 3: 200
sin espera: 200 en 0.10 s
```

Funciona, y rápido. Pero piensa en lo que ha visto el servidor: tres peticiones en una décima de segundo, justo cuando estaba saturado. Si el problema dura un poco más que tus tres intentos, te rindes igual, después de haberlo empeorado. Y si hay cien clientes haciendo lo mismo, el servidor recibe trescientas peticiones en vez de cien.

### 3. Espera exponencial

Descomenta el **PASO 3** y ejecuta:

```
  intento 1: 503
  espera 0.2 s
  intento 2: 503
  espera 0.4 s
  intento 3: 503
  espera 0.8 s
  intento 4: 200
con espera: 200 en 1.4 s
```

Antes de cada **reintento** (no antes del primer intento), una espera que se dobla: `backoff * 2 ** (attempt - 1)`. Las esperas suman 0,2 + 0,4 + 0,8 = 1,4 s, y eso es lo que tardó. Con el `backoff` de tu proyecto, 0,5, serían 0,5 + 1 + 2 = 3,5 s.

El servidor tiene tiempo para recuperarse, y tú no esperas de más: un fallo corto se arregla en el primer reintento, con solo 0,2 s de espera. La espera es `await asyncio.sleep`: si hubiera otras descargas, seguirían mientras esta espera.

### 4. Qué se reintenta y qué no

Descomenta el **PASO 4** y ejecuta:

```
404 · 0.0 s
FetchError: http://127.0.0.1:9/estaciones: ConnectError tras 4 intentos · 1.4 s
```

`fetch` es el bucle completo, con las dos clases de error de la teoría 02:

- **hubo respuesta**: si su código no está en `RETRY_STATUSES`, se devuelve tal cual, sin reintentar. El `404` sale al momento, porque repetir la petición daría lo mismo;
- **no hubo respuesta** (`httpx.TransportError`): se reintenta. En el puerto 9 no escucha nadie, así que los cuatro intentos fallan, y después de 1,4 s de esperas, `FetchError` cuenta qué pasó la última vez y cuántas veces se intentó.

`failure` guarda el último fallo para el mensaje. Tu proyecto hace lo mismo, y además convierte en `FetchError` cualquier otro error HTTP (el `404`), porque para `download` también es un fallo.

### 5. Variación aleatoria (*jitter*)

Descomenta el **PASO 5** y ejecuta:

```
reintento 1: todos a 0.2 s · con jitter [0.04, 0.04, 0.07, 0.1, 0.13]
reintento 2: todos a 0.4 s · con jitter [0.1, 0.11, 0.18, 0.19, 0.2]
reintento 3: todos a 0.8 s · con jitter [0.26, 0.54, 0.55, 0.63, 0.69]
```

Cinco clientes que fallaron a la vez. Sin *jitter*, los cinco vuelven exactamente a la vez en cada reintento, y el servidor recibe otra vez el mismo golpe. Con `random.uniform(0, delay)` (*full jitter*), cada uno espera un tiempo distinto entre 0 y la espera calculada: las peticiones llegan repartidas.

`random.seed(18)` hace que los números "aleatorios" sean siempre los mismos, para que tu salida coincida con esta. En un programa real, no lo pongas.

### 6. `Retry-After`

Descomenta el **PASO 6** y ejecuta:

```
  429: el servidor pide esperar 1 s
200 en 1.0 s
```

`/cuota` contesta `429 Too Many Requests` con la cabecera `Retry-After: 1`: el servidor te dice **exactamente** cuánto esperar. Un cliente educado le hace caso, en lugar de su propio cálculo. El `min(..., 5.0)` pone un máximo, para que un servidor que pide `Retry-After: 3600` no te deje colgado una hora.

`Retry-After` también puede llevar una fecha (`Wed, 21 Oct 2026 07:28:00 GMT`). Con este código, `float(...)` fallaría con un `ValueError`; para tratarla, `email.utils.parsedate_to_datetime` la convierte.

### 7. Un tope de tiempo total

Descomenta el **PASO 7** y ejecuta:

```
tiempo total agotado: 1.0 s
```

Con `retries=10`, las esperas serían 0,2 + 0,4 + 0,8 + 1,6 + ... más de tres minutos. Un tope de intentos no basta si cada espera crece tanto: `asyncio.timeout(1.0)` corta todo el conjunto, esperas incluidas, al segundo. Es lo que harías si `descargar` tuviera un `--tiempo`, como `vigilar`.

### 8. Los reintentos que trae httpx

Descomenta el **PASO 8** y ejecuta:

```
sin servidor: ConnectError en 0.5 s
un 503: 503 sin reintentar
```

`httpx.AsyncHTTPTransport(retries=2)` reintenta, con su propia espera exponencial (0 s y 0,5 s), **solo** cuando falla la conexión: dos reintentos y, al final, el `ConnectError`. Pero en cuanto la conexión se abre, no reintenta nada: el `503` llega tal cual. Para los `5xx`, los `429` y los `ReadTimeout` necesitas tu propio bucle, como el del paso 4.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| El paso 3 espera antes del intento 1 | Te falta el `if attempt > 0:` |
| El paso 3 tarda 0,1 s | Escribiste `asyncio.sleep(delay)` sin `await`: Python avisa con `RuntimeWarning: coroutine 'sleep' was never awaited` |
| El paso 4 tarda 1,4 s con el `404` | Reintentas todos los errores: comprueba `not in RETRY_STATUSES` |
| El paso 4 da `httpx.ConnectError` sin `FetchError` | El `except` captura otra clase: tiene que ser `httpx.TransportError` |
| El paso 5 da otros números | Falta `random.seed(18)`, o lo moviste dentro del bucle |
| El paso 7 tarda más de 1 s | El `asyncio.timeout(1.0)` no envuelve la llamada a `fetch` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Cliente asíncrono y concurrencia](../ejercicio-02-cliente-asincrono-y-concurrencia/README.md) | **Ejercicio 03 · Reintentos con espera** | [Ejercicio 04 · Secretos y configuración](../ejercicio-04-secretos-y-configuracion/README.md) |
