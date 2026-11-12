# Ejercicio 01 — De la pregunta a la métrica

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-de-la-exploracion-a-la-pregunta.md) y [02](../../1-teoria/02-hallazgos-defendibles.md)

## Objetivo

Responder "¿qué zona mide más?" con la misma tabla de tres formas distintas, y obtener tres respuestas:

- con la medida como unidad;
- con el sensor como unidad;
- por estación, donde aparece la paradoja de Simpson;
- y escribir al final una pregunta con sus cuatro piezas y su respuesta defendible.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-30-proyecto_de_fase_analisis_de_tu_dominio/2-practicas/ejercicio-01-de-la-pregunta-a-la-metrica/starter
uv run python main.py
```

```
Ejercicio 01 · De la pregunta a la métrica
400 medidas · zonas: ['Norte', 'Sur']
```

El principio de `main.py` genera 400 medidas de dos zonas, con dos sensores cada una. No leas cómo se generan: el ejercicio es descubrirlo con preguntas.

## Pasos

### 1. Cuántas medidas, de dónde

Descomenta el **PASO 1** y ejecuta:

```
sensor   N1  N2  S1   S2
zona                    
Norte   160  40   0    0
Sur       0   0  40  160
estacion  invierno  verano
zona                      
Norte          160      40
Sur             40     160
```

- Cada zona tiene un sensor que mide mucho (160) y otro que mide poco (40).
- El Norte se midió sobre todo en invierno; el Sur, sobre todo en verano. Apúntalo: va a importar.

### 2. La unidad es la medida

Descomenta el **PASO 2** y ejecuta:

```
{'Norte': 18.23, 'Sur': 28.02}
Sur - Norte, por medida: 9.79
```

Con cada medida pesando lo mismo, el Sur mide casi 10 unidades más. Es la respuesta que daría `hallazgos` si comparas zonas con la instantánea entera.

### 3. La unidad es el sensor

Descomenta el **PASO 3** y ejecuta:

```
{('Norte', 'N1'): 14.23, ('Norte', 'N2'): 34.25, ('Sur', 'S1'): 11.11, ('Sur', 'S2'): 32.25}
Sur - Norte, por sensor: -2.56
```

- Primero la media de cada sensor; después, la media de los dos sensores de cada zona. Cada sensor pesa lo mismo, mida 40 o 160 veces.
- Ahora el **Norte** mide más. Misma tabla, misma métrica (la media), otra unidad: otra respuesta.

### 4. Por estación

Descomenta el **PASO 4** y ejecuta:

```
zona      Norte    Sur  Sur - Norte
estacion                           
invierno  14.23  11.11        -3.11
verano    34.25  32.25        -2.00
```

En invierno y en verano, el Norte mide más que el Sur. Con todo junto (paso 2), el Sur mide más. Es la paradoja de Simpson (teoría 02, sección 3): la estación es una variable de confusión. El verano da valores altos, y el Sur se midió sobre todo en verano.

Aquí cada sensor mide en una sola estación, así que la respuesta "por sensor" coincide con la de "por estación". En tus datos no tiene por qué.

### 5. Una pregunta, con su respuesta

Descomenta el **PASO 5** y ejecuta:

```
invierno: Sur - Norte -3.11, IC 95 % [-4.22, -2.01]
verano: Sur - Norte -2.00, IC 95 % [-3.18, -0.82]
```

Con la estación fijada, la diferencia es clara: ningún intervalo cruza el cero, y los dos dicen lo mismo. Un hallazgo defendible: "a igual estación, el Sur mide entre 1 y 4 unidades menos que el Norte".

Para terminar, escribe en un comentario al final de `main.py` la pregunta que responde el paso 5, con sus cuatro piezas (teoría 01, sección 2): población, unidad, métrica y comparación. Y una segunda frase: qué no puede responder (pista: ¿por qué se midió el Sur sobre todo en verano?).

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `KeyError: 'Sur'` en el paso 3 | Descomentaste `by_sensor` sin `per_sensor`: descomenta el paso entero |
| La tabla del paso 4 no tiene la columna `Sur - Norte` | Falta la línea que la calcula, antes del `print` |
| `IndentationError` en el paso 5 | Al descomentar, quita solo `# `: las líneas del `for` conservan sus cuatro espacios |
| Tus números no coinciden con los del README | Cambiaste la semilla (`30`) o el código que genera la tabla |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Cerrar la fase 4](../../1-teoria/05-cerrar-la-fase-4.md) | **Ejercicio 01 · De la pregunta a la métrica** | [Ejercicio 02 · Muchas comparaciones](../ejercicio-02-muchas-comparaciones/README.md) |
