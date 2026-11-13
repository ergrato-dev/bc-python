# Ejercicio 03 — Entrenar de verdad

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-entrenar-de-verdad.md)

## Objetivo

Entrenar una CNN con pocas imágenes y probar lo que se usa para entrenar mejor:

- mini-lotes, y la distancia entre el acierto de entrenamiento y el de validación;
- *dropout*, en `train()` y en `eval()`;
- aumento de datos: imágenes movidas al azar;
- un ritmo de aprendizaje que baja;
- guardar y cargar los pesos, y un archivo que `weights_only=True` rechaza;
- elegir con validación y medir una sola vez con la prueba.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-35-pytorch_cnn_entrenamiento_y_transfer_learning/2-practicas/ejercicio-03-entrenar-de-verdad/starter
uv run python main.py
```

```
Ejercicio 03 · Entrenar de verdad
entrenamiento 200 · validación 400 · prueba 1197
```

Los dígitos del ejercicio 02, pero solo **200** para entrenar: con pocas imágenes se nota más lo que hace cada técnica. 400 validan, para elegir, y 1197 son la prueba, para medir una vez al final.

- `network(dropout)` es la CNN del ejercicio 02, con un `nn.Dropout` antes de la última capa (con 0, no apaga nada).
- `shift(batch)` mueve cada imagen al azar hasta un píxel en cada dirección.
- `fit(model, epochs, augment, scheduler)` entrena por lotes de 32, barajados, y escribe el acierto en entrenamiento y en validación cada 20 épocas, con el ritmo de ese momento.

## Pasos

### 1. Lotes, y la distancia entre las dos curvas

Descomenta el **PASO 1** y ejecuta:

```
sin nada:
  época 20: entrenamiento 0.980 · validación 0.887 · ritmo 0.0100
  época 40: entrenamiento 1.000 · validación 0.935 · ritmo 0.0100
  época 60: entrenamiento 1.000 · validación 0.938 · ritmo 0.0100
```

En la época 40 ya acierta **todas** las de entrenamiento, y la validación se queda en 0,938. Esa distancia es lo que la red ha memorizado de sus 200 imágenes y no sirve para otras. A diferencia del ejercicio 04 de la semana 34, la validación no empeora; pero tampoco mejora.

Cada época son 7 pasos (200 / 32, el último con 8 imágenes): en 60 épocas, 420 pasos.

### 2. Dropout

Descomenta el **PASO 2** y ejecuta:

```
en train(), dos veces: [0.21, -0.14, -0.26] [0.17, -0.19, -0.01]
en eval(), dos veces:  [0.02, -0.24, -0.16] [0.02, -0.24, -0.16]
con dropout:
  época 20: entrenamiento 0.935 · validación 0.858 · ritmo 0.0100
  época 40: entrenamiento 0.975 · validación 0.897 · ritmo 0.0100
  época 60: entrenamiento 0.995 · validación 0.905 · ritmo 0.0100
```

- En `train()`, la misma imagen da otras puntuaciones cada vez: el *dropout* apaga la mitad de los 64 números, al azar, en cada llamada. En `eval()`, no apaga nada: siempre igual.
- Entrenada con *dropout*, la distancia es algo menor, pero la validación es **peor**: 0,905 frente a 0,938. Esta red es pequeña (1898 parámetros) y no le sobra nada que apagar. El *dropout* es para redes grandes; aquí, no ayuda. Lo dice la validación, no la intuición.

### 3. Aumento de datos

Descomenta el **PASO 3** y ejecuta:

```
con imágenes movidas:
  época 20: entrenamiento 0.875 · validación 0.840 · ritmo 0.0100
  época 40: entrenamiento 0.960 · validación 0.933 · ritmo 0.0100
  época 60: entrenamiento 0.955 · validación 0.897 · ritmo 0.0100
