# 03 · Funciones como valores

⏱️ 40 min

## 🎯 Objetivos

- Guardar una función en una variable y pasarla como argumento a otra.
- Ordenar y buscar con `key=` en `sorted`, `max` y `min`.
- Escribir una `lambda` y saber cuándo no usarla.
- Escribir una función recursiva con su caso base.

---

## 1. Una función es un objeto

En Python, una función es un valor como un número o un texto. El nombre de la función apunta a ella, y puedes darle otro nombre o pasarla a otra función:

```python
def initial(text: str) -> str:
    return text[0]

first = initial          # sin paréntesis: la función misma
print(first("Norte"))    # N
print(initial)           # <function initial at 0x...>
```

La diferencia entre `initial` y `initial("Norte")` es la de siempre: el primero **es** la función; el segundo la **llama** y es su resultado.

## 2. Pasar funciones a otras funciones

```python
def apply(function, texts: list[str]) -> list[str]:
    result = []
    for text in texts:
        result.append(function(text))
    return result

apply(str.upper, ["norte", "sur"])   # ['NORTE', 'SUR']
apply(initial, ["norte", "sur"])     # ['n', 's']
```

`apply` no sabe qué hará con cada texto: se lo dice quien llama. Es la forma de escribir una sola vez el bucle y cambiar solo lo que se hace dentro. Así funcionan muchas herramientas que usarás: pandas aplica tu función a cada fila (semana 24), FastAPI llama a tu función cuando llega una petición (semana 20) y pytest llama a tus `test_*` (teoría 05).

## 3. `key=`: decir por qué comparar

`sorted`, `max` y `min` aceptan un argumento `key`: una función que convierte cada elemento en el valor que se compara. Los elementos no cambian.

```python
stations = ["Occidente", "Sur", "Norte"]
sorted(stations)            # ['Norte', 'Occidente', 'Sur']   alfabético
sorted(stations, key=len)   # ['Sur', 'Norte', 'Occidente']   por longitud
max(stations, key=len)      # 'Occidente'
sorted(stations, key=str.casefold)   # alfabético sin distinguir mayúsculas
```

Un caso típico: ordenar textos que contienen números. Como texto, `"8"` va después de `"55,1"` (se compara carácter a carácter, y `"8" > "5"`):

```python
texts = ["12,5", "8", "55,1"]
sorted(texts)                                                   # ['12,5', '55,1', '8']
sorted(texts, key=lambda text: float(text.replace(",", ".")))   # ['8', '12,5', '55,1']
```

## 4. `lambda`

`lambda parámetros: expresión` crea una función pequeña sin nombre:

```python
lambda text: float(text.replace(",", "."))
```

es lo mismo que

```python
def to_number(text: str) -> float:
    return float(text.replace(",", "."))
```

| Usa `lambda` | Usa `def` |
|---|---|
| Una expresión corta que solo se usa como argumento (`key=`) | Más de una línea, o lógica que merece un nombre |
| | La vas a usar en más de un sitio |
| | La quieres probar con un test |

No asignes una `lambda` a una variable (`double = lambda n: n * 2`): para eso está `def`, que además da un nombre útil en los tracebacks.

## 5. Recursión

Una función **recursiva** se llama a sí misma con un problema más pequeño:

```python
def factorial(n: int) -> int:
    if n <= 1:          # caso base: se responde sin recursión
        return 1
    return n * factorial(n - 1)   # caso recursivo: se acerca al base
```

`factorial(4)` es `4 * factorial(3)`, que es `3 * factorial(2)`, que es `2 * factorial(1)`, que es `1`. Las llamadas se apilan y luego se resuelven en orden inverso: `2`, `6`, `24`.

Las dos reglas: siempre hay un **caso base**, y cada llamada se **acerca** a él. Si falla alguna, la recursión no termina y Python la corta hacia las 1 000 llamadas: `RecursionError: maximum recursion depth exceeded`.

En Python, un bucle suele ser más simple y más rápido que la recursión. La recursión brilla en estructuras que contienen otras como ellas: carpetas con carpetas dentro (semana 7), JSON anidado o árboles de decisión (semana 33).

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: 'str' object is not callable` | Pasaste `f(x)` (un resultado) donde se esperaba `f` (la función) | Quita los paréntesis |
| `TypeError: <lambda>() takes 1 positional argument but 2 were given` | La función de `key` debe recibir un solo argumento | Una `lambda` de un parámetro |
| Ordenado "mal" con números en texto | Se compararon como texto | `key=` que los convierta a número |
| `RecursionError` | Falta el caso base, o no se acerca a él | Revisa el `if` del caso base |

## ✅ Qué debes saber al terminar

- [ ] La diferencia entre `f` y `f()`.
- [ ] Cómo pasar una función a otra y para qué sirve.
- [ ] Qué hace `key=` en `sorted`, `max` y `min`.
- [ ] Cuándo usar `lambda` y cuándo `def`.
- [ ] Las dos reglas de una función recursiva.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Scope y efectos](02-scope-y-efectos.md) | **03 · Funciones como valores** | [04 · Type hints](04-type-hints.md) |
