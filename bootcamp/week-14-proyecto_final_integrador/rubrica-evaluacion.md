# 📋 Rúbrica de Evaluación - Semana 14

## Proyecto Final: Weather Dashboard CLI

**Total de puntos posibles**: 150 puntos
**Puntos mínimos para aprobar**: 105 puntos (70%)

---

## 🧠 Conocimiento (30 puntos)

Evaluación de comprensión conceptual demostrada en el proyecto.

### Arquitectura y Diseño (15 puntos)

| Criterio | Excelente (15) | Bueno (12) | Aceptable (9) | Insuficiente (0-5) |
|----------|----------------|------------|---------------|-------------------|
| Separación de responsabilidades | Módulos claramente definidos, SRP aplicado | Buena separación con algunos acoplamientos | Separación básica | Todo en pocos archivos |
| Estructura de carpetas | Profesional, escalable | Organizada | Funcional | Desorganizada |
| Patrones de diseño | Aplica patrones apropiados | Algunos patrones | Mínimo | Sin patrones |

### Comprensión de APIs (15 puntos)

| Criterio | Excelente (15) | Bueno (12) | Aceptable (9) | Insuficiente (0-5) |
|----------|----------------|------------|---------------|-------------------|
| Uso de requests | Manejo completo con sesiones | Uso correcto básico | Funcional | Con errores |
| Manejo de respuestas | JSON, errores HTTP, timeouts | JSON y errores básicos | Solo JSON | Sin manejo |
| Autenticación API | API key segura (.env) | API key en config | API key hardcoded | Sin implementar |

---

## 💪 Desempeño (60 puntos)

Evaluación de la implementación y calidad del código.

### Funcionalidad Core (25 puntos)

| Funcionalidad | Puntos | Criterio |
|---------------|--------|----------|
| Clima actual | 8 | Muestra temp, humedad, viento, descripción |
| Pronóstico 5 días | 8 | Muestra datos por día correctamente |
| Ciudades favoritas | 5 | CRUD completo con persistencia |
| Historial | 4 | Registro y consulta de búsquedas |

### Calidad del Código (20 puntos)

| Criterio | Excelente (20) | Bueno (16) | Aceptable (12) | Insuficiente (0-8) |
|----------|----------------|------------|----------------|-------------------|
| Type hints | Completos en todo el código | En funciones públicas | Parciales | Sin type hints |
| Nombrado | Claro, consistente, en inglés | Mayormente claro | Aceptable | Confuso |
| Complejidad | Funciones pequeñas, claras | Algunas funciones largas | Varias funciones complejas | Código espagueti |
| DRY | Sin repetición | Mínima repetición | Algo de repetición | Mucha duplicación |

### Manejo de Errores (15 puntos)

| Criterio | Excelente (15) | Bueno (12) | Aceptable (9) | Insuficiente (0-5) |
|----------|----------------|------------|---------------|-------------------|
| Excepciones personalizadas | Jerarquía propia bien diseñada | Algunas excepciones propias | Usa excepciones estándar | Sin manejo |
| Try/except | Específico y bien ubicado | Correcto en la mayoría | Básico | Catch-all o ausente |
| Mensajes de error | Claros y útiles para el usuario | Informativos | Genéricos | Crípticos o ausentes |
| Logging | DEBUG, INFO, ERROR apropiados | Logging básico | Solo print | Sin logging |

---

## 📦 Producto (60 puntos)

Evaluación del entregable final.

### Testing (25 puntos)

| Criterio | Excelente (25) | Bueno (20) | Aceptable (15) | Insuficiente (0-10) |
|----------|----------------|------------|----------------|-------------------|
| Cobertura | >90% | 85-90% | 75-85% | <75% |
| Calidad de tests | AAA, casos edge, parametrizados | Buenos tests unitarios | Tests básicos | Tests mínimos |
| Mocking | Mock de API, fixtures complejas | Mocking básico | Algunos mocks | Sin mocking |
| Organización | conftest.py, bien estructurado | Organizado | Funcional | Desorganizado |

### Documentación (20 puntos)

| Criterio | Excelente (20) | Bueno (16) | Aceptable (12) | Insuficiente (0-8) |
|----------|----------------|------------|----------------|-------------------|
| README.md | Completo, badges, screenshots | Buena documentación | Instrucciones básicas | Mínimo o ausente |
| Docstrings | Google/NumPy style, completos | En funciones públicas | Parciales | Sin docstrings |
| Comentarios | Explican el "por qué" | Útiles | Algunos | Excesivos o ausentes |
| .env.example | Completo con instrucciones | Presente | - | Ausente |

