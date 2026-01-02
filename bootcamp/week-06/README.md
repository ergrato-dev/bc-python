# 📚 Semana 06: Diccionarios

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana serás capaz de:

- ✅ Crear y manipular diccionarios en Python
- ✅ Usar métodos de diccionarios (`get`, `keys`, `values`, `items`)
- ✅ Iterar sobre diccionarios de diferentes formas
- ✅ Aplicar dictionary comprehensions
- ✅ Trabajar con diccionarios anidados
- ✅ Elegir entre diccionarios y otras estructuras de datos

---

## 📋 Contenido

### 1. Teoría

| Archivo | Tema | Duración |
|---------|------|----------|
| [01-intro-diccionarios.md](1-teoria/01-intro-diccionarios.md) | Introducción a Diccionarios | 25 min |
| [02-metodos-diccionarios.md](1-teoria/02-metodos-diccionarios.md) | Métodos de Diccionarios | 25 min |
| [03-iteracion-diccionarios.md](1-teoria/03-iteracion-diccionarios.md) | Iteración sobre Diccionarios | 20 min |
| [04-dict-comprehensions.md](1-teoria/04-dict-comprehensions.md) | Dictionary Comprehensions | 20 min |

### 2. Ejercicios

| Ejercicio | Tema | Duración |
|-----------|------|----------|
| [01-crud-diccionarios](2-ejercicios/01-crud-diccionarios/) | Crear, leer, actualizar, eliminar | 40 min |
| [02-metodos-avanzados](2-ejercicios/02-metodos-avanzados/) | Métodos y operaciones | 40 min |
| [03-diccionarios-anidados](2-ejercicios/03-diccionarios-anidados/) | Estructuras complejas | 45 min |

### 3. Proyecto

| Proyecto | Descripción | Duración |
|----------|-------------|----------|
| [Gestor de Contactos](3-proyecto/) | Sistema CRUD con diccionarios anidados | 90 min |

---

## 🗂️ Estructura de la Semana

```
week-06/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── week-06-header.svg
│   ├── 01-dict-anatomy.svg
│   ├── 02-dict-methods.svg
│   ├── 03-dict-iteration.svg
│   └── 04-nested-dicts.svg
├── 1-teoria/
│   ├── 01-intro-diccionarios.md
│   ├── 02-metodos-diccionarios.md
│   ├── 03-iteracion-diccionarios.md
│   └── 04-dict-comprehensions.md
├── 2-ejercicios/
│   ├── 01-crud-diccionarios/
│   ├── 02-metodos-avanzados/
│   └── 03-diccionarios-anidados/
├── 3-proyecto/
│   ├── README.md
│   └── starter/
├── 4-recursos/
│   ├── ebooks-free/
│   ├── videografia/
│   └── webgrafia/
└── 5-glosario/
    └── README.md
```

---

## ⏱️ Distribución del Tiempo

| Actividad | Tiempo |
|-----------|--------|
| Teoría | 1.5 horas |
| Ejercicios | 2 horas |
| Proyecto | 1.5 horas |
| **Total** | **5 horas** |

---

## 📚 Requisitos Previos

Antes de comenzar esta semana, debes:

- ✅ Dominar listas y sus métodos
- ✅ Entender tuplas y su inmutabilidad
- ✅ Conocer slicing y comprensiones de listas
- ✅ Manejar funciones con parámetros y retorno

---

## 🔑 Conceptos Clave

### ¿Qué es un Diccionario?

Un **diccionario** es una estructura de datos que almacena pares **clave-valor**:

```python
# Sintaxis básica
student: dict[str, any] = {
    "name": "Alice",
    "age": 25,
    "courses": ["Python", "Data Science"]
}

# Acceso por clave
print(student["name"])  # "Alice"

# Método get (más seguro)
print(student.get("email", "N/A"))  # "N/A"
```

### Características Principales

| Característica | Descripción |
|----------------|-------------|
| **Mutables** | Se pueden modificar después de crear |
| **No ordenados** | Desde Python 3.7+, mantienen orden de inserción |
| **Claves únicas** | No puede haber claves duplicadas |
| **Claves hashables** | Solo tipos inmutables como claves |
| **Valores cualquiera** | Los valores pueden ser de cualquier tipo |

### Operaciones Comunes

```python
# Crear
contacts = {"Alice": "555-1234", "Bob": "555-5678"}

# Leer
phone = contacts["Alice"]

# Actualizar
contacts["Alice"] = "555-0000"

# Eliminar
del contacts["Bob"]

# Verificar existencia
if "Alice" in contacts:
    print("Encontrado!")
```

---

## 📌 Entregables

1. **Ejercicios completados** (3 ejercicios)
2. **Proyecto funcional** (Gestor de Contactos)
3. **Código con type hints** y documentación

---

## 🔗 Navegación

← [Semana 05: Listas y Tuplas](../week-05/) | [Inicio](../../README.md) | [Semana 07: Sets](../week-07/) →
