# 05 · PyTorch en tu Observatorio

⏱️ 45 min

## 🎯 Objetivos

- Instalar PyTorch solo para CPU con un índice de uv, y saber por qué.
- Pasar una instantánea de pandas a tensores sin fugas: preparar y escalar con el entrenamiento.
- Hacer que una red dé el mismo resultado en cada ejecución.
- Leer la salida del comando `red` y decidir cuándo una red compensa frente a un árbol o un boosting.

---

## 1. PyTorch solo para CPU

`uv add torch` en Linux instala la versión de PyPI, que trae las bibliotecas de CUDA para tarjetas gráficas de NVIDIA: más de 2 GB que tu proyecto no va a usar. PyTorch publica en su propio índice una versión **solo para CPU**, mucho más pequeña. Se le dice a uv en `pyproject.toml`:

```toml
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cpu" }
```

- `[[tool.uv.index]]` añade un índice de paquetes además de PyPI. Los dobles corchetes son una lista de TOML: puede haber varios.
- `explicit = true`: de ese índice solo sale lo que se le pide **por nombre**. Sin él, uv buscaría ahí también el resto de paquetes y encontraría versiones viejas de algunos (en ese índice hay un `idna` de 2022): `uv add` falla con `No solution found`.
- `[tool.uv.sources]` le pide `torch` a ese índice.

Con eso, `uv add torch==2.15.0` fija la versión y `uv.lock` apunta a las ruedas de CPU:

```bash
uv run python -c "import torch; print(torch.__version__)"
```

```
2.15.0+cpu
```

El `+cpu` lo confirma. En macOS no hay versión con CUDA: el mismo índice da la normal, `2.15.0`, que ya es solo para CPU (y sabe usar la GPU de los Mac con `device="mps"`).

Aun así, PyTorch pesa: unos 800 MB instalado, más que todo lo demás junto. La imagen `runtime` del Observatorio pasa de 1,25 GB a 2,5 GB. Y tarda en importarse, un segundo en un portátil: por eso la CLI lo importa **dentro** de `red`, como hacía con scikit-learn, y `informe` o `--version` no lo pagan.

## 2. De la instantánea al tensor

Las entradas de la red son las mismas que las de la semana 32: la etiqueta en one-hot y la posición escalada, con `prepare()` de `core/validation.py`. Tres detalles nuevos:

```python
train_rows, test_rows = split(frame, seed=seed)
prepared = prepare().set_params(sparse_threshold=0.0).fit(train_rows[INPUTS])
x_train = tensor(prepared.transform(train_rows[INPUTS]))
```

- **El reparto**, con `split` de la semana 31: estratificado por nivel y con la semilla. La red se mide en las medidas de prueba, como `modelo`.
- **Sin matrices dispersas.** Con muchas etiquetas, el one-hot es casi todo ceros, y `ColumnTransformer` devuelve una matriz *dispersa* de SciPy, que guarda solo los números que no son cero. `np.asarray` no sabe convertirla. `sparse_threshold=0.0` pide siempre una tabla normal.
- **`float32`.** `tensor()` convierte con `np.asarray(values, dtype=np.float32)`: las capas de PyTorch no aceptan `float64` (teoría 01).

Y el **valor**, también escalado, con la media y la desviación del entrenamiento:

```python
center, spread = float(train_rows["valor"].mean()), float(train_rows["valor"].std())
y_train = tensor((train_rows["valor"] - center) / spread).reshape(-1, 1)
```

La red aprende a predecir el valor escalado. Para medir el error en tus unidades, se deshace el escalado al predecir: `model(x_test) * spread + center`. Sin escalar el valor, una red que empieza cerca de 0 gasta sus 300 épocas solo en llegar a la media (teoría 03, sección 4). Lo comprueba `test_learn_scales_the_value`.

`reshape(-1, 1)`: la salida de la red es `(n, 1)`, y el objetivo tiene que tener la **misma** forma (teoría 03, sección 3).

## 3. La misma red cada vez

Una red empieza con pesos al azar. Sin semilla, cada ejecución de `red` daría otra red y otro error. Hay dos fuentes de azar, y las dos van con la semilla:

- **el reparto** entrenamiento-prueba: `split(frame, seed=seed)`, de scikit-learn;
- **los pesos iniciales**: `torch.manual_seed(seed)` justo **antes** de crear la red.

```python
torch.manual_seed(seed)
model = mlp(x_train.shape[1], hidden)
```

El proyecto entrena con todas las medidas a la vez, sin mini-lotes: no hay un barajado más que fijar. Con eso, en tu máquina, la misma instantánea y la misma semilla dan exactamente la misma red: `test_learn_uses_the_seed_for_the_split_and_the_weights` lo comprueba.

En **otra** máquina, los últimos decimales pueden cambiar: PyTorch usa bibliotecas de cálculo distintas según el procesador, y sumar en otro orden redondea distinto. Por eso los tests comparan con `pytest.approx` y con umbrales ("menos de la mitad que la referencia"), nunca con el séptimo decimal.

