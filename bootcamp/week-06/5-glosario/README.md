# 📖 Glosario - Semana 6: Diccionarios

## A

### Acceso por Clave (Key Access)
Operación para obtener el valor asociado a una clave en un diccionario.
```python
value = my_dict["key"]  # Lanza KeyError si no existe
value = my_dict.get("key")  # Retorna None si no existe
```

### Aplanar (Flatten)
Convertir una estructura anidada en una estructura plana de un solo nivel.
```python
nested = {"a": {"b": 1}}
flat = {"a.b": 1}
```

---

## C

### Clave (Key)
Identificador único que se usa para acceder a un valor en un diccionario. Debe ser un tipo hashable (inmutable).
```python
my_dict = {"name": "Alice"}  # "name" es la clave
```

### Comprehension de Diccionario (Dict Comprehension)
Sintaxis concisa para crear diccionarios a partir de iterables.
```python
squares = {x: x**2 for x in range(5)}
```

### Copy (Copia)
Crear un duplicado de un diccionario. Puede ser superficial o profunda.
```python
shallow = original.copy()  # Copia superficial
deep = copy.deepcopy(original)  # Copia profunda
```

### CRUD
Acrónimo para las cuatro operaciones básicas: Create, Read, Update, Delete.

---

## D

### Deepcopy (Copia Profunda)
Copia que duplica también los objetos anidados, creando copias completamente independientes.
```python
import copy
deep = copy.deepcopy(original)
```

### Dict (Diccionario)
Estructura de datos que almacena pares clave-valor. También conocido como "mapping" o "hash map".
```python
person = {"name": "Alice", "age": 30}
```

### dict.fromkeys()
Método de clase para crear un diccionario con claves predefinidas y un valor por defecto.
```python
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)  # {'a': 0, 'b': 0, 'c': 0}
```

---

## E

### Estructura Anidada (Nested Structure)
Diccionario que contiene otros diccionarios como valores.
```python
company = {
    "dept": {
        "employee": {"name": "Alice"}
    }
}
```

---

## F

### Filtrar (Filter)
Crear un nuevo diccionario con solo los elementos que cumplen una condición.
```python
adults = {k: v for k, v in people.items() if v >= 18}
```

---

## G

### get()
Método seguro para acceder a valores que retorna None (o un valor por defecto) si la clave no existe.
```python
value = my_dict.get("key", "default")
```

---

## H

### Hashable
Propiedad de un objeto que permite usarlo como clave de diccionario. Los tipos inmutables (str, int, tuple) son hashables.
```python
# ✅ Válido: tipos hashables como claves
d = {"string": 1, 42: 2, (1, 2): 3}

# ❌ Inválido: listas no son hashables
# d = {[1, 2]: "value"}  # TypeError
```

### Hash Table
Estructura de datos subyacente que implementa los diccionarios en Python, permitiendo acceso O(1).

---

## I

### Inmutable (Immutable)
Objeto cuyo valor no puede cambiar después de crearse. Necesario para ser clave de diccionario.

### items()
Método que retorna una vista de los pares (clave, valor) del diccionario.
```python
for key, value in my_dict.items():
    print(f"{key}: {value}")
```

### Iterar (Iterate)
Recorrer los elementos de un diccionario, típicamente con un bucle for.
```python
for key in my_dict:  # Itera sobre claves
for value in my_dict.values():  # Itera sobre valores
for key, value in my_dict.items():  # Itera sobre pares
```

---

## K

### KeyError
Excepción lanzada cuando se intenta acceder a una clave que no existe usando corchetes.
```python
try:
    value = my_dict["nonexistent"]
except KeyError:
    print("La clave no existe")
```

### keys()
Método que retorna una vista de las claves del diccionario.
```python
claves = my_dict.keys()  # dict_keys(['a', 'b', 'c'])
```

---

## L

### Literal de Diccionario
Sintaxis para crear diccionarios directamente con llaves.
```python
my_dict = {"key1": "value1", "key2": "value2"}
```

---

## M

### Mapping
Tipo abstracto que representa una colección de pares clave-valor. dict es el mapping más común en Python.

### Merge (Fusionar)
Combinar dos o más diccionarios en uno solo.
```python
merged = dict1 | dict2  # Python 3.9+
dict1.update(dict2)  # Modifica dict1 in-place
```

---

## N

### Nested (Anidado)
Ver "Estructura Anidada".

---

## O

### Operador | (Pipe/Union)
Operador introducido en Python 3.9 para combinar diccionarios.
```python
combined = dict1 | dict2  # Crea nuevo diccionario
dict1 |= dict2  # Actualiza dict1 in-place
```

---

## P

### Par Clave-Valor (Key-Value Pair)
Unidad fundamental de un diccionario, compuesta por una clave única y su valor asociado.

### pop()
Método que elimina una clave y retorna su valor.
```python
value = my_dict.pop("key")  # Elimina y retorna
value = my_dict.pop("key", "default")  # Con valor por defecto
```

### popitem()
Método que elimina y retorna el último par clave-valor insertado (LIFO).
```python
key, value = my_dict.popitem()
```

---

## S

### setdefault()
Método que retorna el valor de una clave, o lo crea con un valor por defecto si no existe.
```python
# Si "count" no existe, lo crea con valor 0
count = my_dict.setdefault("count", 0)
```

### Shallow Copy (Copia Superficial)
Copia que duplica el diccionario pero mantiene referencias a los objetos internos.
```python
shallow = original.copy()  # Objetos internos compartidos
```

---

## U

### update()
Método que actualiza un diccionario con pares clave-valor de otro diccionario o iterable.
```python
my_dict.update({"new_key": "new_value"})
my_dict.update(key1="value1", key2="value2")
```

---

## V

### Valor (Value)
El dato almacenado en un diccionario, asociado a una clave. Puede ser de cualquier tipo.
```python
my_dict = {"name": "Alice"}  # "Alice" es el valor
```

### values()
Método que retorna una vista de los valores del diccionario.
```python
valores = my_dict.values()  # dict_values(['Alice', 30])
```

### Vista (View)
Objeto dinámico retornado por keys(), values() e items() que refleja el estado actual del diccionario.
```python
keys = my_dict.keys()  # Vista, no copia
my_dict["new"] = 1
# keys ahora incluye "new" automáticamente
```

---

## 🔗 Navegación

- 🏠 **Índice**: [README Semana 6](../README.md)
