# Rúbrica de Evaluación — Semana 34: PyTorch I, tensores, autograd y MLP

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 33 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué tiene un tensor que no tiene un array de NumPy? ¿Por qué las capas de una red esperan `float32`, y qué pasa si les das `float64`? ¿En qué se diferencian `torch.from_numpy` y `torch.tensor`? | 10 |
| 2 | Explica las reglas del broadcasting con `(7, 24)` menos `(7, 1)`, y por qué `(7, 24)` menos `(7,)` falla. ¿Por qué una salida `(n, 1)` y un objetivo `(n,)` son peligrosos aunque no den error? | 10 |
| 3 | ¿Qué es un gradiente y qué dice su signo? En la teoría 02, con la recta `w · x + b`, ¿por qué `w.grad` es mayor que `b.grad`? | 10 |
| 4 | ¿Qué hace `backward()`? ¿Qué es el grafo de operaciones? ¿Por qué hay que poner los gradientes a cero en cada paso, y qué pasa si lo olvidas? | 10 |
| 5 | ¿Para qué sirven `torch.no_grad()`, `detach()` e `item()`? ¿Por qué se guarda `loss.item()` y no `loss`? | 10 |
| 6 | Escribe las cuatro líneas de cada época de un bucle de entrenamiento y di qué hace cada una. ¿Qué pasa con un ritmo de aprendizaje demasiado pequeño y con uno demasiado grande? | 10 |
| 7 | ¿Por qué hay que escalar las entradas antes de entrenar una red? ¿Y por qué también el objetivo, sobre todo con Adam? Usa el ejercicio 03, pasos 5 y 6. | 10 |
| 8 | ¿Por qué tres capas lineales seguidas se comportan como una sola? ¿Qué añade ReLU? ¿Cuántos parámetros tiene `nn.Sequential(nn.Linear(6, 16), nn.ReLU(), nn.Linear(16, 1))`? | 10 |
| 9 | ¿Qué es un mini-lote, un paso y una época? En el ejercicio 04, paso 5, ¿cómo ves el sobreajuste en las dos curvas? ¿Qué hace la parada temprana del paso 6? | 10 |
| 10 | Con los datos de ejemplo, `red` da una pérdida que baja de 1,01 a 0,98 y un MAE de 20,26 frente a 20,07 de la referencia. Explica el resultado. ¿Por qué un "mejora" de dos centésimas con otra semilla no significaría nada? ¿Cuándo elegirías una red y cuándo un *gradient boosting*? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Puede vivir en una tarjeta gráfica (`device`) y puede anotar las operaciones para calcular derivadas solo (*autograd*). Las capas tienen sus pesos en `float32`: la mitad de memoria que `float64` y más rápido; con `float64`, `nn.Linear` lanza `mat1 and mat2 must have the same dtype`. `from_numpy` comparte la memoria con el array (un cambio en uno se ve en el otro) y no copia; `torch.tensor` hace una copia independiente.
2. Las formas se comparan desde la derecha: dos tamaños encajan si son iguales o si uno es 1, y el 1 se estira. `(7, 24)` y `(7, 1)`: 24 y 1 encajan, 7 y 7 también; la media de cada día se resta a sus 24 horas. `(7,)` se alinea con las 24 horas: 24 y 7 no encajan. `(n, 1)` menos `(n,)` encaja como `(n, 1)` menos `(1, n)` y da una tabla `(n, n)`: la pérdida mezcla cada predicción con cada objetivo, y PyTorch solo avisa.
3. Las derivadas de la pérdida respecto de cada parámetro: cuánto cambia la pérdida si ese parámetro sube un poco. Negativo: subirlo baja la pérdida; positivo: hay que bajarlo; cero: un mínimo (o un punto plano). El gradiente de `w` lleva multiplicada la entrada `x` (regla de la cadena), que llega a 3; el de `b`, no.
4. Recorre el grafo desde la pérdida hacia atrás, aplicando la regla de la cadena, y deja en el `.grad` de cada tensor con `requires_grad` su derivada. El grafo es lo que PyTorch anota al calcular: cada operación y de qué tensores salió. `backward()` **suma** al `.grad` que ya había: sin ponerlo a cero, cada paso usa la suma de todos los gradientes anteriores. No hay ningún error: la red entrena peor o diverge.
5. `no_grad()`: lo que se calcula dentro no se anota; para actualizar parámetros a mano y para predecir. `detach()`: el mismo tensor sin historia, por ejemplo para pasarlo a NumPy. `item()`: un `float` de Python. Una lista de `loss` mantendría vivo el grafo de cada época en memoria.
6. `optimizer.zero_grad()` pone los gradientes a cero; `loss = loss_function(model(x), y)` predice y mide; `loss.backward()` calcula los gradientes; `optimizer.step()` mueve cada parámetro en contra de su gradiente. Un ritmo pequeño avanza poco y no llega en las épocas que hay; uno grande se pasa del fondo y la pérdida crece hasta `inf` o `nan`.
7. El gradiente de un peso lleva multiplicada su entrada: con vehículos en unidades (miles), los gradientes son miles de veces mayores y el ritmo que iba bien diverge (`nan`); con entradas en escalas distintas, ningún ritmo va bien a todas. Adam da pasos de un tamaño parecido al ritmo: con 0,05 y 300 épocas, el sesgo avanza unos 15 y no llega a un objetivo que ronda 16; con el objetivo escalado (media 0), el sesgo ya empieza cerca.
8. Una capa lineal de una capa lineal es otra capa lineal: `(x · W1 + b1) · W2 + b2 = x · (W1 · W2) + (b1 · W2 + b2)`. ReLU deja los positivos y cambia los negativos por 0: cada neurona dibuja un codo, y la suma de codos dibuja curvas. `(6 + 1) · 16 + (16 + 1) = 129`.
9. Un mini-lote es un grupo pequeño de medidas; un paso, una actualización del optimizador (una por lote); una época, una pasada por todos los lotes. Con 60 medidas y una red de 66 000 parámetros, las dos pérdidas bajan juntas hasta la época 100; después, la de entrenamiento sigue bajando (0,03) y la de validación sube (de 0,15 a 0,25): memoriza. La parada temprana mide la validación en cada época, guarda los pesos de la mejor (`deepcopy(state_dict())`) y para tras 50 épocas sin mejorar; se queda con la época 79.
10. La pérdida empieza en 1 porque el valor está escalado (predecir la media da 1) y apenas baja: ni la etiqueta ni la posición dicen nada del valor, como en las semanas 30 a 33. En prueba, la red se equivoca un poco más que la media. `red` mide con un solo reparto: con otra semilla, otras medidas en prueba, y unas centésimas de diferencia son ruido; para decir "mejora" harían falta pliegues, como en `competir`. Con tablas pequeñas, un *gradient boosting* suele ganar o empatar con menos trabajo; una red, con imágenes, texto o sonido, o con muchísimas medidas.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| PyTorch bien instalado | Explica el índice de CPU, `explicit = true` y `[tool.uv.sources]`; enseña `torch.__version__` y el tamaño de su imagen | 8 |
| Ejecución en vivo | Ante el instructor: `red` por defecto, con otra semilla y con `--oculta 64 --epocas 2000`, y `pytest` en verde | 8 |
| Rompe y explica | Quita `optimizer.zero_grad()` y explica qué cambia en `red` y qué test lo detecta; quita el escalado del valor y explica la nueva tabla de la pérdida | 8 |
| Explica su red | Lee su salida: los parámetros, la curva de la pérdida y el veredicto; lo compara con `competir` de la semana 33 y dice qué pasa con otra semilla | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 33

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `Training` con `learned` e `improves`; `tensor` en `float32`; `mlp` con ReLU; `train` con Adam, `MSELoss` y `zero_grad`; `learn` con `split`, `prepare` sin dispersas ajustado con el entrenamiento, el valor escalado y deshecho, y la semilla antes de la red; sin reexportar en `core/__init__.py` | 25 |
| El comando | `red` con el import dentro, `--huella`, `--oculta`, `--epocas`, `--ritmo` y `--semilla`, la tabla de seis épocas, el aviso si la pérdida no baja, el veredicto, y código 1 y 2 según el error | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_neural.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde; `torch==2.15.0` desde el índice de CPU; imágenes `week-34` y versión `0.34.0` | 15 |
| Git y README | Rama `week-34` en `python-<nombre>-<apellido>`; README con la sección "Red neuronal", e `informe/README.md` con el resultado en "Siguientes pasos" | 10 |
| Pull request | Salidas, CI, `red` por defecto y con más neuronas y épocas, con su lectura, la tabla de mutantes con las dos respuestas, y el tamaño de la imagen | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 35](../week-35-pytorch_cnn_entrenamiento_y_transfer_learning/README.md) |
