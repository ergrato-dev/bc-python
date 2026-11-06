# Rúbrica de Evaluación — Semana 02: Operadores, strings, entrada/salida y `match`

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 1 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué dan `17 // 5`, `17 % 5`, `-7 // 2` y `8 / 2`? | 10 |
| 2 | ¿Por qué `value is not None and value > 0` funciona con `value = None` y `value > 0 and value is not None` falla? | 10 |
| 3 | ¿Qué devuelve `"" or "sin etiqueta"`? ¿Y `0.0 or "sin dato"`? ¿Qué problema tiene usar `or` para valores por defecto en medidas? | 10 |
| 4 | Clasificas notas con `if score < 4.0: ... elif score < 3.0: ...`. ¿Qué sale con `2.0` y por qué? | 10 |
| 5 | Con `s = "Python"`, ¿qué dan `s[1:4]`, `s[-2:]`, `s[::-1]`, `s[10:]` y `s[10]`? | 10 |
| 6 | Escribes `name.strip()` en una línea y después usas `name`. ¿Por qué sigue teniendo espacios? | 10 |
| 7 | ¿Qué dan `f"{1234.5:,.2f}"`, `f"{0.256:.1%}"` y `f"{'ab':>5}"`? | 10 |
| 8 | ¿Qué produce `t"Hola, {name}"` y para qué sirve que no sea un `str`? | 10 |
| 9 | En un `match`, ¿qué diferencia hay entre `case ["hola", name]:` y `case "hola":`? ¿Qué pasa con `case LIMIT:` si `LIMIT` es una constante? | 10 |
| 10 | ¿Por qué un error se escribe en stderr y no en stdout, y qué código de salida devuelve un programa cuando la línea es inválida y cuando sobran argumentos? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `3`, `2`, `-4` (redondea hacia abajo, no hacia el cero) y `4.0` (`/` siempre da `float`).
2. Por el cortocircuito: en la primera, `value is not None` es `False` y Python no evalúa `value > 0`. En la segunda, compara `None > 0` y lanza `TypeError`. La condición que protege va primero.
3. `"sin etiqueta"` y `"sin dato"`. `or` reemplaza cualquier valor falso, y `0` y `0.0` son falsos: una medida real de `0.0` se convierte en el valor por defecto sin avisar. Para "falta el dato", `is None`.
4. Lo que devuelva la rama de `score < 4.0` ("aceptable" en la teoría 02), no "insuficiente": `2.0 < 4.0` es verdadero y gana el primer `if`; el `elif` nunca se mira. Los rangos van de menor a mayor.
5. `'yth'`, `'on'`, `'nohtyP'`, `''` (un slice fuera de rango no falla) e `IndexError` (un índice fuera de rango sí).
6. Porque los `str` son inmutables: `strip()` devuelve un texto nuevo, y si no lo guardas (`name = name.strip()`) se pierde.
7. `'1,234.50'`, `'25.6%'` y `'   ab'`.
8. Un `Template`, con las partes fijas y los valores por separado. Así, una función puede tratar los valores (escapar HTML, pasarlos como parámetros SQL) antes de unirlos, y se evitan las inyecciones; una f-string ya los pegó y no se puede saber dónde estaban.
9. El primero encaja con una secuencia de dos elementos cuyo primero es `"hola"` y **captura** el segundo en `name`; el segundo encaja solo con el texto `"hola"`. `case LIMIT:` no compara con la constante: captura cualquier valor en `LIMIT`, y Python lo rechaza si hay más `case` después (`name capture 'LIMIT' makes remaining patterns unreachable`).
10. Para que los resultados (stdout) puedan guardarse o pasarse a otro programa sin mezclarse con los errores. Línea inválida: `1`; argumentos de más: `2`; todo bien: `0`.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Rojo antes que verde | El historial de `week-02` muestra los archivos copiados con tests en rojo y después los commits que los ponen en verde | 8 |
| Commits con sentido | Commits pequeños, con Conventional Commits, sin `.venv/` ni `__pycache__/` | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, los comandos del paso 8 con `echo $?` y `docker compose run --build --rm app` | 10 |
| Explica su código | Explica el orden de las ramas de `classify`, la guarda de `parse_line` y por qué el `case` de la ayuda va antes que `[line]` en `main` | 8 |
| Explica sus decisiones | Justifica sus umbrales con una fuente o un criterio del dominio, y explica la diferencia entre stdout y stderr con su propio programa | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 1

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones | `classify`, `format_row`, `parse_line` y `main` pasan los 23 tests de `test_rules.py` y `test_main.py`, y los de la semana 1 siguen en verde | 30 |
| Tests propios | Al menos 6 tests en `tests/test_my_rules.py` con valores del dominio calculados a mano, que cubren los casos del paso 9 | 30 |
| Dominio | `UNIT`, `LOW` y `HIGH` del dominio, con justificación y ejemplo de uso en el `README.md` | 15 |
| Docker | `docker compose run --build --rm app` en verde y `observatorio` funciona en el contenedor | 10 |
| Git | Rama `week-02` en `python-<nombre>-<apellido>`, commits con Conventional Commits | 10 |
| Pull request | Descripción con umbrales, salida de los tests y de los comandos del paso 8 | 5 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 03](../week-03-bucles_iteracion_y_depuracion/README.md) |
