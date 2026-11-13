# Rúbrica de Evaluación — Semana 33: árboles, ensembles, gradient boosting y no supervisado

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 32 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | En la teoría 01, ¿por qué el árbol corta el viento en 2,25 y no en 1,25 o en 4,75? ¿Qué predice cada hoja? ¿Qué es un algoritmo voraz? | 10 |
| 2 | Un árbol sin límite tiene 294 hojas para 300 medidas. ¿Qué ha pasado, y qué hacen `max_depth` y `min_samples_leaf`? En el ejercicio 01, ¿qué profundidad elegirías y por qué? | 10 |
| 3 | ¿Por qué a un árbol no le hace falta escalar? ¿Por qué encuentra la hora punta del Centro y una regresión lineal no? ¿Qué hace un árbol con un día que nunca vio, y qué pasa por eso con `competir --tiempo`? | 10 |
| 4 | ¿Qué es una muestra con repetición, y qué hace el *bagging* con ellas? ¿Qué añade un bosque aleatorio? ¿Qué es la nota *out-of-bag*? | 10 |
| 5 | En el ejercicio 02, la columna `ruido` saca más importancia por impureza que el día de la semana, y 0 por permutación. ¿Por qué? ¿Qué dicen, y qué no, las importancias? | 10 |
| 6 | Explica el *boosting* con los tres árboles de la teoría 03. ¿Qué aprende cada árbol? ¿Por qué el tercero apenas mejora? | 10 |
| 7 | ¿Cómo se relacionan `learning_rate` y el número de árboles? ¿Por qué un boosting puede sobreajustar con demasiados árboles y un bosque no? ¿Qué hace `early_stopping`? | 10 |
| 8 | Describe los dos pasos de KMeans. ¿Por qué hay que escalar antes? ¿Por qué no se elige `k` con la inercia más baja? | 10 |
| 9 | ¿Qué mide la silueta? En el ejercicio 04, KMeans encuentra tres grupos en datos al azar. ¿Cómo sabes que no existen? ¿Qué hace PCA, y qué dice que dos componentes recojan un 94 %? | 10 |
| 10 | Con los datos de ejemplo, en `competir` el lineal empata con la referencia y el bosque y el boosting pierden por casi un punto; `agrupar` aparta el Sur con silueta 0,28. Explica los dos resultados. ¿Es un fallo de los modelos? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Porque es el corte que deja el menor error en los dos lados: la suma de cuadrados baja de 679,5 a 35,5, con los tres valores altos a un lado y los cinco bajos al otro; con 1,25 queda en 246,0 y con 4,75 en 339,5. Cada hoja predice la **media** de las medidas de entrenamiento que llegan a ella (la clase más frecuente, al clasificar). Voraz: en cada paso elige el mejor corte en ese momento, sin mirar los siguientes.
2. Ha memorizado: sigue preguntando hasta que casi cada medida tiene su hoja, ruido incluido, y el error de entrenamiento es 0. `max_depth` limita cuántas preguntas seguidas hace; `min_samples_leaf` no deja hojas con menos de esas medidas, así cada predicción promedia varias y el ruido se cancela. En el ejercicio 01, `max_depth=6`: el menor error de validación (2,96); con menos no aprende, con más memoriza.
3. Un corte solo mira el **orden** de los valores: "¿viento ≤ 1,9?" separa las mismas medidas en m/s o en logaritmo. La regresión lineal suma un peso por columna: no dibuja la hora punta (7-9 y 18-20 no es una recta) ni el cruce Centro × hora punta; el árbol pregunta "¿Centro?" y después "¿hora punta?". Fuera de lo que vio, cae en la hoja del borde y repite su media: no extrapola. Con `--tiempo`, el último pliegue tiene posiciones que el entrenamiento no vio, y el árbol las mete todas en su última hoja.
4. Una muestra del mismo tamaño sacada con reemplazo: unas dos terceras partes de las medidas, algunas repetidas. *Bagging*: un árbol por muestra, y la media de todos; los errores de cada árbol se compensan y baja la varianza. El bosque añade que cada corte mire solo algunas columnas al azar (`max_features`; en la regresión, por defecto, todas). *Out-of-bag*: cada medida se predice solo con los árboles que no la vieron, y se calcula la nota: una validación sin repartir.
5. La importancia por impureza se mide con el **entrenamiento**, sumando cuánto baja el error cada corte; una columna con muchos valores distintos siempre ofrece algún corte que separa por casualidad unas pocas medidas. La permutación baraja la columna en la **prueba**: si el modelo no la necesita para predecir medidas nuevas, no empeora. Dicen qué usa el modelo, no qué causa el PM2.5; y dos columnas que van juntas se reparten la importancia.
6. Empieza prediciendo la media. Cada árbol aprende el **residuo**, lo que les falta a los anteriores, y su predicción se suma. El primero encuentra la calma (MAE de 5,68 a 3,25); el segundo, con la calma ya corregida, la lluvia (2,44). El tercero solo encuentra ruido: lo que queda no tiene estructura (2,43).
7. Cada árbol suma solo `learning_rate` veces su corrección: si lo divides por diez, necesitas unas diez veces más árboles para llegar al mismo sitio (0,1 con 100 ≈ 0,01 con 1000). En un boosting, cada árbol nuevo corrige lo que queda, y al final lo que queda es ruido: lo aprende. En un bosque, más árboles solo hacen la media más estable. `early_stopping` aparta una parte del entrenamiento, mide después de cada árbol y para cuando deja de mejorar; `n_iter_` dice cuántos usó.
8. Asignar cada fila al centro más cercano y mover cada centro a la media de su grupo, hasta que nada cambie. La distancia mezcla todas las columnas: sin escalar, la que tiene números más grandes (la altitud en metros) decide sola. La inercia baja siempre con más grupos (con un grupo por fila es 0); se mira el codo, y la silueta.
9. Para cada fila, compara la distancia media a su grupo (*a*) con la del grupo más cercano (*b*): (*b* − *a*) / máx(*a*, *b*). Cerca de 1, grupos compactos y separados; cerca de 0, filas en la frontera. Con datos al azar, la silueta es baja (0,04 en el ejercicio 04, frente a 0,62 con los tres tipos de sitio): KMeans siempre devuelve `k` grupos, la silueta dice si significan algo. PCA busca las direcciones en que más varían los datos; que dos recojan un 94 % significa que las veinticuatro horas se resumen en dos números casi sin perder nada.
10. Las etiquetas no dicen nada del valor (semanas 30 a 32). El lineal, sin nada que aprender, se queda en la media; los modelos más flexibles aprenden el ruido de cada entrenamiento y se equivocan más en la prueba. En `agrupar`, el escalado estira diferencias de pocas unidades (medias de 38,2 a 40,7, con desviación 23 dentro de cada zona) y KMeans aparta el Sur, pero la silueta, 0,28, dice que los grupos se solapan. No es un fallo: es la misma conclusión, por otro camino. Con tus datos, o con otras entradas, el resultado puede cambiar.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| Una competición justa | Explica por qué los cinco modelos usan los mismos pliegues y la misma preparación, y por qué la mejor media no basta para decir "mejora" | 8 |
| Ejecución en vivo | Ante el instructor: `competir` al azar y con `--tiempo`, `agrupar` con dos números de grupos, y `pytest` en verde | 8 |
| Rompe y explica | Pone `DEPTH = None` y explica qué cambia en `competir`; quita el `StandardScaler` de `cluster` y explica qué cambia en `agrupar` | 8 |
| Explica sus modelos y sus grupos | Lee sus tablas: qué modelo tiene la mejor media, en cuántos pliegues gana, qué pasa por tiempo, y si la silueta dice que hay grupos; lo relaciona con `ajustar` de la semana 32 | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 32

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Los módulos | `Contest` con `means`, `wins`, `best` e `improves`; `candidates` con los cinco modelos en orden, limitados y con semilla; `compete` con `ordered`, `prepare` y `folds` de la semana 32; `profiles` con media, mediana y desviación; `cluster` con `k` comprobado, escalado, semilla, silueta escalada y grupos renumerados; sin reexportar en `core/__init__.py` | 25 |
| Los comandos | `competir` y `agrupar` con el import dentro, `--huella`, `--pliegues`, `--tiempo` y `--grupos`, código 1 y 2 según el error, y sus tablas y veredictos | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_ensembles.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde; imágenes `week-33` y versión `0.33.0` | 15 |
| Git y README | Rama `week-33` en `python-<nombre>-<apellido>`; README con la sección "Modelos y grupos", e `informe/README.md` con los resultados en "Siguientes pasos" | 10 |
| Pull request | Salidas, CI, `competir` al azar y por tiempo y `agrupar`, con su lectura, y la tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 34 (próximamente) |
