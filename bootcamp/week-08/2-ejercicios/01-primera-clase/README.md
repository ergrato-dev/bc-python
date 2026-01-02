# 🎭 Ejercicio 1: Mi Primera Clase

## 🎯 Objetivo

Aprender a crear clases básicas en Python, entender el método `__init__` y usar `self` para definir atributos de instancia.

---

## 📋 Instrucciones

En este ejercicio crearás varias clases desde cero, practicando la sintaxis básica de POO en Python.

### Paso 1: Clase Simple

Crea una clase `Person` con atributos básicos:

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

### Paso 2: Agregar Métodos

Añade métodos a tu clase para que los objetos puedan realizar acciones:

```python
def greet(self) -> str:
    return f"Hola, soy {self.name}"

def is_adult(self) -> bool:
    return self.age >= 18
```

### Paso 3: Valores por Defecto

Crea una clase con parámetros opcionales:

```python
class Product:
    def __init__(
        self,
        name: str,
        price: float,
        quantity: int = 0
    ) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
```

### Paso 4: Clase Completa

Crea una clase `BankAccount` con:
- Atributos: `owner`, `balance`
- Métodos: `deposit()`, `withdraw()`, `get_balance()`

### Paso 5: Múltiples Instancias

Practica creando y manipulando múltiples objetos de tus clases.

---

## ✅ Verificación

Al completar el ejercicio, deberías poder:

```python
# Crear personas
person1 = Person("Ana", 25)
person2 = Person("Bob", 17)

print(person1.greet())      # Hola, soy Ana
print(person1.is_adult())   # True
print(person2.is_adult())   # False

# Crear cuenta bancaria
account = BankAccount("Ana", 1000)
account.deposit(500)
account.withdraw(200)
print(account.get_balance())  # 1300
```

---

## 💡 Consejos

- `self` siempre es el primer parámetro de los métodos de instancia
- Usa type hints en todos los parámetros y retornos
- Los atributos se definen con `self.nombre = valor`
- Cada objeto tiene sus propios valores de atributos

---

## 🔗 Recursos

- [Teoría: Clases y Objetos](../../1-teoria/02-clases-objetos.md)
- [Python Classes - Real Python](https://realpython.com/python3-object-oriented-programming/)
