# 📊 Rúbrica de Evaluación - Semana 13

## Testing con pytest, Debugging y Logging

---

## 🎯 Competencias a Evaluar

| Competencia | Descripción |
|-------------|-------------|
| **Testing** | Capacidad de escribir tests efectivos y mantenibles |
| **Fixtures** | Uso correcto de fixtures para setup/teardown |
| **Parametrización** | Implementación de tests parametrizados |
| **Mocking** | Aislamiento de dependencias con mocks |
| **Debugging** | Técnicas de debugging profesional |
| **Logging** | Configuración y uso de logging |

---

## 📝 Criterios de Evaluación

### 1. Conocimiento Teórico (25 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Tipos de tests | 5 | Distingue unitarios, integración, e2e |
| Patrón AAA | 5 | Aplica Arrange-Act-Assert correctamente |
| Fixtures | 5 | Comprende scopes y uso de conftest.py |
| Logging levels | 5 | Conoce DEBUG, INFO, WARNING, ERROR, CRITICAL |
| TDD | 5 | Entiende el ciclo Red-Green-Refactor |

### 2. Ejercicios Prácticos (35 puntos)

| Ejercicio | Puntos | Criterios |
|-----------|--------|-----------|
| **01: Primeros Tests** | 10 | Tests pasan, assertions correctas, nombres descriptivos |
| **02: Fixtures y Parametrize** | 12 | Fixtures reutilizables, parametrización efectiva |
| **03: Mocking y Coverage** | 13 | Mocks correctos, cobertura > 80% |

#### Desglose Ejercicio 01 (10 puntos)
- Tests ejecutan sin errores: 3 pts
- Assertions apropiadas: 3 pts
- Nombres descriptivos: 2 pts
- Organización de archivos: 2 pts

#### Desglose Ejercicio 02 (12 puntos)
- Fixtures funcionan correctamente: 4 pts
- Uso de scope apropiado: 3 pts
- Tests parametrizados: 3 pts
- conftest.py bien estructurado: 2 pts

#### Desglose Ejercicio 03 (13 puntos)
- Mocks implementados correctamente: 5 pts
- Aislamiento de dependencias: 3 pts
- Reporte de cobertura generado: 3 pts
- Cobertura > 80%: 2 pts

### 3. Proyecto Semanal (40 puntos)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **Funcionalidad** | 15 | Todos los tests pasan |
| **Cobertura** | 10 | Coverage > 90% |
| **Fixtures** | 5 | Uso efectivo de fixtures |
| **Parametrización** | 5 | Tests parametrizados para edge cases |
| **Logging** | 5 | Sistema de logging implementado |

#### Escala de Cobertura
| Cobertura | Puntos |
|-----------|--------|
| > 95% | 10 |
| 90-95% | 8 |
| 80-90% | 6 |
| 70-80% | 4 |
| < 70% | 2 |

---

## 📊 Escala de Calificación

| Nivel | Puntaje | Descripción |
|-------|---------|-------------|
| **Excelente** | 90-100 | Dominio completo, tests de alta calidad |
| **Bueno** | 80-89 | Buen manejo, tests funcionales |
| **Satisfactorio** | 70-79 | Cumple requisitos básicos |
| **En desarrollo** | 60-69 | Necesita práctica adicional |
| **Insuficiente** | < 60 | No cumple objetivos mínimos |

---

## ✅ Lista de Verificación del Proyecto

### Tests Unitarios
- [ ] Cada función tiene al menos un test
- [ ] Tests cubren casos normales
- [ ] Tests cubren casos edge
- [ ] Tests cubren casos de error

### Fixtures
- [ ] Fixtures definidas en conftest.py
- [ ] Scope apropiado (function, class, module, session)
- [ ] Fixtures son reutilizables
- [ ] Cleanup/teardown cuando necesario

### Parametrización
- [ ] Tests parametrizados para múltiples inputs
- [ ] IDs descriptivos para cada caso
- [ ] Cubre casos edge con parametrize

### Mocking
- [ ] Dependencias externas mockeadas
- [ ] patch aplicado correctamente
- [ ] Assertions sobre calls de mocks

### Logging
- [ ] Logger configurado
- [ ] Niveles apropiados usados
- [ ] Formato de mensajes consistente
- [ ] Archivo de log generado

### Cobertura
- [ ] pytest-cov instalado
- [ ] Reporte HTML generado
- [ ] Cobertura > 90%
- [ ] Líneas críticas cubiertas

---

## 🏆 Criterios de Excelencia

Para obtener puntuación máxima:

1. **Tests Descriptivos**: Nombres que explican qué se prueba
2. **Aislamiento**: Cada test es independiente
3. **Rapidez**: Tests ejecutan en < 5 segundos total
4. **Mantenibilidad**: Código de tests limpio y DRY
5. **Edge Cases**: Cobertura de casos límite
6. **Documentación**: Docstrings en fixtures complejas

---

## 📚 Recursos de Apoyo

- [pytest Documentation](https://docs.pytest.org/)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

---

## ⚠️ Penalizaciones

| Situación | Penalización |
|-----------|--------------|
| Tests que fallan | -5 pts por test |
| Sin reporte de cobertura | -10 pts |
| Código duplicado en tests | -5 pts |
| Sin fixtures cuando apropiado | -5 pts |
| Mocks incorrectos | -5 pts |
| Entrega tardía | -10% por día |
