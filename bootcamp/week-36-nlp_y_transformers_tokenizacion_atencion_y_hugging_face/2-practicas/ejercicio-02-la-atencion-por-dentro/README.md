# Ejercicio 02 — La atención por dentro

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-embeddings-y-atencion.md) y [03](../../1-teoria/03-el-transformer.md)

## Objetivo

Calcular la atención a mano, paso a paso, hasta reconocerla dentro de un modelo de verdad:

- vectores de palabras y su parecido;
- la atención con productos escalares y `softmax`;
- consultas, claves y valores, y `scaled_dot_product_attention`;
- las dos máscaras: la del relleno y la del futuro;
- por qué hacen falta las posiciones;
- varias cabezas con `nn.MultiheadAttention`;
- los pesos de atención de un Transformer preentrenado.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/2-practicas/ejercicio-02-la-atencion-por-dentro/starter
uv run python main.py
```

```
Ejercicio 02 · La atención por dentro
5 palabras, vectores de 2 números
```

Cinco palabras con vectores de **2** números hechos a mano: el primero, "cuánto de limpieza"; el segundo, "cuánto de avería". En un modelo real son cientos de números aprendidos, y ninguno tiene un significado tan claro; con dos, puedes seguir cada cuenta.

`show()` escribe una tabla: cada fila es la palabra que mira, cada columna la palabra mirada.

## Pasos

### 1. Palabras parecidas, vectores parecidos

Descomenta el **PASO 1** y ejecuta:

```
            filtro    polvo   sensor responde       no
   filtro     1.00     0.99     0.34     0.20     0.10
    polvo     0.99     1.00     0.45     0.31     0.22
   sensor     0.34     0.45     1.00     0.99     0.97
 responde     0.20     0.31     0.99     1.00     1.00
       no     0.10     0.22     0.97     1.00     1.00
nn.Embedding: (5, 2) · el vector de 'sensor': [-1.96, 0.36]
```

La **similitud coseno** mide si dos vectores apuntan al mismo lado: 1, igual; 0, nada que ver. "filtro" y "polvo" (0,99) son de limpieza; "sensor", "responde" y "no", de avería.

Un **`nn.Embedding`** es esa tabla de vectores, una fila por pieza del vocabulario. Empieza al azar, como cualquier peso, y el entrenamiento la mueve para que las piezas que se usan parecido acaben cerca. Es la primera capa de tu `Encoder` del proyecto.

### 2. La atención a mano

Descomenta el **PASO 2** y ejecuta:

```
            filtro    polvo   sensor responde       no
   filtro     0.28     0.26     0.17     0.16     0.14
    polvo     0.26     0.25     0.17     0.17     0.14
   sensor     0.17     0.18     0.23     0.25     0.17
 responde     0.15     0.16     0.24     0.27     0.17
       no     0.18     0.19     0.21     0.22     0.19
cada fila suma [1.0, 1.0, 1.0, 1.0, 1.0]
'no' antes: tensor([0.00, 0.30]) · después: tensor([0.42, 0.51])
```

Tres operaciones:

1. `X @ X.T`: el producto escalar de cada palabra con todas. Alto si se parecen.
2. `/ math.sqrt(2)`: dividir por la raíz del tamaño del vector, para que con vectores grandes los números no se disparen.
3. `softmax(dim=1)`: cada fila pasa a ser pesos positivos que suman 1.

"filtro" presta más atención a "filtro" y "polvo"; "responde", a "responde" y "sensor". La salida de cada palabra es la **media de todos los vectores con esos pesos**: "no", que solo tenía 0,30 de avería, sale con un poco de todo. Ya no es "no" a secas: es "no" en esta frase. Eso es la atención: cada palabra se mezcla con las demás, más con las que más le importan.

### 3. Consultas, claves y valores

Descomenta el **PASO 3** y ejecuta:

```
q, k, v: (5, 4) · salida: (5, 4)
¿a mano igual que scaled_dot_product_attention? True
```

En el paso 2, cada palabra usaba el mismo vector para buscar, para ser buscada y para dar. Un Transformer usa tres capas lineales:

- la **consulta** (*query*, `q`): qué busca esta palabra;
- la **clave** (*key*, `k`): qué ofrece a las que buscan;
- el **valor** (*value*, `v`): qué da cuando la eligen.

Es la misma cuenta, `softmax(q @ k.T / √4) @ v`, y `F.scaled_dot_product_attention` la hace de una vez (y más rápido). Las tres capas se aprenden: el modelo decide qué buscar.

### 4. No mirar el relleno

Descomenta el **PASO 4** y ejecuta:

```
            filtro    polvo   sensor    [PAD]    [PAD]
   filtro     0.39     0.37     0.24     0.00     0.00
    polvo     0.38     0.36     0.25     0.00     0.00
   sensor     0.30     0.31     0.39     0.00     0.00
