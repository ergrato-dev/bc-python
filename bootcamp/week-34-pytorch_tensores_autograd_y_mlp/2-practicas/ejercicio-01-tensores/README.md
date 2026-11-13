# Ejercicio 01 — Tensores

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-tensores.md)

## Objetivo

Pasar una semana de medidas de NumPy a PyTorch y trabajar con ella como tensor:

- del array al tensor, y de `float64` a `float32`;
- cuándo un tensor comparte memoria con su array y cuándo es una copia;
- cambiar la forma: de 168 horas a 7 días de 24 horas;
- medias por día, por hora y por sensor, con `dim`;
- restar a cada día su media con broadcasting, y el error cuando las formas no encajan;
- combinar tres sensores con una multiplicación de matrices.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-34-pytorch_tensores_autograd_y_mlp/2-practicas/ejercicio-01-tensores/starter
uv run python main.py
```

La primera vez, uv descarga PyTorch para CPU (unos 200 MB) y crea el entorno: tarda un poco. Las siguientes, nada.

```
Ejercicio 01 · Tensores
readings: ndarray (168, 3) float64
```

Una semana de PM2.5, hora a hora (168 horas, de lunes a domingo), en tres sensores del Centro. Sube en las horas punta, las 8 y las 19, y el fin de semana mucho menos. `readings` es un array de NumPy en `float64`, como lo daría pandas. El `pyproject.toml` del ejercicio ya trae el índice de PyTorch para CPU (teoría 05, sección 1).

## Pasos

### 1. Del array al tensor

Descomenta el **PASO 1** y ejecuta:

```
torch.Size([168, 3]) torch.float64 cpu
tensor([[13.9000, 14.5000, 17.1000],
        [15.0000, 18.3000, 11.6000]], dtype=torch.float64)
