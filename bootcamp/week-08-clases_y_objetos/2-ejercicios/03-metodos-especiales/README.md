# ✨ Ejercicio 3: Métodos Especiales (Dunder Methods)

## 🎯 Objetivo

Implementar métodos especiales para que tus clases se comporten como tipos nativos de Python.

---

## 📋 Instrucciones

### Paso 1: Representación (__str__ y __repr__)

Implementa cómo se muestra tu objeto:

```python
def __str__(self) -> str:
    return f"{self.name} - ${self.price:.2f}"

def __repr__(self) -> str:
    return f"Product('{self.name}', {self.price})"
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

### Paso 2: Comparación (__eq__, __lt__)

Permite comparar objetos entre sí:

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Product):
        return NotImplemented
    return self.name == other.name and self.price == other.price
```

### Paso 3: Longitud y Booleano (__len__, __bool__)

Haz que `len()` y evaluaciones booleanas funcionen:

```python
def __len__(self) -> int:
    return len(self.items)

def __bool__(self) -> bool:
    return len(self.items) > 0
```

### Paso 4: Acceso a Elementos (__getitem__)

Permite usar indexación con corchetes:

```python
def __getitem__(self, index: int) -> str:
    return self.items[index]
```

### Paso 5: Clase Completa

Combina todos los métodos especiales en una clase funcional.

---

## ✅ Verificación

```python
# Representación
product = Product("Laptop", 999.99)
print(product)       # Laptop - $999.99
print(repr(product)) # Product('Laptop', 999.99)

# Comparación
p1 = Product("Mouse", 29.99)
p2 = Product("Mouse", 29.99)
print(p1 == p2)  # True

# Contenedor
cart = ShoppingCart()
cart.add("Item 1")
print(len(cart))     # 1
print(bool(cart))    # True
print(cart[0])       # Item 1
```

---

## 💡 Consejos

- `__str__` es para usuarios, `__repr__` para desarrolladores
- Si implementas `__eq__`, considera también `__hash__` para usar en sets/dicts
- Usa `@total_ordering` de `functools` para generar comparadores automáticamente
- Retorna `NotImplemented` (no `raise`) cuando el tipo no es compatible

---

## 🔗 Recursos

- [Teoría: Métodos Especiales](../../1-teoria/04-metodos-especiales.md)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
