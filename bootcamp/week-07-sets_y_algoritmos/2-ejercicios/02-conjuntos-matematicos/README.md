# Ejercicio 02: Operaciones Matemáticas de Conjuntos

## 🎯 Objetivo

Practicar las operaciones matemáticas de conjuntos: unión, intersección, diferencia y diferencia simétrica, así como las relaciones de subconjunto y superconjunto.

---

## 📋 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y su explicación
3. Descomenta el código indicado en cada paso
4. Ejecuta el archivo para verificar los resultados
5. Observa cómo funcionan las operaciones de conjuntos

---

## 📚 Conceptos Cubiertos

- Unión (`|` y `union()`)
- Intersección (`&` y `intersection()`)
- Diferencia (`-` y `difference()`)
- Diferencia simétrica (`^` y `symmetric_difference()`)
- Subconjunto (`<=` y `issubset()`)
- Superconjunto (`>=` y `issuperset()`)
- Conjuntos disjuntos (`isdisjoint()`)
- Operaciones in-place (`|=`, `&=`, `-=`, `^=`)

---

## 🧪 Resultado Esperado

```
=== PASO 1: Unión (|) ===
Set A: {1, 2, 3, 4, 5}
Set B: {4, 5, 6, 7, 8}
A | B (unión): {1, 2, 3, 4, 5, 6, 7, 8}
A.union(B): {1, 2, 3, 4, 5, 6, 7, 8}

=== PASO 2: Intersección (&) ===
A & B (intersección): {4, 5}
A.intersection(B): {4, 5}

=== PASO 3: Diferencia (-) ===
A - B (en A pero no en B): {1, 2, 3}
B - A (en B pero no en A): {8, 6, 7}

=== PASO 4: Diferencia Simétrica (^) ===
A ^ B (exclusivos): {1, 2, 3, 6, 7, 8}
Verificación (A|B) - (A&B): {1, 2, 3, 6, 7, 8}

=== PASO 5: Subconjuntos y Superconjuntos ===
small: {1, 2}
large: {1, 2, 3, 4, 5}
¿small es subconjunto de large? True
¿large es superconjunto de small? True
¿{1, 2} < {1, 2, 3}? (subconjunto propio) True
¿{1, 2} < {1, 2}? (subconjunto propio de sí mismo) False

=== PASO 6: Conjuntos Disjuntos ===
evens: {2, 4, 6, 8}
odds: {1, 3, 5, 7}
mixed: {1, 2, 3}
¿evens y odds son disjuntos? True
¿evens y mixed son disjuntos? False

=== PASO 7: Operaciones In-Place ===
numbers inicial: {1, 2, 3}
Después de |= {4, 5}: {1, 2, 3, 4, 5}
Después de &= {2, 3, 4, 6}: {2, 3, 4}
Después de -= {4}: {2, 3}

=== PASO 8: Caso Práctico - Análisis de Usuarios ===
📊 Análisis de Actividad:
  Usuarios activos ayer: {'alice', 'bob', 'carol', 'david'}
  Usuarios activos hoy: {'bob', 'carol', 'eve', 'frank'}
  ─────────────────────────────────
  Usuarios que volvieron (intersección): {'bob', 'carol'}
  Usuarios nuevos hoy (diferencia): {'eve', 'frank'}
  Usuarios que se fueron (diferencia): {'alice', 'david'}
  Todos los usuarios únicos (unión): {'alice', 'bob', 'carol', 'david', 'eve', 'frank'}
```

---

## 💡 Tips

- `|` es más legible, `union()` acepta múltiples iterables
- La diferencia NO es conmutativa: `A - B ≠ B - A`
- La diferencia simétrica ES conmutativa: `A ^ B = B ^ A`
- Subconjunto propio (`<`) excluye igualdad
- `isdisjoint()` es True si no comparten elementos

---

## 🔗 Navegación

- ⬅️ **Ejercicio anterior**: [01-operaciones-sets](../01-operaciones-sets/)
- ➡️ **Siguiente ejercicio**: [03-algoritmos-basicos](../03-algoritmos-basicos/)
- 🏠 **Volver al índice**: [README](../../README.md)
