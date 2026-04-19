# ⚙️ Parámetros Avanzados

## 🎯 Objetivos de Aprendizaje

- Diferenciar parámetros posicionales y keyword
- Usar valores por defecto correctamente
- Dominar `*args` para argumentos variables
- Dominar `**kwargs` para argumentos con nombre
- Combinar diferentes tipos de parámetros

---

## 1. Parámetros vs Argumentos

Es importante distinguir estos términos:

```python
# 'name' y 'age' son PARÁMETROS (en la definición)
def greet(name: str, age: int) -> str:
    return f"{name} tiene {age} años"

# "Ana" y 25 son ARGUMENTOS (en la llamada)
greet("Ana", 25)
```

| Término | Dónde | Ejemplo |
|---------|-------|---------|
| **Parámetro** | Definición de función | `def func(param):` |
| **Argumento** | Llamada a función | `func(arg)` |

---

## 2. Argumentos Posicionales

Los argumentos se asignan **por posición**:

```python
def describe_pet(animal: str, name: str) -> str:
    return f"Tengo un {animal} llamado {name}"

# Argumentos posicionales - el orden importa
print(describe_pet("perro", "Max"))   # Tengo un perro llamado Max
print(describe_pet("Max", "perro"))   # Tengo un Max llamado perro (¡mal!)
```

---

## 3. Argumentos Keyword (con nombre)

Puedes especificar argumentos **por nombre**, sin importar el orden:

```python
def describe_pet(animal: str, name: str) -> str:
    return f"Tengo un {animal} llamado {name}"

# Argumentos keyword - el orden no importa
print(describe_pet(animal="gato", name="Luna"))  # Tengo un gato llamado Luna
print(describe_pet(name="Luna", animal="gato"))  # Tengo un gato llamado Luna

# Mezclar posicional y keyword
print(describe_pet("pez", name="Nemo"))  # Tengo un pez llamado Nemo
```

### ⚠️ Regla Importante

Los argumentos posicionales deben ir **antes** de los keyword:

```python
# ✅ CORRECTO
describe_pet("perro", name="Max")

# ❌ ERROR - posicional después de keyword
# describe_pet(animal="perro", "Max")  # SyntaxError
```

---

## 4. Valores por Defecto

Puedes dar valores predeterminados a los parámetros:

```python
def greet(name: str, greeting: str = "Hola") -> str:
    """Saluda a una persona.

    Args:
        name: Nombre de la persona.
        greeting: Saludo a usar (default: "Hola").
    """
    return f"{greeting}, {name}!"

# Usar valor por defecto
print(greet("Ana"))           # Hola, Ana!

# Sobrescribir valor por defecto
print(greet("Bob", "Hi"))     # Hi, Bob!
print(greet("Carlos", greeting="Buenos días"))  # Buenos días, Carlos!
```

### Orden de Parámetros

Los parámetros con default deben ir **después** de los sin default:

```python
# ✅ CORRECTO - sin default primero
def create_user(name: str, age: int, active: bool = True) -> dict:
    return {"name": name, "age": age, "active": active}

# ❌ ERROR - default antes de sin default
# def create_user(name: str = "Unknown", age: int) -> dict:  # SyntaxError
```

### ⚠️ Cuidado con Mutables como Default

```python
# ❌ PELIGROSO - lista mutable como default
def add_item(item: str, items: list = []) -> list:
    items.append(item)
    return items

# El mismo objeto lista se reutiliza
print(add_item("a"))  # ['a']
print(add_item("b"))  # ['a', 'b'] - ¡Acumuló el anterior!

# ✅ SOLUCIÓN - usar None y crear dentro
def add_item(item: str, items: list | None = None) -> list:
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item("a"))  # ['a']
print(add_item("b"))  # ['b'] - Nueva lista cada vez
```

---

## 5. *args - Argumentos Posicionales Variables

El `*args` permite recibir **cualquier cantidad** de argumentos posicionales:

