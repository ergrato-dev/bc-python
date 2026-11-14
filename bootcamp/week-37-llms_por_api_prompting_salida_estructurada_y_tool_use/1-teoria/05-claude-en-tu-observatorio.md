# 05 · Claude en tu Observatorio

⏱️ 45 min

## 🎯 Objetivos

- Entender qué hace `leer-notas` y qué compara.
- Conocer `core/llm.py`: el esquema, el prompt, el reparto, las lecturas y el coste.
- Grabar las respuestas de la API y repetirlas sin red ni clave.
- Probar código que llama a una API de pago sin llamarla nunca.
- Leer la salida con la grabación de ejemplo, sin sacar de ella lo que no dice.

---

## 1. Lo que añade la semana

En la semana 36, `clasificar` entrenó dos modelos con 180 de tus notas y los midió con 60. Esta semana, `leer-notas` pide a Claude que lea **las mismas 60** notas de prueba, sin entrenar nada:

```bash
uv run observatorio leer-notas notas.csv
```

Por cada nota, una petición con salida estructurada: el tipo (uno de los de tus notas), si es urgente y un resumen de 12 palabras. El comando cuenta los aciertos, enseña las notas que falla y suma los tokens y su coste.

| Opción | Qué hace |
|---|---|
| `--ejemplos N` | N notas de ejemplo de cada tipo en el prompt, sacadas de las que **no** son de prueba |
| `--semilla` | La del reparto: con la misma que `clasificar`, las mismas notas de prueba |
| `--grabacion ARCHIVO` | Repite las respuestas guardadas en ese JSON: sin red ni clave |
| `--grabar` | Llama a la API de verdad y guarda las respuestas en `--grabacion` |
| `--nota TEXTO` | Lee una nota nueva; se puede repetir |

## 2. `core/llm.py`

| Pieza | Qué hace |
|---|---|
| `MODEL`, `MAX_TOKENS`, `EFFORT`, `PRICES` | `claude-sonnet-5-5`, 1024, `low`, y sus precios del 2026-11-13 |
| `schema(classes)` | La clase de Pydantic de una lectura, creada con `create_model`: `tipo` es un `Literal` con **tus** tipos |
| `instructions(classes, examples)` | El prompt de sistema de la teoría 02: la tarea, los tipos, el criterio, los ejemplos entre etiquetas y que la nota es un dato |
| `split(notes, seed)` y `pick(notes, rest, count)` | El primer reparto estratificado de `clasificar`, y las primeras `count` notas de cada tipo fuera de la prueba |
| `read(client, texts, expected, classes, examples)` | Una petición por nota, con `transform_schema` y `effort` en `output_config`; valida solo si `stop_reason` es `end_turn` |
| `Reading` y `Report` | Cada lectura (o `None`) con su `stop_reason`; el acierto, el coste y los fallos |
| `Recording` y `client(...)` | Grabar y repetir las respuestas de la API (sección 4) |

Tres decisiones:

- **El cliente llega como argumento.** `read` no crea el cliente ni lee el entorno: lo recibe. La CLI decide si es la API de verdad, una grabación o una grabación nueva; los tests le pasan uno falso.
- **`create` y no `parse`.** Con una respuesta cortada, `parse` lanza un error y se pierden la lectura y sus tokens. `read` mira `stop_reason` y deja la nota sin lectura: cuenta como fallo, no se inventa (teoría 03, sección 4).
- **Los ejemplos, fuera de la prueba.** `pick` elige entre `rest`, las notas que `split` no aparta para la prueba. Un test lo comprueba, como el espía del tokenizador en la semana 36.

## 3. Lo que no sale del núcleo

El núcleo no sabe nada de la clave: `client()` la recibe como argumento, y `anthropic.Anthropic(api_key=None)` la busca en `ANTHROPIC_API_KEY`. La CLI comprueba antes de empezar que la clave existe, salvo que vaya a repetir una grabación:

```text
error: falta ANTHROPIC_API_KEY: expórtala, o repite una grabación con --grabacion
```

`anthropic` se importa dentro del comando, como PyTorch en `clasificar`: el resto de la CLI no lo carga.

## 4. Grabar y repetir

Una llamada real cuesta dinero, necesita una clave y no responde dos veces igual. Los tests y la CI no pueden depender de eso. `Recording` es un **transporte** de `httpx2`, la biblioteca HTTP del SDK: se coloca donde iría la conexión de verdad, como `httpx.MockTransport` en los tests de `descargar` (semana 18).

- **Grabando** (`--grabar`), pasa cada petición a la API y guarda la respuesta en el JSON, con la **huella** de la petición: un `sha256` del método, la ruta y el cuerpo con las claves en orden. Las cabeceras no cuentan: la clave nunca se guarda.
- **Repitiendo** (`--grabacion` sin `--grabar`), busca la huella y devuelve lo guardado. No sale nada a Internet ni hace falta clave. Si la petición cambió (otra nota, otro prompt, otra semilla, otros ejemplos), no hay respuesta y es un error, no una llamada de pago:

```text
error: notas-claude-ejemplo.json no tiene respuesta para esta petición; vuelve a grabar con --grabar
```

