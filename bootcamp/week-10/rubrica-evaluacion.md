# 📋 Rúbrica de Evaluación - Semana 10

## 🎯 Clases Abstractas, Módulos y Paquetes

### Información General

| Aspecto | Detalle |
|---------|---------|
| **Semana** | 10 de 14 |
| **Tema** | Clases Abstractas, Módulos y Paquetes |
| **Puntos totales** | 100 |
| **Puntos mínimos para aprobar** | 70 |

---

## 📊 Distribución de Evidencias

| Tipo de Evidencia | Porcentaje | Puntos |
|-------------------|------------|--------|
| 🧠 Conocimiento | 30% | 30 |
| 💪 Desempeño | 40% | 40 |
| 📦 Producto | 30% | 30 |

---

## 🧠 Evidencia de Conocimiento (30 puntos)

### Evaluación Teórica

| Criterio | Excelente (10) | Bueno (7-9) | Regular (4-6) | Insuficiente (0-3) |
|----------|---------------|-------------|---------------|-------------------|
| **Clases Abstractas** | Explica ABC, abstractmethod, cuándo usar y diferencia con clases concretas | Comprende ABC y abstractmethod, alguna confusión en aplicación | Conocimiento básico, no distingue bien cuándo aplicar | No comprende el concepto de abstracción |
| **Protocols vs ABC** | Distingue claramente tipado nominal vs estructural, sabe cuándo usar cada uno | Entiende la diferencia, duda en casos complejos | Confunde los dos conceptos frecuentemente | No diferencia entre Protocol y ABC |
| **Módulos y Paquetes** | Explica `__init__.py`, imports relativos/absolutos, namespace packages | Comprende estructura básica, algún error en imports | Conoce módulos pero confunde paquetes | No entiende la organización modular |

**Puntos Conocimiento: ___ / 30**

---

## 💪 Evidencia de Desempeño (40 puntos)

### Ejercicios Prácticos

#### Ejercicio 1: Sistema de Plugins con ABC (15 puntos)

| Criterio | Puntos | Logrado |
|----------|--------|---------|
| Clase abstracta `Plugin` correctamente definida | 4 | ☐ |
| Métodos abstractos con decoradores apropiados | 3 | ☐ |
| Al menos 2 plugins concretos implementados | 4 | ☐ |
| Gestor de plugins funcional | 4 | ☐ |

#### Ejercicio 2: Organización en Módulos (12 puntos)

| Criterio | Puntos | Logrado |
|----------|--------|---------|
| Separación lógica en múltiples módulos | 3 | ☐ |
| Imports absolutos correctos | 3 | ☐ |
| Imports relativos donde corresponde | 3 | ☐ |
| `__init__.py` con exports públicos | 3 | ☐ |

#### Ejercicio 3: Crear un Paquete Completo (13 puntos)

| Criterio | Puntos | Logrado |
|----------|--------|---------|
| Estructura `src/` layout correcta | 3 | ☐ |
| `pyproject.toml` con metadata completa | 4 | ☐ |
| Dependencias declaradas correctamente | 3 | ☐ |
| Paquete instalable con `uv pip install -e .` | 3 | ☐ |

**Puntos Desempeño: ___ / 40**

---

## 📦 Evidencia de Producto (30 puntos)

### Proyecto: Sistema de Procesamiento de Datos

#### Arquitectura y Diseño (10 puntos)

| Criterio | Excelente (10) | Bueno (7-9) | Regular (4-6) | Insuficiente (0-3) |
|----------|---------------|-------------|---------------|-------------------|
| **Estructura del Proyecto** | Sigue src layout, separación clara de responsabilidades, imports limpios | Buena estructura con detalles menores | Estructura funcional pero desorganizada | Código en un solo archivo o mal organizado |

#### Implementación de Abstracciones (10 puntos)

| Criterio | Puntos | Logrado |
|----------|--------|---------|
| Clase abstracta `DataProcessor` correcta | 3 | ☐ |
| Protocol `DataSource` implementado | 2 | ☐ |
| Al menos 3 procesadores concretos | 3 | ☐ |
| Sistema de plugins funcional | 2 | ☐ |

