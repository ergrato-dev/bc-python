# Webgrafía — Semana 13

| Recurso | Para qué |
|---|---|
| [Módulo `typing`](https://docs.python.org/es/3.14/library/typing.html) (en español) | La referencia de `TypedDict`, `Literal`, `Final`, `NewType`, `TypeIs`, `cast`, `assert_never` y `reveal_type`: las teorías 01 y 02 |
| [mypy: opciones de la línea de órdenes](https://mypy.readthedocs.io/en/stable/command_line.html) (en inglés) | Qué activa `--strict`, opción por opción, con un ejemplo de cada una |
| [mypy: usar mypy en código existente](https://mypy.readthedocs.io/en/stable/existing_code.html) (en inglés) | Cómo se llega a `strict` en un proyecto grande, módulo a módulo. Para cuando trabajes en uno que no empezó anotado |
| [mypy: problemas comunes](https://mypy.readthedocs.io/en/stable/common_issues.html) (en inglés) | La invarianza de `list` y `dict`, con la sugerencia de usar `Sequence` y `Mapping`: el paso 6 del proyecto |
| [mypy: estrechar tipos](https://mypy.readthedocs.io/en/stable/type_narrowing.html) (en inglés) | Todas las formas de estrechar, de `isinstance` a `TypeIs`: la teoría 01 |
| [mypy: `TypedDict`](https://mypy.readthedocs.io/en/stable/typed_dict.html) (en inglés) | Claves obligatorias y opcionales, `total=False` y herencia entre `TypedDict` |
| [Pydantic: modelos](https://docs.pydantic.dev/latest/concepts/models/) (en inglés) | `BaseModel`, `model_validate`, `model_copy` y modelos anidados: la teoría 03 |
| [Pydantic: tabla de conversiones](https://docs.pydantic.dev/latest/concepts/conversion_table/) (en inglés) | Qué convierte el modo normal y qué rechaza el estricto, tipo a tipo: por qué `true` pasa a `1.0` |
| [Pydantic: validadores](https://docs.pydantic.dev/latest/concepts/validators/) (en inglés) | `field_validator` y `model_validator` en sus modos `before`, `after`, `wrap` y `plain`: la teoría 04 |
| [Pydantic: `TypeAdapter`](https://docs.pydantic.dev/latest/concepts/type_adapter/) (en inglés) | Validar listas, dataclasses y cualquier tipo, y por qué conviene crearlo una sola vez |
| [Pydantic: el plugin de mypy](https://docs.pydantic.dev/latest/integrations/mypy/) (en inglés) | Qué aprende mypy con `plugins = ["pydantic.mypy"]` y sus opciones |
| [Pydantic: errores de validación](https://docs.pydantic.dev/latest/errors/validation_errors/) (en inglés) | Cada `type` de error (`missing`, `extra_forbidden`, `float_parsing`...) con un ejemplo que lo provoca |
| [Parse, don't validate — Alexis King](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) (en inglés) | El artículo que da nombre a la idea de la teoría 05. Los ejemplos están en Haskell, pero el argumento se entiende sin saberlo |
| [PEP 589 — TypedDict](https://peps.python.org/pep-0589/) (en inglés) | Por qué un `TypedDict` es un `dict` en ejecución y no una clase nueva |
| [PEP 695 — Type Parameter Syntax](https://peps.python.org/pep-0695/) (en inglés) | La sintaxis `def first[T]` y `type Record = ...`. Solo para curiosos |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
