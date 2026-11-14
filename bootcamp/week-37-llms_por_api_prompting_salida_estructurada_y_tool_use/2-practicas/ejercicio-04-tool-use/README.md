# Ejercicio 04 — Tool use

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-tool-use.md)

## Objetivo

Que Claude responda con **tus** datos, pidiendo que ejecutes tus funciones:

- cómo pide Claude una herramienta;
- ejecutarla tú y devolverle el resultado;
- el bucle, con varias herramientas a la vez;
- una herramienta que falla;
- un límite de vueltas;
- el *tool runner* del SDK.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-37-llms_por_api_prompting_salida_estructurada_y_tool_use/2-practicas/ejercicio-04-tool-use/starter
uv run python main.py
```

```
Ejercicio 04 · Tool use
```

Las respuestas salen de `respuestas.json` (de ejemplo); con tu clave, `CLAUDE_REAL=1`. Arriba de `main.py`:

- `READINGS` y `NOTES`: medidas de PM2.5 y notas de cinco estaciones, los datos que Claude no tiene;
- `statistics_of(label)` y `notes_of(label)`: las funciones de verdad; las dos lanzan `KeyError` con una estación que no existe;
- `TOOLS`: cómo se describen a Claude: un nombre, una descripción y un esquema JSON de la entrada, con `strict: True` (la entrada cumplirá el esquema);
- `FUNCTIONS`: de nombre de herramienta a función.

## Pasos

### 1. Claude pide una herramienta

Descomenta el **PASO 1** y ejecuta:

```
stop_reason: tool_use
texto: Consulto las estadísticas de Norte.
tool_use: estadisticas({'etiqueta': 'Norte'}) · id toolu_df80f62427ae0447b4b4a647
```

Claude no ejecuta nada: **pide**. Con `tools=TOOLS`, ve las dos descripciones; la pregunta necesita un dato que no tiene, y responde con `stop_reason: tool_use` y un bloque `tool_use`: qué herramienta, con qué entrada (que cumple el esquema) y un `id`.

### 2. Tú ejecutas la herramienta y devuelves el resultado

Descomenta el **PASO 2** y ejecuta:

```
resultado: {'etiqueta': 'Norte', 'n': 4, 'media': 44.0, 'minimo': 38.0, 'maximo': 52.5}
stop_reason: end_turn
La media de PM2.5 en Norte es 44.0 µg/m³, con 4 medidas entre 38.0 y 52.5.
```

Tu código ejecuta `statistics_of("Norte")` y hace una segunda petición con la conversación entera: la pregunta, la respuesta de Claude **tal cual** (con su bloque `tool_use`) y un mensaje `user` con un bloque `tool_result` que lleva el mismo `tool_use_id`. Ahora Claude tiene el dato, y contesta: `end_turn`.

### 3. El bucle

Descomenta el **PASO 3** y ejecuta:

```
vuelta 1: estadisticas(Norte)
vuelta 1: estadisticas(Sur)
vuelta 1: estadisticas(Centro)
vuelta 1: estadisticas(Este)
vuelta 1: estadisticas(Oeste)
vuelta 2: notas(Sur)
vuelta 3: Sur tiene la media más alta, 56.0 µg/m³. Sus notas: «La placa está quemada, se pidió un repuesto.» y «Se recalibró con gas de referencia.». Con la placa quemada, conviene comprobar si esas medidas son fiables antes de sacar conclusiones.
3 vueltas · 3055 tokens
```

`run` repite los pasos 1 y 2 mientras `stop_reason` sea `tool_use`. Claude decide el plan:

- en la vuelta 1 pide **cinco** herramientas a la vez: no depende una de otra. Todos los resultados vuelven en **un** mensaje;
- en la 2, ya sabe cuál es la más alta y pide sus notas;
- en la 3, contesta, y relaciona los dos datos (una placa quemada, una media alta) como no lo haría una consulta fija.

Cada vuelta reenvía la conversación entera: 3055 tokens para una pregunta.

### 4. Cuando la herramienta falla

Descomenta el **PASO 4** y ejecuta:

```
vuelta 1: estadisticas(Sureste) → error
vuelta 2: No tengo datos de Sureste: no hay estación Sureste; las estaciones son Norte, Sur, Centro, Este, Oeste. ¿Te refieres a alguna de ellas?
2 vueltas · 1321 tokens
```

`statistics_of("Sureste")` lanza `KeyError`. El bucle no se cae: devuelve un `tool_result` con el mensaje del error e `is_error: True`. Claude lo lee y se lo explica al usuario, con las estaciones que sí existen. Un mensaje de error útil (qué falló y qué vale) es parte del diseño de una herramienta.

### 5. Un límite de vueltas

Descomenta el **PASO 5** y ejecuta:

```
vuelta 1: estadisticas(Norte)
vuelta 1: estadisticas(Sur)
vuelta 1: estadisticas(Centro)
vuelta 1: estadisticas(Este)
vuelta 1: estadisticas(Oeste)
sin respuesta: límite de vueltas (1) · 637 tokens
```

La misma pregunta del paso 3 con `turns=1`. Un bucle sin límite puede encadenar herramientas sin fin y gastar tokens en cada vuelta: pon siempre un tope, y decide qué hacer al llegar (aquí, avisar).

### 6. El *tool runner* del SDK

Descomenta el **PASO 6** y ejecuta:

```
tool_use: ['text', 'tool_use']
end_turn: ['text']
La media de PM2.5 en Sur es 56.0 µg/m³, con 4 medidas entre 49.5 y 61.0.
```

`@beta_tool` lee el nombre, el docstring y los tipos de la función y crea la herramienta: el esquema sale de `etiqueta: str` y la descripción de `Args:`. `client.beta.messages.tool_runner(...)` hace el bucle del paso 3 por ti: cada mensaje del `for` es una vuelta. Es **beta**: su forma puede cambiar entre versiones del SDK. El bucle a mano es más largo, pero ves y controlas cada paso (los errores, el límite, qué se registra); en la semana 39, con agentes, verás cuándo conviene cada uno.

Para terminar, escribe en un comentario al final de `main.py` dos herramientas que darías a Claude en tu Observatorio, con su nombre, su descripción y su entrada. ¿Alguna cambia datos (borrar, guardar)? Entonces, ¿quién debería confirmarla antes de ejecutarla?

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `LookupError: respuestas.json no tiene esta petición` | Cambiaste una pregunta, una herramienta o un resultado: vuelve al código del paso, o pruébalo con tu clave y `CLAUDE_REAL=1` |
| `BadRequestError: 400 ... tool_use ids were found without tool_result blocks` | Cada `tool_use` necesita su `tool_result` con el mismo `tool_use_id`, todos en el mensaje siguiente |
| `BadRequestError: 400 ... tool_choice` con tu clave | Forzar una herramienta (`tool_choice` `any` o `tool`) no se admite en Sonnet 5.5: pídela en el prompt, con `tool_choice` `auto` |
| El bucle no termina con tu clave | Revisa que el límite (`turns`) está en el `for`, y que añades la respuesta de Claude antes de los resultados |
| `KeyError: 'etiqueta'` | La entrada no cumple el esquema: comprueba `"strict": True` y `required` en `label_schema` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Salida estructurada](../ejercicio-03-salida-estructurada/README.md) | **Ejercicio 04 · Tool use** | [Proyecto](../../3-proyecto/README.md) |
