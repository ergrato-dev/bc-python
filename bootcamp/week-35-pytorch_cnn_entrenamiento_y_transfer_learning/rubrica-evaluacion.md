# Rúbrica de Evaluación — Semana 35: PyTorch II, CNN, entrenamiento y transfer learning

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 34 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué dos problemas de un MLP con imágenes o series resuelve una convolución? Calcula a mano las dos primeras salidas del filtro `[1/3, 1/3, 1/3]` sobre 12, 11, 10, 10. | 10 |
| 2 | Una serie de 24 valores y un filtro de 3: ¿cuántas salidas con `padding=1, stride=1`? ¿Y con `padding=0, stride=2`? Da la fórmula. | 10 |
| 3 | ¿Cuántos parámetros tiene `nn.Conv1d(3, 4, kernel_size=3)`? ¿Y `nn.Conv2d(8, 16, kernel_size=3)`? ¿Por qué no dependen del tamaño de la entrada? ¿Cuántos tiene `MaxPool2d(2)`? | 10 |
| 4 | ¿Qué son las puntuaciones de una red que clasifica? ¿Qué hace `softmax`? ¿Por qué `CrossEntropyLoss` recibe las puntuaciones y no las probabilidades, y qué forma y tipo tienen las clases? | 10 |
| 5 | En el ejercicio 02, el MLP acierta 0,983 y la CNN 0,973. Con las imágenes movidas un píxel, 0,451 y 0,685. ¿Qué dice cada par de números? ¿Cuál elegirías, y de qué depende? | 10 |
| 6 | ¿Para qué sirve cada parte: entrenamiento, validación y prueba? ¿Por qué se mira la prueba una sola vez? ¿Dónde van `model.train()`, `model.eval()` y `torch.no_grad()` en el bucle? | 10 |
| 7 | ¿Qué hace `nn.Dropout(0.5)` en `train()` y en `eval()`? ¿Y el aumento de datos? En el ejercicio 03, ¿por qué el *dropout* no ayuda y el aumento de datos sí, pero solo con la validación movida? | 10 |
| 8 | Describe la parada temprana de `fit` en `core/convolution.py`: qué se guarda, cuándo para y qué pasa al final. ¿Por qué `copy.deepcopy`? ¿Por qué `torch.load(..., weights_only=True)`? | 10 |
| 9 | ¿Cuáles son los pasos del *transfer learning*? ¿Qué hace `requires_grad = False`? ¿Por qué se afina con un ritmo pequeño? Con los números del ejercicio 04, ¿cuándo ayuda y cuándo no? | 10 |
| 10 | ¿Por qué `pronosticar` reparte las ventanas por tiempo y escala con `values[: train_end + window]`? Con la etiqueta Sur, `--desde` da 17,948 frente a 18,104 de la referencia: "mejora". ¿Qué dirías de ese resultado? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Un MLP usa un peso por cada par entrada-salida (con imágenes grandes, millones) y aprende cada patrón en cada posición por separado. Una convolución mira un trozo pequeño cada vez, con los mismos pesos en todas las posiciones: pocos parámetros, y un patrón se reconoce donde esté. (12 + 11 + 10) / 3 = 11; (11 + 10 + 10) / 3 ≈ 10,3.
2. `(n + 2p − k) // s + 1`. Con `padding=1, stride=1`: (24 + 2 − 3) // 1 + 1 = 24. Con `padding=0, stride=2`: (24 − 3) // 2 + 1 = 11.
3. `Conv1d(3, 4, 3)`: 4 filtros de 3 × 3 pesos y 4 sesgos, 40. `Conv2d(8, 16, 3)`: 16 filtros de 8 × 3 × 3 y 16 sesgos, 1168. Los filtros se deslizan: los mismos pesos sirven para cualquier longitud o tamaño de imagen; lo que crece es la salida. `MaxPool2d` no tiene parámetros: toma el máximo de cada cuadrado.
4. Un número por clase (*logits*); gana el más alto (`argmax`). `softmax` los convierte en probabilidades positivas que suman 1, sin cambiar cuál es el mayor. `CrossEntropyLoss` aplica su propio `softmax` (en versión logarítmica, más estable): darle probabilidades lo aplicaría dos veces, y entrena peor sin avisar. Las clases, un tensor de enteros con forma `(n,)`.
5. En imágenes centradas, las dos aciertan casi igual: con 8 × 8 píxeles, 64 entradas no son un problema para un MLP. Movidas, el MLP pierde más de la mitad: aprendió píxeles concretos; la CNN aguanta mejor: busca trazos donde estén. Elegiría según los datos que llegarán: si pueden venir movidos, la CNN; y lo comprobaría con una validación como esos datos.
6. Entrenamiento: ajustar los pesos. Validación: elegir épocas, hiperparámetros o qué red. Prueba: medir la elegida. Si eliges mirando la prueba, ya no es una medida limpia: eliges lo que mejor le salía. `model.train()` antes del bucle de lotes; `model.eval()` y `torch.no_grad()` antes de validar o de predecir.
7. En `train()`, apaga al azar la mitad de los números y multiplica los demás por 2; en `eval()`, no hace nada. El aumento de datos fabrica variantes de las imágenes de entrenamiento (movidas un píxel) en cada lote. La red del ejercicio es pequeña y no le sobra nada que apagar: con *dropout*, 0,905 frente a 0,938. Las imágenes movidas no mejoran la validación normal (0,897), pero con la validación movida pasan de 0,507 a 0,820: ayudan si los datos llegarán movidos.
8. Tras cada época mide la pérdida de validación; si es la menor hasta ahora, guarda la época y una copia de los pesos; si pasan `patience` épocas sin mejorar, para; al final, `load_state_dict(best_state)` devuelve la red a su mejor época. `state_dict()` devuelve los tensores de la red, que el entrenamiento sigue cambiando: sin `deepcopy`, "la mejor" sería la última. `torch.save` usa `pickle`, y un archivo `pickle` puede ejecutar código al cargarse; con `weights_only=True`, solo se aceptan tensores, números, textos, listas y diccionarios.
9. Copiar las capas que miran de una red de origen, congelarlas, cambiar la salida por una con las clases nuevas, entrenar la salida y, si hace falta, afinar todo con un ritmo pequeño. `requires_grad = False`: el parámetro no recibe gradiente y el optimizador no lo mueve. Con un ritmo grande, unos pasos con pocas imágenes destrozan lo aprendido (con 0,05, 0,797). En el ejercicio 04 ayuda con 10, 20 y 50 imágenes (0,895 frente a 0,865 con 20) y estorba con 100 y 400 (0,944 frente a 0,966 con 400). Tiene que haber aprendido algo útil para la tarea nueva.
10. Al azar, ventanas casi iguales a las de prueba estarían en el entrenamiento, y también lo que viene después: un error que nunca tendrías con el futuro de verdad. Con la media de toda la serie, una tendencia de la parte de prueba se colaría en el entrenamiento. Sur tiene 53 ventanas de prueba y es un solo corte: desde cero con `--semilla 7` también "mejora" (17,889), y por 0,16 sobre un MAE de 18. Es ruido; para afirmarlo harían falta varios cortes por tiempo y una mejora que se repita.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| Ejecución en vivo | Ante el instructor: `pronosticar` por defecto, con `--ventana 24`, con `--guardar` y con `--etiqueta X --desde`, y `pytest` en verde | 8 |
| Rompe y explica | Baraja las ventanas antes de repartir y explica qué test falla y por qué el resultado es engañoso; quita `load_state_dict(best_state)` y explica qué cambia en la salida | 8 |
| Explica su red | Cuenta a mano los 41 parámetros y los 25 entrenables con `--desde`; lee la tabla, dónde paró y el veredicto, y qué pasa con otra semilla | 8 |
| Pesos con cuidado | Explica por qué `save` guarda un diccionario y `load` usa `weights_only=True`; enseña el error de un archivo que no son solo pesos, y que `*.pt` está en su `.gitignore` | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 34

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `Forecast` con `improves`; `windows` con forma `(n, 1, w)`; `cnn` con `Conv1d`, ReLU, `Flatten` y `Linear`; `freeze` y `count`; `fit` con lotes barajados, validación en `eval()`, mejor época con `deepcopy`, paciencia y `load_state_dict`; `forecast` ordenado, por tiempo, escalado con lo que ve el entrenamiento y la semilla antes de la red; `save` con diccionario y `load` con `weights_only=True`; sin reexportar en `core/__init__.py` | 25 |
| El comando | `pronosticar` con el import dentro y las ocho opciones; `loss_table(losses, title)` con `math.ceil` usada también por `red`; dónde paró y la mejor época; código 1 y 2 según el error | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_convolution.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde; imágenes `week-35` y versión `0.35.0` | 15 |
| Git y README | Rama `week-35` en `python-<nombre>-<apellido>`; README con la sección "Pronóstico", e `informe/README.md` con el resultado en "Siguientes pasos"; sin archivos `.pt` en el repositorio | 10 |
| Pull request | Salidas, CI, `pronosticar` por defecto, con una etiqueta y con `--desde`, con su lectura, y la tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 36 (próximamente) |
