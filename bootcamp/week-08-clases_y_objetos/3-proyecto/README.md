# 📚 Proyecto: Sistema de Biblioteca

## 🎯 Objetivo

Crear un sistema de gestión de biblioteca que aplique todos los conceptos de POO aprendidos: clases, atributos, métodos, métodos especiales y diferentes tipos de métodos.

---

## 📋 Descripción

Desarrollarás un sistema con tres clases principales:

1. **Book**: Representa un libro en la biblioteca
2. **User**: Representa un usuario que puede pedir préstamos
3. **Loan**: Representa un préstamo de libro

---

## 🏗️ Estructura del Proyecto

```
starter/
├── main.py           # Punto de entrada y demostración
├── models/
│   ├── __init__.py   # Exports de los modelos
│   ├── book.py       # Clase Book
│   ├── user.py       # Clase User
│   └── loan.py       # Clase Loan
└── library.py        # Clase Library (gestor principal)
```

---

## 📝 Requisitos

### Clase Book

**Atributos de clase:**
- `total_books: int` - Contador de libros creados

**Atributos de instancia:**
- `title: str` - Título del libro
- `author: str` - Autor
- `isbn: str` - Código ISBN
- `year: int` - Año de publicación
- `is_available: bool` - Disponibilidad (default: True)

**Métodos:**
- `__init__()` - Constructor con validación de ISBN
- `__str__()` - Formato: "Título por Autor (Año)"
- `__repr__()` - Formato técnico
- `__eq__()` - Dos libros son iguales si tienen el mismo ISBN
- `__hash__()` - Para usar en sets/dicts
- `get_age()` - Retorna antigüedad del libro
- `@classmethod from_dict()` - Factory method
- `@staticmethod is_valid_isbn()` - Valida formato ISBN

### Clase User

**Atributos de clase:**
- `total_users: int` - Contador de usuarios

**Atributos de instancia:**
- `user_id: str` - ID único del usuario
- `name: str` - Nombre completo
- `email: str` - Email
- `active_loans: list[Loan]` - Préstamos activos
- `loan_history: list[Loan]` - Historial de préstamos

**Métodos:**
- `__init__()` - Constructor
- `__str__()` - Formato legible
- `__repr__()` - Formato técnico
- `__eq__()` - Igualdad por user_id
- `can_borrow()` - Verifica si puede pedir préstamos (max 3)
- `add_loan()` - Agrega préstamo activo
- `return_loan()` - Procesa devolución
- `@classmethod from_dict()` - Factory method
- `@staticmethod generate_id()` - Genera ID único

### Clase Loan

**Atributos de instancia:**
- `loan_id: str` - ID único del préstamo
- `book: Book` - Libro prestado
- `user: User` - Usuario que pidió el préstamo
- `loan_date: date` - Fecha del préstamo
- `due_date: date` - Fecha de vencimiento
- `return_date: date | None` - Fecha de devolución (None si no devuelto)
- `is_returned: bool` - Estado del préstamo

**Métodos:**
- `__init__()` - Constructor (calcula due_date automáticamente)
- `__str__()` - Formato legible
- `__repr__()` - Formato técnico
- `is_overdue()` - Verifica si está vencido
- `days_until_due()` - Días hasta vencimiento
- `complete_return()` - Marca como devuelto
- `@staticmethod generate_loan_id()` - Genera ID único

### Clase Library

**Atributos:**
- `name: str` - Nombre de la biblioteca
- `books: dict[str, Book]` - Libros indexados por ISBN
- `users: dict[str, User]` - Usuarios indexados por ID
- `loans: list[Loan]` - Todos los préstamos

**Métodos:**
- `add_book()` - Agrega libro a la colección
- `remove_book()` - Elimina libro
- `register_user()` - Registra nuevo usuario
- `borrow_book()` - Procesa préstamo
- `return_book()` - Procesa devolución
- `search_books()` - Busca libros por título/autor
- `get_available_books()` - Lista libros disponibles
- `get_overdue_loans()` - Lista préstamos vencidos
- `get_statistics()` - Estadísticas de la biblioteca

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| Clases correctamente definidas | 20 |
| Atributos de clase e instancia | 15 |
| Métodos especiales (`__str__`, `__repr__`, `__eq__`) | 20 |
| Factory methods (`@classmethod`) | 15 |
| Métodos estáticos (`@staticmethod`) | 10 |
| Type hints completos | 10 |
| Documentación (docstrings) | 10 |

---

## 🚀 Cómo Empezar

1. Revisa los archivos en `starter/`
2. Completa las clases en `models/`
3. Implementa la clase `Library`
4. Ejecuta `main.py` para probar

```bash
cd starter
python main.py
```

---

## 💡 Consejos

- Empieza por `Book`, es la más simple
- Usa `uuid` para generar IDs únicos
- `datetime.date.today()` para fecha actual
- Implementa `__eq__` y `__hash__` juntos
- Prueba cada clase antes de pasar a la siguiente

---

## 🎯 Entregables

1. Código completo de las 4 clases
2. `main.py` con demostración funcional
3. Al menos 3 libros y 2 usuarios de prueba
4. Demostrar: agregar libros, registrar usuarios, hacer préstamos, devoluciones

---

## 📚 Recursos

- [Teoría: Clases y Objetos](../../1-teoria/02-clases-objetos.md)
- [Teoría: Métodos Especiales](../../1-teoria/04-metodos-especiales.md)
- [Python datetime](https://docs.python.org/3/library/datetime.html)
- [Python uuid](https://docs.python.org/3/library/uuid.html)
