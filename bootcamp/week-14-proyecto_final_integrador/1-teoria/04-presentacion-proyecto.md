# 🎤 Presentación del Proyecto

## 🎯 Objetivos

- Estructurar una presentación técnica efectiva
- Preparar una demo que destaque tu trabajo
- Responder preguntas técnicas con confianza
- Comunicar decisiones de diseño claramente

---

## 1. Estructura de la Presentación (10 minutos)

### 1.1 Distribución del Tiempo

| Sección | Tiempo | Contenido |
|---------|--------|-----------|
| Introducción | 1 min | Qué hace tu proyecto |
| Demo en vivo | 4 min | Mostrar funcionalidades |
| Arquitectura | 2 min | Decisiones técnicas |
| Desafíos | 2 min | Problemas y soluciones |
| Cierre | 1 min | Aprendizajes y mejoras futuras |

### 1.2 Script de Presentación

```
🎬 INTRODUCCIÓN (1 min)
"Weather Dashboard es una aplicación CLI que permite consultar
el clima de cualquier ciudad del mundo. Las principales
características son: clima actual, pronóstico de 5 días,
sistema de favoritos y historial de búsquedas."

🖥️ DEMO (4 min)
[Mostrar cada funcionalidad en terminal]

🏗️ ARQUITECTURA (2 min)
"El proyecto sigue una arquitectura en capas..."
[Mostrar diagrama o estructura de carpetas]

⚠️ DESAFÍOS (2 min)
"El mayor desafío fue manejar errores de la API..."
[Explicar solución implementada]

🎯 CIERRE (1 min)
"Los principales aprendizajes fueron...
Como mejora futura implementaría..."
```

---

## 2. Preparando la Demo

### 2.1 Checklist Pre-Demo

```bash
# Verificar que todo funciona
□ API key configurada en .env
□ Dependencias instaladas (uv sync)
□ Tests pasando (uv run pytest)
□ Terminal con fuente legible
□ Conexión a internet estable
□ Datos de prueba preparados
```

### 2.2 Guión de Demo

```bash
# 1. Mostrar ayuda del CLI
uv run python -m src.main --help

# 2. Consultar clima actual
uv run python -m src.main weather Madrid
# → Mostrar formato de salida, colores, información

# 3. Consultar otra ciudad (con país)
uv run python -m src.main weather "London,UK"

# 4. Mostrar pronóstico
uv run python -m src.main forecast Barcelona

# 5. Gestionar favoritos
uv run python -m src.main favorites add Madrid
uv run python -m src.main favorites add Barcelona
uv run python -m src.main favorites list
uv run python -m src.main favorites weather

# 6. Mostrar historial
uv run python -m src.main history

# 7. Demostrar manejo de errores
uv run python -m src.main weather "CiudadQueNoExiste123"
# → Mostrar mensaje de error amigable
```

### 2.3 Plan B: Si Algo Falla

```python
# Tener datos mockeados listos
MOCK_WEATHER = {
    "city": "Madrid",
    "temperature": 22.5,
    "description": "Cielo despejado",
    "humidity": 45,
}

# Script de respaldo que no requiere API
def demo_offline():
    """Demo que funciona sin conexión."""
    print("=== MODO DEMO (offline) ===")
    print(f"Ciudad: {MOCK_WEATHER['city']}")
    print(f"Temperatura: {MOCK_WEATHER['temperature']}°C")
    # ...
```

---

## 3. Explicando Arquitectura

### 3.1 Diagrama Simple

```
┌─────────────────────────────────────────────────┐
│                    CLI (main.py)                │
│            Interacción con usuario              │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│               SERVICES                          │
│  WeatherService │ FavoritesService │ History    │
│         Lógica de negocio                       │
└────────┬────────────────────────────┬───────────┘
         │                            │
┌────────▼────────┐          ┌────────▼────────┐
│   API CLIENT    │          │    STORAGE      │
│  WeatherClient  │          │   JsonStorage   │
│  (requests)     │          │   (archivos)    │
└────────┬────────┘          └────────┬────────┘
         │                            │
         ▼                            ▼
   OpenWeatherMap              favorites.json
       API                     history.json
```

### 3.2 Puntos Clave a Explicar

1. **Separación de responsabilidades**
   > "Cada módulo tiene una sola función. El cliente API solo hace requests,
   > los servicios manejan la lógica, el storage solo persiste datos."

2. **Inyección de dependencias**
   > "Los servicios reciben sus dependencias por constructor,
   > lo que facilita el testing con mocks."

3. **Manejo de errores**
   > "Tengo excepciones personalizadas para cada tipo de error:
   > CityNotFoundError, APIError, StorageError..."

4. **Testing**
   > "Mockeo la API externa para tests rápidos y confiables.
   > Tengo cobertura del 90% con pytest-cov."

---

## 4. Hablando de Desafíos

### 4.1 Formato: Problema → Solución → Resultado

```
❌ PROBLEMA:
"La API a veces tardaba mucho o fallaba,
haciendo que la aplicación se colgara."

✅ SOLUCIÓN:
"Implementé timeouts de 10 segundos, reintentos
automáticos con backoff exponencial, y mensajes
de error amigables para el usuario."

📊 RESULTADO:
"Ahora la app siempre responde en menos de 30 segundos
y el usuario siempre recibe feedback claro."
```

### 4.2 Desafíos Comunes y Cómo Explicarlos

| Desafío | Explicación |
|---------|-------------|
| Manejo de API | "Implementé retry con backoff y cache para reducir requests" |
| Persistencia | "Usé JSON para simplicidad, con validación al cargar" |
| Testing | "Mockeé servicios externos para tests determinísticos" |
| CLI UX | "Usé colores y formato tabular para mejor legibilidad" |
| Configuración | "Variables de entorno con .env para seguridad" |

