# 04 · Decoradores con argumentos

⏱️ 45 min

## 🎯 Objetivos

- Escribir un decorador que recibe argumentos, como `@rounded(1)` o `@retry(3, ConnectionError)`.
- Reconocer qué pasa si se olvidan los paréntesis.
- Usar un decorador para registrar funciones en un diccionario.
- Entender que `@dataclass(frozen=True)` y `@functools.wraps(func)` son decoradores con argumentos.

---

## 1. Tres niveles

`@announce` no admite opciones. Para escribir `@repeat(3)`, hace falta una función que reciba el `3` y **devuelva el decorador**:

```python
def repeat(times: int) -> Callable[[Callable[[str], None]], Callable[[str], None]]:
    def decorator(func: Callable[[str], None]) -> Callable[[str], None]:
        @functools.wraps(func)
        def wrapper(text: str) -> None:
            for _ in range(times):
                func(text)

        return wrapper

    return decorator


@repeat(3)
def beep(text: str) -> None:
    print(text)
```

`@repeat(3)` se lee en dos tiempos: primero se **llama** a `repeat(3)`, que devuelve `decorator`; después ese `decorator` se aplica a `beep`. Es decir, `beep = repeat(3)(beep)`.

![Tres funciones, una dentro de otra. repeat recibe times y devuelve decorator; decorator recibe func y devuelve wrapper; wrapper recibe los argumentos de cada llamada. Debajo, cuándo se ejecuta cada una: repeat(3) y decorator al definir la función, wrapper en cada llamada](../0-assets/03-decorador-con-argumentos.svg)

| Nivel | Recibe | Devuelve | Se ejecuta |
|---|---|---|---|
| `repeat` | Los argumentos del decorador (`times`) | `decorator` | Al definir la función |
| `decorator` | La función (`func`) | `wrapper` | Al definir la función |
| `wrapper` | Los argumentos de cada llamada | El resultado | En cada llamada |

`wrapper` recuerda `func` y `times`: es una closure de dos niveles.

### El tipo con `ParamSpec`

El decorador de tu proyecto, `rounded`, sirve para cualquier función que devuelva un `float`:

```python
def rounded[**P](digits: int) -> Callable[[Callable[P, float]], Callable[P, float]]:
    def decorator(func: Callable[P, float]) -> Callable[P, float]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> float:
            return round(func(*args, **kwargs), digits)

        return wrapper

    return decorator
```

La anotación del retorno es larga, pero dice algo preciso: `rounded(1)` devuelve un decorador que convierte una función con parámetros `P` que da `float` en otra con los **mismos** parámetros que también da `float`.

---

## 2. Olvidar los paréntesis

```python
@repeat            # sin (3)
def broken(text: str) -> None:
    print(text)
```

Python hace `broken = repeat(broken)`: `times` recibe la función y `broken` pasa a ser `decorator`. No falla al definirla; al llamarla, `broken("alerta")` trata `"alerta"` como si fuera la función que decorar y devuelve un `wrapper` sin imprimir nada. Un error silencioso. mypy lo detecta en la línea del decorador:

```
error: Argument 1 to "repeat" has incompatible type "Callable[[str], None]"; expected "int"  [arg-type]
```

---

## 3. Registrar funciones

Un decorador no tiene por qué envolver. Puede apuntar la función en algún sitio y devolverla **tal cual**:

```python
PARSERS: dict[str, Callable[[str], float]] = {}


def parser(suffix: str) -> Callable[[Callable[[str], float]], Callable[[str], float]]:
    def decorator(func: Callable[[str], float]) -> Callable[[str], float]:
        PARSERS[suffix] = func
        return func

    return decorator


@parser(".txt")
def parse_comma(text: str) -> float:
    return float(text.replace(",", "."))


PARSERS[".txt"]("12,5")      # 12.5
```

Así funcionan las rutas de FastAPI (`@app.get("/medidas")`, semana 20), los comandos de Typer (`@app.command()`, semana 15) y los *fixtures* de pytest (`@pytest.fixture`, semana 14): la función se registra al importar el módulo y el *framework* la llama cuando toca.

---

## 4. Decoradores con argumentos que ya conoces

```python
@dataclass(frozen=True, slots=True)
class Measurement: ...
```

`dataclass(frozen=True, slots=True)` devuelve un decorador, que recibe la **clase** y devuelve la clase con `__init__`, `__eq__` y `__repr__` añadidos. Un decorador también se aplica a clases. `dataclass` acepta las dos formas, `@dataclass` y `@dataclass(...)`, porque comprueba si su primer argumento es una clase.

| Decorador | Argumentos | Qué hace |
|---|---|---|
| `@dataclass(frozen=True)` | Opciones | Genera métodos en la clase |
| `@functools.wraps(func)` | La función original | Copia `__name__`, `__doc__` y añade `__wrapped__` |
| `@functools.lru_cache(maxsize=128)` | Tamaño | Recuerda resultados (teoría 05) |
| `@pytest.mark.parametrize(...)` | Casos | Repite un test con datos distintos (semana 14) |

---

## 5. Un decorador con lógica: `retry`

Cuando el Observatorio lea de una API (semana 18), algunas llamadas fallarán por la red y conviene reintentar:

```python
def retry[**P, R](times: int, error: type[Exception]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except error as problem:
                    print(f"intento {attempt} de {times}: {problem}")
            raise RuntimeError(f"{func.__name__} falló {times} veces")

        return wrapper

    return decorator


@retry(3, ConnectionError)
def read_sensor() -> float: ...
```

Solo se reintenta el error indicado: otro error (un `ValueError` por un dato mal formado) sale en el primer intento, porque repetir no lo arreglaría. Las bibliotecas reales (`tenacity`, `stamina`) añaden esperas entre intentos; la estructura es esta.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| La función decorada no hace nada y devuelve otra función | `@repeat` sin paréntesis | `@repeat(3)` |
| `AttributeError: 'int' object has no attribute '__name__'` al definir la función | `@announce(3)` en un decorador sin argumentos: `3` hace de función | `@announce` |
| `TypeError: 'function' object cannot be interpreted as an integer` | `@repeat` sin paréntesis, al llamar al `wrapper` | `@repeat(3)` |
| El registro está vacío | El módulo con los `@parser(...)` no se ha importado | Impórtalo antes de usar el diccionario |
| La función registrada es `None` | El decorador de registro no devuelve `func` | `return func` |
| `retry` reintenta errores que no debería | `error=Exception` atrapa todo | Pasa el tipo concreto (`ConnectionError`) |

---

## ✅ Qué debes saber al terminar

- [ ] Escribir un decorador con argumentos con sus tres niveles y decir cuándo se ejecuta cada uno.
- [ ] Qué hace `@repeat` sin paréntesis y cómo lo detecta mypy.
- [ ] Usar un decorador para registrar funciones sin envolverlas.
- [ ] Por qué `@dataclass(frozen=True)` es un decorador con argumentos que se aplica a una clase.
- [ ] Qué errores debe reintentar `retry` y cuáles no.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Decoradores](03-decoradores.md) | **04 · Decoradores con argumentos** | [05 · functools](05-functools.md) |
