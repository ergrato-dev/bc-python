# Semana 19: HTTP y APIs con httpx

> **Fase 2 — Python Profesional** · _Junior → Mid-level_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Usar **httpx** en modo sync y async con sesiones reutilizables
- Implementar los esquemas de autenticación más comunes: Bearer Token, API Key, OAuth2 client credentials
- Hacer APIs resilientes con **tenacity**: retry, backoff exponencial y timeouts
- Respetar rate limits con token bucket y el header `Retry-After`
- Validar respuestas de APIs con **Pydantic** y manejar errores HTTP de forma robusta

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [httpx — Fundamentos](1-teoria/01-httpx-fundamentos.md) | Sync/async, Client, params, headers, response object |
| 02 | [Autenticación](1-teoria/02-autenticacion.md) | Bearer Token, API Key, OAuth2 client credentials |
| 03 | [Resiliencia y Retry](1-teoria/03-resiliencia-retry.md) | tenacity, backoff exponencial, timeouts, circuit breaker |
| 04 | [Rate Limiting](1-teoria/04-rate-limiting.md) | Token bucket, sliding window, Retry-After |
| 05 | [Manejo de Errores](1-teoria/05-manejo-errores.md) | HTTPStatusError, ConnectError, validación con Pydantic |

---

## Estructura de la Semana

```
week-19-http_y_apis_httpx/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-ejercicio-httpx-basico/
│   ├── 02-ejercicio-autenticacion/
│   ├── 03-ejercicio-retry-tenacity/
│   └── 04-ejercicio-pydantic-responses/
├── 3-proyecto/
│   ├── README.md           # Studio BC API Client
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: httpx fundamentos + autenticación | 1.5h |
| 2 | Teoría: resiliencia + rate limiting + errores | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Entregables

- [ ] Ejercicio 01: Cliente httpx sync/async, params y headers
- [ ] Ejercicio 02: Auth — Bearer Token y API Key con `httpx.Auth`
- [ ] Ejercicio 03: Retry con tenacity, timeouts configurables
- [ ] Ejercicio 04: Validar respuestas de API con modelos Pydantic
- [ ] Proyecto: `studio-api-client` — cliente de APIs de proveedores de Studio BC

---

## Navegación

← [Semana 18](../week-18-gestion_datos_polars/README.md) · [Semana 20](../week-20-bases_de_datos_sqlmodel/README.md) →