---

## 5. Respondiendo Preguntas

### 5.1 Preguntas Técnicas Frecuentes

**"¿Por qué elegiste esta estructura de carpetas?"**
> "Seguí el patrón de arquitectura en capas para separar
> responsabilidades. Esto hace el código más testeable
> y fácil de mantener."

**"¿Cómo manejas errores de la API?"**
> "Tengo una jerarquía de excepciones personalizadas.
> El cliente API captura errores HTTP y los transforma
> en excepciones de dominio como CityNotFoundError."

**"¿Por qué usaste dataclasses en lugar de diccionarios?"**
> "Las dataclasses dan type safety, autocompletado en el IDE,
> y hacen el código más legible. Además, puedo añadir
> métodos y validación."

**"¿Cómo testeas el código que llama a la API?"**
> "Uso unittest.mock para mockear el cliente HTTP.
> Así mis tests son rápidos, no dependen de internet,
> y puedo simular diferentes escenarios."

**"¿Qué harías diferente si empezaras de nuevo?"**
> "Implementaría cache desde el principio para reducir
> llamadas a la API. También consideraría usar una
> base de datos SQLite en lugar de JSON."

### 5.2 Cómo Responder Si No Sabes

```
✅ BIEN:
"No estoy seguro de eso específicamente, pero investigaría
en la documentación de [X]. Lo que sí sé es que..."

"Esa es una buena pregunta. En mi implementación actual
no lo consideré, pero sería una mejora interesante porque..."

❌ MAL:
"No sé" (sin más)
Inventar una respuesta
Ponerse nervioso y divagar
```

---

## 6. Tips para el Día de la Presentación

### 6.1 Antes de Presentar

```
□ Dormir bien la noche anterior
□ Probar todo 1 hora antes
□ Tener terminal lista con comandos recientes
□ Cerrar notificaciones y apps innecesarias
□ Preparar agua
□ Respirar profundo
```

### 6.2 Durante la Presentación

```
✅ HACER:
• Hablar claro y a ritmo moderado
• Mirar a la audiencia (o cámara)
• Mostrar entusiasmo por tu trabajo
• Admitir limitaciones honestamente
• Agradecer las preguntas

❌ EVITAR:
• Leer de un script palabra por palabra
• Hablar demasiado rápido
• Disculparse excesivamente
• Menospreciar tu trabajo
• Exceder el tiempo asignado
```

### 6.3 Lenguaje Corporal (presencial)

- Mantén contacto visual
- Usa las manos para enfatizar puntos
- Párate derecho/a con confianza
- Sonríe naturalmente
- No cruces los brazos

---

## 7. Ejemplo de Presentación Completa

### Slide 1: Título
```
🌤️ Weather Dashboard CLI
Tu clima en la terminal

[Tu nombre]
Bootcamp Python Zero to Hero
Enero 2026
```

### Slide 2: ¿Qué hace?
```
✨ Funcionalidades:

• 🌡️ Clima actual de cualquier ciudad
• 📊 Pronóstico de 5 días
• ⭐ Ciudades favoritas
• 📈 Historial de búsquedas
• 🎨 Interfaz colorida
```

### Slide 3: Demo
```
[DEMO EN VIVO]

Comandos a mostrar:
1. weather Madrid
2. forecast Barcelona
3. favorites add/list
4. history
5. Manejo de errores
```

### Slide 4: Arquitectura
```
[DIAGRAMA DE CAPAS]

• CLI → Services → API/Storage
• Separación de responsabilidades
• Inyección de dependencias
• Excepciones personalizadas
```

### Slide 5: Números
```
📊 Métricas del proyecto:

• 📁 15 archivos de código
• 📝 ~1,200 líneas de Python
• ✅ 45 tests
• 📈 92% cobertura
• 🔧 5 dependencias
```

### Slide 6: Desafíos
```
⚠️ Mayor desafío: Manejo de errores de API

Problema: Timeouts y errores 404
Solución: Retry + excepciones personalizadas
Resultado: UX robusta y amigable
```

### Slide 7: Aprendizajes
```
🎓 Lo que aprendí:

• Arquitectura de software real
• Consumo de APIs con requests
• Testing con mocks
• Documentación profesional
• ¡Python es genial! 🐍
```

### Slide 8: Futuro
```
🚀 Mejoras futuras:

• Cache con TTL
• Soporte multi-idioma
• Exportación a PDF
• Alertas meteorológicas
• Containerización con Docker
```

### Slide 9: Cierre
```
¡Gracias!

🔗 github.com/tu-usuario/weather-dashboard

¿Preguntas?
```

---

## ✅ Checklist Final

- [ ] Presentación estructurada (10 min máx)
- [ ] Demo probada y funcionando
- [ ] Plan B si falla la conexión
- [ ] Diagramas de arquitectura preparados
- [ ] Respuestas a preguntas comunes ensayadas
- [ ] Métricas del proyecto listas (líneas, tests, cobertura)
- [ ] Hablar de desafíos y soluciones
- [ ] Mencionar aprendizajes y mejoras futuras

---

## 📚 Recursos Adicionales

- [How to Give a Great Technical Presentation](https://www.freecodecamp.org/news/how-to-give-a-great-technical-presentation/)
- [The Art of the Demo](https://medium.com/swlh/the-art-of-the-demo-8c6e7e0e1d0e)
- [Presentation Tips for Developers](https://dev.to/aspittel/public-speaking-for-developers-42g9)
