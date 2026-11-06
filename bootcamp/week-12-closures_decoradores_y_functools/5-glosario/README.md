# Glosario — Semana 12

| Término | Definición |
|---|---|
| **`cache` / `lru_cache`** | Decoradores de `functools` que guardan el resultado de cada combinación de argumentos. `lru_cache(maxsize=n)` guarda solo los `n` usados más recientemente |
| **`cached_property`** | Como `@property`, pero calcula el valor una vez y lo guarda en el `__dict__` del objeto. No funciona con `slots=True` |
| **`Callable`** | Tipo de `collections.abc` para "algo que se puede llamar": `Callable[[float], bool]` recibe un `float` y devuelve un `bool` |
| **Celda** (*cell*) | Donde vive una variable que recuerda una closure; `f.__closure__` es la tupla de celdas |
| **Closure** | Función que recuerda las variables de la función que la rodeaba, aunque esta ya haya terminado |
| **Decorador** | Función que recibe una función (o una clase) y devuelve otra en su lugar. `@d` encima de `def f` equivale a `f = d(f)` |
| **Decorador con argumentos** | Función que recibe opciones y devuelve un decorador: `@rounded(1)` es `f = rounded(1)(f)` |
| **Fábrica de funciones** | Función que crea y devuelve otra función, como `above(limit)` |
| **Función de orden superior** | Función que recibe o devuelve funciones: `sorted` con `key=`, `map`, `Series.where`, cualquier decorador |
| **Función pura** | Función cuyo resultado solo depende de sus argumentos y que no cambia nada fuera. Solo esas se pueden cachear sin riesgo |
| ***Hit* / *miss*** | En una caché, encontrar el resultado ya guardado (*hit*) o tener que calcularlo (*miss*) |
| **`lambda`** | Función anónima de una sola expresión: `lambda v: v > 50` |
| ***Late binding*** | Una closure lee el valor de la variable al **llamarse**, no al crearse: la trampa de las `lambda` en un bucle |
| **LEGB** | Orden en que Python busca un nombre: *Local*, *Enclosing*, *Global*, *Built-in* |
| **`nonlocal`** | Declara que un nombre es el de la función que rodea a esta, para poder asignarlo |
| **`ParamSpec`** | Variable de tipo para los parámetros de una función (`[**P]`); con ella, un decorador conserva la firma de la función decorada |
| **`partial`** | Función de `functools` que fija algunos argumentos de otra: `partial(int, base=2)` |
| **`reduce`** | Función de `functools` que combina los elementos de dos en dos hasta dejar un valor |
| **`singledispatch`** | Decorador de `functools` que elige la versión de una función según el tipo del primer argumento; los tipos se añaden con `.register` |
| **`wraps`** | Decorador de `functools` para el `wrapper`: copia el nombre y el *docstring* de la original y la guarda en `__wrapped__` |
| ***Wrapper*** | La función interna de un decorador, la que se ejecuta en cada llamada y llama a la original |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
