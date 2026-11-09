# Rúbrica de Evaluación — Semana 22: Rendimiento

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 21 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Mides tu cambio una vez y tarda 0,9 s; antes tardaba 1,0 s. ¿Puedes decir que mejoró? ¿Cómo lo medirías bien, y por qué se compara el mínimo y no la media? | 10 |
| 2 | `time` dice `real 10s`, `user 0.4s`, `sys 0.1s`. ¿Qué hace el programa la mayor parte del tiempo? ¿Le ayudaría vectorizar? | 10 |
| 3 | Una función ocupa el 20 % del tiempo y la haces 10 veces más rápida. ¿Cuánto tarda ahora el programa, en proporción? ¿Y si la dejas en cero? | 10 |
| 4 | En un perfil, `main` tiene el `cumtime` más alto y `cell_len`, de Rich, el `tottime` más alto. ¿Qué te dice cada uno? ¿Arreglarías `cell_len`? | 10 |
| 5 | Con cProfile tu `informe` pasa de 21 a 51 s. ¿Por qué? ¿Qué partes del perfil te siguen sirviendo, y cuáles no? | 10 |
| 6 | ¿En qué se diferencia py-spy de cProfile en cómo mide? Di una cosa que sabe cProfile y py-spy no, y una situación en la que solo py-spy sirve | 10 |
| 7 | Grabas con py-spy un programa que tarda 10 s y el gráfico solo tiene 50 muestras. ¿Qué está pasando, y con qué opción lo ves? ¿Para qué sirve `--nonblocking`? | 10 |
| 8 | `py-spy dump --pid 1234` dice `Permission Denied`, y en Docker, `Permission denied (os error 13)` aun siendo root. ¿Por qué en cada caso, y qué haces? ¿Por qué no añades `SYS_PTRACE` al servicio `api`? | 10 |
| 9 | ¿Por qué `np.sum(array)` es mucho más rápido que un bucle, y por qué `np.sum(np.array(lista))` puede ser más lento que `sum(lista)`? | 10 |
| 10 | Tus tests de rendimiento no miden segundos. ¿Qué miden, cómo, y por qué es mejor? ¿Qué mutante de la semana solo lo mata un test así? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. **No**: una medida suelta lleva ruido (otros procesos, la frecuencia de la CPU, las cachés), y un 10 % está dentro de lo que varía. Se repite varias veces cada versión, alternando antes y después en la misma máquina y el mismo rato, con `timeit.repeat` o `time` varias veces, y se comparan los mínimos. El ruido solo **suma** tiempo, así que el mínimo es lo más cerca del coste real; la media se la lleva una ejecución con mala suerte (como los 4,58 s entre dos de 1,07).
2. El programa **espera**: la CPU solo trabajó 0,5 s de 10. Está esperando a la red, al disco, a una base de datos o un `sleep`. Vectorizar acelera el cálculo, que aquí es el 5 %: casi no se notaría. Lo que ayuda es esperar varias cosas a la vez (semanas 16 y 17) o esperar menos. py-spy con `--idle` dice dónde espera.
3. `0,8 + 0,2 / 10 = 0,82`: un 18 % menos. Aunque la dejes en cero, `0,8`: nunca más del 20 %. Es la ley de Amdahl: lo que puedes ganar lo limita la fracción que ocupa esa parte.
4. `cumtime` alto en `main` solo dice que todo pasa por ahí: sirve para orientarse, de arriba abajo. `tottime` alto en `cell_len` dice dónde se trabaja. Pero no se arregla `cell_len`: es de Rich, y cada llamada es rápida; el problema es que se llama millones de veces porque pides una tabla de 100 000 filas. Se busca con `print_callers` quién la llama tanto y se llama **menos**: pintar 20 filas.
5. cProfile es **determinista**: hace trabajo en cada llamada y cada retorno, y el informe hace 137 millones de llamadas. Los tiempos absolutos no sirven, ni para medir la mejora. Las **proporciones** y `ncalls` sí; pero las funciones muy pequeñas y muy llamadas salen infladas, y el código en C cuenta como una sola llamada.
6. cProfile anota **cada** llamada; py-spy mira la pila cada 10 ms desde **otro proceso** y cuenta. cProfile sabe `ncalls`, cuántas veces se llamó cada función (como las 200 000 de `parse_record`); py-spy no. py-spy se engancha a un proceso que **ya corre** sin cambiarlo ni reiniciarlo: un servidor en producción o un programa colgado (`dump --pid`), y dice la **línea**.
7. Por defecto py-spy no cuenta las muestras en que el programa está **parado** (`sleep`, red, disco): 50 muestras son 0,5 s de cálculo y el resto espera. Con `--idle` cuentan también. `--nonblocking` evita que py-spy pause el programa en cada muestra: con pilas profundas esa pausa lo frena mucho (55 s frente a 8 en la semana 21 con 50 000 medidas), a cambio de algunas muestras rotas.
8. En Linux, `ptrace_scope` = 1 solo deja leer la memoria de un proceso a su **padre**; con `--pid`, py-spy no lo es: `sudo .venv/bin/py-spy dump --pid 1234`. En Docker, el contenedor no tiene la capacidad `SYS_PTRACE`, ni para root: `docker run --cap-add SYS_PTRACE`. En `api` deshaces el `cap_drop: [ALL]` de la semana 21: cualquiera que tome el contenedor podría leer otros procesos. Para depurar se usa un contenedor aparte, temporal.
9. Un array guarda los números **seguidos**, sin objetos, todos del mismo `dtype`: NumPy los recorre con un bucle en C, sin mirar tipos ni crear objetos, y suma varios por instrucción. El bucle de Python, en cada vuelta, sigue una referencia, mira el tipo y crea un `float`. Pero `np.array(lista)` tiene que leer un millón de objetos (16 ms), más que `sum(lista)` entera (5 ms): convertir para una sola operación pierde.
10. Miden **trabajo**: cuántas veces se llama a `Table.add_row` y a `parse_record`, contadas con cProfile (`calls_of`) y la clave `(archivo, línea, nombre)`. No depende de la máquina: un test con segundos falla en una máquina lenta o cargada sin que el código cambie (*flaky*), y acaba ignorado. El mutante que añade `Series.from_lines(lines)` en `informe` da la misma salida: solo lo mata `test_informe_reads_each_line_once`, que ve 104 llamadas en vez de 52.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-22` muestra un commit por paso (tests, py-spy, `perfil/`, `--filas`, `Series.parse`, versión, tests propios), con `perf:` en los arreglos, sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Midió antes de cambiar | La primera fila de la tabla de medidas es anterior al primer cambio de `cli.py`; cada fila repetida y con el mínimo; la hipótesis escrita antes de perfilar | 8 |
| Ejecución en vivo | Ante el instructor: `time` del `informe` grande, `python -m cProfile -o` y `pstats` con `sort` y `callers`, `py-spy record --nonblocking` abierto en el navegador, `py-spy dump` de un proceso, `-X importtime` y `pytest` en verde | 8 |
| Rompe y explica | Quita `[:rows]` y explica qué test falla y por qué; vuelve a llamar a `Series.from_lines` y enseña el 104; quita `min=0` y prueba `-n -1` | 8 |
| Explica sus decisiones | Explica la tabla de medidas con Amdahl, por qué la segunda vuelta no se nota, por qué no usa NumPy y qué haría con el arranque, y qué mutante sobrevivió y cómo lo mata | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 21

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Tabla limitada | `ROWS = 20`, `table_of` con `rows` por defecto, `shown` y el pie `"N de M medidas"` solo si no caben; `--filas`/`-n` con `min=0`; la media móvil con las últimas `filas` y el `if` del `[-0:]` | 20 |
| Una sola lectura | `records_with_errors` en `groups.py` con la numeración, el `strip` y el `DEBUG`; `records_of` que la usa; `Series.parse`; `informe` sin `process_lines` ni `from_lines`, con `scale.row` | 20 |
| Herramientas | `py-spy==0.4.2` en `dev`; `perfil/` en `.gitignore` y `.dockerignore`; imágenes `week-22` | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_performance.py`, cada uno visto fallar con un mutante; al menos uno mata el mutante que sobrevive a los tests del bootcamp | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde; CI en verde; versión `0.22.0` | 10 |
| Git y README | Rama `week-22` en `python-<nombre>-<apellido>`; README con la sección "Rendimiento" | 5 |
| Pull request | Salidas, CI, tabla de medidas, capturas de los gráficos, tabla de mutantes, y las decisiones sobre NumPy y el arranque con números | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 23](../week-23-numpy_arrays_broadcasting_y_estadistica/README.md) |
