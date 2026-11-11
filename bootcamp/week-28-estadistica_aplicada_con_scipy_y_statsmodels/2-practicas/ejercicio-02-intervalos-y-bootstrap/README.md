# Ejercicio 02 — Intervalos de confianza y bootstrap

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-estimar-con-incertidumbre.md)

## Objetivo

Ponerle a una media su incertidumbre, y comprobar con simulaciones que el método cumple lo que promete:

- el error estándar y el intervalo t, a mano y con SciPy;
- qué significa "95 %", contando cuántos intervalos aciertan;
- cómo cambia el ancho con los datos y con el nivel;
- el *bootstrap* para la mediana;
- lo que pasa con pocos datos muy asimétricos.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-28-estadistica_aplicada_con_scipy_y_statsmodels/2-practicas/ejercicio-02-intervalos-y-bootstrap/starter
uv run python main.py
```

```
Ejercicio 02 · Intervalos de confianza y bootstrap
25 días: [16.4 20.4 19.3 18.4 20.9 22.8] ...
```

Aquí juegas con ventaja: conoces la población (media 20 °C, desviación 3 °C), porque la generas tú. Eso permite comprobar si los intervalos aciertan. En la vida real, solo tienes los 25 días.

## Pasos

### 1. El error estándar y el intervalo t

Descomenta el **PASO 1** y ejecuta:

```
media 20.07 · desviación 2.96 · error estándar 0.59
t crítico con 24 gl: 2.064 (la normal daría 1.960)
IC 95 % a mano: [18.85, 21.29]
IC 95 % con SciPy: [18.85, 21.29]
```

- El **error estándar** es la desviación entre √n: 2,96 / 5 = 0,59. Mide cuánto variaría la media si repitieras los 25 días.
- `stats.t.ppf(0.975, df=24)` es el valor crítico: deja un 2,5 % en cada cola de una t con 24 grados de libertad. Es algo mayor que el 1,96 de la normal, porque la desviación también es una estimación.
- `ttest_1samp(...).confidence_interval(0.95)` hace lo mismo que tus tres líneas. El `popmean` no cambia el intervalo: solo lo usa para el p-valor.

### 2. Qué significa "95 %"

Descomenta el **PASO 2** y ejecuta:

```
n =   5: con t 95.0 % · con la normal 87.9 %
n =  25: con t 95.2 % · con la normal 94.1 %
n = 100: con t 95.3 % · con la normal 95.2 %
```

- `coverage` saca 10 000 muestras de la población, calcula el intervalo de cada una y cuenta cuántos contienen la media de verdad (20).
- Con t, aciertan el 95 %, sea cual sea n. Eso es lo que significa "95 %": una propiedad del **método**, no de un intervalo concreto (teoría 02, sección 4).
- Con 1,96 (la normal) y 5 datos, el "95 %" es un 88 %. Con 100 datos ya da igual: las dos distribuciones casi coinciden.
- Todo vectorizado (semana 23): `samples` es una matriz de 10 000 × n, y cada operación va por filas con `axis=1`.

### 3. Cuatro veces más datos, la mitad de ancho

Descomenta el **PASO 3** y ejecuta:

```
n =   25: ancho 2.593
n =  100: ancho 1.200
n =  400: ancho 0.573
n = 1600: ancho 0.290
80 %: [19.29, 20.85] · ancho 1.56
95 %: [18.85, 21.29] · ancho 2.44
99 %: [18.42, 21.73] · ancho 3.31
```

- Cada vez que n se multiplica por 4, el ancho se divide más o menos entre 2: el error estándar va con √n. Para un intervalo diez veces más estrecho, cien veces más datos.
- Con los mismos 25 días, más confianza da un intervalo más ancho. No hay intervalo estrecho y seguro a la vez sin más datos.

### 4. Bootstrap: remuestrear tu propia muestra

Descomenta el **PASO 4** y ejecuta:

```
mediana de la muestra: 20.0
percentiles 2,5 y 97,5 de 10 000 medianas: [18.6 21.2]
stats.bootstrap (BCa): [18.60, 21.20] · error estándar 0.71
```

- Para la mediana no hay una fórmula sencilla como la del error estándar. El *bootstrap* la evita: `rng.choice(days, size=(10_000, 25), replace=True)` saca 10 000 muestras de 25 días **de tus propios 25 días**, con reemplazo (un día puede salir varias veces y otro ninguna).
- La mediana de cada una varía como variaría la de muestras nuevas de la población. Sus percentiles 2,5 y 97,5 son el intervalo **percentil**.
- `stats.bootstrap` hace lo mismo con el método BCa, que corrige sesgo y asimetría. Los datos van en una tupla, `(days,)`, y `rng=28` lo hace reproducible.
- La mediana sale 20,0 y su intervalo tiene escalones (18,6, 21,2): con 25 valores redondeados a una décima, la mediana solo puede ser uno de ellos.

### 5. Cuando los datos no son una campana

Descomenta el **PASO 5** y ejecuta. Tarda unos segundos: hace 2000 *bootstraps*.

```
15 esperas: [1.4, 1.9, 2.2, 2.3, 3.4, 3.9, 12.6, 15.0, 18.7, 19.8, 26.8, 39.6, 40.8, 47.2, 122.5]
media 23.87 · t: [6.48, 41.26]
           bootstrap: [13.24, 48.68]
cobertura con 15 esperas · t: 90.6 % · bootstrap: 89.7 %
```

- 15 esperas exponenciales: seis de menos de 4 minutos y una de 122. El intervalo t es simétrico alrededor de la media; el del bootstrap, no: se estira hacia la derecha, donde están las esperas largas.
- `hits` repite el experimento 2000 veces y cuenta los aciertos. **Ninguno** de los dos llega al 95 %. Con 15 datos tan asimétricos, la muestra casi nunca contiene las esperas muy largas que mueven la media, y remuestrearla no puede crearlas.
- El bootstrap es muy útil para estadísticos sin fórmula y muestras razonables. No es un remedio para pocos datos.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'scipy'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| El intervalo a mano no coincide con el de SciPy | Falta `ddof=1` en `days.std`, o `df` no es `n - 1` |
| La cobertura con t del paso 2 sale cerca del 93 % con `n = 5` | Usaste `std()` sin `ddof=1` dentro de `coverage`: la desviación sale más pequeña, y el intervalo también |
| `AxisError: axis is out of bounds for array of dimension 0` en `stats.bootstrap` | Los datos van en una tupla: `(days,)`, no `days` |
| Los intervalos del paso 4 cambian en cada ejecución | Falta `rng=28` en `stats.bootstrap` |
| El paso 5 tarda más de un minuto | Normal en máquinas lentas: son 2000 bootstraps de 999 remuestreos. Baja `repeats` a 500 para probar; los porcentajes cambiarán un poco |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Distribuciones con scipy.stats](../ejercicio-01-distribuciones-con-scipy/README.md) | **Ejercicio 02 · Intervalos de confianza y bootstrap** | [Ejercicio 03 · Pruebas de hipótesis](../ejercicio-03-pruebas-de-hipotesis/README.md) |