### Interfaz CLI (15 puntos)

| Criterio | Excelente (15) | Bueno (12) | Aceptable (9) | Insuficiente (0-5) |
|----------|----------------|------------|---------------|-------------------|
| UX | Intuitiva, colores, formato | Clara y usable | Funcional | Confusa |
| Comandos | argparse/click bien implementado | Argumentos básicos | Input simple | Sin estructura |
| Ayuda | --help completo y útil | Ayuda básica | Mínima | Sin ayuda |
| Feedback | Spinners, progreso, confirmaciones | Mensajes claros | Básico | Sin feedback |

---

## 🌟 Puntos Extra (hasta 20 puntos adicionales)

| Feature Extra | Puntos |
|---------------|--------|
| Cache de respuestas API (con TTL) | +5 |
| Exportación a CSV | +3 |
| Exportación a PDF | +5 |
| Gráficos ASCII del pronóstico | +4 |
| Soporte multi-idioma (i18n) | +5 |
| Docker + docker-compose | +5 |
| CI/CD con GitHub Actions | +5 |
| Alertas meteorológicas | +3 |

**Máximo puntos extra**: 20 puntos

---

## 📊 Escala de Calificación

| Puntos | Calificación | Descripción |
|--------|--------------|-------------|
| 135-150+ | A (Excelente) | Excede expectativas, listo para producción |
| 120-134 | B (Muy Bueno) | Cumple todos los requisitos con calidad |
| 105-119 | C (Bueno) | Cumple requisitos mínimos |
| 90-104 | D (Aceptable) | Necesita mejoras, aprobado condicional |
| <90 | F (Insuficiente) | No aprueba, requiere reentrega |

---

## 📝 Checklist de Entrega

### Estructura del Proyecto
- [ ] Carpeta `src/` con código organizado en módulos
- [ ] Carpeta `tests/` con suite de tests
- [ ] Carpeta `data/` para archivos de persistencia
- [ ] `pyproject.toml` con dependencias
- [ ] `README.md` completo
- [ ] `.env.example` con variables necesarias
- [ ] `.gitignore` apropiado

### Funcionalidad
- [ ] Consulta de clima actual funciona
- [ ] Pronóstico de 5 días funciona
- [ ] Agregar/eliminar favoritos funciona
- [ ] Ver historial funciona
- [ ] Manejo de errores (ciudad no encontrada, sin conexión)

### Calidad
- [ ] Type hints en todo el código
- [ ] Docstrings en funciones públicas
- [ ] Sin errores de linting
- [ ] Tests pasan al 100%
- [ ] Cobertura >85%

### Documentación
- [ ] README con descripción del proyecto
- [ ] Instrucciones de instalación
- [ ] Guía de uso con ejemplos
- [ ] Documentación de la API consumida
- [ ] Screenshots o GIFs de demostración

---

## 🎯 Presentación (Evaluación Oral - 10 minutos)

| Aspecto | Puntos | Criterio |
|---------|--------|----------|
| Demo funcional | 5 | Muestra todas las funcionalidades |
| Explicación técnica | 5 | Explica decisiones de diseño |
| Respuesta a preguntas | 5 | Demuestra comprensión profunda |
| Tiempo | - | Penalización si excede 15 min |

**Nota**: La presentación es parte del 10% del criterio "Presentación" en la calificación general.

---

## 📅 Fechas Importantes

| Hito | Fecha |
|------|-------|
| Inicio del proyecto | Día 1 de la semana |
| Checkpoint (50% funcionalidad) | Día 3 |
| Entrega final | Día 7 |
| Presentaciones | Día 7-8 |

---

## 💡 Consejos para Maximizar tu Puntuación

1. **Empieza por la arquitectura**: Un buen diseño inicial ahorra tiempo
2. **Tests primero**: TDD te ayuda a pensar mejor
3. **Commits descriptivos**: Demuestra tu proceso de desarrollo
4. **No dejes la documentación para el final**: Documenta mientras codeas
5. **Prueba tu app como usuario**: ¿Es intuitiva?
6. **Pide feedback**: Un compañero puede encontrar bugs que tú no ves

---

*Rúbrica v1.0 | Proyecto Final | Bootcamp Python Zero to Hero*
