# Ejercicio 02 — Tipos avanzados

⏱️ 1 h · Teoría previa: [02](../../1-teoria/02-tipos-avanzados.md)

## Objetivo

Usar los tipos que van más allá de `int` o `list[str]`:

- `TypedDict`, para un diccionario con claves fijas;
- `Mapping` y `Sequence`, que aceptan más que `dict` y `list`;
- funciones y clases genéricas con `[T]`;
- alias con `type` y `NewType`;
- un `match` que mypy comprueba que cubre todos los casos.

El `Summary` de tu proyecto es un `TypedDict`, y `write_json` pasa a recibir un `Mapping`. Ejercicio **guiado**: descomentas cada paso de `types_lab.py`, ejecutas el programa y mypy y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-13-typing_estricto_mypy_y_pydantic/2-practicas/ejercicio-02-tipos-avanzados/starter
uv run python types_lab.py
uvx --from mypy==2.4.1 mypy --strict types_lab.py
```

```
Ejercicio 02 · Tipos avanzados
Success: no issues found in 1 source file
```

Como en el ejercicio 01, las líneas que darían error llevan un `# type: ignore[código]`: lo quitas para ver el error y lo vuelves a poner. Descomenta en orden: el paso 2 usa el `summary` del paso 1. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. `TypedDict`, un `dict` con claves fijas

Descomenta el **PASO 1** y ejecuta:

```
Es un dict normal: dict {'registros': 3, 'mediana': 12.5}
mediana: 12.5
Una clave mal escrita: KeyError 'media'
Le falta una clave y Python no se queja: {'registros': 3}
```

En ejecución, `Summary` no existe: `summary` es un `dict` como cualquier otro. La diferencia está en mypy. Quita los `# type: ignore` de las líneas 26 y 29:

```
types_lab.py:26: error: TypedDict "Summary" has no key "media"  [typeddict-item]
types_lab.py:26: note: Did you mean "mediana"?
types_lab.py:29: error: Missing key "mediana" for TypedDict "Summary"  [typeddict-item]
```

Con `dict[str, object]`, mypy no sabría qué claves hay ni de qué tipo es cada valor. Vuelve a ponerlos.

### 2. `dict` frente a `Mapping`

Descomenta el **PASO 2** y ejecuta:

```
Con dict: 2
Con Mapping: 2
Con list: 20.5
Con Sequence: 20.5
```

Las cuatro funciones van bien al ejecutar. Quita los `# type: ignore` de las líneas 44 y 57 y ejecuta mypy:

```
types_lab.py:44: error: Argument 1 to "count_keys" has incompatible type "Summary"; expected "dict[str, object]"  [arg-type]
types_lab.py:57: error: Argument 1 to "total" has incompatible type "list[float]"; expected "list[float | None]"  [arg-type]
types_lab.py:57: note: "list" is invariant -- see https://mypy.readthedocs.io/en/stable/common_issues.html#variance
types_lab.py:57: note: Consider using "Sequence" instead, which is covariant
```

`count_keys` podría hacer `data["otra"] = "texto"`, y eso rompería un `Summary`. `total` podría añadir un `None` a una lista que solo admite `float`. mypy no mira qué hace la función por dentro: con `dict` y `list` puede cambiarlos, así que no acepta un tipo más estrecho. `Mapping` y `Sequence` son de solo lectura: las dos llamadas pasan. Si una función solo lee, pide `Mapping` o `Sequence`. Vuelve a poner los dos comentarios.

### 3. Funciones y clases genéricas

Descomenta el **PASO 3** y ejecuta:

```
first de floats: 12.5 · first de textos: Norte
Runtime type is 'str'
Las dos últimas: [8.0, 55.1]
```

`first[T]` declara una variable de tipo: lo que entra en `Sequence[T]` es lo que sale. `reveal_type` sirve a la vez para Python, que escribe `Runtime type is 'str'` en stderr, y para mypy, que escribe una nota:

```
types_lab.py:78: note: Revealed type is "str"
```

La línea `window = ...` crea una ventana de `float` de tamaño 2. Quita el `# type: ignore` de la línea 83:

```
types_lab.py:83: error: Argument 1 to "push" of "Window" has incompatible type "str"; expected "float"  [arg-type]
```

Al ejecutar, `push("alto")` habría metido el texto sin quejarse. Vuelve a ponerlo y borra el `reveal_type` cuando termines: es para mirar, no para dejarlo en el código.

### 4. Alias con `type` y `NewType`

Descomenta el **PASO 4** y ejecuta:

```
Record es un alias: ('Norte', 12.5) · su valor: tuple[str, float | None]
10 °C: 50.0 °F
Celsius(10.0) es un float normal: float
Sin Celsius(...): 50.0
```

`type Record = ...` es un alias: otro nombre para el mismo tipo, como el `Record` de tu proyecto desde la semana 5. `NewType` crea un tipo **distinto** para mypy, aunque en ejecución `Celsius(10.0)` es el mismo `float`. Quita el `# type: ignore` de la línea 101:

```
types_lab.py:101: error: Argument 1 to "to_fahrenheit" has incompatible type "float"; expected "Celsius"  [arg-type]
```

Así mypy no deja pasar un `float` cualquiera, que podría estar en °F, donde se esperan grados Celsius. Vuelve a ponerlo.

### 5. `match` exhaustivo con `assert_never`

Descomenta el **PASO 5** y ejecuta:

```
Consejos: ['sin aviso', 'vigilar', 'alerta']
```

`assert_never(level)` en el `case _` le dice a mypy que ahí no debe llegar ningún valor. Borra las líneas 116 y 117 (el `case "alto"` y su `return`) y ejecuta mypy:

```
types_lab.py:117: error: Argument 1 to "assert_never" has incompatible type "Literal['alto']"; expected "Never"  [arg-type]
```

mypy ha visto que `"alto"` llega al `case _`: si mañana añades un nivel a `Level`, te dice en qué `match` falta. Vuelve a poner las dos líneas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'summary' is not defined` en el paso 2 | Descomenta antes el paso 1 |
| `Runtime type is 'str'` sale al final y no en su sitio | Lo escribe en stderr, que puede aparecer desordenado si rediriges la salida. En la terminal sale en orden |
| `error: unused "type: ignore" comment` | Ese comentario ya no tapa nada: bórralo o deja la línea como estaba |
| `SyntaxError` en `def first[T]` o en `type Record` | Tu Python es anterior a 3.12: comprueba que `uv run python --version` da 3.14.10 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · mypy estricto](../ejercicio-01-mypy-estricto/README.md) | **Ejercicio 02 · Tipos avanzados** | [Ejercicio 03 · Modelos de Pydantic](../ejercicio-03-modelos-pydantic/README.md) |
