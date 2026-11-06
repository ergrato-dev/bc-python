# Proyecto — Observatorio, capa 0: el registro

⏱️ 5 h

## Qué construyes

El primer archivo del proyecto que te acompaña las 42 semanas ([proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md)): un paquete `observatorio` que lee **una medida** de tu dominio desde texto, la valida y la muestra. Es la pieza más pequeña del sistema. En la semana 7 leerás miles de registros de un CSV con estas mismas funciones, y en la fase 4 los promediarás. Si hoy un dato faltante se lee como `0`, todos esos promedios saldrán mal sin dar error.

| Función | Recibe | Devuelve |
|---|---|---|
| `parse_value("12,5")` | El texto de una medida | `12.5`, o `None` si es un marcador de dato faltante (`""`, `"NA"`, `"N/A"`, `"-"`) |
| `describe_record("Estación Norte", 12.54, "µg/m³")` | Etiqueta, valor y unidad | `"Estación Norte: 12.5 µg/m³"`, o `"Estación Norte: sin dato"` si el valor es `None` |
| `is_valid(12.5, 0.0, 500.0)` | Valor, mínimo y máximo | `True` si el valor existe y está en el rango, límites incluidos |

## Pasos

### 1. Elige tu dominio

Lee [`docs/dominios.md`](../../../docs/dominios.md) y elige uno. Confírmalo con tu instructor: dos aprendices de la misma ficha no pueden repetir dominio. Anota tres cosas: qué registras, la medida principal con su unidad, y su rango razonable (mínimo y máximo).

| Ejemplo (calidad del aire) | Tu dominio |
|---|---|
| Lecturas de estaciones | … |
| PM2.5 en µg/m³ | … |
| 0 a 500 | … |

### 2. Crea tu repositorio

En GitHub, crea un repositorio **vacío** (sin README ni `.gitignore`) llamado `bc-python-<tu-dominio>`, por ejemplo `bc-python-calidad-aire`. Después, en tu terminal (fuera de la carpeta del bootcamp):

```bash
mkdir -p ~/proyectos && cd ~/proyectos
cp -r <ruta-al-bootcamp>/bootcamp/week-01-entorno_docker_uv_y_tipos/3-proyecto/starter bc-python-<tu-dominio>
cd bc-python-<tu-dominio>
ls -A
```

Debes ver: `.dockerignore  .python-version  Dockerfile  README.md  compose.yaml  pyproject.toml  src  tests  uv.lock`.

### 3. Prepara Git y la rama de la semana

Crea el `.gitignore` y el primer commit en `main`:

```bash
printf '.venv/\n__pycache__/\n.pytest_cache/\n.env\n' > .gitignore
git init -b main
git add .
git commit -m "chore: start observatorio from week-01 starter"
git remote add origin git@github.com:<tu-usuario>/bc-python-<tu-dominio>.git
git push -u origin main
git switch -c week-01
```

Desde ahora trabajas en la rama `week-01`. Cada semana tendrá su rama y su *pull request*.

### 4. Tests en rojo

```bash
uv run pytest
```

Salida esperada: `13 failed`. Fallan los 12 de `tests/test_record.py` y el de ejemplo de `tests/test_my_domain.py`, todos con `NotImplementedError`.

Mira cómo está organizado el código: `src/observatorio/` es el **paquete** (teoría 03). `__init__.py` lo marca como paquete; `record.py` tiene tus funciones; `__main__.py` es lo que se ejecuta con `uv run observatorio`.

### 5. `parse_value`

Abre `src/observatorio/record.py`. La docstring de cada función dice exactamente qué debe hacer. Para `parse_value` necesitas tres pasos, cada uno visto en la teoría 05 y el ejercicio 03:

1. Quitar los espacios de los lados (`strip`) y guardar el resultado en `text`.
2. Si `text` está en `MISSING_MARKERS`, devolver `None`. Para preguntar si un valor está en una tupla, Python usa `in`: `if text in MISSING_MARKERS:`.
3. Si no, cambiar la coma por punto y convertir con `float`.

```bash
uv run pytest -k parse_value
```

Esperado: `8 passed`. Fíjate en `test_parse_value_zero_is_a_real_value`: `"0"` es un dato, no un faltante.

### 6. `describe_record`

Dos casos: si `value is None`, devuelve `f"{label}: sin dato"`; si no, la f-string con el valor formateado a un decimal (`{value:.1f}`, teoría 05, sección 4).

