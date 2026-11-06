# Ejercicio 02 — Python en Docker

⏱️ 2 h 30 min · Teoría previa: [03](../../1-teoria/03-uv-proyectos-y-entornos.md) y [04](../../1-teoria/04-docker-para-python.md)

## Objetivo

Ejecutar el mismo programa en tu máquina y en un contenedor, ver la caché de capas en acción, corregir una imagen que corre como root y ver cómo `--locked` frena un lock desactualizado. Ejercicio **guiado**: descomentas, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-01-entorno_docker_uv_y_tipos/2-practicas/ejercicio-02-python-en-docker/starter
docker run --rm hello-world
```

La segunda línea debe terminar con `Hello from Docker!`. Si falla, revisa [`docs/setup.md`](../../../../docs/setup.md) antes de seguir.

Archivos del starter:

| Archivo | Qué es |
|---|---|
| `report.py` | El programa: un informe del entorno, con un paso comentado |
| `Dockerfile` | La receta de la imagen (teoría 04), con un paso comentado |
| `compose.yaml` | El servicio `app` que construye esa imagen |
| `.dockerignore` | Lo que no se copia a la imagen |

## Pasos

### 1. Lee el Dockerfile

Ábrelo y relaciona cada bloque con la teoría 04. Fíjate en el orden: `pyproject.toml` y `uv.lock` se copian **antes** que el código. La razón la ves en el paso 4.

### 2. El programa, en tu máquina y en el contenedor

En tu máquina:

```bash
uv run python report.py
```

```
Contenedor: False
Carpeta:    /home/<tu-usuario>/.../starter
```

En el contenedor:

```bash
docker compose run --build --rm app
```

La primera vez descarga las imágenes de Python y uv (unos 50 MB) y construye. Al final:

```
Contenedor: True
Carpeta:    /app
```

El mismo archivo, dos entornos: dentro del contenedor el código vive en `/app` (el `WORKDIR` del Dockerfile).

### 3. Quién ejecuta el programa

Descomenta el **PASO 3** de `report.py` y ejecuta en tu máquina:

```bash
uv run python report.py
```

Las tres líneas nuevas muestran `Python: 3.14.10`, tu usuario y `Es root: False`.

### 4. La caché de capas

```bash
docker compose run --build --rm app
```

Mira las líneas del build: la de `RUN uv sync --locked` dice `CACHED`. Solo cambió tu código, así que Docker reutilizó la capa de dependencias y solo rehízo `COPY . .`. Si el `COPY . .` fuera antes del `uv sync`, cada cambio de una línea de código reinstalaría todas las dependencias.

### 5. Root dentro del contenedor

La salida del paso 4 termina así:

```
Contenedor: True
Carpeta:    /app
Python:     3.14.10
Usuario:    root
Es root:    True
```

Por defecto, el proceso del contenedor es root. Si un fallo de tu programa permite ejecutar código, ese código tiene todos los permisos dentro del contenedor: leer secretos montados, instalar herramientas, escribir donde quiera. La teoría 04 explica por qué la regla del bootcamp es **nunca root**.

### 6. Corrige la imagen: usuario sin privilegios

Descomenta el **PASO 6** del `Dockerfile` (las líneas `RUN useradd ...` y `USER app`). `useradd` crea el usuario `app` con el identificador 10001 (un número alto, que no coincide con usuarios del sistema). `USER app` hace que todo lo que viene después, incluido el `CMD`, corra con ese usuario.

```bash
docker compose run --build --rm app
```

Salida esperada al final: `Usuario: app` y `Es root: False`.

### 7. Rompe el lock a propósito

Abre `pyproject.toml` y cambia `version = "0.1.0"` por `version = "0.2.0"`, **sin** ejecutar `uv lock`. Reconstruye:

```bash
docker compose run --build --rm app
```

El build se detiene en `RUN uv sync --locked` con:

```
error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.
```

`pyproject.toml` y `uv.lock` ya no coinciden, y `--locked` prefiere fallar a instalar algo distinto de lo que se probó. Con dependencias reales, esto evita que una imagen salga con versiones que nadie revisó. Deja `version = "0.1.0"` y comprueba que vuelve a construir.

### 8. Limpia

```bash
docker image rm local/python-en-docker:week-01
```

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `permission denied while trying to connect to the Docker daemon socket` | `sudo usermod -aG docker $USER`, cierra sesión y entra de nuevo |
| `Cannot connect to the Docker daemon` | Arranca Docker Desktop o `sudo systemctl start docker` |
| El contenedor no ve tu cambio en `report.py` | Te faltó `--build` |
| `docker: 'compose' is not a docker command` | Tienes Compose v1; instala el plugin `docker compose` ([`docs/setup.md`](../../../../docs/setup.md)) |
| `unknown instruction: USER` o `RUN` raro | Al descomentar quedó un espacio o un `#` de más al principio de la línea |
| La descarga de imágenes se corta | Repite el comando; Docker retoma lo ya descargado |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Hola, entorno](../ejercicio-01-hola-entorno/README.md) | **Ejercicio 02 · Python en Docker** | [Ejercicio 03 · Tipos y conversiones](../ejercicio-03-tipos-y-conversiones/README.md) |
