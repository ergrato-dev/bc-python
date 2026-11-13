# 03 · Entrenar de verdad

⏱️ 50 min

## 🎯 Objetivos

- Repartir en entrenamiento, validación y prueba, y usar cada parte para lo suyo.
- Escribir el bucle completo: mini-lotes, `model.train()` y `model.eval()`, y la validación tras cada época.
- Frenar el sobreajuste con *dropout* y con aumento de datos, y saber cuándo no ayudan.
- Bajar el ritmo de aprendizaje con un *scheduler*.
- Parar a tiempo, quedarte con la mejor época y guardar los pesos sin abrir la puerta a código ajeno.

---

## 1. Tres partes, tres usos

Hasta ahora repartías en dos: entrenar y medir. Pero en cuanto usas la medida para **elegir** algo (la época en la que parar, el tamaño de la ventana, si poner *dropout*), esa medida deja de ser limpia: elegiste lo que mejor le salía a esa parte. Por eso, tres partes:

| Parte | Para qué | Cuántas veces la miras |
|---|---|---|
| Entrenamiento | Ajustar los pesos | En cada paso |
| Validación | Elegir: épocas, hiperparámetros, qué red | En cada época |
| Prueba | Decir cuánto se equivoca la red elegida | **Una vez**, al final |

Es la misma idea que el `GridSearchCV` de la semana 32 con una prueba aparte: la validación cruzada elige, la prueba mide.

## 2. El bucle completo

El bucle de la semana 34 entrenaba con todas las medidas a la vez. El de verdad lo hace por **mini-lotes**, barajados en cada época, y mide la validación al final de cada una:

```python
import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(35)
t = torch.arange(600.0)
values = torch.sin(2 * torch.pi * t / 12) + 0.3 * torch.randn(600)
x = values.unfold(0, 8, 1)[:-1].unsqueeze(1)
y = values[8:].reshape(-1, 1)
train, validation = (x[:400], y[:400]), (x[400:], y[400:])
print(x.shape, y.shape)
```

```
torch.Size([592, 1, 8]) torch.Size([592, 1])
```

Seiscientos valores de una onda con ruido, cortados en ventanas de 8 (`unfold` es el `sliding_window_view` de PyTorch). Las 400 primeras entrenan y las siguientes validan, **en orden**: es una serie (teoría 05).

```python
def run(model, epochs=30, rate=0.01):
    optimizer = torch.optim.Adam(model.parameters(), lr=rate)
    loss_function = nn.MSELoss()
    loader = DataLoader(TensorDataset(*train), batch_size=32, shuffle=True)
    history = []
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            loss_function(model(xb), yb).backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            history.append(loss_function(model(validation[0]), validation[1]).item())
    return history

torch.manual_seed(35)
net = nn.Sequential(nn.Conv1d(1, 4, 3), nn.ReLU(), nn.Flatten(), nn.Linear(24, 1))
history = run(net)
print([round(v, 3) for v in history[::5]])
```

```
[0.255, 0.091, 0.088, 0.087, 0.09, 0.087]
```

- `DataLoader(..., shuffle=True)` reparte las 400 ventanas de entrenamiento en lotes de 32, en otro orden cada época. Barajar **dentro** del entrenamiento está bien: lo que no se baraja es el reparto entre partes.
- `model.train()` antes de entrenar y `model.eval()` antes de validar. Con capas como `Dropout` (sección 3) cambian el resultado; sin ellas no, pero ponerlas siempre evita el error el día que las añadas.
- La pérdida de validación baja hacia 0,09: lo que queda es, sobre todo, el ruido de la onda (0,3² = 0,09), que nadie puede pronosticar.

## 3. Dropout

Una capa **`nn.Dropout(p)`** apaga al azar, en cada paso, una parte `p` de los números que le llegan, y multiplica los demás por `1 / (1 − p)` para que la suma no cambie. La red no puede confiar en una sola neurona: tiene que repartir lo que sabe. Solo en entrenamiento: en `eval()`, no apaga nada.

