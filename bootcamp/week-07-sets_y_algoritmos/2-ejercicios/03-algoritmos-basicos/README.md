# Ejercicio 03: Algoritmos Básicos de Búsqueda y Ordenamiento

## 🎯 Objetivo

Practicar algoritmos de búsqueda (lineal y binaria) y ordenamiento (`sorted()`, `sort()`) con diferentes criterios y parámetros.

---

## 📋 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y su explicación
3. Descomenta el código indicado en cada paso
4. Ejecuta el archivo para verificar los resultados
5. Compara el rendimiento de los diferentes algoritmos

---

## 📚 Conceptos Cubiertos

- Búsqueda lineal (O(n))
- Búsqueda binaria (O(log n))
- `sorted()` con `key` y `reverse`
- `sort()` in-place
- Ordenar por múltiples criterios
- Módulo `bisect` para búsqueda binaria

---

## 🧪 Resultado Esperado

```
=== PASO 1: Búsqueda Lineal ===
Lista: [64, 34, 25, 12, 22, 11, 90, 45]
Buscando 22...
✓ Encontrado en índice 4

=== PASO 2: Búsqueda Lineal (Todos los Índices) ===
Lista: ['apple', 'banana', 'apple', 'cherry', 'apple']
Índices de 'apple': [0, 2, 4]

=== PASO 3: Búsqueda Binaria ===
Lista ordenada: [11, 12, 22, 25, 34, 45, 64, 90]
Buscando 25...
✓ Encontrado en índice 3

=== PASO 4: Comparación de Búsquedas ===
Buscando 750000 en lista de 1,000,000 elementos:
  Búsqueda lineal: 750001 comparaciones
  Búsqueda binaria: 20 comparaciones
  Binaria es 37500x más rápida

=== PASO 5: sorted() Básico ===
Original: [64, 34, 25, 12, 22, 11, 90]
Ordenado ascendente: [11, 12, 22, 25, 34, 64, 90]
Ordenado descendente: [90, 64, 34, 25, 22, 12, 11]
Original sin cambios: [64, 34, 25, 12, 22, 11, 90]

=== PASO 6: sorted() con key ===
Palabras: ['Python', 'is', 'awesome', 'and', 'fun']
Por longitud: ['is', 'and', 'fun', 'Python', 'awesome']
Alfabético (ignorando mayúsculas): ['and', 'awesome', 'fun', 'is', 'Python']

=== PASO 7: Ordenar Diccionarios ===
Estudiantes:
  {'name': 'Alice', 'grade': 85, 'age': 22}
  {'name': 'Bob', 'grade': 92, 'age': 20}
  {'name': 'Carol', 'grade': 78, 'age': 23}
  {'name': 'David', 'grade': 92, 'age': 21}

Por calificación (descendente):
  Bob: 92
  David: 92
  Alice: 85
  Carol: 78

=== PASO 8: sort() In-Place ===
Lista original: [5, 2, 8, 1, 9]
Después de sort(): [1, 2, 5, 8, 9]
sort() retorna: None
```

---

## 💡 Tips

- Búsqueda binaria REQUIERE lista ordenada
- `sorted()` retorna nueva lista, `sort()` modifica la original
- `key` acepta cualquier función que retorne un valor comparable
- Para ordenar por múltiples criterios, usa tuplas en `key`
- `bisect` es más eficiente que implementar búsqueda binaria manual

---

## 🔗 Navegación

- ⬅️ **Ejercicio anterior**: [02-conjuntos-matematicos](../02-conjuntos-matematicos/)
- ➡️ **Siguiente**: [Proyecto](../../3-proyecto/)
- 🏠 **Volver al índice**: [README](../../README.md)
