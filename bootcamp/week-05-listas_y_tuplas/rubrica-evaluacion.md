# 📋 Rúbrica de Evaluación - Semana 05

## Listas y Tuplas

### 📊 Distribución de Puntos

| Evidencia | Porcentaje | Puntos |
|-----------|------------|--------|
| 🧠 Conocimiento | 30% | 30 pts |
| 💪 Desempeño | 40% | 40 pts |
| 📦 Producto | 30% | 30 pts |
| **Total** | **100%** | **100 pts** |

---

## 🧠 Evidencia de Conocimiento (30 pts)

### Cuestionario Teórico

| Criterio | Excelente (10) | Bueno (7) | Regular (4) | Insuficiente (0) |
|----------|----------------|-----------|-------------|------------------|
| **Métodos de listas** | Explica correctamente todos los métodos (append, extend, insert, remove, pop, sort, reverse) con ejemplos | Explica la mayoría de métodos correctamente | Confunde algunos métodos o sus comportamientos | No comprende los métodos de listas |
| **Slicing** | Domina sintaxis completa [start:stop:step] incluyendo índices negativos | Usa slicing básico correctamente | Comete errores con step o índices negativos | No comprende slicing |
| **Listas vs Tuplas** | Explica claramente mutabilidad, casos de uso y diferencias de rendimiento | Conoce las diferencias principales | Confunde algunos conceptos | No diferencia listas de tuplas |

---

## 💪 Evidencia de Desempeño (40 pts)

### Ejercicios en Clase

| Ejercicio | Criterios | Puntos |
|-----------|-----------|--------|
| **01 - Métodos de Listas** | | **15 pts** |
| | Usa `append`, `extend` correctamente | 3 |
| | Usa `insert`, `remove`, `pop` correctamente | 3 |
| | Usa `sort`, `reverse`, `index`, `count` | 3 |
| | Comprende modificación in-place vs retorno | 3 |
| | Código limpio con type hints | 3 |
| **02 - Slicing Avanzado** | | **13 pts** |
| | Slicing básico [start:stop] | 3 |
| | Slicing con step [::step] | 3 |
| | Índices negativos | 3 |
| | Copia de listas con slicing | 2 |
| | Modificación con slicing | 2 |
| **03 - Tuplas y Estructuras** | | **12 pts** |
| | Crea y usa tuplas correctamente | 3 |
| | Aplica tuple unpacking | 3 |
| | Trabaja con estructuras anidadas | 3 |
| | Named tuples (opcional/bonus) | 3 |

---

## 📦 Evidencia de Producto (30 pts)

### Proyecto: Gestor de Playlist

| Criterio | Excelente (6) | Bueno (4) | Regular (2) | Insuficiente (0) |
|----------|---------------|-----------|-------------|------------------|
| **Funcionalidad** | Todas las funciones implementadas y funcionando correctamente | La mayoría de funciones funcionan | Algunas funciones con errores | No funciona |
| **Estructura de datos** | Usa listas y tuplas apropiadamente según el caso | Usa las estructuras correctamente en la mayoría de casos | Mezcla estructuras sin criterio claro | Estructuras incorrectas |
| **Manipulación** | Aplica métodos y slicing de forma eficiente y Pythonic | Usa métodos correctamente | Implementación funcional pero no óptima | No usa métodos apropiados |
| **Código limpio** | Type hints, docstrings, nombres descriptivos, sin código duplicado | Buen código con pequeñas mejoras posibles | Código funcional pero desordenado | Código difícil de leer |
| **Casos especiales** | Maneja listas vacías, índices inválidos y casos edge | Maneja la mayoría de casos especiales | Maneja algunos casos | No considera casos especiales |

---

## 📝 Lista de Verificación

### Métodos de Listas
- [ ] `append()` - Agregar elemento al final
- [ ] `extend()` - Agregar múltiples elementos
- [ ] `insert()` - Insertar en posición específica
- [ ] `remove()` - Eliminar por valor
- [ ] `pop()` - Eliminar y retornar por índice
- [ ] `clear()` - Vaciar lista
- [ ] `index()` - Encontrar posición de elemento
- [ ] `count()` - Contar ocurrencias
- [ ] `sort()` - Ordenar in-place
- [ ] `reverse()` - Invertir in-place
- [ ] `copy()` - Crear copia superficial

### Slicing
- [ ] `list[start:stop]` - Rango básico
- [ ] `list[:stop]` - Desde el inicio
- [ ] `list[start:]` - Hasta el final
- [ ] `list[::step]` - Con paso
- [ ] `list[::-1]` - Invertir
- [ ] Índices negativos
- [ ] Slicing para copiar `list[:]`
- [ ] Slicing para modificar

### Tuplas
- [ ] Crear tuplas con `()`
- [ ] Tupla de un elemento `(x,)`
- [ ] Tuple unpacking
- [ ] Extended unpacking `*rest`
- [ ] Inmutabilidad
- [ ] Named tuples (bonus)

### Estructuras Anidadas
- [ ] Lista de listas (matrices)
- [ ] Acceso multidimensional `[i][j]`
- [ ] Iteración anidada
- [ ] List comprehension anidada

---

## 🎯 Criterios de Aprobación

| Requisito | Mínimo |
|-----------|--------|
| Conocimiento | ≥ 21/30 pts (70%) |
| Desempeño | ≥ 28/40 pts (70%) |
| Producto | ≥ 21/30 pts (70%) |
| **Total** | ≥ 70/100 pts |

---

## 📅 Fechas de Entrega

| Entregable | Fecha |
|------------|-------|
| Ejercicios | Final de la semana 05 |
| Proyecto | Final de la semana 05 |
| Quiz teórico | Durante la sesión |

---

## 💡 Consejos para Éxito

1. **Practica los métodos** - Escribe código que use cada método al menos 3 veces
2. **Experimenta con slicing** - Prueba diferentes combinaciones de start:stop:step
3. **Compara estructuras** - Intenta modificar una tupla para entender la inmutabilidad
4. **Visualiza las matrices** - Dibuja las estructuras anidadas antes de acceder a ellas
5. **Lee la documentación** - Consulta la [documentación oficial de secuencias](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)

---

## 🏆 Puntos Extra (Bonus)

| Criterio | Puntos |
|----------|--------|
| Usar `collections.namedtuple` o `typing.NamedTuple` | +3 pts |
| Implementar función de búsqueda binaria | +3 pts |
| Documentación excepcional con ejemplos | +2 pts |
| Tests unitarios para el proyecto | +2 pts |

---

*Rúbrica Semana 05 | Bootcamp Python Zero to Hero*