```bash
uv run pytest -k describe_record
```

Esperado: `2 passed`.

### 7. `is_valid`

`value` tiene que no ser `None` **y** estar entre `minimum` y `maximum`. En Python, `and` exige que ambas condiciones sean verdaderas, y las comparaciones se encadenan:

```python
>>> 0.0 <= 12.5 <= 500.0
True
>>> value = None
>>> value is not None and 0.0 <= value <= 500.0
False
```

El orden importa: si `value` es `None`, Python ya no evalúa la segunda parte (que fallaría con `TypeError`). Escribe la función con un solo `return`.

```bash
uv run pytest tests/test_record.py
```

Esperado: `12 passed`.

### 8. Tu dominio en el programa

En `src/observatorio/__main__.py`, cambia los tres registros de ejemplo por tres de tu dominio. Uno debe tener un dato faltante (`"NA"`), y otro, coma decimal. Ejecuta:

```bash
uv run observatorio
```

Ejemplo de salida para calidad del aire:

```
Estación Norte: 12.5 µg/m³
Estación Centro: 31.0 µg/m³
Estación Sur: sin dato
```

### 9. Tus tests, calculados a mano

En `tests/test_my_domain.py`, sustituye el test de ejemplo por **al menos 5 tests tuyos**, con etiquetas, valores, unidades y rangos de tu dominio. Calcula a mano el resultado esperado **antes** de ejecutarlos. Cubre al menos:

| Caso | Ejemplo (calidad del aire) |
|---|---|
| Un valor normal con coma decimal | `parse_value("35,2") == 35.2` |
| Un dato faltante | `describe_record("Estación Sur", parse_value("NA"), "µg/m³") == "Estación Sur: sin dato"` |
| El redondeo a un decimal | `describe_record("Estación Norte", 12.46, "µg/m³") == "Estación Norte: 12.5 µg/m³"` |
| Un valor fuera de rango | `not is_valid(612.0, 0.0, 500.0)` |
| Un límite exacto del rango | `is_valid(0.0, 0.0, 500.0)` |

Cada test es una función que empieza por `test_` y contiene un `assert`, como los de `tests/test_record.py`.

```bash
uv run pytest
```

Esperado: todo en verde, con al menos `17 passed`.

### 10. En el contenedor

```bash
docker compose run --build --rm app
docker compose run --rm app observatorio
```

Los mismos tests y la misma salida que en tu máquina. Este `Dockerfile` ya trae el usuario `app` (ejercicio 02) y además instala tu paquete: lee los comentarios para ver por qué hay **dos** `uv sync`.

### 11. README, commit y pull request

Completa el `README.md` de tu proyecto: dominio, qué registras y la medida principal. Después:

```bash
git add .
git commit -m "feat: parse, describe and validate a single record"
git push -u origin week-01
```

En GitHub, abre un *pull request* de `week-01` hacia `main`. En la descripción pega:

1. Tu dominio, medida y rango.
2. La salida de `uv --version` y `uv run python --version`.
3. La salida de `uv run pytest` y de `uv run observatorio`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'observatorio'` | Ejecutaste sin `uv run`, o fuera de la carpeta del proyecto |
| `TypeError: '<=' not supported between instances of 'NoneType' and 'float'` | En `is_valid`, la comparación va **después** de `value is not None` |
| `test_parse_value_missing_markers_give_none[  NA  ]` falla | Te falta el `strip()` antes de comparar con `MISSING_MARKERS` |
| `git push` pide usuario y contraseña | Configura una clave SSH en GitHub (`bc-github`) o usa la URL `https://` con un token |
| `uv run observatorio` dice `Failed to spawn: observatorio` | Borra `.venv/` y repite `uv sync`; el paquete se reinstala con su comando |

## Entrega

- Repositorio `bc-python-<tu-dominio>` con el `README.md` completado.
- Rama `week-01` con `uv run pytest` en verde, al menos 5 tests propios en `tests/test_my_domain.py` y `__main__.py` con datos de tu dominio.
- *Pull request* `week-01` → `main` con la descripción del paso 11.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Tipos y conversiones](../2-practicas/ejercicio-03-tipos-y-conversiones/README.md) | **Proyecto · Observatorio, capa 0** | [Webgrafía](../4-recursos/webgrafia/README.md) |
