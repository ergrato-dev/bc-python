# Webgrafía — Semana 37

Casi todo en inglés, de la documentación oficial de Anthropic. La documentación sigue la última versión de la API y del SDK; si algo no coincide con `anthropic` 2.3.0, manda lo que ves al ejecutar.

| Recurso | Para qué |
|---|---|
| [Claude Docs: introducción](https://docs.claude.com/en/docs/intro) | La puerta de entrada: la consola, las claves y la primera llamada. La teoría 01 |
| [API: Messages](https://docs.claude.com/en/api/messages) | La referencia de la petición y la respuesta, campo a campo. La teoría 01, sección 3 |
| [Modelos](https://docs.claude.com/en/docs/about-claude/models/overview) | Los modelos, sus identificadores, su contexto y su salida máxima. La teoría 01, sección 4 |
| [Precios](https://docs.claude.com/en/docs/about-claude/pricing) | Lo que cuesta cada modelo por millón de tokens, y los descuentos de caché y de lotes. Míralo antes de calcular |
| [Errores](https://docs.claude.com/en/api/errors) | Los códigos HTTP de la API y qué significa cada uno. La teoría 01, sección 7 |
| [Contar tokens](https://docs.claude.com/en/docs/build-with-claude/token-counting) | `count_tokens`: cuántos tokens tiene una petición antes de enviarla |
| [Prompt engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) | La guía oficial: claridad, ejemplos, etiquetas XML, el sistema. La teoría 02 |
| [Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) | Pagar menos por lo que se repite en cada petición. La teoría 02, sección 1 |
| [Crear tests para un prompt](https://docs.claude.com/en/docs/test-and-evaluate/develop-tests) | Cómo medir un prompt con casos etiquetados. La teoría 02, sección 7 |
| [Structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs) | `output_config.format`, el esquema admitido y sus límites. La teoría 03 |
| [Pydantic: JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/) | Cómo convierte Pydantic una clase en un esquema. La teoría 03, sección 3 |
| [Tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview) | Herramientas, el bucle, `tool_choice`, herramientas en paralelo y `strict`. La teoría 04 |
| [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) (Anthropic) | Cómo describir herramientas que un modelo usa bien. La teoría 04, sección 2 |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (Anthropic) | Cuándo basta una llamada, cuándo un flujo y cuándo un agente. Puente a la semana 39 |
| [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) | El SDK: el README, los ejemplos, los reintentos, los transportes y el *tool runner* |
| [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Los riesgos de una aplicación con LLM, con la inyección de prompt la primera. La teoría 02, sección 6, y la semana 41 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
