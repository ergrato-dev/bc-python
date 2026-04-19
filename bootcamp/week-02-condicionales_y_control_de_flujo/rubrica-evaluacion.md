# 📊 Rúbrica de Evaluación - Semana 02

## Condicionales y Control de Flujo

---

## 📋 Resumen de Evaluación

| Tipo de Evidencia | Peso | Actividades |
|-------------------|------|-------------|
| 🧠 Conocimiento | 30% | Cuestionario teórico |
| 💪 Desempeño | 40% | Ejercicios prácticos |
| 📦 Producto | 30% | Proyecto "Juego de Aventura" |

**Nota mínima aprobatoria**: 70%

---

## 🧠 Evidencia de Conocimiento (30%)

### Cuestionario Teórico

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Operadores de comparación | 5 | Identificar ==, !=, <, >, <=, >= correctamente |
| Diferencia entre == e is | 5 | Comprender igualdad vs identidad |
| Operadores lógicos | 5 | Uso correcto de and, or, not |
| Precedencia de operadores | 5 | Conocer orden de evaluación |
| Truthiness/Falsiness | 5 | Identificar valores truthy y falsy |
| Match statements | 5 | Sintaxis y casos de uso |
| **Total** | **30** | |

---

## 💪 Evidencia de Desempeño (40%)

### Ejercicio 01: Comparaciones (10 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Comparaciones numéricas | 3 | Usar operadores con números |
| Comparaciones de strings | 3 | Comparar textos correctamente |
| Uso de is e in | 2 | Identidad y pertenencia |
| Type hints | 2 | Incluir anotaciones de tipo |

### Ejercicio 02: Condicionales (15 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Estructura if/elif/else | 5 | Implementar correctamente |
| Condiciones compuestas | 4 | Combinar con and/or/not |
| Operador ternario | 3 | Usar expresiones condicionales |
| Código limpio | 3 | Legibilidad y organización |

### Ejercicio 03: Match Patterns (15 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Match básico | 4 | Patrones literales |
| Patrones con guardas | 4 | Usar condiciones if en case |
| Patrones de secuencia | 4 | Desempaquetado en case |
| Caso wildcard | 3 | Uso de case _ |

---

## 📦 Evidencia de Producto (30%)

### Proyecto: Juego de Aventura

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **Funcionalidad** | 12 | |
| - Sistema de decisiones | 4 | if/elif/else funcionando |
| - Pattern matching | 4 | match statements implementados |
| - Múltiples caminos | 4 | Al menos 3 finales diferentes |
| **Calidad de Código** | 10 | |
| - Type hints | 3 | Todas las funciones tipadas |
| - Nombres descriptivos | 3 | Variables y funciones claras |
| - Estructura modular | 4 | Código organizado en funciones |
| **Creatividad** | 8 | |
| - Historia interesante | 4 | Narrativa atractiva |
| - Opciones significativas | 4 | Decisiones con consecuencias |
| **Total** | **30** | |

---

## 📈 Escala de Calificación

| Rango | Calificación | Descripción |
|-------|--------------|-------------|
| 90-100% | ⭐ Excelente | Dominio completo |
| 80-89% | ✅ Muy Bien | Sólido entendimiento |
| 70-79% | 👍 Aprobado | Cumple objetivos mínimos |
| 60-69% | ⚠️ En Desarrollo | Requiere refuerzo |
| <60% | ❌ No Aprobado | Debe repetir la semana |

---

## ✅ Checklist de Entrega

Antes de entregar, verifica:

- [ ] Todos los ejercicios ejecutan sin errores
- [ ] El proyecto tiene al menos 3 finales diferentes
- [ ] Se usan type hints en todas las funciones
- [ ] El código está formateado correctamente
- [ ] Se usaron tanto if/elif/else como match
- [ ] Los nombres de variables son descriptivos

---

## 📝 Criterios de Código

### Ejemplos de Buen Código ✅

```python
# Type hints claros
def check_age(age: int) -> str:
    """Verifica la categoría de edad."""
    if age < 0:
        return "Edad inválida"
    elif age < 13:
        return "Niño"
    elif age < 18:
        return "Adolescente"
    else:
        return "Adulto"

# Match statement bien estructurado
def handle_command(command: str) -> str:
    match command.lower():
        case "north" | "n":
            return "Vas hacia el norte"
        case "south" | "s":
            return "Vas hacia el sur"
        case "help" | "h":
            return "Comandos: north, south, help"
        case _:
            return "Comando desconocido"
```

### Ejemplos de Código a Evitar ❌

```python
# Sin type hints
def check(a):  # ❌ Nombre poco descriptivo
    if a < 0:
        return "bad"
    if a < 13:
        return "kid"
    if a < 18:
        return "teen"
    return "adult"

# Condiciones redundantes
if x == True:  # ❌ Debería ser: if x:
    pass

if x == None:  # ❌ Debería ser: if x is None:
    pass
```

---

## 🔄 Retroalimentación

El instructor proporcionará:

1. **Feedback de código** - Sugerencias de mejora
2. **Revisión de lógica** - Validación de estructuras de control
3. **Consejos de estilo** - Mejores prácticas Python

---

*Fecha de evaluación: Final de Semana 02*
