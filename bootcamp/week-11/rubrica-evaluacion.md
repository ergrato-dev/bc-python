# 📋 Rúbrica de Evaluación - Semana 11

## Archivos, Excepciones y Context Managers

---

## 📊 Resumen de Evaluación

| Tipo de Evidencia | Porcentaje | Puntos |
|-------------------|------------|--------|
| 🧠 Conocimiento | 30% | 30 pts |
| 💪 Desempeño | 40% | 40 pts |
| 📦 Producto | 30% | 30 pts |
| **Total** | **100%** | **100 pts** |

**Nota mínima aprobatoria**: 70 puntos

---

## 🧠 Evidencia de Conocimiento (30 pts)

### Cuestionario Teórico

| Criterio | Excelente (10) | Bueno (7) | Suficiente (5) | Insuficiente (0-4) |
|----------|----------------|-----------|----------------|-------------------|
| **Modos de apertura de archivos** | Explica correctamente todos los modos (r, w, a, x, b, +) con ejemplos | Explica la mayoría de modos correctamente | Conoce modos básicos (r, w) | No distingue entre modos |
| **Jerarquía de excepciones** | Domina la jerarquía completa y cuándo usar cada tipo | Conoce excepciones comunes y su uso | Conoce try/except básico | No entiende el sistema de excepciones |
| **Context managers** | Explica `__enter__`/`__exit__` y `@contextmanager` | Entiende el uso de `with` y su propósito | Usa `with` sin entender internamente | No conoce context managers |

---

## 💪 Evidencia de Desempeño (40 pts)

### Ejercicio 1: Lectura y Escritura (12 pts)

| Criterio | Excelente (12) | Bueno (9) | Suficiente (6) | Insuficiente (0-5) |
|----------|----------------|-----------|----------------|-------------------|
| **Operaciones de archivo** | Implementa lectura/escritura con encoding correcto, maneja archivos grandes eficientemente | Opera archivos correctamente con encoding | Operaciones básicas funcionan | Errores en operaciones básicas |

**Checklist**:
- [ ] Usa `encoding="utf-8"` explícitamente
- [ ] Implementa lectura línea por línea para archivos grandes
- [ ] Maneja correctamente diferentes modos de apertura
- [ ] Usa `with` para todas las operaciones

### Ejercicio 2: Excepciones Robustas (14 pts)

| Criterio | Excelente (14) | Bueno (10) | Suficiente (7) | Insuficiente (0-6) |
|----------|----------------|-----------|----------------|-------------------|
| **Manejo de excepciones** | Jerarquía correcta, excepciones específicas, logging apropiado, re-raise cuando corresponde | Maneja excepciones correctamente con mensajes claros | Try/except funcional básico | Captura genérica sin manejo adecuado |

**Checklist**:
- [ ] Captura excepciones específicas antes que genéricas
- [ ] Usa `else` y `finally` apropiadamente
- [ ] Crea excepciones personalizadas con mensajes útiles
- [ ] No silencia excepciones sin justificación
- [ ] Implementa logging de errores

### Ejercicio 3: Context Managers Custom (14 pts)

| Criterio | Excelente (14) | Bueno (10) | Suficiente (7) | Insuficiente (0-6) |
|----------|----------------|-----------|----------------|-------------------|
| **Context managers propios** | Implementa con clase y decorador, maneja excepciones en `__exit__`, documentación completa | Implementa context manager funcional con cleanup | Context manager básico funciona | No logra implementar context manager |

**Checklist**:
- [ ] Implementa `__enter__` y `__exit__` correctamente
- [ ] Usa `@contextmanager` de `contextlib`
- [ ] Maneja excepciones dentro del context manager
- [ ] Garantiza liberación de recursos en todos los casos
- [ ] Type hints en firmas

---

## 📦 Evidencia de Producto (30 pts)

### Proyecto: Sistema de Logs y Análisis

| Criterio | Excelente (10) | Bueno (7) | Suficiente (5) | Insuficiente (0-4) |
|----------|----------------|-----------|----------------|-------------------|
| **Procesamiento de archivos** | Lee múltiples formatos, procesa archivos grandes eficientemente, encoding robusto | Procesa archivos correctamente con buen manejo de errores | Procesamiento básico funciona | Errores frecuentes en procesamiento |
| **Manejo de errores** | Sistema completo de excepciones, recuperación de errores, logging detallado | Manejo robusto de errores comunes | Try/except en puntos críticos | Sin manejo de errores o muy básico |
| **Context managers** | Context managers propios para recursos, composición de managers, cleanup garantizado | Usa context managers apropiadamente | Usa `with` para archivos | No usa context managers |

