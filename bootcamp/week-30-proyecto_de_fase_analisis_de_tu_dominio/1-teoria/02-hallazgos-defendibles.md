# 02 · Hallazgos defendibles

⏱️ 50 min

## 🎯 Objetivos

- Escribir un hallazgo con su tamaño y su incertidumbre, no solo con un p-valor.
- Distinguir una diferencia significativa de una importante, y "no significativa" de "no hay diferencia".
- Reconocer la paradoja de Simpson y las variables de confusión.
- Comprobar que una conclusión no depende de una sola decisión del análisis.

---

## 1. Qué es un hallazgo defendible

Un hallazgo es una frase que alguien puede usar para decidir. Es **defendible** si resiste tres preguntas de quien lo lee: ¿cuánto?, ¿seguro? y ¿seguro que es por eso?

| Frase | Problema |
|---|---|
| "El Sur mide más que el Norte" | ¿Cuánto más? ¿Puede ser azar? |
| "El Sur mide más que el Norte (p = 0,003)" | El p no dice cuánto: puede ser 0,1 unidades |
| "El Sur mide 4,2 unidades más que el Norte, entre 2,1 y 6,3 con un 95 % de confianza; d = 0,45" | Defendible: tamaño, incertidumbre y escala |

La semana 28 te dio las piezas, en `inference.difference`: la diferencia, su intervalo (Welch), el tamaño del efecto (d de Cohen) y dos p-valores. Esta semana las usas para **escribir**.

## 2. Significativo no es importante

Un p-valor pequeño dice que la diferencia probablemente no es cero. No dice que sea grande. Con suficientes medidas, cualquier diferencia minúscula sale significativa:

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(30)
for size, shift in [(20_000, 0.3), (8, 8.0)]:
    north = rng.normal(50, 10, size)
    south = rng.normal(50 + shift, 10, size)
    welch = stats.ttest_ind(south, north, equal_var=False)
    interval = welch.confidence_interval(0.95)
    effect = (south.mean() - north.mean()) / np.sqrt((south.var(ddof=1) + north.var(ddof=1)) / 2)
    print(f"n={size}: diferencia {south.mean() - north.mean():.2f},"
          f" IC [{interval.low:.2f}, {interval.high:.2f}], d {effect:.2f}, p {welch.pvalue:.2g}")
```

```
n=20000: diferencia 0.36, IC [0.17, 0.56], d 0.04, p 0.00026
n=8: diferencia 3.20, IC [-10.10, 16.49], d 0.26, p 0.61
```

- Con 20 000 medidas por zona, una diferencia de 0,36 unidades en una escala con desviación 10 es "muy significativa" (p = 0,00026). Su d, 0,04, dice que es cinco veces menor que un efecto pequeño (0,2). Probablemente no importa a nadie.
- Con 8 medidas, la diferencia de verdad es de 8 unidades, pero el intervalo va de −10 a 16: los datos no pueden distinguirla del cero. **No significativa no es "no hay diferencia"**: es "con estos datos, no se puede saber".

Por eso el informe de `hallazgos` escribe siempre el intervalo y la d, no solo el p. Y por eso, al leerlo, empiezas por el intervalo:

| El intervalo... | Se lee |
|---|---|
| no cruza el cero, y es estrecho | Hay diferencia, y se sabe cuánta |
| no cruza el cero, pero es ancho | Hay diferencia; su tamaño, poco preciso |
| cruza el cero, y es estrecho | Si hay diferencia, es pequeña |
| cruza el cero, y es ancho | No se sabe: hacen falta más datos |

## 3. La paradoja de Simpson

Dos zonas, medidas en invierno (valores bajos) y en verano (valores altos). El Norte se midió sobre todo en invierno; el Sur, sobre todo en verano:

| | Norte | Sur |
|---|---|---|
| Invierno | 80 medidas, media 12 | 20 medidas, media 10 |
| Verano | 20 medidas, media 32 | 80 medidas, media 30 |
| **Todas** | **100 medidas, media 16** | **100 medidas, media 26** |

En cada estación, el Norte mide **más** que el Sur (12 frente a 10; 32 frente a 30). Con todo junto, mide **menos** (16 frente a 26). Las dos tablas son correctas. La de "todas" mezcla zona y estación: la estación es una **variable de confusión**, algo que influye en el valor y que está repartido de forma distinta entre los grupos que comparas.

`hallazgos` compara etiquetas con todo lo demás mezclado. Antes de escribir "el Sur mide más", pregúntate qué más es distinto entre el Sur y el Norte en tus datos: la hora, el día, el sensor, la carga. Lo que no puedas descartar va en **Limitaciones**.

## 4. Correlación no es causa

Aunque la diferencia sea real y grande, el informe no dice **por qué**. "El Sur mide más" no es "estar en el Sur hace medir más": puede que los sensores del Sur sean de otro modelo, o que estén más cerca de una carretera. Para hablar de causas hace falta un experimento (cambiar una sola cosa y ver qué pasa) o un análisis causal, que este bootcamp no cubre.

En tu informe, escribe lo que los datos muestran ("difiere") y deja las causas como hipótesis, en **Siguientes pasos**.

## 5. Robustez: ¿depende de una decisión?

Un hallazgo es **robusto** si no cambia al cambiar una decisión razonable del análisis. Tu Observatorio comprueba una gratis: junto al p de Welch, que compara medias y supone algo parecido a una campana, el informe escribe el de **Mann-Whitney**, que compara rangos y no supone ninguna forma.

| Welch | Mann-Whitney | Se lee |
|---|---|---|
| pequeño | pequeño | Robusto: no depende de la forma |
| pequeño | grande | Lo empujan pocos valores extremos: míralos (teoría 01 de la semana 29) |
| grande | pequeño | Las formas difieren más que las medias: mira los histogramas |
| grande | grande | Sin diferencia que mostrar |

Otras comprobaciones que puedes hacer en tu notebook, y contar en el informe: repetir con otra carga, sin los atípicos de Tukey, o con la mediana. Si el hallazgo aguanta, dilo: "se mantiene sin los 12 atípicos".

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| Publicar solo el p-valor | Una diferencia de 0,1 unidades parece un hallazgo | Diferencia, intervalo y d |
| "No significativa, así que son iguales" | Se descarta una diferencia que no se pudo medir | "No se puede saber con estos datos" |
| Comparar grupos con todo mezclado sin pensar | Paradoja de Simpson | Buscar qué más difiere entre los grupos |
| "Difiere, porque..." | Una causa que nadie comprobó | La causa como hipótesis |
| Un solo análisis | Un hallazgo que depende de una decisión | Welch y Mann-Whitney; otra carga |

## ✅ Qué debes saber al terminar

- Qué tres preguntas resiste un hallazgo defendible, y cómo las responde el informe.
- Por qué con muchas medidas todo es significativo, y con pocas casi nada.
- Cómo se lee un intervalo según cruce o no el cero, y su anchura.
- Qué es la paradoja de Simpson y qué es una variable de confusión.
- Para qué escribe el informe el p de Mann-Whitney junto al de Welch.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · De la exploración a la pregunta](01-de-la-exploracion-a-la-pregunta.md) | **02 · Hallazgos defendibles** | [03 · Muchas comparaciones](03-muchas-comparaciones.md) |
