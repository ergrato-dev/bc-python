# Ejercicio 01: Operaciones con Sets

## 🎯 Objetivo

Practicar la creación de sets y sus métodos básicos de manipulación: `add()`, `remove()`, `discard()`, `pop()`, `update()` y `clear()`.

---

## 📋 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y su explicación
3. Descomenta el código indicado en cada paso
4. Ejecuta el archivo para verificar los resultados
5. Observa cómo funcionan los diferentes métodos

---

## 📚 Conceptos Cubiertos

- Crear sets con `{}` y `set()`
- Agregar elementos con `add()` y `update()`
- Eliminar elementos con `remove()`, `discard()` y `pop()`
- Verificar pertenencia con `in`
- Vaciar sets con `clear()`
- Convertir entre listas y sets

---

## 🧪 Resultado Esperado

```
=== PASO 1: Crear Sets ===
Frutas: {'cherry', 'apple', 'banana'}
Números únicos: {1, 2, 3, 4, 5}
Set vacío: set()
Tipo de set vacío: <class 'set'>

=== PASO 2: Agregar Elementos ===
Después de add('mango'): {'cherry', 'apple', 'banana', 'mango'}
Después de add('apple'): {'cherry', 'apple', 'banana', 'mango'}
Después de update: {'cherry', 'apple', 'banana', 'mango', 'kiwi', 'grape'}

=== PASO 3: Verificar Pertenencia ===
¿'apple' está en fruits? True
¿'orange' está en fruits? False
¿'orange' NO está en fruits? True

=== PASO 4: Eliminar con remove() ===
Después de remove('banana'): {'cherry', 'apple', 'mango', 'kiwi', 'grape'}
Error al eliminar 'banana' de nuevo: 'banana'

=== PASO 5: Eliminar con discard() ===
Después de discard('cherry'): {'apple', 'mango', 'kiwi', 'grape'}
Después de discard('pineapple'): {'apple', 'mango', 'kiwi', 'grape'}

=== PASO 6: Eliminar con pop() ===
Elemento eliminado con pop(): apple
Set después de pop(): {'mango', 'kiwi', 'grape'}

=== PASO 7: Copiar y Vaciar ===
Copia: {'mango', 'kiwi', 'grape'}
Original después de clear(): set()
Copia sigue intacta: {'mango', 'kiwi', 'grape'}

=== PASO 8: Eliminar Duplicados ===
Lista original: ['python', 'java', 'python', 'javascript', 'java', 'go']
Como set (únicos): {'python', 'java', 'javascript', 'go'}
De vuelta a lista: ['python', 'java', 'javascript', 'go']
```

> **Nota**: El orden de los elementos en los sets puede variar.

---

## 💡 Tips

- `{}` crea un diccionario vacío, usa `set()` para un set vacío
- `remove()` lanza error si el elemento no existe
- `discard()` no lanza error si el elemento no existe
- `pop()` elimina y retorna un elemento arbitrario
- Sets eliminan duplicados automáticamente

---

## 🔗 Navegación

- ➡️ **Siguiente ejercicio**: [02-conjuntos-matematicos](../02-conjuntos-matematicos/)
- 🏠 **Volver al índice**: [README](../../README.md)
