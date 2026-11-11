# 05 · Estadística en un proyecto

⏱️ 50 min

## 🎯 Objetivos

- Repartir el código estadístico entre `core` y la CLI, sin que la CLI cargue SciPy al arrancar.
- Decidir qué hace el código cuando una prueba no tiene sentido, en lugar de escribir un número sin sentido.
- Probar código estadístico con valores calculados a mano y con propiedades.
- Darle tipos a SciPy para mypy.
- Medir lo que cuesta SciPy, y decidir por qué statsmodels no entra en el proyecto.

---

## 1. Dónde vive cada pieza

| Archivo | Qué sabe hacer | Qué importa |
|---|---|---|
| `core/arrays.py` (semana 23) | `values_array` y `labels_array`: la serie como arrays de NumPy | NumPy |
| `core/inference.py` | `sample` saca los valores de una etiqueta; `difference` compara dos muestras y devuelve un `Comparison` | NumPy, `scipy.stats` |
| `cli.py` | `comparar RUTA ETIQUETA OTRA [--confianza]` lee el archivo, compara y escribe el informe | SciPy **solo** dentro de `comparar` |

`inference.py` reutiliza `values_array` y `labels_array`: no hace falta pandas para sacar los valores de una etiqueta, y `comparar` no lo carga. Sigue la regla de `charts.py`: no se reexporta en `core/__init__.py`, y `test_importing_the_cli_does_not_load_scipy` lo vigila en otro proceso.

`difference` no sabe de archivos ni de etiquetas: recibe dos arrays y un nivel de confianza. Se prueba con arrays escritos a mano, y la API podría usarla mañana.

---

## 2. Qué devuelve `difference`

```python
@dataclass(frozen=True)
class Comparison:
    sizes: tuple[int, int]
    means: tuple[float, float]
    stds: tuple[float, float]
    difference: float
    low: float
    high: float
    effect: float
    p_welch: float
    p_ranks: float
```

Todo lo que pide un informe honrado (teoría 03, sección 9): los tamaños, las medias y desviaciones, la diferencia con su intervalo, el tamaño del efecto y dos p-valores. Cada decisión tiene su razón:

| Decisión | Por qué |
|---|---|
| `std(ddof=1)` | Estimas la dispersión de todas las medidas posibles, no describes estas (teoría 02) |
| `ttest_ind(..., equal_var=False)` | Welch: no supone que las dos etiquetas tengan la misma dispersión. El valor por defecto de SciPy es Student |
| `welch.confidence_interval(confidence)` | El intervalo de la diferencia, coherente con el p-valor de Welch |
| `effect = diferencia / sqrt((s₁² + s₂²) / 2)` | La d de Cohen con la media de las dos varianzas: comparable entre dominios |
| `mannwhitneyu` además de Welch | Si un valor extremo mueve a Welch, Mann-Whitney lo dice (teoría 03, sección 6) |
| Sin veredicto "significativo" | Un sí o un no esconde el intervalo y el tamaño del efecto. El informe da los números; tú decides |

---

## 3. Cuándo no hay nada que calcular

```python
if first.size < 2 or second.size < 2:
    raise ValueError(...)
if first.min() == first.max() or second.min() == second.max():
    raise ValueError("las dos muestras tienen que variar: una tiene todos sus valores iguales")
```

Sin estas dos comprobaciones, SciPy **no falla**:

| Caso | Lo que haría SciPy | Lo que hace `difference` |
|---|---|---|
| Una muestra con 1 valor | `nan` en t, en p y en el intervalo, sin aviso | `ValueError: cada muestra necesita al menos 2 valores (tienen 3 y 1)` |
| Una etiqueta que no está | `nan` en todo, con un `SmallSampleWarning` | El mismo error, `tienen 3 y 0` |
| Un sensor atascado (todos iguales) | `RuntimeWarning: Precision loss occurred in moment calculation...`, y números que no significan nada | `ValueError: las dos muestras tienen que variar...` |

Un `nan` que llega hasta la pantalla del usuario como `p (Welch): nan` es peor que un error claro. `comparar` convierte el `ValueError` en código 2 y en un mensaje que dice qué etiquetas y por qué.

¿Por qué `min() == max()` y no `std() == 0`? Por el redondeo: la desviación de `[0.1, 0.1, 0.1]` sale `1.4e-17`, no 0, y la comprobación no lo vería. `min() == max()` es exacto. Uno de los tests lo vigila con esos tres valores.

---

## 4. Probar estadística

Un contraste mal hecho no falla: escribe un p-valor con buena cara. Usar Student en lugar de Welch cambia p de 0,037 a 0,030; usar `ddof=0` cambia la desviación de 1,58 a 1,41. Ningún test del tipo "p está entre 0 y 1" lo ve. Hacen falta tres clases de tests.

**Valores calculados a mano.** Muestras pequeñas cuyo resultado sale con papel y lápiz:

```python
LOW = floats(1, 2, 3, 4, 5)    # media 3, desviación sqrt(2,5)
HIGH = floats(6, 7, 8, 9, 10)  # media 8, desviación sqrt(2,5)
# Error estándar sqrt(2,5/5 + 2,5/5) = 1, t = -5 con 8 grados de libertad.
```

- El intervalo es -5 ± `t.ppf(0.975, 8)` = -5 ± 2,306.
- La d de Cohen es -5 / 1,581 = -3,162.
- El p de Mann-Whitney es exacto: todos los de `LOW` están por debajo de todos los de `HIGH`, y solo 2 de los 252 repartos posibles de 10 rangos en dos grupos de 5 son así de extremos: 2/252.

