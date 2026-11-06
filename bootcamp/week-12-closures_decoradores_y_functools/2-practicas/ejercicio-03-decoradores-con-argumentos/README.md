# Ejercicio 03 — Decoradores con argumentos

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-decoradores-con-argumentos.md)

## Objetivo

Escribir decoradores que reciben opciones (`@repeat(3)`), ver qué pasa al olvidar los paréntesis, usar un decorador para registrar funciones, reconocer `@dataclass(frozen=True)` como uno de ellos y escribir un `retry` que reintenta una función que falla. Es lo que hace `rounded` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `factory_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-12-closures_decoradores_y_functools/2-practicas/ejercicio-03-decoradores-con-argumentos/starter
uv run python factory_lab.py
```

```
Ejercicio 03 · Decoradores con argumentos
```

Descomenta en orden: el paso 2 usa `repeat`, del paso 1. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. Una fábrica de decoradores

Descomenta el **PASO 1** y ejecuta:

```
    alerta
    alerta
    alerta
repeat(2) es un decorador: decorator
a mano
a mano
```

`repeat` tiene tres niveles: `repeat(times)` devuelve `decorator`; `decorator(func)` devuelve `wrapper`; `wrapper(text)` hace el trabajo. `@repeat(3)` primero **llama** a `repeat(3)` y después aplica lo que devuelve a `beep`.

Las dos últimas líneas lo hacen por partes: `twice = repeat(2)` es el decorador, sin aplicar todavía, y `twice(print)` decora la función `print`, que se llama dos veces con `"a mano"`.

### 2. Olvidar los paréntesis

Descomenta el **PASO 2** y ejecuta:

```
Sin paréntesis, broken es: decorator
Y llamarla no imprime nada; devuelve: wrapper
```

`@repeat` sin `(3)` hace `broken = repeat(broken)`: `times` recibe tu función y `broken` pasa a ser `decorator`. Python no se queja al definirla. Al llamarla, `broken("alerta")` trata el texto como si fuera la función que decorar y devuelve un `wrapper`, sin imprimir nada.

Los `# type: ignore` están porque mypy sí lo detecta. Quita el de la línea `@repeat` y ejecuta `uvx --from mypy==2.4.1 mypy factory_lab.py`:

```
factory_lab.py:43: error: Argument 1 to "repeat" has incompatible type "Callable[[str], None]"; expected "int"  [arg-type]
```

Vuelve a ponerlo.

### 3. Un registro de funciones

Descomenta el **PASO 3** y ejecuta:

```
Registrados: {'.txt': 'parse_comma', '.csv': 'parse_point'}
  12,5 con .txt: 12.5
  55.1 con .csv: 55.1
```

`parser(".txt")` devuelve un decorador que **no envuelve**: apunta la función en `PARSERS` y la devuelve tal cual. Los registros se llenan al definir las funciones, antes de que nadie las llame. Elegir el lector por el sufijo es ahora una consulta al diccionario, como hacía `open_file` en la semana 10 con un `if`. Así registran FastAPI sus rutas, Typer sus comandos y pytest sus *fixtures*.

### 4. Decoradores que ya usabas

Descomenta el **PASO 4** y ejecuta:

```
Con @: WithAt(label='Norte') · a mano: ByHand(label='Norte')
dataclass(frozen=True) devuelve: function
property, classmethod y staticmethod son clases: <class 'property'> <class 'classmethod'> <class 'staticmethod'>
```

`@dataclass(frozen=True)` es un decorador con argumentos: `dataclass(frozen=True)` devuelve una función, el decorador, que recibe la **clase** y la devuelve con `__init__`, `__repr__` y `__eq__`. Aplicarlo a mano (`ByHand = dataclass(frozen=True)(ByHand)`) da lo mismo, aunque mypy no lo entiende y pide los `# type: ignore`. `property`, `classmethod` y `staticmethod` son clases: decorar con ellas crea un objeto de esa clase.

### 5. Reintentar una función que falla

Descomenta el **PASO 5** y ejecuta:

```
    intento 1 de 3: sin red
    intento 2 de 3: sin red
Lectura: 21.5
Sin más respuestas: StopIteration no es ConnectionError y no se reintenta
```

`read_sensor` simula un sensor: las dos primeras respuestas son errores de red y la tercera, `21.5`. `@retry(3, ConnectionError)` la llama hasta tres veces y solo reintenta ese error. La segunda llamada a `read_sensor` ya no tiene respuestas: `next(answers)` lanza `StopIteration`, que no es un `ConnectionError`, así que sale al primer intento. Reintentar un error que no se arregla solo (un dato mal formado, un archivo que no existe) es perder el tiempo.

Si los tres intentos fallaran, `retry` lanzaría `RuntimeError: read_sensor falló 3 veces`. En la semana 18 harás esto contra una API de verdad.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: 'function' object cannot be interpreted as an integer` | Usaste `@repeat` sin paréntesis y llamaste al `wrapper`: escribe `@repeat(3)` |
| `NameError: name 'repeat' is not defined` en el paso 2 | Descomenta antes el paso 1 |
| `KeyError: '.txt'` en el paso 3 | El decorador no guarda la función en `PARSERS`, o el sufijo no coincide |
| `TypeError: 'NoneType' object is not callable` en el paso 3 | El decorador de registro no tiene `return func` |
| `retry` reintenta para siempre | `range(1, times + 1)` debe acabar; revisa que el `for` tiene el `return` dentro del `try` |
| `RuntimeError: read_sensor falló 3 veces` | Cambiaste las respuestas: con tres errores seguidos, `retry` se rinde |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Decoradores](../ejercicio-02-decoradores/README.md) | **Ejercicio 03 · Decoradores con argumentos** | [Ejercicio 04 · functools](../ejercicio-04-functools/README.md) |