## 4. El comando `red`

```bash
uv run observatorio red notebooks/instantanea.csv
```

```
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
red de 16 neuronas ocultas y 129 parámetros · 300 épocas · ritmo 0.01
Pérdida en entrenamiento (MSE del valor escalado)
┏━━━━━━━┳━━━━━━━━━┓
┃ Época ┃ Pérdida ┃
┡━━━━━━━╇━━━━━━━━━┩
│     1 │  1.0149 │
│    61 │  0.9812 │
│   121 │  0.9769 │
│   181 │  0.9767 │
│   241 │  0.9766 │
│   300 │  0.9765 │
└───────┴─────────┘
regresión del valor · MAE en prueba: red 20.261 · referencia 20.066: la red no mejora la referencia
```

- **129 parámetros**: cinco etiquetas y la posición son 6 entradas, y `(6 + 1) · 16 + (16 + 1) = 129` (teoría 04, sección 3).
- **La pérdida** empieza en 1,01 (con el valor escalado, lo que se equivoca predecir la media) y se queda en 0,98. La red apenas encuentra nada que aprender.
- **El veredicto**: en prueba, la red se equivoca 20,26 de media; la referencia, 20,07. No mejora.

Es lo mismo que dijeron `hallazgos` (semana 30), `modelo` (31), `ajustar` (32) y `competir` (33): en los datos de ejemplo, ni la etiqueta ni la posición dicen mucho del valor. Una red no inventa una señal que no está. ¿Y una red más grande?

```bash
uv run observatorio red notebooks/instantanea.csv --oculta 64 --epocas 2000
```

```
...
│  2000 │  0.9480 │
└───────┴─────────┘
regresión del valor · MAE en prueba: red 20.228 · referencia 20.066: la red no mejora la referencia
```

La pérdida de entrenamiento baja un poco más (0,95), y la de prueba no mejora: lo que gana es memoria del ruido.

Las opciones: `--oculta` (neuronas de la capa oculta), `--epocas`, `--ritmo` (el de Adam) y `--semilla`. Si la pérdida de la última época no es menor que la de la primera, `red` lo avisa: `la pérdida no bajó: prueba otro --ritmo o más --epocas`.

## 5. ¿Red, árbol o boosting?

Con tablas como las de tu Observatorio (unas columnas, unos miles de filas), los modelos de la semana 33, sobre todo el *gradient boosting*, suelen ganar a una red, o empatar con mucho menos trabajo:

| | Red (MLP) | Gradient boosting |
|---|---|---|
| Preparar entradas | Escalar todo, también el objetivo | Casi nada: ni escalar |
| Hiperparámetros sensibles | Ritmo, neuronas, capas, épocas | Pocos, con buenos valores por defecto |
| Datos tabulares pequeños | Sobreajusta con facilidad | Suele ser el mejor |
| Imágenes, texto, sonido | Lo que mejor funciona | No sirve |
| Dependencia | PyTorch, 800 MB | scikit-learn, ya instalado |

Entonces, ¿por qué una red? Porque es la pieza de todo lo que viene: las redes convolucionales que miran imágenes (semana 35), los *transformers* que leen texto (semana 36) y los modelos de lenguaje (semanas 37 a 39) son redes que se entrenan con este mismo bucle: predecir, medir la pérdida, `backward()`, `step()`. Esta semana lo has escrito tú, con una red pequeña que puedes entender entera.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| `uv add torch` sin el índice de CPU | Más de 2 GB de CUDA en tu proyecto y en tu imagen | `[[tool.uv.index]]` y `[tool.uv.sources]` antes de `uv add` |
| El índice sin `explicit = true` | `No solution found`: uv busca ahí otros paquetes | `explicit = true` |
| Escalar el valor con todas las medidas | Fuga de la prueba al entrenamiento | La media y la desviación del entrenamiento |
| Medir el MAE sin deshacer el escalado | Un error en desviaciones, no en tus unidades | `model(x) * spread + center` |
| `torch.manual_seed` después de crear la red | Los pesos iniciales ya salieron al azar | La semilla justo antes de `mlp(...)` |
| `import torch` al principio de `cli.py` | Cada comando tarda un segundo más | Importarlo dentro de `red` |

## ✅ Qué debes saber al terminar

- Cómo instalar PyTorch solo para CPU con uv, y qué hace `explicit = true`.
- Los tres pasos de la instantánea al tensor: reparto, preparación sin dispersas y `float32`, y el valor escalado.
- Qué dos semillas hacen falta para repetir una red, y por qué otra máquina puede dar otros decimales.
- Leer la salida de `red`: los parámetros, la curva de la pérdida y el veredicto.
- Cuándo una red compensa y cuándo un boosting es mejor elección.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Redes neuronales: el MLP](04-redes-neuronales-mlp.md) | **05 · PyTorch en tu Observatorio** | [Ejercicio 01 · Tensores](../2-practicas/ejercicio-01-tensores/README.md) |
