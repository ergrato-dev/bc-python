# 📋 Rúbrica de Evaluación - Semana 8

## 🎭 Clases y Objetos

---

## 📊 Distribución de Puntos

| Componente | Puntos | Porcentaje |
|------------|--------|------------|
| Conocimiento (Teoría) | 30 | 30% |
| Desempeño (Ejercicios) | 40 | 40% |
| Producto (Proyecto) | 30 | 30% |
| **Total** | **100** | **100%** |

---

## 🧠 Conocimiento (30 puntos)

### Evaluación Teórica

| Criterio | Excelente (10) | Bueno (7) | Regular (5) | Insuficiente (0-3) |
|----------|----------------|-----------|-------------|---------------------|
| **Conceptos POO** | Explica con precisión clase, objeto, instancia y los 4 pilares de POO | Explica conceptos principales con ejemplos | Conoce conceptos básicos pero confunde algunos | No comprende conceptos fundamentales |
| **Atributos y Métodos** | Diferencia claramente atributos de clase/instancia y tipos de métodos | Entiende diferencias principales | Confunde algunos conceptos | No diferencia tipos de atributos/métodos |
| **Métodos Especiales** | Conoce propósito y uso de múltiples dunder methods | Conoce `__init__`, `__str__`, `__repr__` | Solo conoce `__init__` | No comprende métodos especiales |

---

## 💪 Desempeño (40 puntos)

### Ejercicio 1: Mi Primera Clase (12 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Sintaxis de clase | 4 | Clase definida correctamente con `class` |
| Método `__init__` | 4 | Inicializador con parámetros tipados |
| Atributos de instancia | 4 | Uso correcto de `self` para atributos |

### Ejercicio 2: Atributos y Métodos (14 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Atributos de clase | 3 | Variables compartidas entre instancias |
| Atributos de instancia | 3 | Variables únicas por objeto |
| Métodos de instancia | 3 | Métodos que usan `self` |
| Métodos de clase | 3 | Uso correcto de `@classmethod` y `cls` |
| Métodos estáticos | 2 | Uso correcto de `@staticmethod` |

### Ejercicio 3: Métodos Especiales (14 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| `__str__` | 3 | Representación legible para usuarios |
| `__repr__` | 3 | Representación técnica/debug |
| `__eq__` | 3 | Comparación de igualdad entre objetos |
| `__len__` | 2 | Implementación de longitud |
| `__bool__` | 3 | Evaluación booleana del objeto |

---

## 📦 Producto (30 puntos)

### Proyecto: Sistema de Biblioteca

| Criterio | Excelente (6) | Bueno (4) | Regular (2) | Insuficiente (0) |
|----------|---------------|-----------|-------------|-------------------|
| **Clase Book** | Implementa todos los atributos y métodos requeridos con type hints | Implementa mayoría de funcionalidades | Implementación básica incompleta | No funciona o no existe |
| **Clase User** | Gestión completa de usuario con historial de préstamos | Funcionalidad principal implementada | Implementación parcial | No funciona o no existe |
| **Clase Loan** | Maneja préstamos con fechas, estados y validaciones | Funcionalidad básica de préstamos | Solo almacena datos básicos | No funciona o no existe |
| **Métodos Especiales** | Implementa `__str__`, `__repr__`, `__eq__` en todas las clases | Implementa en algunas clases | Solo `__init__` | No implementa ninguno |
| **Documentación** | Docstrings completos, código limpio, README claro | Documentación adecuada | Documentación mínima | Sin documentación |

---

## ✅ Lista de Verificación

### Conceptos Obligatorios

- [ ] Definir clases usando `class`
- [ ] Implementar `__init__` con type hints
- [ ] Usar `self` para atributos de instancia
- [ ] Crear atributos de clase
- [ ] Definir métodos de instancia
- [ ] Implementar `@classmethod`
- [ ] Implementar `@staticmethod`
- [ ] Usar `__str__` para representación legible
- [ ] Usar `__repr__` para representación técnica
- [ ] Crear múltiples instancias de una clase
- [ ] Acceder a atributos y llamar métodos

### Buenas Prácticas

- [ ] Type hints en todos los métodos
- [ ] Docstrings en clases y métodos públicos
- [ ] Nombres descriptivos (PascalCase para clases)
- [ ] Atributos privados con prefijo `_` cuando corresponda
- [ ] Separación de responsabilidades entre clases

---

## 🎯 Niveles de Logro

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| 🏆 Sobresaliente | 90-100 | Dominio completo de POO, código ejemplar |
| ✅ Aprobado | 70-89 | Comprende y aplica conceptos correctamente |
| ⚠️ En desarrollo | 50-69 | Necesita reforzar algunos conceptos |
| ❌ No aprobado | 0-49 | Requiere revisión completa del material |

---

## 📝 Retroalimentación

### Fortalezas Comunes
- Creación básica de clases
- Uso del método `__init__`
- Instanciación de objetos

### Áreas de Mejora Frecuentes
- Confusión entre atributos de clase e instancia
- Olvidar `self` en métodos de instancia
- No implementar `__repr__` para debugging
- Falta de type hints en métodos
- Documentación insuficiente

### Recursos de Apoyo
- [Teoría: Clases y Objetos](1-teoria/02-clases-objetos.md)
- [Teoría: Atributos y Métodos](1-teoria/03-atributos-metodos.md)
- [Python OOP Tutorial - Real Python](https://realpython.com/python3-object-oriented-programming/)

---

## 🔄 Proceso de Evaluación

1. **Autoevaluación** - Revisa tu código contra esta rúbrica
2. **Pruebas** - Ejecuta los tests proporcionados
3. **Revisión de pares** - Intercambia código con un compañero
4. **Feedback del instructor** - Retroalimentación final

---

*Rúbrica Week 08 - Bootcamp Python Zero to Hero*