sin nada · validación movida 0.507
movidas  · validación movida 0.820
```

- En cada lote, `shift` mueve las imágenes de entrenamiento al azar: la red casi nunca ve dos veces la misma. Ya no llega a 1,0 en entrenamiento.
- Con la validación tal cual, sube y baja (0,933 y 0,897): no es mejor que sin nada.
- Con la validación **movida**, cada imagen desplazada al azar como podrían llegar en la realidad: la red sin nada se queda en 0,507; la entrenada con imágenes movidas, 0,820.

Qué red es mejor depende de qué imágenes vas a recibir. Si llegarán movidas, la validación tiene que estar movida también.

### 4. Un ritmo que baja

Descomenta el **PASO 4** y ejecuta:

```
con imágenes movidas y un ritmo que baja:
  época 20: entrenamiento 0.875 · validación 0.840 · ritmo 0.0030
  época 40: entrenamiento 0.955 · validación 0.900 · ritmo 0.0009
  época 60: entrenamiento 0.955 · validación 0.920 · ritmo 0.0003
```

`StepLR(step_size=20, gamma=0.3)` multiplica el ritmo por 0,3 cada 20 épocas. Las primeras 20 épocas son iguales que en el paso 3 (la misma semilla y el mismo ritmo); el ritmo que se escribe es el de la época **siguiente**, ya bajado. Después, con pasos más pequeños, la validación deja de saltar y acaba en 0,920, mejor que el 0,897 del paso 3.

### 5. Guardar y cargar

Descomenta el **PASO 5** y ejecuta:

```
pesos.pt: 10365 bytes · validación 0.920
modelo.pt: Weights only load failed. This file can still be loaded, to ...
```

- `torch.save(scheduled.state_dict(), path)` guarda los pesos: unos 10 KB. `network()` crea una red nueva, con pesos al azar, y `load_state_dict` le pone los guardados: la misma validación, 0,920.
- `torch.save(scheduled, ...)` guarda la red **entera**, con `pickle`. `torch.load(..., weights_only=True)` se niega a cargarla: un archivo `pickle` puede ejecutar código al abrirse (teoría 03, sección 7). El mensaje completo dice cómo cargarlo con `weights_only=False`: hazlo solo con archivos que hayas creado tú.

El paso deja `pesos.pt` y `modelo.pt` en la carpeta `starter/`. Bórralos cuando termines; no los subas a ningún repositorio.

### 6. La prueba, una sola vez

Descomenta el **PASO 6** y ejecuta:

```
sin nada         validación 0.938
dropout          validación 0.905
movidas          validación 0.897
movidas y ritmo  validación 0.920
elegida: sin nada · prueba 0.940
```

Cuatro redes, una elección con validación, y una sola medida con la prueba: 0,940. Ese número dice cuánto acertará la red elegida con dígitos nuevos **como los de validación**. Si miraras la prueba de las cuatro y eligieras la mejor, ese número ya no sería una medida limpia.

Si las imágenes que te van a llegar pueden venir movidas, la elección cambia: valida con imágenes movidas (como en el paso 3) y repite el paso 6.

Para terminar, escribe en un comentario al final de `main.py` qué aumento de datos tendría sentido para las medidas de tu dominio (¿ruido?, ¿otra escala?) y cuál no, porque cambiaría su significado.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| En `eval()` también salen dos resultados distintos en el paso 2 | Falta `dropping.eval()` antes de las dos llamadas |
| El ritmo no baja en el paso 4 | `scheduled` tiene que entrenarse con `scheduler=True` |
| El ritmo baja a casi 0 en pocas épocas | `steps.step()` está dentro del bucle de lotes: va una vez por época |
| `_pickle.UnpicklingError: Weights only load failed` al cargar `pesos.pt` | Guardaste la red entera: `torch.save(scheduled.state_dict(), path)` |
| `RuntimeError: Error(s) in loading state_dict for Sequential` | La red nueva tiene otra forma: créala con `network()`, como la guardada |
| Tus números difieren en el tercer decimal | Otro procesador suma en otro orden: es normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Una CNN](../ejercicio-02-una-cnn/README.md) | **Ejercicio 03 · Entrenar de verdad** | [Ejercicio 04 · Transfer learning](../ejercicio-04-transfer-learning/README.md) |
