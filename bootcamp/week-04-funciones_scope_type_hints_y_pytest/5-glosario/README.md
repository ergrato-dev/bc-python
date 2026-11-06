# Glosario — Semana 04

| Término | Definición |
|---|---|
| **Anotación de tipo** (*type hint*) | Indica el tipo esperado de un parámetro, un valor de vuelta o una variable: `value: float`, `-> str`. Python no la comprueba |
| **Argumento** | El valor que se pasa en una llamada: en `describe("Norte")`, `"Norte"` |
| **Argumento por nombre** | El que se pasa con el nombre del parámetro: `describe(label="Norte")` |
| **`assert`** | Comprueba una condición; si es falsa, lanza `AssertionError`. Es la base de los tests |
| **Caso base** | En una función recursiva, el caso que se responde sin volver a llamarse |
| **Cláusula de guarda** | `if` al principio de una función que descarta un caso raro con `return` o `raise` |
| **Docstring** | Texto entre `"""` al principio de una función que explica qué hace |
| **Efecto** (*side effect*) | Lo que una función cambia o lee fuera de ella: escribir en la terminal, modificar un argumento, leer la hora |
| **Estrechar un tipo** | Después de `if value is None: return`, el comprobador sabe que `value` ya no es `None` |
| **Función pura** | Su resultado depende solo de sus argumentos y no tiene efectos |
| **`Iterable`** | Tipo de cualquier cosa que se pueda recorrer con `for`; se importa de `collections.abc` |
| **`lambda`** | Función de una sola expresión, sin nombre, escrita donde se usa: `lambda t: float(t)` |
| **LEGB** | Orden en que Python busca un nombre: *Local*, *Enclosing*, *Global*, *Built-in* |
| **`mypy`** | Comprobador de tipos: lee el código sin ejecutarlo y avisa de los tipos incompatibles |
| **Parámetro** | El nombre que recibe un argumento, en la definición: en `def describe(label)`, `label` |
| **Parámetro solo por nombre** | El que va después de `*` en la firma: solo se puede pasar por nombre |
| **`parametrize`** | `@pytest.mark.parametrize`: ejecuta un test una vez por cada conjunto de valores |
| **`pytest.approx`** | Compara decimales con una tolerancia pequeña, en lugar de exigir igualdad exacta |
| **`pytest.raises`** | Comprueba que un bloque lanza un error concreto |
| **Recursión** | Una función que se llama a sí misma con un problema más pequeño |
| **Refactorizar** | Mejorar el código sin cambiar lo que hace, con los tests como red |
| **`return`** | Termina la función y entrega un valor a quien la llamó; sin él, se devuelve `None` |
| **Scope** (ámbito) | Parte del programa donde un nombre existe y se puede usar |
| **TDD** | Desarrollo guiado por tests: rojo (test que falla), verde (lo mínimo para que pase), refactorizar |
| **Tupla** | Valor con varias partes, como el que devuelve `return a, b`; se desempaqueta con `x, y = ...` |
| **Valor por defecto** | El que toma un parámetro si no se le pasa argumento: `unit: str = "µg/m³"` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
