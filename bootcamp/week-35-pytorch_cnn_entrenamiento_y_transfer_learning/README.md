# Semana 35 — PyTorch II: CNN, entrenamiento y transfer learning

> En la semana 34 escribiste el bucle de entrenamiento y una red de capas lineales. Ahora entrenas redes que miran la forma de los datos: las convoluciones, con filtros que se deslizan sobre una imagen o una serie. Entrenas como se hace de verdad (lotes, validación, *dropout*, aumento de datos, parada temprana, puntos de control) y reutilizas una red ya entrenada para una tarea con pocas etiquetas. Tu Observatorio gana un comando: `pronosticar`, una red convolucional que pronostica cada valor con los anteriores y que puede empezar desde los pesos de otra.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Calcular** la salida de una convolución a mano y **predecir** su tamaño con el relleno y el paso
- **Construir** una CNN con `Conv2d`, `MaxPool2d` y `Conv1d`, **seguir** su forma capa a capa y **contar** sus parámetros
- **Clasificar** con `CrossEntropyLoss` y **leer** puntuaciones, probabilidades y acierto
- **Entrenar** con mini-lotes, validación, *dropout*, aumento de datos, un ritmo que baja y parada temprana, y **guardar** los pesos con `weights_only=True`
- **Aplicar** *transfer learning*: congelar, cambiar la salida, entrenar y afinar, y **decidir** cuándo ayuda
- **Pronosticar** tu serie con ventanas repartidas por tiempo, sin dejar que el futuro se cuele en el entrenamiento

---

## 📋 Prerrequisitos

