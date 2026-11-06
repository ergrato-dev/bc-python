# Rúbrica de Evaluación — Semana 03: Bucles e iteración; depuración

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución, depuración en vivo y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 2 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué números dan `range(4)`, `range(2, 8, 2)` y `range(5, 0, -2)`? ¿Cuántas vueltas da `for _ in range(3, 3):`? | 10 |
| 2 | ¿Cuántas veces se ejecuta el `print` de `for i in range(3): for j in range(4): print(i, j)`? | 10 |
| 3 | ¿Qué da `list(zip(["a", "b", "c"], [1, 2]))`? ¿Y `list(enumerate("ab", start=1))`? | 10 |
| 4 | Un programa suma valores y el resultado siempre es el último valor. ¿Cuál es la causa más probable? | 10 |
| 5 | ¿Por qué el máximo a mano empieza en `None` y no en `0`? ¿Y por qué un producto empieza en `1`? | 10 |
| 6 | ¿Qué diferencia hay entre `continue`, `break` y `return` dentro de un `for`? | 10 |
| 7 | ¿Cuándo se ejecuta el `else` de un `for`? Pon un ejemplo en que sea útil. | 10 |
| 8 | Recorres `sys.stdin` y comparas `line == "fin"`, pero nunca es verdadero. ¿Por qué? ¿Cómo terminas la entrada desde el teclado? | 10 |
| 9 | En un traceback de tres bloques, ¿qué te dice la última línea, qué el bloque de encima y qué los de arriba? | 10 |
| 10 | Estás en `pdb` sobre `value = parse_reading(text)`. ¿Qué hacen `n`, `s` y `c`, y cuáles son sus teclas en VS Code? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `0 1 2 3`; `2 4 6`; `5 3 1`. Ninguna: `range(3, 3)` está vacío.
2. 12 veces: 3 vueltas fuera × 4 dentro.
3. `[('a', 1), ('b', 2)]`: `zip` para en la más corta y `'c'` se pierde. `[(1, 'a'), (2, 'b')]`.
4. El acumulador (`total = 0`) está dentro del bucle y se reinicia en cada vuelta. Va antes del `for`.
5. Con `0`, si todos los valores son negativos el "máximo" sería `0`, que ni siquiera está en los datos; `None` significa "aún no he visto ninguno". El producto empieza en `1` porque es el neutro: con `0`, todo daría `0`.
6. `continue` salta el resto del cuerpo y pasa a la siguiente vuelta; `break` termina el bucle y sigue después de él; `return` termina la función entera (y con ella el bucle) y devuelve un valor.
7. Si el bucle terminó sin `break`. Útil en búsquedas: en `is_prime`, si ningún divisor provocó `break`, el `else` devuelve `True`.
8. Cada línea trae `"\n"` al final: `"fin\n" != "fin"`. Hay que comparar `line.strip()`. Desde el teclado, `Ctrl+D` envía el fin de la entrada (EOF).
9. La última línea: el tipo de error y su mensaje. El bloque de encima: el archivo, la línea y la función donde ocurrió. Los de arriba: quién llamó a esa función (la pila de llamadas), donde suele estar la causa.
10. `n` ejecuta la línea entera, sin entrar en `parse_reading`, y para en la siguiente (`F10`). `s` entra en `parse_reading` y para en su primera línea (`F11`). `c` sigue hasta el próximo punto de parada o el final (`F5`).

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Rojo antes que verde | El historial de `week-03` muestra los archivos copiados con tests en rojo y después los commits que los ponen en verde | 6 |
| Commits con sentido | Commits pequeños, con Conventional Commits, sin `.venv/`, `__pycache__/` ni `informe.txt` | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `uv run observatorio < medidas.txt; echo $?` y `docker compose run --rm -T app observatorio < medidas.txt` | 8 |
| Depuración en vivo | Pone un punto de parada en `longest_streak` (VS Code o `breakpoint()`), avanza con `n`/`F10` y dice el valor de `current` y `best` en cada vuelta | 8 |
| Explica su código | Por qué los contadores van antes del bucle, por qué `enumerate` numera también las líneas saltadas y por qué una línea inválida no detiene el resto | 6 |
| Explica sus decisiones | Por qué eligió las líneas de su `medidas.txt` y qué caso cubre cada uno de sus tests | 6 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 2

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones | `is_data_line`, `level_of`, `summarize`, `longest_streak` y `main` pasan los 27 tests de `test_report.py` y `test_main.py`, y los de las semanas 1 y 2 siguen en verde | 30 |
| Tests propios | Al menos 6 tests en `tests/test_my_report.py` con filas del dominio calculadas a mano, que cubren los casos del paso 10 | 25 |
| Datos del dominio | `medidas.txt` con al menos 10 líneas del dominio y los casos del paso 9 | 15 |
| Docker | `docker compose run --build --rm app` en verde y el informe con `-T` en el contenedor | 10 |
| Git y README | Rama `week-03` en `python-<nombre>-<apellido>`, Conventional Commits y README con uso con archivo e informe de ejemplo | 10 |
| Pull request | Descripción con tests, informe, código de salida y un error depurado explicado | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 04](../week-04-funciones_scope_type_hints_y_pytest/README.md) |
