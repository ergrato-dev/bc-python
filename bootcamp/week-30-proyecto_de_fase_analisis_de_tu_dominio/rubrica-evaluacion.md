# Rúbrica de Evaluación — Semana 30: proyecto de fase, análisis de tu dominio

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 29, y el informe de tu dominio |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué diferencia hay entre un análisis exploratorio y uno confirmatorio? ¿Por qué no se confirma una idea con los mismos datos con los que se tuvo? ¿Cómo lo resuelve tu proyecto? | 10 |
| 2 | "¿Qué zona está peor?" no se puede responder con datos. Nombra las cuatro piezas que le faltan y escribe una versión que sí se pueda responder, con un "no" como respuesta posible. | 10 |
| 3 | En el ejercicio 01, el Sur mide 9,79 más que el Norte por medida, y 2,56 menos por sensor. ¿Cuál es la respuesta correcta? ¿Qué es lo que pasa, cómo se llama, y qué tabla lo descubre? | 10 |
| 4 | Con 20 000 medidas por zona, una diferencia de 0,36 unidades da p = 0,00026; con 8, una de 3,20 da p = 0,61. ¿Qué escribes en el informe en cada caso? ¿Qué te dice el intervalo que no dice el p? | 10 |
| 5 | Tu Observatorio compara 5 etiquetas. ¿Cuántos pares? Sin corregir y sin ninguna diferencia real, ¿qué probabilidad hay de algún "hallazgo"? Explica la fórmula. | 10 |
| 6 | ¿Qué promete una corrección FWER y qué promete una FDR? ¿Cuál usa tu Observatorio y por qué? ¿Cuándo usarías Holm? | 10 |
| 7 | Calcula a mano los p corregidos por BH de 0,01, 0,04 y 0,03 (en ese orden). ¿Cuáles bajan de 0,05? ¿Por qué `false_discovery_control` no necesita que los ordenes? | 10 |
| 8 | ¿Qué partes del informe escribe `hallazgos` y cuáles escribes tú? ¿Por qué no se copian los números a mano? ¿Qué comprueba `test_report_is_up_to_date`, y qué tres cosas harían que el informe cambiara de bytes sin que cambiaran los datos? | 10 |
| 9 | ¿Por qué el título de `diferencias.svg` es una conclusión? ¿Qué mira el lector en un *forest plot*, y qué hacen `xerr=[below, above]` e `invert_yaxis()`? | 10 |
| 10 | ¿Por qué `cell()` escapa las barras, `read_snapshot` fija los tipos y comprueba las columnas, y `compare_all` deja fuera algunas etiquetas? ¿Qué pasaría en cada caso sin ello? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Explorar es mirar los datos para tener ideas y encontrar problemas; confirmar es responder una pregunta decidida antes, con un método fijado, y aceptar lo que salga. Si eliges la comparación porque en un gráfico se veía una diferencia y luego la pruebas con esos mismos datos, la prueba sale bien casi siempre: la elegiste por eso. En el proyecto, la pregunta va en un commit **antes** de ejecutar `hallazgos` (paso 4), el método está fijado en el código y escrito en el informe, y el informe sale de un comando, no de celdas ejecutadas a mano.
2. Población (de qué medidas: qué carga, qué fechas), unidad (qué es un caso: una medida, un sensor, un día), métrica (qué número resume "peor": la media del valor, en su unidad) y comparación (peor que qué: cada zona frente a cada otra). Por ejemplo: "en la carga 3, del 1 al 30 de marzo, ¿difiere la media de las medidas entre zonas?". Puede responderse "no difieren".
3. Depende de la pregunta, pero la de "por medida" está confundida: es la **paradoja de Simpson**. La estación es una variable de confusión: el verano da valores altos, y el Sur se midió sobre todo en verano (160 de sus 200 medidas). La tabla por estación (paso 4) lo descubre: en invierno y en verano el Norte mide más (2 a 3 unidades). La respuesta defendible es la que fija la estación: "a igual estación, el Sur mide entre 1 y 4 unidades menos".
4. Con 20 000: la diferencia es real (el intervalo [0,17; 0,56] no cruza el cero) pero mínima (d = 0,04, cinco veces menos que un efecto pequeño): "difieren, pero tan poco que no importa". Con 8: no se puede saber; el intervalo [−10,10; 16,49] cruza el cero y es enorme: "con estos datos no se distingue; harían falta más medidas". No es "son iguales": de hecho la diferencia real era de 8. El intervalo da el tamaño y la precisión; el p solo dice si el cero es plausible.
5. 5·4/2 = 10 pares. 1 − 0,95^10 = 40,1 %. Cada prueba sin diferencia tiene un 95 % de no dar falso positivo; si son independientes, que ninguna lo dé es 0,95 multiplicado diez veces, y "alguna" es lo contrario.
6. FWER: probablemente ningún hallazgo publicado es falso (la probabilidad de alguno, por debajo de α). FDR: como mucho una proporción α de los hallazgos son falsos. El Observatorio usa FDR (Benjamini-Hochberg): el informe dice qué pares merece la pena investigar, y FDR encuentra más diferencias reales a cambio de algún falso (en el ejercicio 02, 3,50 de 4 frente a 3,02 de Bonferroni, con un 4,3 % de falsos entre los hallazgos). Holm, cuando un solo falso positivo es caro: una alarma que para una planta, un tratamiento.
7. Ordenados: 0,01 (puesto 1), 0,03 (2), 0,04 (3); m = 3. Multiplicados por m/k: 0,03, 0,045, 0,04. De abajo arriba, cada uno con el menor de los que tiene debajo: 0,04 se queda; 0,045 pasa a 0,04; 0,03 se queda. En el orden original: 0,03, 0,04, 0,04. Los tres bajan de 0,05. `false_discovery_control` ordena por dentro y devuelve cada p corregido en la posición en que lo diste; por eso `compare_all` puede emparejarlos con `zip`.
8. `hallazgos` escribe `hallazgos.md` (datos con su huella, método, resumen, tabla de pares) y `diferencias.svg`; tú escribes `README.md` (pregunta, datos, hallazgos con su lectura en tu dominio, limitaciones, siguientes pasos). Copiados a mano, los números se quedan viejos cuando cambian los datos o el código, y un solo error de copia no lo ve nadie. El test genera el informe de nuevo con la instantánea y las opciones por defecto, y lo compara con el guardado: si no coincide, la CI falla. Sin `render` cuidadoso cambiaría con la fecha de generación, una ruta absoluta, o el orden de un `set`; en el SVG, la fecha y los identificadores al azar.
9. Porque un gráfico de informe prueba una frase: el lector no tiene que adivinar qué mirar, y el título se calcula con los mismos números que el dibujo (`headline`), así que no pueden contradecirse. En un *forest plot* mira qué intervalos cruzan la línea del cero. `xerr=[below, above]` dice cuánto se extiende la barra a cada lado del punto (`difference - low` y `high - difference`); `invert_yaxis()` pone el primer par arriba, como en la tabla.
10. Los datos vienen de fuera. Sin `cell()`, una etiqueta con `|` parte la fila y descuadra la tabla. Sin fijar tipos, una etiqueta `01` se leería como el número 1 (y no coincidiría con las comparadas) y un valor `doce` haría la columna de texto; con ellos, `01` sigue siendo `01` y `doce` es un `ValueError`. Sin comprobar columnas, un CSV que no es una instantánea daría un `KeyError` en mitad del análisis en vez de un mensaje claro. Sin `comparable`, una etiqueta con un solo valor, o con todos iguales, haría que `difference` lanzara `ValueError` y `hallazgos` no escribiría ningún informe.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| La pregunta, antes | El commit `docs: state the question of the report` es anterior a `docs: add findings report`, y la pregunta tiene sus cuatro piezas | 8 |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| Ejecución en vivo | Ante el instructor: `hallazgos` con su instantánea y `--huella`, otra vez sin cambios en `git status`, la figura abierta, y `pytest` en verde | 8 |
| Rompe y explica | Cambia `method="bh"` por `"by"` y explica qué test falla; cambia un valor de la instantánea y enseña qué tests fallan y por qué | 8 |
| Explica sus hallazgos | Lee su tabla de pares con intervalo, d, p corregido y Mann-Whitney; dice qué variable de confusión no puede descartar y por qué eligió FDR | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 29

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `read_snapshot` con una sola lectura, los tipos fijados y las columnas comprobadas; `compare_all` con todos los pares y BH sobre todos juntos; `differences_figure` y `render` deterministas; sin reexportar `findings` en `core/__init__.py` | 15 |
| El comando | `hallazgos` con el import dentro, `--huella`, `--confianza` y `--alfa`, código 1 y 2 según el error, sin carpeta a medias si falla la lectura | 10 |
| El informe | `informe/README.md` de su dominio: una pregunta con sus cuatro piezas, los datos con su huella, dos o tres hallazgos defendibles (intervalo y d), limitaciones con al menos una variable de confusión, y siguientes pasos; `hallazgos.md` y `diferencias.svg` al día | 30 |
| Tests propios | Al menos 6 tests en `tests/test_my_findings.py` con datos de su dominio, cada uno visto fallar con un mutante | 15 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde; imágenes `week-30` y versión `0.30.0` | 15 |
| Git y README | Rama `week-30` en `python-<nombre>-<apellido>`; README con la sección "Informe" | 5 |
| Pull request | Salidas, CI, `hallazgos`, el enlace al informe y al commit de la pregunta, y la tabla de mutantes con las dos respuestas | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 31 (próximamente) |
