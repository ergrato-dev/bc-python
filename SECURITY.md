# 🔒 Política de Seguridad

## Versiones Soportadas

Este proyecto es principalmente educativo. Las siguientes versiones reciben actualizaciones de seguridad:

| Versión | Soportada |
| ------- | --------- |
| main    | ✅ Sí     |
| < main  | ❌ No     |

## Reportar una Vulnerabilidad

Si descubres una vulnerabilidad de seguridad en este proyecto, por favor sigue estos pasos:

### 🚨 NO reportes vulnerabilidades públicamente

**No** abras un Issue público para reportar vulnerabilidades de seguridad.

### 📧 Proceso de Reporte

1. **Envía un reporte privado** a través de [GitHub Security Advisories](https://github.com/epti-dev/bc-python/security/advisories/new)

2. **Incluye en tu reporte**:

   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducir el problema
   - Impacto potencial
   - Sugerencias de mitigación (si las tienes)

3. **Espera confirmación**: Responderemos dentro de 48 horas confirmando la recepción del reporte.

### ⏱️ Proceso de Respuesta

| Fase                      | Tiempo Estimado |
| ------------------------- | --------------- |
| Confirmación de recepción | 48 horas        |
| Evaluación inicial        | 1 semana        |
| Resolución (si aplica)    | 2-4 semanas     |
| Divulgación pública       | Después del fix |

### 🎖️ Reconocimiento

Agradecemos a quienes reportan vulnerabilidades de manera responsable. Los reportes válidos serán reconocidos en:

- Sección de agradecimientos del README
- Changelog del proyecto

## Mejores Prácticas de Seguridad

Este bootcamp enseña buenas prácticas de seguridad en Python:

### ✅ Lo que enseñamos

- Validación de inputs del usuario
- Manejo seguro de archivos
- No hardcodear secrets
- Uso de variables de entorno
- Hashing seguro de contraseñas
- Sanitización de datos

### ❌ Lo que evitamos

- Ejecución de código arbitrario
- Almacenamiento de credenciales en código
- Operaciones inseguras con archivos
- SQL injection (en ejemplos con DB)

## Dependencias

Mantenemos las dependencias actualizadas y monitoreamos vulnerabilidades conocidas usando:

- Dependabot (GitHub)
- Auditorías periódicas de seguridad

## Contacto

Para cualquier pregunta relacionada con seguridad que no sea una vulnerabilidad, puedes abrir un [Discussion](https://github.com/epti-dev/bc-python/discussions) en la categoría de Seguridad.

---

Gracias por ayudarnos a mantener este proyecto seguro para la comunidad educativa. 🙏