**Valores que distinguen las alternativas.** Con `LOW` y `HIGH`, Welch y Student coinciden (mismo tamaño, misma dispersión). `test_difference_does_not_assume_equal_spreads` usa dos muestras de dispersiones muy distintas, donde solo Welch da 0,0372. Cada test existe para matar un error concreto: comprueba con mutantes que lo hace (paso 10 del proyecto).

**Propiedades, con Hypothesis.** Se cumplen con cualquier par de muestras:

- el intervalo contiene la diferencia, y los p-valores están entre 0 y 1;
- intercambiar las muestras solo cambia el signo de la diferencia, del intervalo y del efecto, no los p-valores;
- sumar la misma constante a todas las medidas (otro cero de la escala) no cambia ni la diferencia ni los p-valores.

Los valores que genera Hypothesis son **décimas** entre -1000 y 1000, y no cualquier `float`: con valores como `1e-300` y `0`, SciPy pierde precisión y avisa, y el test fallaría por la aritmética, no por tu código. Elegir bien el dominio de los datos es parte del test.

---

## 5. Tipos para SciPy

SciPy no trae anotaciones de tipos. Con `mypy --strict`, cada llamada a `stats` sería `Any`, y mypy se quejaría de devolverlas. El paquete `scipy-stubs` (con su dependencia `optype`) las añade, y va en el grupo `dev`: solo lo necesita mypy, no la imagen.

Un detalle de NumPy: indexar un array con una máscara de booleanos devuelve `Any` para mypy. Por eso `sample` anota la variable:

```python
chosen: Floats = values[(labels_array(series) == label) & ~np.isnan(values)]
return chosen
```

---

## 6. Lo que cuesta

```
week-27   986 MB
week-28   1.18 GB
```

La imagen `runtime` crece unos 190 MB por una sola dependencia:

| Paquete | En disco | Qué es |
|---|---|---|
| `scipy` | 110 MB | Estadística, optimización, álgebra lineal, funciones especiales... Unos 33 MB son sus propios tests |
| `scipy.libs` | 30 MB | OpenBLAS (álgebra lineal) y las bibliotecas de Fortran con las que se compila |

`docker history local/observatorio:week-28` atribuye 146 MB más a la capa de `/opt/venv`: esas dos carpetas. A diferencia de matplotlib (semana 27), SciPy no necesita nada en el `Dockerfile`: no escribe cachés ni busca fuentes.

Importar `scipy.stats` cuesta unos 0,4 s en tu máquina, y más de un segundo la primera vez en un contenedor recién arrancado. Por eso, como `charts`, se importa dentro de `comparar`.

### ¿Y statsmodels?

| | Lo que daría al proyecto | Lo que costaría |
|---|---|---|
| statsmodels | Nada que `comparar` necesite: Welch, Mann-Whitney y el intervalo están en SciPy | 43 MB más, con patsy y formulaic, y otro `import` de casi un segundo |

Si mañana tu Observatorio necesita una regresión con categorías o predicciones con su intervalo (teoría 04), entonces statsmodels se gana su sitio. Hoy no.

---

## 7. Medir

Con las 100 000 medidas de `generar_medidas.py`:

| Comando | Tiempo |
|---|---|
| `resumir` | 0,95 s |
| `comparar ... Norte Sur` | 1,3-1,5 s |

Casi todo es leer el texto, como siempre. SciPy añade su `import`; las pruebas con 19 000 valores por etiqueta tardan milisegundos (Mann-Whitney usa una aproximación normal cuando hay tantos datos).

```
Norte: 18898 medidas, media 40.26, desviación 23.25
Sur: 19206 medidas, media 39.95, desviación 23.08
diferencia Norte - Sur: 0.32, IC 95 %: [-0.15, 0.78]
tamaño del efecto (d de Cohen): 0.01
p (Welch): 0.184 · p (Mann-Whitney): 0.184
```

`generar_medidas.py` saca todos los valores de la misma distribución, sea cual sea la etiqueta. Y eso es lo que dice el informe: el intervalo contiene el 0 y es estrecho (±0,47 °C con tantos datos); el efecto es diminuto. Con datos al azar, `comparar` no se inventa una diferencia. Con los de tu dominio, ¿la hay?

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Dejar que SciPy devuelva `nan` | El usuario ve `p: nan` sin saber por qué | Comprobar antes y lanzar `ValueError` con el motivo |
| `std() == 0` para detectar una muestra constante | El redondeo deja 1e-17 | `min() == max()` |
| Tests que solo miran que p esté entre 0 y 1 | Student, `ddof=0` o la dirección de la resta pasan | Valores calculados a mano, que distingan las alternativas |
| Hypothesis con cualquier `float` | SciPy pierde precisión y el test falla por la aritmética | Un dominio realista: décimas, rangos acotados |
| Importar `scipy.stats` al principio de `cli.py` | Todos los comandos pagan su `import` | Dentro de `comparar` |
| Escribir "significativo" en el informe | Esconde cuánto y cuán seguro | Diferencia, intervalo, efecto y p |
| Añadir statsmodels "por si acaso" | 43 MB y un `import` lento sin usarlo | Cuando haga falta un modelo |

---

## ✅ Qué debes saber al terminar

- [ ] Qué hace `difference`, y por qué cada una de sus decisiones.
- [ ] Qué haría SciPy sin las dos comprobaciones, y por qué es peor.
- [ ] Qué tres clases de tests tiene `test_inference.py`, y qué mata cada una.
- [ ] Para qué sirve `scipy-stubs`, y por qué va en `dev`.
- [ ] Cuánto crece la imagen, y por qué statsmodels no entra.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Regresión con statsmodels](04-regresion-con-statsmodels.md) | **05 · Estadística en un proyecto** | [Ejercicio 01 · Distribuciones con scipy.stats](../2-practicas/ejercicio-01-distribuciones-con-scipy/README.md) |