```python
def sum_all(*numbers: int) -> int:
    """Suma cualquier cantidad de números.

    Args:
        *numbers: Números a sumar (cantidad variable).
    """
    total = 0
    for num in numbers:
        total += num
    return total

# Llamar con diferente cantidad de argumentos
print(sum_all(1, 2))           # 3
print(sum_all(1, 2, 3, 4, 5))  # 15
print(sum_all(10))             # 10
print(sum_all())               # 0

# 'numbers' es una tupla dentro de la función
def show_args(*args):
    print(type(args))  # <class 'tuple'>
    print(args)

show_args(1, 2, 3)  # (1, 2, 3)
```

### Combinar con Parámetros Regulares

```python
def greet_all(greeting: str, *names: str) -> list[str]:
    """Saluda a múltiples personas.

    Args:
        greeting: El saludo a usar.
        *names: Nombres de personas a saludar.
    """
    return [f"{greeting}, {name}!" for name in names]

print(greet_all("Hola", "Ana", "Bob", "Carlos"))
# ['Hola, Ana!', 'Hola, Bob!', 'Hola, Carlos!']
```

### Desempaquetar Lista en Llamada

```python
def add(a: int, b: int, c: int) -> int:
    return a + b + c

numbers = [1, 2, 3]

# ❌ Esto no funciona
# add(numbers)  # TypeError: falta b y c

# ✅ Desempaquetar con *
print(add(*numbers))  # 6
```

---

## 6. **kwargs - Argumentos Keyword Variables

El `**kwargs` permite recibir **cualquier cantidad** de argumentos con nombre:

```python
def print_info(**info: str) -> None:
    """Imprime información como pares clave-valor.

    Args:
        **info: Pares clave-valor de información.
    """
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Ana", age=25, city="Madrid")
# name: Ana
# age: 25
# city: Madrid

# 'info' es un diccionario dentro de la función
def show_kwargs(**kwargs):
    print(type(kwargs))  # <class 'dict'>
    print(kwargs)

show_kwargs(a=1, b=2)  # {'a': 1, 'b': 2}
```

### Combinar con Parámetros Regulares

```python
def create_profile(name: str, **details: str | int) -> dict:
    """Crea un perfil de usuario.

    Args:
        name: Nombre requerido.
        **details: Detalles adicionales opcionales.
    """
    profile = {"name": name}
    profile.update(details)
    return profile

user = create_profile("Ana", age=25, city="Madrid", job="Developer")
print(user)
# {'name': 'Ana', 'age': 25, 'city': 'Madrid', 'job': 'Developer'}
```

### Desempaquetar Diccionario en Llamada

```python
def greet(name: str, greeting: str = "Hola") -> str:
    return f"{greeting}, {name}!"

config = {"name": "Bob", "greeting": "Hi"}

# ✅ Desempaquetar con **
print(greet(**config))  # Hi, Bob!
```

---

## 7. Combinando Todo

El orden de parámetros debe ser:

1. Parámetros posicionales regulares
2. `*args`
3. Parámetros keyword-only (después de `*`)
4. `**kwargs`

```python
def complex_function(
    required: str,           # 1. Posicional requerido
    optional: str = "default",  # 2. Posicional con default
    *args: int,              # 3. *args
    keyword_only: str = "kw",  # 4. Keyword-only (después de *)
    **kwargs: str            # 5. **kwargs
) -> None:
    print(f"required: {required}")
    print(f"optional: {optional}")
    print(f"args: {args}")
    print(f"keyword_only: {keyword_only}")
    print(f"kwargs: {kwargs}")

complex_function(
    "valor1",
    "valor2",
    1, 2, 3,
    keyword_only="especial",
    extra="adicional"
)
# required: valor1
# optional: valor2
# args: (1, 2, 3)
# keyword_only: especial
# kwargs: {'extra': 'adicional'}
```

---

## 8. Parámetros Keyword-Only

Parámetros después de `*` o `*args` son **keyword-only**:

```python
def search(query: str, *, case_sensitive: bool = False) -> list:
    """Busca con opción solo por keyword.

    El * fuerza a que case_sensitive solo se pueda
    pasar como keyword argument.
    """
    # implementación...
    pass

# ✅ CORRECTO - como keyword
search("python", case_sensitive=True)

# ❌ ERROR - como posicional
# search("python", True)  # TypeError
```

### Uso Práctico