lo que reciben las dos de relleno: 0.00
```

Una nota de 3 palabras en un lote de 5: las dos últimas son relleno (ejercicio 01, paso 7). Si se pone `-inf` en sus puntuaciones antes de `softmax`, su peso es exactamente 0 y el resto se reparte entre las de verdad. Es lo que hace `src_key_padding_mask` en tu `Encoder`: sin ella, el resultado de una nota cambiaría según la longitud de la más larga del lote.

### 5. No mirar el futuro

Descomenta el **PASO 5** y ejecuta:

```
            filtro    polvo   sensor responde       no
   filtro     1.00     0.00     0.00     0.00     0.00
    polvo     0.51     0.49     0.00     0.00     0.00
   sensor     0.30     0.31     0.39     0.00     0.00
 responde     0.19     0.20     0.29     0.33     0.00
       no     0.18     0.19     0.21     0.22     0.19
¿igual que is_causal=True? True
```

Un modelo que **escribe** texto (como GPT o Claude) predice la palabra siguiente con las anteriores: no puede mirar las que vienen después. La máscara triangular tapa todo lo que está a la derecha de la diagonal: "filtro" solo se mira a sí misma; "no", a todas. Los modelos que **leen** una frase entera para clasificarla (como BERT, o tu `Encoder`) no usan esta máscara.

### 6. La atención no ve el orden

Descomenta el **PASO 6** y ejecuta:

```
¿mismas salidas, en otro orden? True
posiciones 0 a 4: [[0.0, 1.0], [0.84, 0.54], [0.91, -0.42], [0.14, -0.99], [-0.76, -0.65]]
con posiciones, ¿mismas salidas en otro orden? False
```

Desordenas las cinco palabras y cada una recibe **exactamente lo mismo** que antes: la atención es una media con pesos, y una media no sabe de orden. Para la atención, "no se limpió el filtro, se cambió" y "se limpió el filtro, no se cambió" son lo mismo: el problema del ejercicio 01, paso 3.

La solución es sumar a cada vector uno que dice su **posición**. El artículo original de 2017 usaba senos y cosenos de distintas frecuencias; tu `Encoder` usa otra tabla `nn.Embedding` de posiciones, aprendida, como BERT. Con las posiciones sumadas, desordenar sí cambia el resultado.

### 7. Varias cabezas

Descomenta el **PASO 7** y ejecuta:

```
entrada (3, 5, 16) · salida (3, 5, 16) · pesos (3, 2, 5, 5)
parámetros: 1088 = 4 x 16 x 16 (q, k, v y salida) + 4 x 16
```

**`nn.MultiheadAttention`** hace varias atenciones a la vez (*cabezas*), cada una con su parte del vector: con 16 números y 2 cabezas, cada una trabaja con 8. Una cabeza puede fijarse en qué se hizo y otra en dónde. Al final se juntan y pasan por una capa lineal de salida.

- La entrada y la salida tienen la misma forma: `(lote, piezas, 16)`. Por eso se pueden apilar capas.
- Los pesos: `(lote, cabezas, piezas, piezas)`, una tabla como las de los pasos anteriores por cabeza.
- 1088 parámetros: cuatro matrices de 16 × 16 (consulta, clave, valor y salida) y sus sesgos. Es la parte de atención de tu `Encoder`.

### 8. La atención de un modelo de verdad

Descomenta el **PASO 8** y ejecuta. La primera vez descarga unos 470 MB:

```
12 capas · pesos de cada una: (1, 12, 9, 9)
'▁responde' mira sobre todo a: <s> 0.44, </s> 0.23, ▁sensor 0.08
sin <s> ni </s>: ▁sensor 0.08, . 0.07, ▁no 0.07
```

El modelo multilingüe de los ejercicios 03 y 04: 12 capas, 12 cabezas en cada una, y la frase partida en 9 piezas. `output_attentions=True` devuelve las tablas de pesos (con `attn_implementation="eager"`, la versión que las calcula a la vista).

En la capa 6, `▁responde` pone el **67 %** de su atención en `<s>` y `</s>`, las piezas especiales del principio y el final. Es habitual: cuando una cabeza no tiene nada útil que mirar, aparca la atención ahí (lo llaman *attention sink*). Del resto, lo que más mira es `▁sensor` y `▁no`: quién no responde, y que no lo hace.

No leas demasiado en una sola tabla: son 144 (12 capas × 12 cabezas), y la información viaja de unas a otras. Mirar los pesos de atención ayuda a entender un modelo, pero no lo explica.

Para terminar, cambia la frase del paso 8 por una nota de tu dominio y mira a qué piezas atiende una palabra importante. Anótalo en un comentario al final de `main.py`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tu tabla del paso 1 no coincide en el `nn.Embedding` | Falta `torch.manual_seed(36)` antes de crearlo |
| `False` en el paso 3 | El divisor es `math.sqrt(4)`: el tamaño de `q` y `k`, no el de `X` |
| Las columnas `[PAD]` no son 0 en el paso 4 | `masked_fill` va **antes** de `softmax`, con `float("-inf")` |
| `AttributeError: 'NoneType' object has no attribute ...` en el paso 8 | Falta `attn_implementation="eager"`: la atención rápida no devuelve los pesos |
| `ValueError: '▁responde' is not in list` | La frase del paso 8 cambió: busca la pieza tal como sale en `tokens` |
| El paso 8 tarda la primera vez | Descarga el modelo; las siguientes lo lee de `~/.cache/huggingface` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Del texto a números](../ejercicio-01-del-texto-a-numeros/README.md) | **Ejercicio 02 · La atención por dentro** | [Ejercicio 03 · Modelos preentrenados](../ejercicio-03-modelos-preentrenados/README.md) |
