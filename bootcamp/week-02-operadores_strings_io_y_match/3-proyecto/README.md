# Proyecto — Observatorio, capa 1: reglas y línea de comandos

⏱️ 5 h 30 min · Capa 1 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Sobre la capa 0 (leer, validar y mostrar una medida), añades las **reglas de tu dominio** y una forma de usar el Observatorio desde la terminal. Cada medida recibe un nivel según dos umbrales (`bajo`, `medio`, `alto` o `sin dato`), una línea de texto `etiqueta;valor` se convierte en una fila de columnas alineadas, y el programa `observatorio` la lee por argumento o por teclado y termina con el código de salida correcto.

| Función | Archivo | Recibe | Devuelve |
|---|---|---|---|
| `classify(12.5, 10.0, 50.0)` | `rules.py` | Valor y umbrales | `"medio"` |
| `format_row("Norte", 12.54, "µg/m³", "medio")` | `rules.py` | Etiqueta, valor, unidad y nivel | `"Norte               12.5 µg/m³ \| medio"` |
| `parse_line("Norte;12,5", "µg/m³", 10.0, 50.0)` | `rules.py` | Una línea y las reglas | La fila, o `None` si la línea es inválida |
| `main(["Norte;12,5"])` | `__main__.py` | Los argumentos | El código de salida: `0`, `1` o `2` |

En la semana 3 el programa leerá muchas líneas seguidas con un bucle; en la 7, un CSV entero. Las dos usarán `parse_line` tal como la escribas hoy.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-02`. El `starter/` contiene la capa 0 resuelta (`record.py`) para que funcione solo; **tú usas la tuya** y copias únicamente los archivos nuevos.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-01` está fusionado en `main` en GitHub. Después, en tu repositorio:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-02
```

### 2. Copia los archivos nuevos

Desde tu repositorio, con la ruta del bootcamp en una variable para no repetirla:

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-02-operadores_strings_io_y_match/3-proyecto/starter
cp $STARTER/src/observatorio/rules.py src/observatorio/
cp $STARTER/src/observatorio/__main__.py src/observatorio/
cp $STARTER/tests/test_rules.py $STARTER/tests/test_main.py $STARTER/tests/test_my_rules.py tests/
sed -i 's/week-01/week-02/' compose.yaml
git status --short
```

`git status` debe mostrar `__main__.py` y `compose.yaml` modificados y los otros cuatro archivos nuevos. Tu `record.py` y tus tests de la semana 1 no se tocan. El `__main__.py` nuevo sustituye al de la semana 1: tus tres registros de ejemplo ya no hacen falta, porque ahora el programa lee la línea que le pases.

### 3. Tests en rojo

```bash
uv run pytest
```

Salida esperada: `24 failed` y, en verde, los tests de la semana 1 (los 12 de `test_record.py` más los tuyos de `test_my_domain.py`). Fallan los de `test_rules.py`, `test_main.py` y el de ejemplo de `test_my_rules.py`, todos con `NotImplementedError`.

Dos cosas nuevas en los tests, que no necesitas escribir pero sí leer:

| En el test | Qué hace |
|---|---|
| `@pytest.mark.parametrize(...)` | Ejecuta el mismo test con varios valores; cada valor cuenta como un test |
| `capsys` | Captura lo que el programa escribió: `capsys.readouterr().out` es stdout y `.err` es stderr |
| `monkeypatch.setattr("builtins.input", ...)` | Sustituye `input()` por una función que devuelve un texto fijo, para probar sin teclado |

### 4. Tus umbrales y `classify`

Decide la unidad y los dos umbrales de tu dominio (por ejemplo, PM2.5: por debajo de 12 µg/m³ "bajo", desde 35 "alto"). Escríbelos en `src/observatorio/__main__.py` (`UNIT`, `LOW`, `HIGH`) y anótalos con su justificación en el `README.md` de tu repositorio.

Implementa `classify` en `src/observatorio/rules.py`: un `if`/`elif`/`else` de cuatro ramas (teoría 02). Empieza por `None`, después los rangos de menor a mayor.

```bash
uv run pytest -k classify
```

Esperado: `7 passed`. Fíjate en `0.0`: es `"bajo"`, no `"sin dato"`. Si te sale `"sin dato"`, usaste `not value` en lugar de `value is None`.

### 5. `format_row`

Dos pasos: primero el texto del valor (`"sin dato"` si `value is None`; si no, `f"{value:.1f} {unit}"`, con una expresión condicional), después la f-string con anchos `<16` y `>14` (teoría 04).

```bash
uv run pytest -k format_row
```

Esperado: `3 passed`. Si falla, pytest muestra las dos filas una encima de otra con `+` y `-`: cuenta los espacios.

### 6. `parse_line`

Usa `match` sobre `line.split(";")` (teoría 02):

- Un `case` con dos capturas, `[label, text]`, y una guarda que exija que la etiqueta no quede vacía después de `strip()`.
- Dentro: convierte `text` con tu `parse_value` de la semana 1, clasifica y devuelve `format_row(...)` con la etiqueta limpia.
- `case _:` devuelve `None`.

```bash
uv run pytest -k parse_line
```

Esperado: `7 passed`. Las líneas inválidas que prueba el test son `"Norte 12,5"` (sin `;`), `"Norte;12;5"` (dos `;`), `";12,5"` y `"   ;8"` (etiqueta vacía) y `""`.