```python
drop = nn.Dropout(0.5)
ones = torch.ones(8)
drop.train()
print(drop(ones), drop(ones))
drop.eval()
print(drop(ones))
```

```
tensor([2., 0., 2., 0., 0., 2., 0., 0.]) tensor([2., 2., 0., 0., 2., 0., 0., 2.])
tensor([1., 1., 1., 1., 1., 1., 1., 1.])
```

¿Ayuda? Depende. En el ejercicio 03, con 200 dígitos para entrenar, la red sin nada llega a 0,938 de acierto en validación, y con `Dropout(0.5)`, a 0,905: la red era tan pequeña que no le sobraba nada que apagar. El *dropout* se nota en redes grandes, con muchos más parámetros que medidas.

## 4. Aumento de datos

Si tus imágenes podrían llegar un poco movidas, giradas o con otra luz, puedes **fabricar** variantes de las de entrenamiento en cada lote: el dígito movido un píxel sigue siendo el mismo dígito. Se llama **aumento de datos** (*data augmentation*). Solo en entrenamiento; la validación y la prueba, tal cual.

En el ejercicio 03, paso 3:

| Red | Validación | Validación con las imágenes movidas |
|---|---|---|
| Sin nada | 0,938 | 0,507 |
| Con imágenes movidas al entrenar | 0,897 | 0,820 |

En la validación normal, algo peor. Con imágenes movidas, mucho mejor. Qué red es mejor depende de qué imágenes vas a recibir: **valida con datos como los que llegarán**. En una serie, un aumento razonable sería añadir un poco de ruido o escalar la ventana; mover la serie en el tiempo no, porque cambiaría qué viene después.

## 5. Un ritmo que baja

Al principio interesa dar pasos grandes; cerca del fondo, pasos pequeños, para no saltar de un lado a otro. Un **scheduler** baja el ritmo según avanzan las épocas. `StepLR` lo multiplica por `gamma` cada `step_size` épocas:

```python
model = nn.Linear(1, 1)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.3)
rates = []
for epoch in range(60):
    rates.append(optimizer.param_groups[0]["lr"])
    optimizer.step()
    scheduler.step()
print([round(rates[i], 5) for i in (0, 19, 20, 39, 40, 59)])
```

```
[0.01, 0.01, 0.003, 0.003, 0.0009, 0.0009]
```

El ritmo de las épocas 1, 20, 21, 40, 41 y 60: 0,01 las veinte primeras, 0,003 las veinte siguientes y 0,0009 las últimas. `scheduler.step()` va una vez por **época**, después de `optimizer.step()`, no en cada lote. En el ejercicio 03, paso 4, la misma red con imágenes movidas pasa de 0,897 a 0,920 en validación: al final, con pasos pequeños, deja de oscilar.

## 6. Parar a tiempo, y quedarse con la mejor

En la semana 34 (ejercicio 04, paso 6) viste la **parada temprana**: medir la validación en cada época, guardar una copia de los pesos cuando mejora y parar tras `patience` épocas sin mejorar. Es lo que hace `fit` en `core/convolution.py`:

```python
def fit_with_patience(model, epochs=200, patience=10):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_function = nn.MSELoss()
    loader = DataLoader(TensorDataset(*train), batch_size=32, shuffle=True)
    losses, best, best_state = [], 0, copy.deepcopy(model.state_dict())
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            loss_function(model(xb), yb).backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            loss = loss_function(model(validation[0]), validation[1]).item()
        if loss < min(losses, default=float("inf")):
            best, best_state = epoch, copy.deepcopy(model.state_dict())
        losses.append(loss)
        if epoch - best >= patience:
            break
    model.load_state_dict(best_state)
    return losses, best

torch.manual_seed(35)
net = nn.Sequential(nn.Conv1d(1, 4, 3), nn.ReLU(), nn.Flatten(), nn.Linear(24, 1))
losses, best = fit_with_patience(net)
print(f"{len(losses)} épocas; la mejor, la {best + 1}, con {losses[best]:.4f}")
```

