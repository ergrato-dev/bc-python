# 📊 Rúbrica de Evaluación - Semana 12

## Decoradores, Generadores y Expresiones Regulares

---

## 🎯 Competencias a Evaluar

| Competencia | Descripción |
|-------------|-------------|
| **C1** | Crear y aplicar decoradores correctamente |
| **C2** | Implementar generadores e iteradores |
| **C3** | Escribir expresiones regulares efectivas |
| **C4** | Combinar conceptos en soluciones prácticas |

---

## 📝 Evidencias de Aprendizaje

### 1. Conocimiento 🧠 (30%)

| Criterio | Excelente (10) | Bueno (8) | Suficiente (6) | Insuficiente (0-5) |
|----------|----------------|-----------|----------------|-------------------|
| **Decoradores** | Explica closures, `@wraps`, decoradores con argumentos | Explica decoradores básicos y su sintaxis | Conoce la sintaxis pero no el funcionamiento | No comprende decoradores |
| **Generadores** | Explica `yield`, lazy evaluation, pipelines | Diferencia generadores de listas | Conoce `yield` básico | Confunde generadores con funciones |
| **Regex** | Domina metacaracteres, grupos, lookahead | Escribe patrones moderadamente complejos | Conoce patrones básicos | No comprende regex |

### 2. Desempeño 💪 (40%)

| Criterio | Excelente (10) | Bueno (8) | Suficiente (6) | Insuficiente (0-5) |
|----------|----------------|-----------|----------------|-------------------|
| **Ejercicio 1: Decoradores** | Implementa decoradores con args, preserva metadata | Crea decoradores funcionales | Decoradores básicos con errores menores | Decoradores no funcionan |
| **Ejercicio 2: Generadores** | Pipelines eficientes, manejo de datos grandes | Generadores funcionales | Generadores básicos | No implementa generadores |
| **Ejercicio 3: Regex** | Patrones complejos, validaciones robustas | Patrones correctos para casos comunes | Patrones simples | Regex no funcional |
| **Código limpio** | Type hints, docstrings, PEP 8 | Código legible con algunos type hints | Código funcional pero desorganizado | Código difícil de leer |

### 3. Producto 📦 (30%)

| Criterio | Excelente (10) | Bueno (8) | Suficiente (6) | Insuficiente (0-5) |
|----------|----------------|-----------|----------------|-------------------|
| **Funcionalidad** | Todas las funciones implementadas y probadas | Mayoría de funciones correctas | Funciones básicas implementadas | Proyecto incompleto |
| **Decoradores** | Usa decoradores para validación, logging, timing | Implementa 2+ decoradores útiles | 1 decorador funcional | No usa decoradores |
| **Generadores/Regex** | Combina generadores con regex eficientemente | Usa ambos conceptos correctamente | Usa solo uno de los conceptos | No integra los conceptos |

---

## 🏆 Escala de Calificación

| Rango | Calificación | Descripción |
|-------|--------------|-------------|
| 90-100 | **A** | Excelente - Dominio completo de los conceptos |
| 80-89 | **B** | Bueno - Comprensión sólida con mejoras menores |
| 70-79 | **C** | Suficiente - Cumple requisitos mínimos |
| 60-69 | **D** | Insuficiente - Requiere refuerzo significativo |
| 0-59 | **F** | Reprobado - No demuestra comprensión |

---

## 📋 Checklist de Evaluación

### Ejercicio 01: Decoradores Prácticos
- [ ] Decorador `@timer` mide tiempo correctamente
- [ ] Decorador `@retry` reintenta en caso de error
- [ ] Decorador `@validate` valida argumentos
- [ ] Usa `@functools.wraps` para preservar metadata
- [ ] Decorador con argumentos funciona

### Ejercicio 02: Generadores de Datos
- [ ] Generador de números infinitos
- [ ] Pipeline de transformación de datos
- [ ] Expresión generadora correcta
- [ ] Uso de `yield from` cuando aplica
- [ ] Manejo eficiente de memoria

### Ejercicio 03: Regex y Validación
- [ ] Valida emails correctamente
- [ ] Valida teléfonos con diferentes formatos
- [ ] Extrae información de texto
- [ ] Usa grupos de captura
- [ ] Reemplazos con `re.sub`

### Proyecto: Validador de Datos
- [ ] Decorador `@validate_input` funcional
- [ ] Generador para procesar datos grandes
- [ ] Regex para validación de campos
- [ ] Manejo de errores apropiado
- [ ] Código documentado y type hints

---

## 📊 Distribución de Puntos

```
Total: 100 puntos

Conocimiento (30 pts)
├── Decoradores: 10 pts
├── Generadores: 10 pts
└── Regex: 10 pts

Desempeño (40 pts)
├── Ejercicio 1: 10 pts
├── Ejercicio 2: 10 pts
├── Ejercicio 3: 10 pts
└── Código limpio: 10 pts

Producto (30 pts)
├── Funcionalidad: 10 pts
├── Decoradores: 10 pts
└── Generadores/Regex: 10 pts
```

---

## 🎯 Criterio de Aprobación

- **Mínimo 70%** en cada tipo de evidencia
- **Todos los ejercicios** entregados
- **Proyecto funcional** con los tres conceptos integrados
