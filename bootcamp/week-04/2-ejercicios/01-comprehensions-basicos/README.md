# 🏋️ Ejercicio 01: Comprehensions Básicos

## 🎯 Objetivo

Practicar la creación de list, dict y set comprehensions con transformaciones y filtros.

---

## 📋 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y descomenta el código correspondiente
3. Ejecuta el archivo para verificar los resultados
4. Compara tu output con el esperado

---

## 📚 Conceptos Cubiertos

- List comprehensions con transformaciones
- List comprehensions con filtros
- Expresiones condicionales (if-else en expresión)
- Dict comprehensions
- Set comprehensions
- Comprehensions anidados

---

## ✅ Resultado Esperado

```
=== PASO 1: List Comprehension Básico ===
Cuadrados: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

=== PASO 2: Transformación de Strings ===
Mayúsculas: ['PYTHON', 'JAVASCRIPT', 'RUST', 'GO']
Longitudes: [6, 10, 4, 2]

=== PASO 3: Filtrado con if ===
Pares: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
Palabras largas: ['python', 'javascript']

=== PASO 4: Transformar y Filtrar ===
Cuadrados de impares: [1, 9, 25, 49, 81]

=== PASO 5: Expresión Condicional (if-else) ===
Etiquetas: ['par', 'impar', 'par', 'impar', 'par']
Aprobados: ['PASS', 'FAIL', 'PASS', 'FAIL', 'PASS', 'FAIL']

=== PASO 6: Dict Comprehension ===
Cuadrados dict: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
Longitud palabras: {'python': 6, 'es': 2, 'genial': 6}

=== PASO 7: Dict con Filtro ===
Aprobados: {'Ana': 85, 'Carlos': 91, 'Eva': 78}
Invertido: {1: 'a', 2: 'b', 3: 'c'}

=== PASO 8: Set Comprehension ===
Letras únicas: {'h', 'e', 'l', 'o'}
Vocales: {'o', 'a', 'i', 'e', 'u'}

=== PASO 9: Comprehension Anidado ===
Aplanado: [1, 2, 3, 4, 5, 6, 7, 8, 9]
Combinaciones: [('A', 1), ('A', 2), ('B', 1), ('B', 2)]

=== PASO 10: Caso Práctico ===
Productos caros: {'Laptop': 1210.0, 'Phone': 968.0}
```

---

## 🚀 Ejecución

```bash
cd bootcamp/week-04/2-ejercicios/01-comprehensions-basicos/starter
python main.py
```

---

## 💡 Tips

- La sintaxis básica es `[expresion for elemento in iterable]`
- El filtro `if` va al **final** para excluir elementos
- La expresión condicional `if-else` va al **inicio** para transformar
- Dict comprehension usa `{clave: valor for ...}`
- Set comprehension usa `{expresion for ...}` (sin clave-valor)

---

## 📖 Referencia

- [Teoría: List Comprehensions](../../1-teoria/01-list-comprehensions.md)
- [Teoría: Dict y Set Comprehensions](../../1-teoria/02-dict-set-comprehensions.md)
