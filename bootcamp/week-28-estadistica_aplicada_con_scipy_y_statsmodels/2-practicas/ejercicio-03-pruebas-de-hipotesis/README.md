# Ejercicio 03 — Pruebas de hipótesis

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-pruebas-de-hipotesis.md)

## Objetivo

Comparar dos estaciones con las pruebas que usará tu proyecto, y ver dónde engaña un p-valor:

- Welch y Student, y el intervalo de la diferencia;
- el p-valor calculado barajando etiquetas;
- una medida extrema frente a Welch y Mann-Whitney;
- chi cuadrado para variables con categorías;
- muchas pruebas a la vez, la potencia y "significativo" frente a "importante".

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-28-estadistica_aplicada_con_scipy_y_statsmodels/2-practicas/ejercicio-03-pruebas-de-hipotesis/starter
uv run python main.py
```

```
Ejercicio 03 · Pruebas de hipótesis
Norte: media 20.14, desviación 1.89
Sur:   media 21.52, desviación 4.03
```

Veinte días de cada estación. Tú sabes algo que en la vida real no sabrías: el Sur mide **de verdad** 1,5 °C más que el Norte, y es el doble de variable. Ten eso en mente en cada paso.

## Pasos

### 1. Welch y Student

Descomenta el **PASO 1** y ejecuta:

```
Welch:   t = 1.386, gl = 26.9, p = 0.1771
Student: t = 1.386, gl = 38.0, p = 0.1738
Sur - Norte: 1.38, IC 95 %: [-0.66, 3.42]
¿cero dentro del intervalo? True · ¿p < 0,05? False
```

- Las dos pruebas dan el mismo t porque los grupos tienen el mismo tamaño; cambian los grados de libertad. Student supone la misma dispersión (38 = 20 + 20 − 2); Welch no, y los ajusta a 26,9 porque el Sur varía el doble.
- p = 0,18: no puedes distinguir la diferencia del azar... aunque existe. Es un **error de tipo II**. El paso 5 explica por qué pasa.
- El 0 está dentro del intervalo y p ≥ 0,05: las dos cosas van siempre juntas. Pero el intervalo dice más: la diferencia de verdad puede estar entre −0,66 y 3,42 °C. El 1,5 real está dentro.

### 2. El p-valor, por simulación

Descomenta el **PASO 2** y ejecuta:

```
diferencia observada: 1.38
repartos al azar con una diferencia igual o mayor: 0.1714
p de la permutación: 0.1698 · p de Welch: 0.1771
```

- Si las estaciones no se distinguieran, las etiquetas "Sur" y "Norte" serían intercambiables. `permutation_test` reparte los 40 valores al azar en dos grupos de 20, 20 000 veces, y calcula la diferencia de medias de cada reparto.
- `null_distribution` guarda esas 20 000 diferencias. En el 17 % de ellas, la diferencia es tan grande como la observada: eso es el p-valor, sin ninguna fórmula.
- SciPy cuenta cada cola por separado y añade el reparto observado, por eso su p (0,1698) difiere en la tercera cifra del recuento directo. Y Welch llega a casi lo mismo con su fórmula.
- `vectorized=True` le dice a SciPy que `mean_difference` acepta muchas muestras a la vez con `axis`: mucho más rápido.

### 3. Una medida extrema: Welch y Mann-Whitney

Descomenta el **PASO 3** y ejecuta:

```
sin el extremo: media Norte 20.14 · p Welch 0.1771 · p Mann-Whitney 0.1166
con el extremo: media Norte 24.01 · p Welch 0.5263 · p Mann-Whitney 0.2673
```

- Un solo día a 95 °C sube la media del Norte casi 4 °C, y ahora el Norte parece **más** caliente que el Sur. El p de Welch se triplica.
- Mann-Whitney compara rangos: para ella, 95 °C es solo el valor más alto. Su p también sube (ese día pasa de los más bajos al primero), pero bastante menos.
- Cuando Welch y Mann-Whitney dicen cosas muy distintas, mira los datos antes de creerte a ninguna. Tu proyecto escribe las dos por eso.

### 4. Variables con categorías: chi cuadrado

Descomenta el **PASO 4** y ejecuta:

```
chi² = 8.23, gl = 2, p = 0.0163
lo esperado si el nivel no dependiera de la estación:
[[43.5 30.5 16. ]
 [43.5 30.5 16. ]]
```

- La tabla cuenta días de nivel bajo, medio y alto de cada estación. La pregunta: ¿el nivel depende de la estación?
- `expected_freq` es lo que verías si no dependiera: cada estación con los totales repartidos igual. El Sur tiene 22 días altos frente a 16 esperados; el Norte, 10.
- `gl = 2`: (filas − 1) × (columnas − 1). p = 0,016: una tabla así sería rara si el nivel no dependiera de la estación.
- Funciona con **conteos**, no con porcentajes, y pide que lo esperado en cada casilla no baje de 5.

### 5. Muchas pruebas, potencia y tamaño del efecto

Descomenta el **PASO 5** y ejecuta:

```
con p < 0,05 sin ninguna diferencia real: 5 de 100
tras Bonferroni (p < 0,05 / 100): 0
tras Benjamini-Hochberg: 0
potencia con  10 por grupo y 1,5 °C de diferencia: 18 %
potencia con  30 por grupo y 1,5 °C de diferencia: 50 %
potencia con 100 por grupo y 1,5 °C de diferencia: 94 %
200 000 por grupo y 0,05 °C: p = 1.2e-10, d de Cohen = 0.020
```

- **Muchas pruebas**: 100 comparaciones entre grupos sin ninguna diferencia, y 5 salen con p < 0,05. Si comparas todo con todo, siempre "encuentras" algo. Bonferroni (dividir α entre el número de pruebas) y Benjamini-Hochberg (`false_discovery_control`) lo corrigen.
- **Potencia**: `power` repite 2000 experimentos con una diferencia real de 1,5 °C y cuenta cuántos la detectan. Con 10 días por estación, menos de uno de cada cinco. Por eso el paso 1 no la vio: con 20 días y el Sur tan variable, la potencia ronda el 31 %.
- `ttest_ind(first, second, axis=1)` hace las 2000 pruebas de una vez, una por fila.
- **Significativo no es importante**: con 200 000 medidas por grupo, una diferencia de 0,05 °C da p = 0,0000000001. La d de Cohen (0,02) dice que es diminuta. Da siempre el tamaño del efecto.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'scipy'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| Welch y Student dan los mismos grados de libertad | Falta `equal_var=False` en la de Welch: SciPy usa Student por defecto |
| El paso 2 tarda mucho | Falta `vectorized=True`: SciPy llama a la función 20 000 veces en lugar de una |
| `TypeError: mean_difference() got an unexpected keyword argument 'axis'` | `vectorized=True` necesita que la función acepte `axis` |
| La tabla esperada del paso 4 tiene decimales distintos | Pasaste porcentajes en lugar de conteos |
| Tus números de los pasos 3 a 5 no coinciden | Cambiaste el orden de los pasos o volviste a crear `rng`: cada uno sigue la secuencia del anterior |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Intervalos de confianza y bootstrap](../ejercicio-02-intervalos-y-bootstrap/README.md) | **Ejercicio 03 · Pruebas de hipótesis** | [Ejercicio 04 · Regresión con statsmodels](../ejercicio-04-regresion-con-statsmodels/README.md) |
