# Rúbrica de Evaluación — Semana 28: Estadística aplicada con SciPy y statsmodels

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 27 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | La temperatura a mediodía sigue una normal de media 20 °C y desviación 3 °C. ¿Qué método de `scipy.stats` usas para saber qué fracción de días pasa de 26 °C, y cuál para saber por debajo de qué valor queda el 95 % de los días? ¿Por qué `pdf(20)` no es una probabilidad? | 10 |
| 2 | ¿Qué dice el teorema central del límite? Las esperas entre alertas son muy asimétricas: ¿por qué funciona un intervalo t para su media con 200 esperas, y por qué no con 15? | 10 |
| 3 | 25 días con desviación 2,96 °C. ¿Cuánto vale el error estándar de la media? ¿Cuántos días necesitas para que el intervalo del 95 % sea la mitad de ancho, y por qué? | 10 |
| 4 | Tu intervalo del 95 % para la media es [18,85, 21,29]. Un compañero dice: "hay un 95 % de probabilidad de que la media de verdad esté ahí". ¿Qué está mal, y cuál es la lectura correcta? | 10 |
| 5 | Comparas dos estaciones y sale p = 0,18. ¿Puedes concluir que miden lo mismo? Explica qué es un error de tipo II y qué es la potencia, con los números del ejercicio 03. | 10 |
| 6 | ¿Qué diferencia hay entre la prueba de Welch y la de Student? ¿Cuál usa SciPy por defecto, y por qué `difference` pasa `equal_var=False`? ¿Por qué con `LOW` y `HIGH` dan el mismo p-valor? | 10 |
| 7 | Un sensor marca 95 °C un día. ¿Qué le pasa al p-valor de Welch, y qué al de Mann-Whitney? ¿Por qué? ¿Por qué Mann-Whitney no puede dar p < 0,05 con 3 y 3 valores? | 10 |
| 8 | Comparas todas las parejas de tus 10 etiquetas y 3 salen con p < 0,05. ¿Qué problema hay, y cómo lo corriges? Con 200 000 medidas por grupo, una diferencia de 0,05 °C da p = 1,2e-10: ¿es importante? ¿Qué número lo dice? | 10 |
| 9 | En `smf.ols("value ~ C(station)", data=...)`, ¿qué significa el coeficiente `C(station)[T.Sur]`? Para el día 100, ¿qué diferencia hay entre `mean_ci` y `obs_ci`, y cuál usarías para avisar de la temperatura de un día? | 10 |
| 10 | ¿Por qué `difference` lanza `ValueError` con una muestra de un valor o sin variación, en lugar de dejar trabajar a SciPy? ¿Por qué compara `min() == max()` y no `std() == 0`? ¿Por qué el proyecto añade SciPy y no statsmodels? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `noon.sf(26)` = 0,023 (o `1 - cdf(26)`, que pierde precisión en colas pequeñas) y `noon.ppf(0.95)` = 24,93. `pdf` es una densidad, la altura de la curva: en una variable continua, la probabilidad de un valor exacto es 0, y lo que se mide es el área entre dos valores (`cdf(b) - cdf(a)`). Una densidad puede incluso valer más de 1.
2. La media de n valores independientes se reparte cada vez más como una normal, sea cual sea la distribución de partida, con desviación igual a la de los datos entre √n. Con 200 esperas, la media ya es casi normal y el intervalo t acierta casi lo prometido (un 94,7 % en una simulación como la del ejercicio 02). Con 15, la distribución de la media sigue siendo asimétrica y la muestra casi nunca contiene las esperas muy largas: el ejercicio 02 mide una cobertura del 90,6 % en lugar del 95 %, y el *bootstrap* tampoco lo arregla (89,7 %).
3. 2,96 / √25 = 0,59 °C. El ancho va con 1/√n: para dividirlo entre 2 hace falta multiplicar n por 4, 100 días. (El t crítico también baja un poco con más datos, de 2,06 a 1,98.)
4. La media de verdad es un número fijo: está dentro del intervalo o no lo está, sin probabilidad. El 95 % es del **método**: si repites el experimento muchas veces, el 95 % de los intervalos construidos así contienen la media de verdad. De este intervalo concreto no sabes si es de los buenos.
5. No. p ≥ 0,05 significa que con estos datos no se distingue la diferencia del azar, no que no exista. En el ejercicio 03, el Sur mide de verdad 1,5 °C más y aun así p = 0,18: un error de tipo II (no rechazar una H₀ falsa). La potencia, la probabilidad de detectar una diferencia que existe, era de un 31 % con 20 días por estación y esas dispersiones; con 10 días y desviación 3, un 18 %; con 100, un 94 %.
6. Student supone que los dos grupos tienen la misma dispersión y usa n₁ + n₂ − 2 grados de libertad; Welch no lo supone y los ajusta. SciPy usa Student por defecto (`equal_var=True`). Con tamaños y dispersiones distintos, Student da p-valores equivocados, y Welch apenas pierde nada cuando sí son iguales, así que el proyecto lo pide explícito. Con `LOW` y `HIGH`, los dos grupos tienen el mismo tamaño y la misma desviación: el estadístico y los grados de libertad (8) coinciden. Por eso hace falta `NARROW` y `WIDE` para distinguirlos.
7. La media del Norte sube de 20,14 a 24,01 y el p de Welch pasa de 0,18 a 0,53: la prueba t compara medias, y una media se mueve con un solo valor. Mann-Whitney compara rangos: el 95 es solo "el más alto", como lo sería un 30; su p cambia menos (de 0,12 a 0,27). Con 3 y 3 valores solo hay 20 formas de repartir los rangos, y la más extrema en cada sentido es una: el p bilateral más pequeño es 2/20 = 0,1.
8. Con 45 parejas y α = 0,05, esperas unas 2 o 3 con p < 0,05 aunque no haya ninguna diferencia: falsos positivos. Se corrige decidiendo antes qué comparar y ajustando: Bonferroni (α / 45) o Benjamini-Hochberg (`false_discovery_control`). Lo de 0,05 °C no es importante: el p-valor solo dice que se distingue del azar, y con tantos datos cualquier cosa se distingue. Lo dice el tamaño del efecto: la diferencia en °C (0,05) y la d de Cohen (0,02, muy por debajo de "pequeña", 0,2).
9. Es la diferencia entre la media del Sur y la de la referencia, `Centro` (el primer nivel en orden alfabético): 1,559 °C, con su error estándar, su intervalo y su p-valor. `mean_ci` es el intervalo de la **media** de los días 100 (±0,5 °C); `obs_ci`, el de **un** día 100 concreto, que suma el ruido diario (±2,9 °C). Para avisar de un día, `obs_ci`.
10. Con 1 valor SciPy devuelve `nan` sin avisar; con 0, `nan` y un `SmallSampleWarning`; con una muestra constante, un `RuntimeWarning` de pérdida de precisión y números sin sentido. Un `p: nan` en la pantalla no dice qué pasa; un `ValueError` con el motivo, sí, y `comparar` lo convierte en código 2. `std() == 0` falla por el redondeo: la desviación de `[0.1, 0.1, 0.1]` sale 1,4e-17; `min() == max()` es exacto. SciPy trae todo lo que `comparar` necesita (Welch, Mann-Whitney, el intervalo); statsmodels serían 43 MB más y casi un segundo de `import` sin usar ninguno de sus modelos.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-28` muestra un commit por paso (tests, dependencias, módulo, comprobaciones, comando, versión, imágenes, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Rojo a verde | Leyó `test_inference.py` antes de escribir; puede decir qué tests pasaron a verde con cada paso, y qué avisos daba SciPy antes de las comprobaciones | 8 |
| Ejecución en vivo | Ante el instructor: `comparar` con dos parejas de su dominio, `--confianza 0.99`, una etiqueta que falla con código 2, el comprobante de `sys.modules` y `pytest` en verde | 8 |
| Rompe y explica | Cambia `equal_var=False` por `True` y explica qué test falla y por qué los de `LOW` y `HIGH` no; quita la comprobación de `min() == max()` y enseña el aviso de SciPy | 8 |
| Explica sus decisiones | Explica por qué Welch, por qué el intervalo y el tamaño del efecto además del p-valor, por qué tests con valores a mano, y por qué SciPy y no statsmodels, con los números de su imagen | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 27

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `sample` con los arrays de la semana 23 y sin pandas; `Comparison` congelada; `difference` con `ddof=1`, Welch explícito, su intervalo, la d de Cohen y Mann-Whitney; sin reexportar `inference` en `core/__init__.py` | 20 |
| Las comprobaciones | `ValueError` con menos de 2 valores y con una muestra sin variación (`min() == max()`), con los mensajes exactos | 10 |
| El comando | `comparar RUTA ETIQUETA OTRA` con `--confianza` entre 0,5 y 0,999, el import dentro, `ValueError` con código 2, código 1 con líneas malas y las cinco líneas del informe | 20 |
| Tests propios | Al menos 6 tests en `tests/test_my_inference.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde; CI en verde; `scipy` y `scipy-stubs` fijados; imágenes `week-28`; versión `0.28.0` | 10 |
| Git y README | Rama `week-28` en `python-<nombre>-<apellido>`; README con la sección "Comparar etiquetas", con lo que se puede y lo que no se puede concluir | 5 |
| Pull request | Salidas, CI, dos comparaciones con sus conclusiones, tabla de tiempos, tamaño de la imagen y tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 29 (próximamente) |
