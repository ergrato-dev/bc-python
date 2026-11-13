# Semana 34 — PyTorch I: tensores, autograd y MLP

> Hasta la semana 33, scikit-learn entrenaba por ti: `fit` y listo. Ahora entrenas tu primera red neuronal con PyTorch, y el bucle lo escribes tú: predecir, medir la pérdida, calcular los gradientes con autograd y dar un paso. Empiezas por los tensores, sigues con las derivadas y el descenso de gradiente, y terminas con un MLP. Tu Observatorio gana un comando: `red`, una red pequeña que predice el valor y se compara con la referencia.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Crear** tensores, **leer** su forma, su tipo y su dispositivo, y **predecir** el resultado del broadcasting
- **Calcular** gradientes con autograd y **explicar** el grafo de operaciones y la regla de la cadena
- **Escribir** el bucle de entrenamiento de PyTorch y **elegir** el ritmo de aprendizaje
- **Construir** un MLP con `nn.Sequential` y `nn.Module`, y **contar** sus parámetros
- **Reconocer** el sobreajuste en las curvas de entrenamiento y validación, y **parar** a tiempo
- **Instalar** PyTorch solo para CPU con uv, y **entrenar** una red repetible con los datos de tu dominio

---

## 📋 Prerrequisitos

- [Semana 33](../week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/README.md): árboles, ensembles, el comando `competir`.
- [Semana 23](../week-23-numpy_arrays_broadcasting_y_estadistica/README.md): arrays, forma y broadcasting en NumPy.
- El *pull request* `week-33` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-34-pytorch_tensores_autograd_y_mlp/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 33 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Tensores](1-teoria/01-tensores.md) | Forma, tipo y dispositivo, NumPy y PyTorch, reducciones, broadcasting y `@` | 45 min |
| [02 · Autograd](1-teoria/02-autograd.md) | El gradiente, `requires_grad` y `backward`, el grafo, gradientes que se acumulan, `no_grad` y `detach` | 50 min |
| [03 · Descenso de gradiente](1-teoria/03-descenso-de-gradiente.md) | El bucle de entrenamiento, el ritmo de aprendizaje, `nn.Linear` y el optimizador, escalar, Adam | 50 min |
| [04 · Redes neuronales: el MLP](1-teoria/04-redes-neuronales-mlp.md) | Capas y activaciones, `nn.Module`, mini-lotes, validación y sobreajuste | 50 min |
| [05 · PyTorch en tu Observatorio](1-teoria/05-pytorch-en-tu-observatorio.md) | PyTorch solo CPU con uv, de la instantánea al tensor, semillas, el comando `red`, ¿red o boosting? | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · Tensores](2-practicas/ejercicio-01-tensores/README.md) | Una semana de PM2.5 en un tensor: tipo, memoria compartida, forma, medias por día y por hora, broadcasting y `@` | 1 h 30 min |
| [02 · Autograd](2-practicas/ejercicio-02-autograd/README.md) | Derivadas con autograd y a mano, los gradientes de una recta, una neurona muerta, gradientes acumulados y cinco pasos a mano | 1 h 30 min |
| [03 · El bucle de entrenamiento](2-practicas/ejercicio-03-el-bucle-de-entrenamiento/README.md) | Descenso a mano, cuatro ritmos, `nn.Linear` frente a mínimos cuadrados, la forma del objetivo, escalar, SGD frente a Adam | 1 h 30 min |
| [04 · Un MLP](2-practicas/ejercicio-04-un-mlp/README.md) | Recta frente a red, capas sin activación, cuántas neuronas, mini-lotes, sobreajuste y parada temprana | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- PyTorch 2.15.0 solo para CPU, con `[[tool.uv.index]]` y `[tool.uv.sources]`;
- `core/neural.py`: `mlp` (la red), `train` (el bucle, con Adam), `learn` (reparte, prepara, escala, entrena y mide en prueba) y `Training`;
- el comando `red INSTANTANEA [--huella] [--oculta] [--epocas] [--ritmo] [--semilla]`.

48 tests nuevos: 47 de `neural` y `red`, y un ejemplo tuyo; uno más en `test_package`. La versión sube a `0.34.0`. **Es el único entregable de la semana.**
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
| Ver forma, tipo y dispositivo de un vistazo | `print(t.shape, t.dtype, t.device)` |
| De pandas a una red | `torch.from_numpy(np.asarray(tabla, dtype=np.float32))` |
| Una columna para `nn.Linear` | `y.reshape(-1, 1)` |
| El número de un tensor de cero dimensiones | `loss.item()` |
| Cuántos parámetros tiene tu red | `sum(p.numel() for p in model.parameters())` |
| Los nombres y formas de cada parámetro | `for name, p in model.named_parameters(): print(name, p.shape)` |
| Predecir sin anotar el grafo | `model.eval()` y `with torch.no_grad():` |
| La misma red cada vez | `torch.manual_seed(semilla)` justo antes de crear la red |
| Guardar la mejor red | `best = copy.deepcopy(model.state_dict())` y, al final, `model.load_state_dict(best)` |
| ¿Instalaste la versión de CPU? | `uv run python -c "import torch; print(torch.__version__)"` termina en `+cpu` |
| Probar tu red | `uv run observatorio red notebooks/instantanea.csv --oculta 32 --epocas 1000` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-34` de `python-<nombre>-<apellido>` con:
   - `torch==2.15.0` desde el índice de CPU, con `explicit = true`;
   - `core/neural.py` sin reexportar en `core/__init__.py`, y el comando `red`, con el import dentro;
   - las imágenes `week-34`, la versión `0.34.0` y al menos 6 tests propios en `tests/test_my_neural.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Red neuronal", e `informe/README.md` con el resultado en "Siguientes pasos"
3. ✅ Pull request `week-34` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `red` con tu instantánea, por defecto y con más neuronas y épocas, y tu lectura;
   - la tabla de mutantes con las dos respuestas del paso 9, y el tamaño de tu imagen.

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
uv run python -c "import torch; print(torch.__version__)"
uv run observatorio red notebooks/instantanea.csv
uv run observatorio red notebooks/instantanea.csv --oculta 4 --epocas 3
uv run observatorio red notebooks/instantanea.csv --huella 0000
uv run python -c "import sys, observatorio.cli; print('torch' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1346;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.34.0`;
- la versión de PyTorch es `2.15.0+cpu` (en macOS, `2.15.0`);
- el primer `red` escribe tu número de medidas, tu huella, la red con sus parámetros, la tabla de seis épocas y el veredicto;
- el segundo, una red de 4 neuronas y una tabla de las épocas 1, 2 y 3;
- el tercero, `error: la huella de instantanea.csv es ..., no 0000` y código 1;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 33](../week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/README.md) | **Semana 34** | Semana 35 (próximamente) |