### Criterios Adicionales del Proyecto

| Aspecto | Puntos | Descripción |
|---------|--------|-------------|
| **Código limpio** | +2 | Funciones pequeñas, nombres descriptivos |
| **Type hints** | +2 | Tipado completo y correcto |
| **Documentación** | +2 | Docstrings en funciones principales |
| **Tests** | +2 | Tests para casos edge y errores |
| **Eficiencia** | +2 | Manejo eficiente de memoria con archivos grandes |

**Puntos extra máximos**: 10 pts (no excede 100 total)

---

## 📝 Rúbrica Detallada por Competencias

### Manejo de Archivos

| Nivel | Descripción | Indicadores |
|-------|-------------|-------------|
| **Experto** | Domina todas las operaciones de archivo | Usa pathlib, maneja encodings, procesa binarios |
| **Competente** | Opera archivos correctamente | Lectura/escritura con `with`, encoding UTF-8 |
| **En desarrollo** | Conoce operaciones básicas | Abre y lee archivos simples |
| **Inicial** | Dificultad con archivos | Errores frecuentes, no usa `with` |

### Excepciones

| Nivel | Descripción | Indicadores |
|-------|-------------|-------------|
| **Experto** | Sistema completo de manejo de errores | Excepciones custom, jerarquía, logging, recovery |
| **Competente** | Maneja errores apropiadamente | Try/except específicos, mensajes claros |
| **En desarrollo** | Conoce try/except | Captura básica, puede silenciar errores |
| **Inicial** | No maneja excepciones | Código sin protección ante errores |

### Context Managers

| Nivel | Descripción | Indicadores |
|-------|-------------|-------------|
| **Experto** | Crea y usa context managers | Implementa con clase y decorador, composición |
| **Competente** | Usa context managers correctamente | `with` para archivos y recursos |
| **En desarrollo** | Conoce `with` para archivos | Uso básico de `with open()` |
| **Inicial** | No usa context managers | Open/close manual, fugas de recursos |

---

## ⚠️ Penalizaciones

| Infracción | Penalización |
|------------|--------------|
| No usar `with` para archivos | -5 pts |
| Silenciar excepciones sin justificación (`except: pass`) | -5 pts |
| Capturar `Exception` o `BaseException` sin re-raise | -3 pts |
| No especificar encoding en archivos de texto | -3 pts |
| Hardcodear rutas de archivo | -2 pts |
| No cerrar recursos manualmente si no usa `with` | -5 pts |
| Código sin type hints | -3 pts |
| Funciones sin docstrings | -2 pts |

---

## 🎯 Criterios de Aprobación

### Requisitos Mínimos

- [ ] Puntuación total ≥ 70 pts
- [ ] Conocimiento ≥ 21 pts (70% de 30)
- [ ] Desempeño ≥ 28 pts (70% de 40)
- [ ] Producto ≥ 21 pts (70% de 30)

### Para Obtener Distinción (90+ pts)

- [ ] Excepciones personalizadas bien diseñadas
- [ ] Context managers con clase y decorador
- [ ] Manejo eficiente de archivos grandes
- [ ] Sistema completo de logging
- [ ] Cobertura de tests > 80%
- [ ] Documentación completa

---

## 📊 Escala de Calificación

| Rango | Calificación | Descripción |
|-------|--------------|-------------|
| 95-100 | A+ | Excepcional |
| 90-94 | A | Excelente |
| 85-89 | B+ | Muy Bueno |
| 80-84 | B | Bueno |
| 75-79 | C+ | Satisfactorio |
| 70-74 | C | Suficiente |
| 60-69 | D | Insuficiente |
| 0-59 | F | Reprobado |

---

## 📅 Fechas Importantes

| Entregable | Fecha Límite |
|------------|--------------|
| Ejercicios 1-3 | Día 5 de la semana |
| Proyecto completo | Día 6 de la semana |
| Cuestionario teórico | Día 7 de la semana |

---

## 💡 Consejos para Maximizar Puntuación

1. **Siempre usa `with`** para operaciones con archivos
2. **Especifica encoding** en todas las operaciones de texto
3. **Captura excepciones específicas** antes que genéricas
4. **No silencies errores** - al menos loguéalos
5. **Implementa context managers** de ambas formas (clase y decorador)
6. **Procesa archivos grandes** línea por línea
7. **Documenta** el comportamiento ante errores
8. **Testea** casos edge (archivo vacío, permisos, encoding)