```python
# Evitar errores de orden en funciones con booleanos
def delete_user(user_id: int, *, confirm: bool = False) -> bool:
    """Elimina un usuario.

    Args:
        user_id: ID del usuario.
        confirm: Debe ser True para confirmar (keyword-only).
    """
    if not confirm:
        raise ValueError("Debe confirmar con confirm=True")
    # eliminar usuario...
    return True

# Claro qué significa el True
delete_user(123, confirm=True)

# No accidental: delete_user(123, True) daría error
```

---

## 9. Parámetros Positional-Only (Python 3.8+)

Parámetros antes de `/` son **positional-only**:

```python
def greet(name: str, /, greeting: str = "Hola") -> str:
    """El parámetro name solo puede pasarse por posición."""
    return f"{greeting}, {name}!"

# ✅ CORRECTO
greet("Ana")
greet("Ana", "Hi")
greet("Ana", greeting="Hi")

# ❌ ERROR - name es positional-only
# greet(name="Ana")  # TypeError
```

### Sintaxis Completa

```python
def func(pos_only, /, standard, *, kw_only):
    """
    pos_only: Solo posicional (antes de /)
    standard: Posicional o keyword (entre / y *)
    kw_only: Solo keyword (después de *)
    """
    pass

# Uso
func(1, 2, kw_only=3)        # ✅
func(1, standard=2, kw_only=3)  # ✅
# func(pos_only=1, ...)      # ❌ Error
# func(1, 2, 3)              # ❌ Error (kw_only debe ser keyword)
```

---

## 10. Ejemplos Prácticos

### Logger Flexible

```python
def log(message: str, *tags: str, level: str = "INFO", **metadata) -> None:
    """Registra un mensaje con tags y metadata.

    Args:
        message: Mensaje a registrar.
        *tags: Tags para categorizar.
        level: Nivel de log (INFO, WARNING, ERROR).
        **metadata: Información adicional.
    """
    tag_str = f"[{', '.join(tags)}]" if tags else ""
    meta_str = " ".join(f"{k}={v}" for k, v in metadata.items())
    print(f"[{level}] {tag_str} {message} {meta_str}")

log("Usuario creado", "auth", "user", user_id=123, ip="192.168.1.1")
# [INFO] [auth, user] Usuario creado user_id=123 ip=192.168.1.1

log("Error de conexión", level="ERROR", service="database")
# [ERROR]  Error de conexión service=database
```

### Constructor de HTML

```python
def html_tag(tag: str, content: str = "", **attributes: str) -> str:
    """Genera un elemento HTML.

    Args:
        tag: Nombre del tag (div, p, a, etc.)
        content: Contenido interno del tag.
        **attributes: Atributos HTML (class_, href, id, etc.)

    Note:
        Usa class_ en lugar de class (palabra reservada).
    """
    # Convertir class_ a class
    attrs = {k.rstrip("_"): v for k, v in attributes.items()}
    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())

    if attr_str:
        return f"<{tag} {attr_str}>{content}</{tag}>"
    return f"<{tag}>{content}</{tag}>"

print(html_tag("div", "Hello", class_="container", id="main"))
# <div class="container" id="main">Hello</div>

print(html_tag("a", "Click here", href="https://python.org"))
# <a href="https://python.org">Click here</a>
```

---

## ✅ Checklist de Verificación

- [ ] Distingo entre parámetro y argumento
- [ ] Sé usar argumentos posicionales y keyword
- [ ] Entiendo el orden de parámetros con defaults
- [ ] Evito usar mutables como valores por defecto
- [ ] Puedo usar `*args` para argumentos variables
- [ ] Puedo usar `**kwargs` para keywords variables
- [ ] Sé desempaquetar listas con `*` y dicts con `**`
- [ ] Entiendo keyword-only y positional-only parameters

---

## 📚 Recursos Adicionales

- [Python Docs - More on Functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [PEP 3102 - Keyword-Only Arguments](https://peps.python.org/pep-3102/)
- [PEP 570 - Positional-Only Parameters](https://peps.python.org/pep-0570/)

---

*Siguiente: [Return y Scope](05-return-scope.md)* ➡️