- [Semana 34](../week-34-pytorch_tensores_autograd_y_mlp/README.md): tensores, autograd, el bucle de entrenamiento, el MLP y el comando `red`.
- [Semana 32](../week-32-features_pipelines_validacion_cruzada_y_tuning/README.md): validación por tiempo con `TimeSeriesSplit` y `ordered`.
- El *pull request* `week-34` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-35-pytorch_cnn_entrenamiento_y_transfer_learning/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 34 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · La convolución](1-teoria/01-la-convolucion.md) | Lo que un MLP no sabe, un filtro que se desliza, qué detecta, relleno y paso, canales, en dos dimensiones y `MaxPool2d` | 45 min |
| [02 · Redes convolucionales](1-teoria/02-redes-convolucionales.md) | Bloques que se repiten, puntuaciones y `CrossEntropyLoss`, ¿CNN o MLP?, una CNN para una serie | 50 min |
| [03 · Entrenar de verdad](1-teoria/03-entrenar-de-verdad.md) | Tres partes, el bucle completo, *dropout*, aumento de datos, un ritmo que baja, parada temprana, guardar y cargar | 50 min |
| [04 · Transfer learning](1-teoria/04-transfer-learning.md) | Congelar, afinar, cuándo ayuda, redes preentrenadas y pesos ajenos | 50 min |
| [05 · Pronosticar en tu Observatorio](1-teoria/05-pronosticar-en-tu-observatorio.md) | Ventanas, reparto por tiempo, escalar sin mirar el futuro, `core/convolution.py` y el comando `pronosticar` | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · La convolución](2-practicas/ejercicio-01-la-convolucion/README.md) | Un filtro a mano y con `F.conv1d`, subidas, relleno y paso, los bordes de un dígito, una capa `Conv2d` y su tamaño | 1 h 30 min |
| [02 · Una CNN](2-practicas/ejercicio-02-una-cnn/README.md) | Dígitos escritos a mano: un MLP frente a una CNN, la forma capa a capa, dígitos movidos, errores y probabilidades | 1 h 30 min |
| [03 · Entrenar de verdad](2-practicas/ejercicio-03-entrenar-de-verdad/README.md) | 200 dígitos: lotes, *dropout*, imágenes movidas, `StepLR`, guardar y cargar, y la prueba una sola vez | 1 h 30 min |
| [04 · Transfer learning](2-practicas/ejercicio-04-transfer-learning/README.md) | De leer dígitos a "¿es par?" con 20 imágenes: congelar, afinar y cuántas imágenes hacen falta | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/convolution.py`: `windows`, `cnn`, `freeze`, `count`, `fit` (lotes y parada temprana), `forecast` (por tiempo), `save`, `load` y `Forecast`;
- el comando `pronosticar INSTANTANEA [--huella] [--etiqueta] [--ventana] [--epocas] [--paciencia] [--semilla] [--guardar] [--desde]`;
- `loss_table`, compartida por `red` y `pronosticar`, con seis épocas como mucho.

59 tests nuevos: 58 de `convolution` y `pronosticar`, y un ejemplo tuyo. La versión sube a `0.35.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
|---|---|
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| El tamaño tras una convolución | `(n + 2 * padding - kernel) // stride + 1` |
| La forma capa a capa | `for layer in model: x = layer(x); print(type(layer).__name__, x.shape)` |
| Una serie para `Conv1d` | `serie.reshape(1, 1, -1)`: lote, canal, longitud |
| Ventanas sin copiar | `np.lib.stride_tricks.sliding_window_view(values[:-1], w)` o `tensor.unfold(0, w, 1)` |
| La clase con más puntuación | `scores.argmax(dim=1)`; probabilidades, `scores.softmax(dim=1)` |
| Parámetros entrenables | `sum(p.numel() for p in model.parameters() if p.requires_grad)` |
| Congelar una parte | `model[0].requires_grad_(False)` |
| Guardar y cargar pesos | `torch.save(model.state_dict(), path)` y `model.load_state_dict(torch.load(path, weights_only=True))` |
| Ver dónde paró | `uv run observatorio pronosticar notebooks/instantanea.csv --paciencia 3` |
| Reutilizar una red | `pronosticar ... --guardar pesos.pt` y `pronosticar ... --etiqueta X --desde pesos.pt` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-35` de `python-<nombre>-<apellido>` con:
   - `core/convolution.py` sin reexportar en `core/__init__.py`, y el comando `pronosticar`, con el import dentro;
   - `loss_table(losses, title)` con `math.ceil`, usada por `red` y `pronosticar`;
   - las imágenes `week-35`, la versión `0.35.0` y al menos 6 tests propios en `tests/test_my_convolution.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Pronóstico", e `informe/README.md` con el resultado en "Siguientes pasos"
3. ✅ Pull request `week-35` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `pronosticar` con tu instantánea, por defecto, con una etiqueta desde cero y con `--desde`, y tu lectura;
   - la tabla de mutantes con las dos respuestas del paso 8.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pre-commit run --all-files
uv run pytest
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
uv run observatorio --version
uv run observatorio pronosticar notebooks/instantanea.csv
uv run observatorio pronosticar notebooks/instantanea.csv --epocas 3
uv run observatorio pronosticar notebooks/instantanea.csv --guardar pesos.pt
uv run observatorio pronosticar notebooks/instantanea.csv --etiqueta <una-etiqueta> --desde pesos.pt
uv run observatorio pronosticar notebooks/instantanea.csv --huella 0000
uv run python -c "import sys, observatorio.cli; print('torch' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1405;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.35.0`;
- el primer `pronosticar` escribe tu número de medidas, tu huella, la serie y su reparto, la red, la tabla de la pérdida de validación, dónde paró y el veredicto;
- el segundo, `entrenó 3 épocas`;
- el tercero, `pesos guardados en pesos.pt`; el cuarto, `filtros congelados de pesos.pt` y 25 parámetros entrenables;
- el quinto, `error: la huella de instantanea.csv es ..., no 0000` y código 1;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 34](../week-34-pytorch_tensores_autograd_y_mlp/README.md) | **Semana 35** | [Semana 36](../week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/README.md) |