torch.float32 8 bytes por número frente a 4
```

- `torch.tensor(readings)` conserva la forma y el tipo: 168 filas, 3 columnas, `float64`. Como no es el tipo por defecto de PyTorch, el tensor lo dice al imprimirse: `dtype=torch.float64`.
- `.float()` lo pasa a `float32`, el tipo con el que trabajan las capas de una red. Ocupa la mitad: 4 bytes por número.
- `device` es `cpu`: el tensor vive en la memoria normal.

### 2. Copiar o compartir

Descomenta el **PASO 2** y ejecuta:

```
compartido 999.0 · copiado 13.9
de vuelta: 13.9
```

Se cambia el **array** de NumPy, no los tensores. `from_numpy` comparte la memoria con él: ve el 999. `torch.tensor` hizo una copia al crearse: sigue en 13,9. La última línea deja el array como estaba, para los pasos siguientes.

`from_numpy` es instantáneo con millones de números, porque no copia nada; a cambio, un cambio en uno se ve en el otro. Cuando no estés seguro, `torch.tensor`.

### 3. La forma

Descomenta el **PASO 3** y ejecuta:

```
torch.Size([168]) → torch.Size([7, 24])
martes a las 8: 31.5
las 8 de cada día: tensor([32.3000, 31.5000, 31.7000, 29.5000, 32.0000, 24.7000, 21.6000])
como columna: torch.Size([168, 1]) · otra vez fila: torch.Size([168])
```

- `light[:, 0]` es el primer sensor: 168 números en una dimensión.
- `reshape(7, 24)` los reparte en 7 filas de 24: una fila por día, una columna por hora. Funciona porque las horas van en orden; si estuvieran desordenadas, el reparto no tendría sentido y PyTorch no te avisaría.
- `by_day[1, 8]` es el día 1 (martes, empezando en 0) a las 8. `by_day[:, 8]`, las 8 de **cada** día: el sábado y el domingo (los dos últimos) mucho más bajos.
- `unsqueeze(1)` añade una dimensión de tamaño 1 en la posición 1: de `(168,)` a `(168, 1)`, una columna. `squeeze(1)` la quita.

### 4. Reducir a lo largo de una dimensión

Descomenta el **PASO 4** y ejecuta:

```
media de cada día: tensor([18.3000, 18.1000, 18.1000, 17.0000, 18.0000, 16.3000, 15.6000])
hora con la media más alta: 8 (29.0)
media de cada sensor: tensor([17.4000, 20.0000, 15.4000])
```

- `by_day.mean(dim=1)`: la dimensión 1 (las horas) desaparece. Queda un número por día.
- `by_day.mean(dim=0)`: desaparecen los días. Queda un número por hora, y `argmax` dice cuál es la más alta: las 8.
- `light.mean(dim=0)`: en la tabla de 168 × 3, desaparecen las horas y queda la media de cada sensor. El segundo mide unos 3 puntos más que el primero; el tercero, 2 menos. En un sensor de verdad, eso sería un problema de calibración.

### 5. Broadcasting

Descomenta el **PASO 5** y ejecuta:

```
torch.Size([7, 24]) - torch.Size([7, 1]) = torch.Size([7, 24])
el lunes, de media, tras centrar: 0.0
sin keepdim: The size of tensor a (24) must match the size of tensor b (7) at non-singleton dimension 1
```

- Con `keepdim=True`, la media de cada día sale como una columna `(7, 1)`. Comparando desde la derecha, 24 y 1 encajan y 7 y 7 también: la media de cada día se resta a sus 24 horas. Cada día queda centrado en 0.
- Sin `keepdim`, la media es `(7,)`, que se alinea por la derecha con las **24 horas**: 24 y 7 no encajan. Error.

El error es la buena noticia: con una semana de 7 días **y 7 horas**, las formas encajarían y restarías la media del martes a las 1 de cada día, sin aviso. Antes de un broadcasting, escribe las dos formas y alinéalas por la derecha.

### 6. Multiplicar matrices

Descomenta el **PASO 6** y ejecuta:

```
torch.Size([168, 3]) @ torch.Size([3, 1]) = torch.Size([168, 1])
primeras tres horas: tensor([14.8500, 14.9750, 14.5750])
¿lo mismo que NumPy? True
```

Una media ponderada de los tres sensores: el primero cuenta la mitad, y los otros dos, un cuarto cada uno. `(168, 3) @ (3, 1)`: las dimensiones de dentro (3 y 3) desaparecen y queda una columna, un valor por hora. Para la primera hora, 13,9 × 0,5 + 14,5 × 0,25 + 17,1 × 0,25 = 14,85.

Una capa `nn.Linear(3, 1)` hace exactamente esto, con los pesos aprendidos en vez de elegidos, y un sesgo sumado (teoría 01, sección 6).

Para terminar, escribe en un comentario al final de `main.py` qué forma tendría un tensor con las medidas de **tu** dominio: ¿cuántas dimensiones?, ¿qué es cada una?

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `uv run` tarda varios minutos la primera vez | Descarga PyTorch: es normal. Si se corta, vuelve a ejecutarlo |
| `NameError: name 'light' is not defined` | El paso 3 usa `light`, del paso 1: descoméntalo antes |
| `compartido 13.9` en el paso 2 | Has cambiado el tensor, no el array: `readings[0, 0] = 999.0` |
| Los números del paso 4 cambian en el último decimal | Otro procesador redondea distinto: compara a una cifra decimal |
| `-0.0` en vez de `0.0` en el paso 5 | Lo mismo: un número diminuto negativo, redondeado. Es 0 |
| `RuntimeError: expected m1 and m2 to have the same dtype` en el paso 6 | Usas `week` (`float64`) en vez de `light` (`float32`) con pesos `float32` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · PyTorch en tu Observatorio](../../1-teoria/05-pytorch-en-tu-observatorio.md) | **Ejercicio 01 · Tensores** | [Ejercicio 02 · Autograd](../ejercicio-02-autograd/README.md) |
