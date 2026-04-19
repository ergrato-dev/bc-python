# 🎯 Ejercicio 2: Atributos y Métodos Avanzados

## 🎯 Objetivo

Dominar los diferentes tipos de atributos (clase vs instancia) y métodos (instancia, clase y estáticos) en Python.

---

## 📋 Instrucciones

### Paso 1: Atributos de Clase vs Instancia

Entiende la diferencia entre atributos compartidos y únicos:

```python
class Employee:
    # Atributo de clase - compartido
    company_name: str = "TechCorp"
    employee_count: int = 0

    def __init__(self, name: str) -> None:
        # Atributos de instancia - únicos
        self.name = name
        Employee.employee_count += 1
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

### Paso 2: Métodos de Clase (@classmethod)

Aprende a crear métodos que operan sobre la clase, no la instancia:

```python
@classmethod
def from_string(cls, data: str) -> "Employee":
    """Factory method para crear desde string."""
    name, department = data.split(",")
    return cls(name, department)
```

### Paso 3: Métodos Estáticos (@staticmethod)

Crea utilidades que pertenecen a la clase pero no necesitan acceso a instancia ni clase:

```python
@staticmethod
def is_valid_email(email: str) -> bool:
    """Valida formato de email."""
    return "@" in email and "." in email
```

### Paso 4: Combinando Todo

Crea una clase completa que use los tres tipos de métodos.

### Paso 5: Properties

Aprende a controlar el acceso a atributos con `@property`.

---

## ✅ Verificación

```python
# Atributos de clase
print(Employee.company_name)  # TechCorp
print(Employee.employee_count)  # Número de empleados creados

# Factory methods
emp = Employee.from_string("Ana,Engineering")
print(emp.name)  # Ana

# Métodos estáticos
print(Employee.is_valid_email("test@email.com"))  # True
```

---

## 💡 Consejos

- `@classmethod` recibe `cls` (la clase) como primer parámetro
- `@staticmethod` no recibe ni `self` ni `cls`
- Usa atributos de clase para datos compartidos (contadores, constantes)
- Factory methods son `@classmethod` que retornan nuevas instancias

---

## 🔗 Recursos

- [Teoría: Atributos y Métodos](../../1-teoria/03-atributos-metodos.md)
- [Python @classmethod vs @staticmethod](https://realpython.com/instance-class-and-static-methods-demystified/)
