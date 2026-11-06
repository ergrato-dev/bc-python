# 04 · Type hints

⏱️ 40 min

## 🎯 Objetivos

- Anotar parámetros, valores de vuelta y variables con los tipos básicos y de colecciones.
- Escribir con `X | None` que un valor puede faltar, y tratarlo.
- Entender que Python no comprueba las anotaciones y que `mypy` sí, sin ejecutar el código.

---

## 1. Qué son

Los *type hints* (anotaciones de tipo) dicen qué tipo se espera en cada sitio:

```python
def classify(value: float | None, low: float, high: float) -> str: ...
```

Se leen: "`classify` recibe un `float` o `None` y dos `float`, y devuelve un `str`". Los llevas usando desde la semana 1 en los starters; aquí aprendes a escribirlos tú.

Sirven a tres lectores:

| Lector | Qué gana |
|---|---|
| Tú, dentro de un mes | Sabes qué pasar sin leer el cuerpo |
| VS Code | Autocompleta los métodos correctos y subraya los errores mientras escribes |
| `mypy` | Encuentra errores de tipo en todo el proyecto sin ejecutarlo |

## 2. Python no los comprueba

```python
def double(n: int) -> int:
    return n * 2

double("ab")   # 'abab', sin ningún error
```

Al ejecutar, las anotaciones solo se guardan (`double.__annotations__`); nadie las mira. Por eso existen los comprobadores de tipos, como `mypy`, que leen el código **sin ejecutarlo**:

```bash
uv run --with mypy==2.4.1 mypy archivo.py
```

```
archivo.py:4: error: Argument 1 to "double" has incompatible type "str"; expected "int"  [arg-type]
```

Un test encuentra el error si alguien escribió un test para ese caso; `mypy` revisa todas las llamadas, también las que nadie ha probado. Son complementarios. En la semana 13 configurarás `mypy` en modo estricto dentro del proyecto.

## 3. Los tipos que usarás ya

| Anotación | Significa | Ejemplo |
|---|---|---|
| `int`, `float`, `str`, `bool` | Ese tipo | `count: int` |
| `None` | No devuelve nada útil | `def main() -> None:` |
| `float \| None` | Un `float` o `None` | El resultado de `parse_value` |
| `int \| float` | Cualquiera de los dos | Aunque `float` ya acepta un `int` |
| `list[str]` | Una lista de textos | `rows: list[str]` |
| `tuple[str, float]` | Una pareja: texto y número | `return name, value` |
| `tuple[list[str], list[str]]` | Una pareja de listas | El resultado de `process_lines` |
| `Iterable[str]` | Cualquier cosa que se recorra y dé textos | Las líneas: una lista o `sys.stdin` |

`Iterable` se importa: `from collections.abc import Iterable`. Pide lo mínimo que tu función necesita: si solo recorres las líneas una vez, `Iterable[str]` acepta una lista, `sys.stdin` o un archivo, mientras que `list[str]` rechazaría `sys.stdin`.

Para variables, la anotación solo hace falta cuando no se deduce del valor:

```python
rows: list[str] = []    # vacía: sin anotación, mypy no sabe de qué será la lista
count = 0               # ya se ve que es int
```

## 4. `None` obliga a decidir

Cuando una función devuelve `float | None`, quien la llama **tiene** que tratar el `None` antes de usar el número:

```python
value = parse_value(text)
return value * 2          # mypy: Unsupported operand types for * ("None" and "int")
```

```python
value = parse_value(text)
if value is None:
    return None
return value * 2          # aquí mypy ya sabe que value es float
```

Después de `if value is None: return ...`, `mypy` sabe que en el resto de la función `value` no es `None`. Esto se llama **estrechar** el tipo. Es exactamente el error que causaría un `TypeError` en la línea 900 de un archivo con un `NA`, encontrado antes de ejecutar.

## 5. Mentir en la anotación es peor que no ponerla

```python
def average(values: list[float]) -> float:
    return f"{sum(values) / len(values):.1f}"    # devuelve str
```

Se ve bien al imprimir, pero quien sume dos promedios recibirá `"12.5" + "8.0" == "12.58.0"`. `mypy` lo detecta (`Incompatible return value type`). Regla: la función devuelve el dato; el formato se hace al mostrarlo.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| Creer que `n: int` impide pasar un `str` | Python no comprueba las anotaciones | Usa `mypy`, y valida en la frontera lo que llegue de fuera |
| `Unsupported operand types ... "None"` en `mypy` | Usas un `X \| None` sin comprobar | `if value is None:` antes |
| `Incompatible return value type` | La función devuelve otro tipo del que promete | Cambia lo que devuelve o la anotación |
| `Need type annotation for "rows"` | Lista vacía sin tipo | `rows: list[str] = []` |
| `NameError: name 'Iterable' is not defined` | Falta el import | `from collections.abc import Iterable` |

## ✅ Qué debes saber al terminar

- [ ] Para qué sirven las anotaciones y quién las comprueba.
- [ ] Cómo anotar un valor que puede faltar y cómo estrechar su tipo.
- [ ] Cuándo usar `list[str]` y cuándo `Iterable[str]`.
- [ ] Cómo ejecutar `mypy` sobre un archivo con `uv run --with`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Funciones como valores](03-funciones-como-valores.md) | **04 · Type hints** | [05 · Tests con pytest](05-tests-con-pytest.md) |