#### Configuración y Distribución (10 puntos)

| Criterio | Puntos | Logrado |
|----------|--------|---------|
| `pyproject.toml` completo y correcto | 3 | ☐ |
| Dependencias con versiones especificadas | 2 | ☐ |
| Entry points configurados (opcional) | 2 | ☐ |
| Tests con pytest pasando | 3 | ☐ |

**Puntos Producto: ___ / 30**

---

## 📝 Criterios Adicionales

### Calidad del Código

| Aspecto | Cumple | No Cumple |
|---------|--------|-----------|
| Type hints en todas las funciones públicas | ☐ | ☐ |
| Docstrings en clases y métodos públicos | ☐ | ☐ |
| Nombres descriptivos (snake_case, PascalCase) | ☐ | ☐ |
| Sin código duplicado | ☐ | ☐ |
| Imports organizados (stdlib, third-party, local) | ☐ | ☐ |

### Penalizaciones

| Infracción | Penalización |
|------------|--------------|
| Imports circulares | -5 puntos |
| `from module import *` usado | -3 puntos |
| Código sin type hints | -5 puntos |
| pyproject.toml mal formado | -5 puntos |
| Entrega tardía (por día) | -10 puntos |

### Bonificaciones

| Logro Extra | Bonificación |
|-------------|--------------|
| Entry points CLI configurados | +5 puntos |
| Plugin dinámico con importlib | +5 puntos |
| Documentación con ejemplos de uso | +3 puntos |
| Publicado en TestPyPI | +5 puntos |

---

## 🎯 Resumen de Evaluación

```
┌─────────────────────────────────────────────────────────┐
│ RESUMEN DE PUNTUACIÓN                                   │
├─────────────────────────────────────────────────────────┤
│ Conocimiento (Teoría):           ___ / 30              │
│ Desempeño (Ejercicios):          ___ / 40              │
│ Producto (Proyecto):             ___ / 30              │
├─────────────────────────────────────────────────────────┤
│ Penalizaciones:                  - ___                  │
│ Bonificaciones:                  + ___                  │
├─────────────────────────────────────────────────────────┤
│ TOTAL:                           ___ / 100             │
└─────────────────────────────────────────────────────────┘

Calificación:
- 90-100: Excelente (A)
- 80-89:  Muy Bueno (B)
- 70-79:  Bueno (C)
- 60-69:  Regular (D)
- < 60:   Insuficiente (F)
```

---

## ✅ Checklist de Entrega

Antes de entregar, verifica:

### Ejercicios
- [ ] Ejercicio 1: Sistema de plugins funcional
- [ ] Ejercicio 2: Módulos correctamente organizados
- [ ] Ejercicio 3: Paquete instalable con uv

### Proyecto
- [ ] Estructura src layout
- [ ] pyproject.toml configurado
- [ ] Clases abstractas implementadas
- [ ] Al menos 3 procesadores concretos
- [ ] Tests pasando
- [ ] Documentación incluida

### Calidad
- [ ] Type hints completos
- [ ] Docstrings presentes
- [ ] Sin imports circulares
- [ ] Código ejecuta sin errores

---

## 📚 Recursos de Apoyo

Si tienes dificultades, revisa:

1. **Clases Abstractas**: [1-teoria/01-clases-abstractas.md](1-teoria/01-clases-abstractas.md)
2. **Protocols**: [1-teoria/02-protocols-interfaces.md](1-teoria/02-protocols-interfaces.md)
3. **Módulos**: [1-teoria/03-modulos-imports.md](1-teoria/03-modulos-imports.md)
4. **Paquetes**: [1-teoria/04-paquetes-dependencias.md](1-teoria/04-paquetes-dependencias.md)

---

## 🔗 Navegación

| ← Anterior | Actual | Siguiente → |
|------------|--------|-------------|
| [Rúbrica Week-09](../week-09/rubrica-evaluacion.md) | **Rúbrica Week-10** | [Rúbrica Week-11](../week-11/rubrica-evaluacion.md) |
