# Proyecto Semana 6: Gestor de Contactos 📇

## 🎯 Objetivo

Crear un sistema de gestión de contactos que permita almacenar, buscar, actualizar y organizar información de personas usando diccionarios como estructura de datos principal.

---

## 📋 Descripción

Desarrollarás un gestor de contactos con las siguientes funcionalidades:

1. **CRUD de contactos**: Crear, leer, actualizar y eliminar
2. **Búsqueda**: Por nombre, email o etiquetas
3. **Organización**: Etiquetas/grupos para categorizar contactos
4. **Exportación**: Generar resumen de contactos
5. **Estadísticas**: Análisis de la agenda

---

## 🏗️ Estructura del Proyecto

```
3-proyecto/
├── README.md          # Este archivo
├── starter/
│   └── main.py        # Código inicial con TODOs
└── solution/
    └── main.py        # Solución completa (solo instructores)
```

---

## 📝 Requisitos Funcionales

### 1. Estructura de Datos

Cada contacto debe tener:

```python
contact = {
    "id": 1,                          # Identificador único
    "name": "Alice Johnson",          # Nombre completo
    "email": "alice@example.com",     # Email (único)
    "phone": "+1-555-0101",           # Teléfono
    "tags": ["work", "important"],    # Etiquetas/categorías
    "notes": "Project manager",       # Notas adicionales
    "created_at": "2026-01-02"        # Fecha de creación
}
```

La agenda completa es un diccionario donde la clave es el ID:

```python
contacts: dict[int, dict] = {
    1: {...},
    2: {...}
}
```

### 2. Funciones a Implementar

| Función | Descripción |
|---------|-------------|
| `create_contact()` | Crear nuevo contacto con ID autoincremental |
| `get_contact()` | Obtener contacto por ID |
| `update_contact()` | Actualizar campos de un contacto |
| `delete_contact()` | Eliminar contacto por ID |
| `search_by_name()` | Buscar contactos por nombre (parcial) |
| `search_by_email()` | Buscar contacto por email exacto |
| `search_by_tag()` | Buscar contactos por etiqueta |
| `add_tag()` | Agregar etiqueta a un contacto |
| `remove_tag()` | Eliminar etiqueta de un contacto |
| `get_all_tags()` | Obtener todas las etiquetas únicas |
| `get_contacts_by_tag()` | Agrupar contactos por etiqueta |
| `export_summary()` | Generar resumen de todos los contactos |
| `get_statistics()` | Estadísticas de la agenda |

### 3. Validaciones

- No permitir emails duplicados
- Validar que el contacto exista antes de actualizar/eliminar
- Manejar etiquetas sin duplicados dentro de un contacto

---

## 💡 Ejemplos de Uso

```python
# Crear contactos
create_contact("Alice Johnson", "alice@example.com", "+1-555-0101", ["work"])
create_contact("Bob Smith", "bob@example.com", "+1-555-0102", ["personal", "family"])

# Buscar
results = search_by_name("alice")  # [{"id": 1, "name": "Alice Johnson", ...}]

# Actualizar
update_contact(1, phone="+1-555-9999", notes="Updated contact")

# Etiquetas
add_tag(1, "important")
contacts_by_tag = get_contacts_by_tag()  # {"work": [...], "personal": [...], ...}

# Estadísticas
stats = get_statistics()
# {"total_contacts": 2, "total_tags": 3, "contacts_with_notes": 1, ...}
```

---

## ✅ Criterios de Evaluación

### Conocimiento (30%)
- [ ] Uso correcto de type hints
- [ ] Comprensión de operaciones CRUD en diccionarios
- [ ] Manejo adecuado de diccionarios anidados

### Desempeño (40%)
- [ ] Todas las funciones implementadas correctamente
- [ ] Búsquedas funcionan con coincidencias parciales
- [ ] Manejo correcto de casos edge (contacto no existe, etc.)

### Producto (30%)
- [ ] Código limpio y bien documentado
- [ ] Funciones con docstrings descriptivos
- [ ] Validaciones implementadas

---

## 🚀 Instrucciones

1. Abre `starter/main.py`
2. Lee los TODOs y docstrings de cada función
3. Implementa las funciones una por una
4. Ejecuta el archivo para probar con los casos de ejemplo
5. Verifica que todos los tests pasen

---

## 📚 Recursos

- [Teoría: Introducción a Diccionarios](../1-teoria/01-intro-diccionarios.md)
- [Teoría: Métodos de Diccionarios](../1-teoria/02-metodos-diccionarios.md)
- [Teoría: Iteración sobre Diccionarios](../1-teoria/03-iteracion-diccionarios.md)
- [Teoría: Dict Comprehensions](../1-teoria/04-dict-comprehensions.md)

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Ejercicio 03 - Diccionarios Anidados](../2-ejercicios/03-diccionarios-anidados/README.md)
- ➡️ **Siguiente**: [Semana 7](../../week-07/README.md)
- 🏠 **Índice**: [README Semana 6](../README.md)