### 7. `main`

La docstring de `main` describe los cuatro casos; es el mismo esqueleto del ejercicio 04:

1. `args = sys.argv[1:] if argv is None else argv`.
2. `match args:` con cuatro `case`: `[]` (lee con `input`), `["-h" | "--ayuda"]`, `[line]` y `_`. El de la ayuda va **antes** que `[line]`: si no, `"--ayuda"` se capturaría como línea.
3. `parse_line(line, UNIT, LOW, HIGH)`; si da `None`, mensaje a stderr y `return 1`; si no, `print` y `return 0`.

Para el mensaje de error usa `{line!r}`: muestra la línea entre comillas, y así se ven los espacios.

```bash
uv run pytest tests/test_main.py
```

Esperado: `6 passed`.

### 8. Pruébalo en la terminal

Con datos de tu dominio:

```bash
uv run observatorio "Norte;12,5"; echo "código: $?"
uv run observatorio "Norte 12,5"; echo "código: $?"
uv run observatorio Norte 12,5; echo "código: $?"
uv run observatorio --ayuda
echo "Sur;NA" | uv run observatorio
```

Ejemplo con los umbrales de partida (`unidad`, 10 y 50):

```
Norte              12.5 unidad | medio
código: 0
error: línea inválida: 'Norte 12,5'
código: 1
uso: observatorio ["etiqueta;valor"]
código: 2
uso: observatorio ["etiqueta;valor"]
Registro (etiqueta;valor): Sur                   sin dato | sin dato
```

### 9. Tus tests, calculados a mano

En `tests/test_my_rules.py`, sustituye el test de ejemplo por **al menos 6 tests tuyos**, con etiquetas, valores, unidad y umbrales de tu dominio. Calcula el resultado esperado **antes** de ejecutar; para las filas, cuenta los espacios. Cubre al menos:

| Caso | Ejemplo (calidad del aire, umbrales 12 y 35) |
|---|---|
| Un valor justo en `LOW` y otro justo por debajo | `classify(12.0, 12.0, 35.0) == "medio"` y `classify(11.9, 12.0, 35.0) == "bajo"` |
| Un valor justo en `HIGH` | `classify(35.0, 12.0, 35.0) == "alto"` |
| Una fila exacta de `format_row` | `format_row("Estación Norte", 8.04, "µg/m³", "bajo") == "Estación Norte       8.0 µg/m³ \| bajo"` |
| Una línea válida de tu dominio con coma decimal | `parse_line("Centro;40,2", "µg/m³", 12.0, 35.0)` da la fila con `"alto"` |
| Una línea inválida de tu dominio | `parse_line("Centro-40", "µg/m³", 12.0, 35.0) is None` |
| El código de salida de `main` con una línea inválida | `main(["Centro-40"]) == 1` |

```bash
uv run pytest
```

Esperado: todo en verde, al menos `46 passed`: los 12 de `test_record.py`, los 23 de `test_rules.py` y `test_main.py`, tus 6 o más de esta semana y tus 5 o más de la semana 1.

### 10. En el contenedor

```bash
docker compose run --build --rm app
docker compose run --rm app observatorio "Norte;12,5"
```

Los mismos tests y la misma fila que en tu máquina. `docker compose run` es interactivo: sin argumentos, `docker compose run --rm app observatorio` también te pide la línea.

### 11. README, commit y pull request

Añade al `README.md` de tu repositorio la unidad, los umbrales y por qué los elegiste, y un ejemplo de uso con salida. Después:

```bash
git add .
git commit -m "feat: classify readings and read a line from the command line"
git push -u origin week-02
```

En GitHub, abre un *pull request* de `week-02` hacia `main` con:

1. Tus umbrales y su justificación.
2. La salida de `uv run pytest`.
3. La salida de los comandos del paso 8 con datos de tu dominio.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'observatorio.rules'` | `rules.py` no está en `src/observatorio/`: repite el paso 2 |
| `test_classify_levels_and_limits[0.0-bajo]` falla | Usaste `not value`; usa `value is None` |
| `test_main_help[--ayuda]` falla y sale una fila de error | El `case [line]` está antes que el de la ayuda |
| `ValueError: could not convert string to float` en la terminal | Pasaste un valor no numérico: es el comportamiento esperado hasta la semana 7 |
| `uv run observatorio` sigue mostrando los registros de la semana 1 | No copiaste el `__main__.py` nuevo; si ya lo hiciste, `uv sync` |
| El contenedor se queda esperando | Sin argumentos lee del teclado: escribe la línea y pulsa Enter, o pásala como argumento |

## Entrega

- Rama `week-02` de `python-<nombre>-<apellido>` con `rules.py`, `__main__.py` con tu unidad y tus umbrales, al menos 6 tests propios en `tests/test_my_rules.py` y todo en verde, también en Docker.
- `README.md` del repositorio con umbrales, justificación y ejemplo de uso.
- *Pull request* `week-02` → `main` con la descripción del paso 11.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Entrada, salida y `match`](../2-practicas/ejercicio-04-entrada-salida-y-match/README.md) | **Proyecto · Observatorio, capa 1** | [Webgrafía](../4-recursos/webgrafia/README.md) |