Repitiendo, el cliente no reintenta (`max_retries=0`): la segunda vez saldría igual.

Una grabación sirve para tres cosas: enseñar la salida sin gastar, repetir un análisis exactamente, y comprobar que un cambio en tu código no cambia lo que envías (si cambia, la huella no está).

## 5. Tests sin red

`tests/test_llm.py` no llama nunca a la API. Un "Claude falso" es una función que recibe la petición de `httpx2` y devuelve una respuesta con la forma exacta de la API:

```python
def fake(seen=None, stop="end_turn"):
    def handler(request):
        if seen is not None:
            seen.append(request)  # el test mira lo que se envió
        text = note_of(request)
        answer = {"tipo": guess(text), "urgente": "roto" in text, "resumen": text[:20]}
        return httpx2.Response(200, json=message(answer, stop))
    return handler
```

Con él, los tests comprueban lo que se **envía** (el modelo, el esquema con tus tipos, el sistema, la nota entre etiquetas, el esfuerzo) y lo que se **hace** con cada respuesta (una cortada, una rechazada, un 401, un 529, una conexión que falla), sin gastar nada.

## 6. Lo que dice la grabación de ejemplo

```text
$ uv run observatorio leer-notas notas.csv --grabacion notas-claude-ejemplo.json
notas.csv: 300 notas · 3 tipos: averia 100, calibracion 100, limpieza 100
claude-sonnet-5-5 · esfuerzo low · 60 notas de prueba (las de `clasificar --semilla 31`) · 0 ejemplos por tipo · respuestas grabadas en notas-claude-ejemplo.json, sin red
Notas que no acierta (5)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Nota                                                ┃ Tipo        ┃ Claude   ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Se pasó por Centro, ver informe del técnico.        │ limpieza    │ averia   │
│ Oeste: revisión de rutina, detalles en la planilla. │ averia      │ limpieza │
│ Se pasó por Norte, ver informe del técnico.         │ calibracion │ averia   │
│ Se pasó por Este, ver informe del técnico.          │ calibracion │ averia   │
│ Norte: revisión de rutina, detalles en la planilla. │ calibracion │ limpieza │
└─────────────────────────────────────────────────────┴─────────────┴──────────┘
acierta 55 de 60 (0.917) · 18 urgentes · 0 sin lectura
tokens: 28359 de entrada y 1796 de salida · 0.0747 dólares con los precios de claude-sonnet-5-5
```

**Cuidado con lo que se concluye.** `notas-claude-ejemplo.json` son respuestas **de ejemplo**, escritas para el bootcamp con la forma exacta de la API: no las escribió Claude, y los tokens son aproximados. Sirven para ver la salida, leer los fallos y probar el comando sin clave; no son una medida de Claude. Con tu clave y `--grabar`, la tuya sí lo será.

Lo que sí enseña la forma de la salida:

- los cinco fallos son notas que **no dicen qué se hizo**: ningún modelo las acierta más que por suerte (semana 36, teoría 05);
- leer 60 notas cuesta unos céntimos: mil notas al día, unos 37 dólares al mes con Sonnet 5.5. TF-IDF, nada;
- con `--ejemplos 2`, la grabación tiene unos 12 000 tokens más de entrada (40 302 frente a 28 359) para el mismo acierto: los ejemplos se pagan en cada nota.

La comparación honesta, con tus notas y tu clave: si Claude acierta lo mismo que TF-IDF, TF-IDF gana (gratis, rápido, sin enviar datos fuera). Claude aporta cuando las notas usan palabras que el entrenamiento no vio, cuando no tienes notas etiquetadas para entrenar, o cuando quieres más que un tipo: la urgencia y un resumen salen en la misma petición.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| Tests que llaman a la API | La CI falla sin clave y cada ejecución cuesta | Un transporte falso con `httpx2.MockTransport` |
| Crear el cliente dentro de `read` | No se puede probar sin red | El cliente como argumento |
| Guardar las cabeceras en la grabación | La clave queda en un archivo del repositorio | Guardar solo el cuerpo de la respuesta |
| Ejemplos del prompt sacados de las notas de prueba | Un acierto falso | `pick` entre las notas que no son de prueba |
| Presentar la grabación de ejemplo como una medida de Claude | Conclusiones sobre algo que no se midió | Medir con tu clave y tus notas |
| Comparar con otras notas que `clasificar` | Una comparación injusta | La misma semilla: las mismas notas de prueba |

## ✅ Qué debes saber al terminar

- Qué hace `leer-notas`, con qué opciones, y con qué se compara.
- Qué hace cada pieza de `core/llm.py`, y por qué `read` usa `create` y no `parse`.
- Cómo graba y repite `Recording`, qué es la huella y por qué no guarda la clave.
- Cómo se prueba código que llama a una API de pago sin llamarla.
- Qué se puede concluir de la grabación de ejemplo y qué no.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Tool use](04-tool-use.md) | **05 · Claude en tu Observatorio** | [Ejercicio 01 · La primera llamada](../2-practicas/ejercicio-01-la-primera-llamada/README.md) |