```
33 épocas; la mejor, la 23, con 0.0857
```

- `min(losses, default=inf)`: en la primera época la lista está vacía, y cualquier pérdida es la mejor.
- `copy.deepcopy`: `state_dict()` devuelve los tensores de la red, no una copia; sin `deepcopy`, "la mejor" cambiaría con cada paso.
- `epoch - best >= patience`: con `patience=10`, si la mejor fue la época 30, para al terminar la 40.
- `load_state_dict(best_state)`: la red vuelve a su mejor época. Sin esta línea, te quedas con la última, que puede ser peor.

## 7. Guardar y cargar los pesos

Entrenar cuesta; los pesos se guardan para no repetirlo. Se guarda el **`state_dict`**, un diccionario de tensores, no la red entera:

```python
import pickle
import tempfile
from pathlib import Path

folder = Path(tempfile.mkdtemp())
torch.save({"window": 8, "state": net.state_dict()}, folder / "pesos.pt")
checkpoint = torch.load(folder / "pesos.pt", weights_only=True)
again = nn.Sequential(nn.Conv1d(1, 4, 3), nn.ReLU(), nn.Flatten(), nn.Linear(24, 1))
again.load_state_dict(checkpoint["state"])
print(checkpoint["window"], list(checkpoint["state"]))

torch.save(net, folder / "red.pt")
try:
    torch.load(folder / "red.pt", weights_only=True)
except pickle.UnpicklingError as problem:
    print(str(problem).splitlines()[0][:70])
```

```
8 ['0.weight', '0.bias', '3.weight', '3.bias']
Weights only load failed. This file can still be loaded, to do so you 
```

- Junto a los pesos puedes guardar números y textos (aquí, la ventana): lo que haga falta para volver a construir la red.
- Para cargar, primero se crea la red con la misma forma y después `load_state_dict` le pone los pesos.
- **`weights_only=True`**. `torch.save` usa `pickle`, y un archivo `pickle` puede llevar código que se ejecuta al cargarlo: abrir unos pesos descargados sería como ejecutar un programa de un desconocido. Con `weights_only=True` (lo normal desde PyTorch 2.6, pero escríbelo), `torch.load` solo acepta tensores, números, textos, listas y diccionarios; una red entera, o cualquier otra cosa, lanza `pickle.UnpicklingError`. Por eso `core/convolution.py` guarda el diccionario y no la red.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| Elegir la época o los hiperparámetros con la prueba | Un error en prueba optimista: has elegido lo que mejor le salía | Elige con validación; la prueba, una vez al final |
| Validar sin `model.eval()` | Con `Dropout`, una validación al azar y peor | `model.eval()` y `torch.no_grad()` antes de validar |
| Aumentar también la validación o la prueba | Mides con datos que no son los que llegarán | El aumento, solo en los lotes de entrenamiento |
| `scheduler.step()` dentro del bucle de lotes | El ritmo baja cada lote: en dos épocas, casi cero | Una vez por época |
| Guardar la mejor época sin `deepcopy` | Al final, "la mejor" es la última | `copy.deepcopy(model.state_dict())` |
| `torch.load(..., weights_only=False)` con un archivo descargado | Puede ejecutar código del archivo | `weights_only=True`, y guarda `state_dict`, no la red |

## ✅ Qué debes saber al terminar

- Para qué sirve cada parte: entrenamiento, validación y prueba, y por qué la prueba se mira una vez.
- El bucle por mini-lotes con `DataLoader`, y dónde van `model.train()`, `model.eval()` y `torch.no_grad()`.
- Qué hacen el *dropout* y el aumento de datos, y por qué se decide con validación si ayudan.
- Bajar el ritmo con `StepLR`, una vez por época.
- La parada temprana con la mejor época, y guardar y cargar pesos con `weights_only=True`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Redes convolucionales](02-redes-convolucionales.md) | **03 · Entrenar de verdad** | [04 · Transfer learning](04-transfer-learning.md) |
