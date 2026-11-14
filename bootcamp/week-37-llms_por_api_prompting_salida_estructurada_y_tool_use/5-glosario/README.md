# Glosario — Semana 37

| Término | Definición |
|---|---|
| **Alucinación** | Un texto falso que el modelo escribe con la misma seguridad que uno cierto, porque no consulta datos: predice lo probable |
| **API de Messages** | El endpoint `POST /v1/messages` de Anthropic: recibe el modelo, el sistema y la conversación, y devuelve la respuesta |
| **Bloque de contenido** (*content block*) | Cada pieza de `content` en una respuesta: `text`, `tool_use`, `thinking` |
| **Bucle de herramientas** (*agentic loop*) | Repetir la petición mientras `stop_reason` sea `tool_use`, ejecutando lo pedido y devolviendo los resultados |
| **Clave de la API** (*API key*) | El secreto con el que se paga la API. En `ANTHROPIC_API_KEY`, nunca en el código ni en un commit |
| ***Constrained decoding*** | Al escribir, solo se permiten los tokens que cumplen el esquema: la salida tiene la forma pedida |
| **Esfuerzo** (*effort*) | Cuánto piensa el modelo antes de responder: `low`, `medium`, `high`. Menos esfuerzo, menos tokens y menos tiempo |
| **Esquema JSON** (*JSON Schema*) | La descripción de la forma de un JSON: tipos, campos obligatorios, valores admitidos |
| ***Few-shot*** | Dar ejemplos resueltos en el prompt para enseñar un formato o un criterio |
| **Grabación** | Un archivo con las respuestas de la API por la huella de cada petición, para repetirlas sin red ni clave |
| **Huella** | El `sha256` de una petición (método, ruta y cuerpo con las claves en orden): la misma petición, la misma huella |
| **Inyección de prompt** (*prompt injection*) | Un texto que llega como dato e intenta dar órdenes al modelo |
| **LLM** (*Large Language Model*) | Un modelo de lenguaje grande: un *decoder* entrenado con muchísimo texto y ajustado para seguir instrucciones |
| ***max_tokens*** | El máximo de tokens que puede escribir una respuesta. Si lo alcanza, se corta con `stop_reason: max_tokens` |
| **Prompt** | Todo lo que el modelo lee antes de responder: el sistema y los mensajes |
| ***Prompt caching*** | Guardar en la API el principio repetido de las peticiones para cobrarlo más barato la siguiente vez |
| ***Refusal*** | Una respuesta en la que el modelo no responde, por seguridad: `stop_reason: refusal` |
| **Salida estructurada** (*structured output*) | Una respuesta con la forma de un esquema JSON, impuesta con `output_config.format` |
| ***stop_reason*** | Por qué terminó una respuesta: `end_turn`, `max_tokens`, `tool_use`, `refusal` |
| **Sistema** (*system prompt*) | La parte fija del prompt: quién responde, la tarea, el formato y el contexto |
| **Token** | La pieza de texto que lee y escribe el modelo, y por la que se paga |
| ***tool_result*** | El bloque con el que tu código devuelve el resultado de una herramienta, con el mismo id que su `tool_use` |
| ***tool_use*** | El bloque con el que Claude pide una herramienta: el nombre, la entrada y un id |
| ***Tool runner*** | El bucle de herramientas que trae el SDK (`client.beta.messages.tool_runner`), en beta |
| **Transporte** (*transport*) | La pieza de `httpx2` que envía las peticiones. Cambiarlo permite tests sin red y grabaciones |
| **Ventana de contexto** | Lo máximo que cabe en una petición: lo enviado más lo que escribe la respuesta |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
