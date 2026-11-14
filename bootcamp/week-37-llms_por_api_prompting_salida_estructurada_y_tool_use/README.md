# Semana 37 — LLMs por API: prompting, salida estructurada y tool use

> En la semana 36 entrenaste modelos de lenguaje pequeños con tus notas. Esta semana usas uno enorme que ya está entrenado: Claude, por la API de Anthropic. Haces llamadas y lees todo lo que devuelven, escribes prompts y los mides, obtienes JSON que se puede leer siempre y das a Claude herramientas para consultar tus datos. Tu Observatorio gana un comando: `leer-notas`, que lee las notas de prueba de `clasificar` con Claude y dice cuánto acierta y cuánto cuesta. Sin gastar en los tests: las respuestas se graban y se repiten.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Llamar** a la API de Messages con el SDK de Python y **leer** su respuesta: bloques, `stop_reason` y tokens
- **Calcular** lo que cuesta una tarea con cada modelo y **guardar** la clave como un secreto
- **Escribir** prompts con contexto, ejemplos y datos separados, y **medirlos** con notas etiquetadas
- **Imponer** la forma de la respuesta con un esquema JSON y Pydantic, y **comprobar** lo que el esquema no garantiza
- **Dar** herramientas a Claude y **escribir** el bucle de tool use, con errores y límites
- **Probar** código que llama a una API de pago sin llamarla, con transportes falsos y grabaciones

---

## 📋 Prerrequisitos

- [Semana 36](../week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/README.md): tokens, Transformers, *encoders* y *decoders*, y `clasificar` con tus notas.
- [Semana 18](../week-18-http_con_httpx_reintentos_secretos_y_env/README.md): HTTP con `httpx`, reintentos, secretos en `.env` y `MockTransport`.
- [Semana 13](../week-13-typing_estricto_mypy_y_pydantic/README.md): Pydantic.
- El *pull request* `week-36` de tu proyecto fusionado en `main`, con la CI en verde.
- **Opcional**: una clave de la API de Anthropic, con un límite de gasto. Todo se puede hacer sin ella.

---

## 🗂️ Estructura de la Semana

```
week-37-llms_por_api_prompting_salida_estructurada_y_tool_use/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 36 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Qué es un LLM y la API](1-teoria/01-que-es-un-llm-y-la-api.md) | Un *decoder* que escribe, tokens y contexto, la petición y la respuesta, modelos y precios, `stop_reason`, la clave y los errores | 45 min |
| [02 · Prompting](1-teoria/02-prompting.md) | Las partes de un prompt, el formato, el contexto, los ejemplos, una salida para lo que no se sabe, la inyección de prompt y medir | 50 min |
| [03 · Salida estructurada](1-teoria/03-salida-estructurada.md) | Por qué no basta pedir JSON, `output_config.format`, Pydantic y `parse`, lo que el esquema no garantiza | 50 min |
| [04 · Tool use](1-teoria/04-tool-use.md) | Describir herramientas, una vuelta, el bucle, errores y límites, `tool_choice`, el *tool runner* y herramientas con cuidado | 50 min |
| [05 · Claude en tu Observatorio](1-teoria/05-claude-en-tu-observatorio.md) | `leer-notas`, `core/llm.py`, grabar y repetir, tests sin red y lo que dice la grabación de ejemplo | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Funcionan **sin clave ni red**: cada ejercicio trae sus respuestas grabadas (de ejemplo, con la forma exacta de la API); con tu clave y `CLAUDE_REAL=1`, las de verdad.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · La primera llamada](2-practicas/ejercicio-01-la-primera-llamada/README.md) | Una pregunta, la respuesta por dentro, el sistema, la historia, `max_tokens`, el coste y los errores | 1 h 30 min |
| [02 · Prompting](2-practicas/ejercicio-02-prompting/README.md) | Doce notas y seis prompts medidos: formato, contexto, ejemplos, `desconocido` y una inyección | 1 h 30 min |
| [03 · Salida estructurada](2-practicas/ejercicio-03-salida-estructurada/README.md) | JSON en el prompt, un esquema, Pydantic, extraer de una nota larga, `maxLength` y una respuesta cortada | 1 h 30 min |
| [04 · Tool use](2-practicas/ejercicio-04-tool-use/README.md) | Una herramienta, el bucle con cinco a la vez, un error, un límite y el *tool runner* | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/llm.py`: `schema`, `instructions`, `split`, `pick`, `read`, `Reading`, `Report`, `Recording` y `client`;
- la dependencia `anthropic`;
- el comando `leer-notas NOTAS [--ejemplos] [--semilla] [--grabacion] [--grabar] [--nota]`.

45 tests nuevos: 44 de `llm` y `leer-notas`, y un ejemplo tuyo. La versión sube a `0.37.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
|---|---|
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| El texto de una respuesta | `next(b.text for b in response.content if b.type == "text")` |
| Contar tokens antes de enviar | `client.messages.count_tokens(model=..., messages=...)` |
| Pensar menos en tareas simples | `output_config={"effort": "low"}` |
| JSON con la forma de una clase | `client.messages.parse(..., output_format=MiClase)` |
| El esquema que acepta la API | `anthropic.transform_schema(MiClase)` |
| El identificador para el soporte | `response.id`, o `response._request_id` |
| Ver qué envía el SDK | Un `httpx2.MockTransport` que imprime `request.content` |
| Repetir sin gastar | `leer-notas ... --grabacion notas-claude.json` |
| Un tope de gasto | El límite mensual de la consola de Anthropic |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-37` de `python-<nombre>-<apellido>` con:
   - `core/llm.py` sin reexportar en `core/__init__.py`, y el comando `leer-notas`, con el import dentro;
   - `anthropic==2.3.0`, las imágenes `week-37` y la versión `0.37.0`;
   - al menos 6 tests propios en `tests/test_my_llm.py`;
   - si tienes clave, `notas-claude.json` con la lectura de tus notas.

   Todo en verde en tu máquina, en Docker y en GitHub Actions, sin ninguna clave en el repositorio.
2. ✅ `README.md` del repositorio con la sección "Lectura con Claude", e `informe/README.md` con el resultado en "Siguientes pasos"
3. ✅ Pull request `week-37` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `leer-notas` y la de `clasificar` con las mismas notas, y tu lectura;
   - la tabla de mutantes con las dos respuestas del paso 9.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pre-commit run --all-files
uv run pytest
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
uv run observatorio --version
uv run observatorio leer-notas $STARTER/notas.csv --grabacion $STARTER/notas-claude-ejemplo.json
uv run observatorio leer-notas notas.csv; echo $?
uv run observatorio leer-notas notas.csv --grabar; echo $?
uv run python -c "import sys, observatorio.cli; print('anthropic' in sys.modules)"
git grep -n "sk-ant-" || echo "sin claves"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1509;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.37.0`;
- la grabación de ejemplo da `acierta 55 de 60 (0.917)` y `tokens: 28359 de entrada y 1796 de salida`;
- sin clave, `error: falta ANTHROPIC_API_KEY` y código 2; `--grabar` solo, `--grabar necesita --grabacion` y código 2;
- la comprobación de `sys.modules` escribe `False`, y `git grep` escribe `sin claves`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 36](../week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/README.md) | **Semana 37** | [Semana 38](../week-38-rag_embeddings_pgvector_en_postgresql_y_evaluacion/README.md) |
