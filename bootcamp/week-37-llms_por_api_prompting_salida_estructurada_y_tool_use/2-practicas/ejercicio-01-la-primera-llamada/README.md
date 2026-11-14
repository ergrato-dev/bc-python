# Ejercicio 01 — La primera llamada a Claude

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-que-es-un-llm-y-la-api.md)

## Objetivo

Hablar con Claude desde Python con la API de Messages y leer todo lo que devuelve:

- una pregunta y su respuesta;
- el identificador, el modelo, los bloques, `stop_reason` y los tokens;
- el prompt de sistema;
- por qué la API no recuerda nada;
- qué pasa cuando se acaba `max_tokens`;
- lo que cuesta, con tres modelos;
- los errores de la API.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-37-llms_por_api_prompting_salida_estructurada_y_tool_use/2-practicas/ejercicio-01-la-primera-llamada/starter
uv run python main.py
```

```
Ejercicio 01 · La primera llamada a Claude
modelo claude-sonnet-5-5 · respuestas grabadas
```

**No necesitas clave ni conexión.** Arriba de `main.py`, `make_client()` crea un cliente de Anthropic de verdad con un transporte HTTP falso, `Replay`: cada petición que haría el SDK se busca en `respuestas.json` y se responde con lo que hay guardado. Es la misma idea que `httpx.MockTransport` en los tests de `descargar` (semana 18).

Las respuestas de `respuestas.json` son **de ejemplo**: las escribimos para el bootcamp con la forma exacta de la API (los mismos campos, los mismos tipos), pero no las escribió Claude, y los tokens son aproximados. Con tu clave, verás respuestas de verdad, distintas en cada ejecución:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # la tuya, de console.anthropic.com
CLAUDE_REAL=1 uv run python main.py
```

Cuesta menos de un céntimo de dólar el ejercicio entero. No escribas la clave en `main.py` ni la subas a Git (teoría 01, sección 6).

## Pasos

### 1. Una pregunta, una respuesta

Descomenta el **PASO 1** y ejecuta:

```
Un sensor de calidad del aire es un dispositivo que mide la concentración de contaminantes, como partículas finas, ozono o dióxido de nitrógeno, en el aire que lo rodea.
```

`client.messages.create` envía una petición `POST /v1/messages` con tres cosas obligatorias:

- `model`: qué modelo responde, `claude-sonnet-5-5`;
- `max_tokens`: cuántos tokens puede escribir como mucho;
- `messages`: la conversación, una lista de mensajes con `role` y `content`.

La respuesta no es un texto: es una lista de bloques. `response.content[0].text` es el texto del primero.

### 2. Lo que trae la respuesta

Descomenta el **PASO 2** y ejecuta:

```
id msg_2d2bc052cb57790cef9bc96c · modelo claude-sonnet-5-5
bloques: ['text']
stop_reason: end_turn
tokens: 30 de entrada, 54 de salida
```

- **`id`**: el identificador de la respuesta. Si algo falla, es lo que pide el soporte de Anthropic.
- **`content`**: una lista de bloques; aquí, uno de texto. Con herramientas habrá bloques `tool_use` (ejercicio 04).
- **`stop_reason`**: por qué paró. `end_turn`, terminó; `max_tokens`, se le acabó el espacio (paso 5); `tool_use`, pide una herramienta; `refusal`, no quiere responder.
- **`usage`**: los tokens de entrada (lo que enviaste) y de salida (lo que escribió). Es lo que pagas.

### 3. El prompt de sistema

Descomenta el **PASO 3** y ejecuta:

```
Mide contaminantes del aire, como partículas u ozono, para saber si es sano.
tokens: 53 de entrada, 26 de salida
```

`system` dice quién responde, a quién y cómo; el mensaje, qué se pregunta. La misma pregunta, con un sistema que pide 15 palabras, da una respuesta corta. Más tokens de entrada (el sistema también se cuenta), menos de salida: aquí sale más barata.

### 4. La API no recuerda nada

Descomenta el **PASO 4** y ejecuta:

