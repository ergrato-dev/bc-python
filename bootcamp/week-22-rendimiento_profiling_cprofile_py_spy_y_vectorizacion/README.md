# Semana 22 — Rendimiento: profiling con cProfile y py-spy, y vectorización

> Tu Observatorio pasa la CI y se entrega en una imagen segura, pero nunca lo has probado con un archivo grande. Con 100 000 medidas, `informe` tarda más de 20 segundos y usa 330 MB. Esta semana aprendes a **medir** sin dejarte engañar por el ruido, a encontrar dónde se va el tiempo con un perfilador **determinista** (cProfile) y uno **por muestreo** (py-spy), a optimizar en el orden que más gana y a **vectorizar** con NumPy. Y a decidir con números cuándo no merece la pena. Al final, el mismo informe tarda alrededor de 1 segundo, y tus tests cuentan el trabajo para que no vuelva a crecer.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Medir** un programa con `time`, `perf_counter` y `timeit`, repitiendo y comparando mínimos, y **distinguir** el tiempo de reloj del de CPU
- **Estimar** con la ley de Amdahl cuánto puede ganar un arreglo antes de hacerlo
- **Perfilar** con cProfile y `pstats`: leer `ncalls`, `tottime` y `cumtime`, y ver quién llama a quién
- **Muestrear** con py-spy: grabar y leer un gráfico de llamas, ver un programa en vivo y preguntarle a uno colgado qué hace
- **Optimizar** en orden: quitar trabajo, no repetirlo, mejor estructura, funciones en C
- **Vectorizar** con NumPy y **decidir** con números cuándo compensa
- **Probar** el rendimiento contando trabajo, no segundos

---

## 📋 Prerrequisitos

- [Semana 21](../week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/README.md): calidad y entrega.
- El *pull request* `week-21` de tu proyecto fusionado en `main`, con la CI en verde.
- Un navegador para abrir los gráficos de llamas (SVG).
- Para `py-spy dump --pid`: poder usar `sudo` en tu máquina (ejercicio 03, paso 5).

---

## 🗂️ Estructura de la Semana

```
week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 21 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Medir antes de optimizar](1-teoria/01-medir-antes-de-optimizar.md) | Cuándo optimizar, el reloj adecuado, reloj y CPU, el ruido, `timeit`, cómo crece, la ley de Amdahl, el ciclo y tests que cuentan trabajo | 45 min |
| [02 · Perfilar con cProfile](1-teoria/02-perfilar-con-cprofile.md) | Qué es un perfil, perfilar un programa y una función, las columnas, `cumulative` y `tottime`, `pstats`, `print_callers` y el precio de mirar | 50 min |
| [03 · Muestrear con py-spy](1-teoria/03-muestrear-con-py-spy.md) | Determinista y por muestreo, cómo mira py-spy, `record`, gráficos de llamas, `--nonblocking`, `--idle`, `top`, `dump` y permisos | 50 min |
| [04 · Optimizar en Python puro](1-teoria/04-optimizar-python-puro.md) | El orden de las optimizaciones, no hacer el trabajo, hacerlo una vez, estructuras y algoritmos, funciones en C, el arranque y la memoria | 45 min |
| [05 · Vectorizar con NumPy](1-teoria/05-vectorizar-con-numpy.md) | Lo que hace un bucle, un array, vectorizar, máscaras, la media móvil con `cumsum`, el precio de convertir y por qué el Observatorio no usa NumPy | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Los tiempos de los README son de un portátil con WSL2: compara proporciones, no segundos.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Medir con `perf_counter` y `timeit`](2-practicas/ejercicio-01-medir-con-timeit/README.md) | El ruido, el mínimo de varias repeticiones, lista frente a `set`, `autorange`, cómo crece `list.insert(0)` y reloj frente a CPU | 1 h 30 min |
| [02 · Perfilar con cProfile](2-practicas/ejercicio-02-perfilar-con-cprofile/README.md) | Un informe lento, `cumtime` y `tottime`, `print_callers`, agrupar una vez (200 veces más rápido) y perfilar otra vez | 1 h 30 min |
| [03 · Muestrear con py-spy](2-practicas/ejercicio-03-muestrear-con-py-spy/README.md) | `record`, leer el gráfico de llamas, `--nonblocking`, `--idle` y `dump` de un programa que no termina | 1 h 30 min |
| [04 · Vectorizar con NumPy](2-practicas/ejercicio-04-vectorizar-con-numpy/README.md) | Sumar un millón de tres formas, puntuaciones z, el precio de convertir, máscaras, `cumsum` y por qué con 10 valores pierde | 1 h 30 min |

### Proyecto

Mides `informe` con 100 000 medidas, lo perfilas con cProfile y py-spy y lo arreglas en dos vueltas:

- `informe --filas N`, que pinta las 20 primeras filas y dice cuántas hay: de 21 s a 1,1 s;
- `Series.parse`, que analiza cada línea una vez, no dos, y cuya mejora resulta estar dentro del ruido;
- `py-spy==0.4.2` como dependencia de desarrollo, y `perfil/` fuera de Git y de la imagen.

Después mides el arranque y decides con números no usar NumPy todavía. 24 tests nuevos cuentan el trabajo con cProfile, sin medir segundos. La versión sube a `0.22.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Reloj y CPU de un programa | `time uv run observatorio informe -f perfil/grande.txt > /dev/null` |
| Y la memoria máxima | `/usr/bin/time -f "%e s %M KB" uv run ...` |
| Medir una expresión | `uv run python -m timeit -s "s = set(range(1000))" "500 in s"` |
| Perfil guardado | `uv run python -m cProfile -o perfil/x.prof -m observatorio informe ...` |
| Explorarlo | `uv run python -m pstats perfil/x.prof`, y `sort tottime`, `stats 10`, `callers f` |
| Gráfico de llamas | `uv run py-spy record --nonblocking -o perfil/x.svg -- python -m observatorio ...` |
| En vivo | `uv run py-spy top -- python main.py` |
| ¿Qué hace un proceso colgado? | `sudo .venv/bin/py-spy dump --pid N` |
| Cuánto tarda importar | `uv run python -X importtime -c "import observatorio.cli" 2>&1 \| tail -1` |
| Probar NumPy sin añadirlo | `uv run --with numpy==2.5.4 python ...` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-22` de `python-<nombre>-<apellido>` con:
   - `informe --filas`/`-n`, `records_with_errors` y `Series.parse`, con `informe` leyendo cada línea una vez;
   - `py-spy==0.4.2` en `dev`, `perfil/` en `.gitignore` y `.dockerignore`, las imágenes `week-22` en `compose.yaml`;
   - la versión `0.22.0` y al menos 6 tests propios en `tests/test_my_performance.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Rendimiento"
3. ✅ Pull request `week-22` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la tabla de medidas, una fila por vuelta, y las capturas de los gráficos de llamas de antes y después;
   - la tabla de mutantes y el test que mata al superviviente;
   - por qué no usas NumPy en `informe` y por qué dejas el arranque para más adelante, con tus números.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pre-commit run --all-files
uv run pytest
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
uv run observatorio --version
uv run python scripts/generar_medidas.py 100000 perfil/grande.txt
time uv run observatorio informe -f perfil/grande.txt > /dev/null
uv run observatorio informe -f perfil/grande.txt | tail -11
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 845;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.22.0`;
- `informe` tarda alrededor de un segundo (no veinte), y bajo la tabla dice `20 de 100000 medidas`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README, con los tiempos de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 21](../week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/README.md) | **Semana 22** | [Semana 23](../week-23-numpy_arrays_broadcasting_y_estadistica/README.md) |
