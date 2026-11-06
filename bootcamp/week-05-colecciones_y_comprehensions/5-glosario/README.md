# Glosario — Semana 05

| Término | Definición |
|---|---|
| **Agrupar** (*group by*) | Juntar los valores que comparten una clave: `{"Norte": [12.5, 48.9]}` |
| **Alias** | Otro nombre para el mismo objeto: después de `b = a`, cambiar `b` cambia `a` |
| **Alias de tipo** | Un nombre para una anotación larga: `Record = tuple[str, float \| None]` |
| **Clave** | En un diccionario, lo que se usa para buscar un valor; única y hashable |
| **Comprehension** | Expresión que construye una lista, un diccionario o un conjunto recorriendo un iterable: `[x * 2 for x in xs if x > 0]` |
| **Conjunto** (`set`) | Colección sin repetidos y sin orden; `in` es casi instantáneo |
| **Copia profunda** | Copia de un objeto y de todo lo que contiene, a todos los niveles: `copy.deepcopy(x)` |
| **Copia superficial** | Objeto nuevo cuyos elementos son los mismos objetos que los del original: `.copy()`, `list(x)`, `x[:]` |
| **Desempaquetar** | Repartir las partes de una secuencia en varios nombres: `label, value = record` |
| **Diccionario** (`dict`) | Colección de parejas clave → valor que busca por la clave y recuerda el orden de inserción |
| **Expresión condicional** | `a if condición else b`: vale `a` o `b` según la condición |
| **Expresión generadora** | Comprehension entre paréntesis: da los valores de uno en uno, sin crear la lista, y se agota |
| **Generador** | Objeto que produce valores cuando se le piden y solo se puede recorrer una vez |
| **Hash** | Número que Python calcula a partir de un valor para guardarlo y encontrarlo rápido en un diccionario o un set |
| **Hashable** | Que tiene un hash que no cambia: textos, números, tuplas de hashables. Las listas y los diccionarios no lo son |
| **Inmutable** | Que no se puede cambiar después de crearse: números, textos, tuplas |
| **`is`** | Pregunta si dos nombres apuntan al mismo objeto; `==` pregunta si tienen el mismo contenido |
| **Lista** (`list`) | Secuencia ordenada y mutable, normalmente de elementos del mismo tipo |
| **Mutable** | Que se puede cambiar en su sitio: listas, diccionarios, conjuntos |
| **Registro** | Los datos de una medida juntos; en el Observatorio, la tupla `(etiqueta, valor)` |
| **`setdefault`** | `d.setdefault(clave, defecto)`: devuelve el valor de la clave y, si no existía, guarda antes el valor por defecto |
| **`sorted`** | Devuelve una lista nueva y ordenada a partir de cualquier iterable; `.sort()` ordena la lista misma y devuelve `None` |
| **Tupla** (`tuple`) | Secuencia ordenada e inmutable; la coma la crea: `1, 2` o `(1,)` |
| **Unión, intersección, diferencia** | `a \| b` (en alguno), `a & b` (en los dos), `a - b` (en `a` y no en `b`) |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