```
sin historia: ¿Qué equipo quieres calibrar? Dímelo y te digo cada cuánto.
con historia: Según el fabricante; lo habitual, cada tres a seis meses y tras cada reparación.
tokens de entrada: 46 sin historia, 104 con historia
```

"¿Y cada cuánto se calibra?" sola no dice de qué se habla. Cada petición empieza de cero: para que Claude sepa de qué hablabais, la petición lleva la **conversación entera**, tus mensajes (`user`) y sus respuestas (`assistant`), alternados. Por eso una conversación larga cuesta cada vez más: la historia se paga en cada petición.

### 5. Cuando se acaba `max_tokens`

Descomenta el **PASO 5** y ejecuta:

```
stop_reason: max_tokens · 20 tokens de salida
texto: Un sensor de calidad del aire es un dispositivo que mide la concentración de contaminantes
```

Con `max_tokens=20`, la frase se corta a la mitad y **no hay ningún error**: la respuesta llega con `stop_reason: max_tokens`. Si tu código no lo mira, usará medio texto como si fuera una respuesta. En el ejercicio 03 y en el proyecto, una respuesta cortada no se lee.

### 6. Lo que cuesta

Descomenta el **PASO 6** y ejecuta:

```
  claude-haiku-5-5 · una respuesta como la del paso 1: 0.000030 $ · mil al día, 30 días: 0.90 $
 claude-sonnet-5-5 · una respuesta como la del paso 1: 0.000600 $ · mil al día, 30 días: 18.00 $
   claude-opus-5-5 · una respuesta como la del paso 1: 0.001200 $ · mil al día, 30 días: 36.00 $
```

El precio va por millón de tokens, distinto para entrada y salida (la salida cuesta cinco veces más). Una respuesta no cuesta casi nada; un millón de respuestas, sí. Entre el modelo más barato y el más caro hay 40 veces de diferencia: elegir el modelo es una decisión de coste, no solo de calidad (teoría 01, sección 4). Los precios son los del 2026-11-13; cambian, mira la página de precios antes de calcular.

### 7. Cuando algo falla

Descomenta el **PASO 7** y ejecuta:

```
NotFoundError 404: model: claude-sonnet-9
BadRequestError 400: messages: at least one message is required
```

El SDK convierte cada error HTTP en una excepción con su tipo: `NotFoundError` (404, un modelo que no existe), `BadRequestError` (400, una petición mal formada), `AuthenticationError` (401, la clave), `RateLimitError` (429, demasiadas peticiones) o `APIStatusError` (los demás). Los 429 y los 5xx los reintenta él solo, dos veces, con espera; los 400 no: repetirlos daría lo mismo.

Para terminar, escribe en un comentario al final de `main.py`: si tu Observatorio leyera con Claude las notas de tu dominio, ¿cuántas al día serían?, ¿cuánto costaría al mes con cada modelo?

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `LookupError: respuestas.json no tiene esta petición` | Cambiaste algo de la petición (el texto, `max_tokens`, el modelo): vuelve al código del paso, o pruébalo con tu clave y `CLAUDE_REAL=1` |
| `FileNotFoundError: respuestas.json` | Ejecuta desde `starter/`, donde está `respuestas.json` |
| `TypeError: Could not resolve authentication method` | Con `CLAUDE_REAL=1` hace falta `ANTHROPIC_API_KEY`: `export ANTHROPIC_API_KEY=...` |
| `AuthenticationError: 401` | La clave no es válida o se revocó: crea otra en la consola de Anthropic |
| Con tu clave, las respuestas no coinciden con el README | Es lo esperado: un modelo no responde dos veces igual. Compara la forma (bloques, `stop_reason`, tokens), no las palabras |
| `NameError: name 'response' is not defined` | Descomentaste un paso sin el anterior: los pasos usan lo de los anteriores |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Claude en tu Observatorio](../../1-teoria/05-claude-en-tu-observatorio.md) | **Ejercicio 01 · La primera llamada** | [Ejercicio 02 · Prompting](../ejercicio-02-prompting/README.md) |
