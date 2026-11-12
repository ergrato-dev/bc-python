# Ejercicio 04 — Un informe desde el código

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-el-informe-desde-el-codigo.md)

## Objetivo

Escribir un informe en Markdown con la biblioteca estándar, y vigilar que no se quede viejo:

- una tabla de Markdown con una lista de líneas y `join`;
- una etiqueta con una barra, que rompe la tabla, y cómo escaparla;
- números con formato fijo;
- los mismos datos, los mismos bytes, y lo que lo estropea;
- un "test" que detecta un informe viejo y enseña qué cambió.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega. No necesita ninguna dependencia: solo la biblioteca estándar.

## Antes de empezar

```bash
cd bootcamp/week-30-proyecto_de_fase_analisis_de_tu_dominio/2-practicas/ejercicio-04-un-informe-desde-el-codigo/starter
uv run python main.py
```

```
Ejercicio 04 · Un informe desde el código
```

`FINDINGS` son los hallazgos ya calculados del ejercicio 03, con un p corregido inventado. `cell`, `table` y `report` son una versión pequeña de `render` de tu Observatorio: léelas antes de empezar.

## Pasos

### 1. Una tabla con join

Descomenta el **PASO 1** y ejecuta:

```
| Zona | Diferencia | IC 95 % | p corregido |
|---|---|---|---|
| Norte | 0.16 | [-2.47, 2.79] | 0.903 |
| Sur | 6.82 | [4.15, 9.49] | 3.12e-05 |
| Oeste | 3.89 | [1.07, 6.71] | 0.0142 |
```

Una lista de líneas y `"\n".join`: no hace falta un motor de plantillas. Pega la salida en cualquier archivo `.md` de VS Code y ábrelo con *Open Preview*: es una tabla.

### 2. Una etiqueta con una barra

Descomenta el **PASO 2** y ejecuta:

```
sin escapar: 5 columnas
| Norte\|Este | 1.00 | [0.10, 1.90] | 0.04 |
escapada:    4 columnas
```

Una etiqueta `Norte|Este` (dos zonas juntas, o un error al escribirla) sin escapar parte la fila en cinco columnas, y la tabla se descuadra. `cell()` la escapa como `\|`, y Markdown la muestra como una barra dentro de la celda. Los datos vienen de fuera: tu informe no puede confiar en ellos.

### 3. Números con formato fijo

Descomenta el **PASO 3** y ejecuta:

```
sin formato: 0.30000000000000004 · :.2f: 0.30 · :.3g de 0.0000312: 3.12e-05
```

- Un `float` sin formato enseña sus 17 cifras: 0,1 + 0,2 no es 0,3 exacto en binario.
- `:.2f`, dos decimales: para diferencias e intervalos, en las unidades de tu dominio.
- `:.3g`, tres cifras significativas: para p-valores, que pueden ser 0,9 o 0,00003.

### 4. Los mismos datos, los mismos bytes

Descomenta el **PASO 4** y ejecuta:

```
dos veces: 32be37977814 32be37977814
con la hora: 12b3739accb4 b2585868e4b5
```

El mismo informe, escrito dos veces, da la misma huella. Con una línea "Generado el ..." cada escritura es distinta, aunque los datos no cambien: cada `git diff` mostraría un cambio. Tus dos huellas "con la hora" serán otras.

### 5. ¿El informe está al día?

Descomenta el **PASO 5** y ejecuta:

```
al día: True
al día tras cambiar un p: False
--- guardado
+++ nuevo
@@ -1,9 +1,9 @@
 # Hallazgos: cada zona frente a Centro
 
-Difieren 2 de 3 zonas.
+Difieren 1 de 3 zonas.
 
 | Zona | Diferencia | IC 95 % | p corregido |
 |---|---|---|---|
 | Norte | 0.16 | [-2.47, 2.79] | 0.903 |
 | Sur | 6.82 | [4.15, 9.49] | 3.12e-05 |
-| Oeste | 3.89 | [1.07, 6.71] | 0.0142 |
+| Oeste | 3.89 | [1.07, 6.71] | 0.0712 |
```

- Es lo que hace `test_report_is_up_to_date` en tu Observatorio: generar de nuevo y comparar con el archivo guardado.
- Cambia un número de los datos y el informe guardado ya no está al día. `difflib.unified_diff` enseña qué cambió, como `git diff`: el p del Oeste, y con él el resumen. Un solo dato cambia dos líneas del informe; copiadas a mano, es fácil corregir una y olvidar la otra.

Para terminar, añade una columna `d` a `table()` con el tamaño del efecto, con dos decimales, y un valor en cada hallazgo de `FINDINGS`. Ejecuta: el paso 5 sigue diciendo `True` en la primera línea, porque guardado y nuevo se generan con el mismo código.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| La tabla no se ve como tabla en la vista previa | Falta la línea `\|---\|---\|...` debajo de la cabecera, o tiene otro número de columnas |
| `KeyError: 'd'` al añadir la columna | Añadiste `d` a `table()` pero no a todos los hallazgos de `FINDINGS` |
| En el paso 4, las huellas "dos veces" son distintas | Añadiste algo que cambia en cada ejecución, como la hora, a `report()` |
| El paso 5 dice `False` en la primera línea | Descomentaste la línea que cambia el p antes de la que guarda el informe |
| `UnicodeEncodeError` al escribir | Falta `encoding="utf-8"` en `write_text` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Un gráfico por afirmación](../ejercicio-03-un-grafico-por-afirmacion/README.md) | **Ejercicio 04 · Un informe desde el código** | [Proyecto](../../3-proyecto/README.md) |
