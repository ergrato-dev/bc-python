# Ejercicio 02 — Python en Docker

⏱️ 2 h 30 min · Teoría previa: [03](../../1-teoria/03-uv-proyectos-y-entornos.md) y [04](../../1-teoria/04-docker-para-python.md)

## Objetivo

Ejecutar el mismo código y los mismos tests en tu máquina y en un contenedor, ver la caché de capas en acción y corregir una imagen que corre como root.

## Antes de empezar

```bash
cd bootcamp/week-01-entorno_docker_uv_y_tipos/2-practicas/ejercicio-02-python-en-docker/starter
docker run --rm hello-world
```

La segunda línea debe terminar con `Hello from Docker!`. Si falla, revisa [`docs/setup.md`](../../../../docs/setup.md) antes de seguir.

Archivos del starter:

| Archivo | Qué es |
|---|---|
| `report.py` | Tres funciones por completar y una ya hecha (`inside_container`) |
| `tests/test_report.py` | 4 tests; uno solo se ejecuta dentro del contenedor |
| `Dockerfile` | La receta de la imagen (teoría 04) |
| `compose.yaml` | El servicio `app` que construye esa imagen |
| `.dockerignore` | Lo que no se copia a la imagen |

## Pasos

### 1. Lee el Dockerfile

Ábrelo y relaciona cada bloque con la teoría 04. Responde en `NOTAS.md`: ¿por qué se copian `pyproject.toml` y `uv.lock` **antes** que el resto del código?

### 2. Tests en rojo, en tu máquina y en el contenedor

En tu máquina:

```bash
uv run pytest
```

Salida esperada al final: `3 failed, 1 skipped`. El `skipped` es `test_container_does_not_run_as_root`: solo tiene sentido dentro de un contenedor, y el decorador `@pytest.mark.skipif` lo salta fuera.

En el contenedor:

```bash
docker compose run --build --rm app
```

La primera vez descarga las imágenes de Python y uv (unos 50 MB) y construye. Al final: `4 failed`. Dentro del contenedor, el cuarto test sí se ejecuta.

### 3. Implementa las tres funciones

En `report.py`, sustituye cada `raise NotImplementedError(...)`:

| Función | Sustitúyelo por | Qué hace |
|---|---|---|
| `python_version` | `return platform.python_version()` | Versión del intérprete, como en el ejercicio 01 |
| `current_user` | `return getpass.getuser()` | Nombre del usuario que ejecuta el proceso |
| `is_root` | `return os.geteuid() == 0` | En Linux, root es el usuario con identificador 0; `==` compara y da `True` o `False` |

Los módulos `platform`, `getpass` y `os` ya están importados al principio del archivo.

En tu máquina:

```bash
uv run pytest
uv run python report.py
```

Salida esperada: `3 passed, 1 skipped`, y un informe con tu usuario, `Es root: False` y `Contenedor: False`.

### 4. Mira la caché de capas

Reconstruye y ejecuta en el contenedor:

```bash
docker compose run --build --rm app
```

Mira las líneas del build: la de `RUN uv sync --locked` dice `CACHED`. Solo cambió tu código, así que Docker reutilizó la capa de dependencias y solo rehízo `COPY . .`.

Los tests dan `3 passed, 1 failed`. El que falla es `test_container_does_not_run_as_root`, con el mensaje `Paso 6: añade un usuario sin privilegios al Dockerfile`.

### 5. Comprueba quién eres dentro del contenedor

```bash
docker compose run --rm app python report.py
```

```
Python:     3.14.10
Usuario:    root
Es root:    True
Contenedor: True
Carpeta:    /app
Sistema:    Linux
```

Por defecto, el proceso del contenedor es root. Responde en `NOTAS.md`: ¿qué podría hacer un atacante que aprovechara un fallo de tu programa si este corre como root?

### 6. Corrige la imagen: usuario sin privilegios

En el `Dockerfile`, sustituye la línea `# Paso 6: aquí falta un usuario sin privilegios.` por:

```dockerfile
RUN useradd --create-home --uid 10001 app
USER app
```

`useradd` crea el usuario `app` con el identificador 10001 (un número alto, que no coincide con usuarios del sistema). `USER app` hace que todo lo que viene después, incluido el `CMD`, corra con ese usuario.

```bash
docker compose run --build --rm app
docker compose run --rm app python report.py
```

Salida esperada: `4 passed`, y en el informe `Usuario: app` y `Es root: False`.

### 7. Rompe el lock a propósito

Abre `pyproject.toml` y cambia `"pytest==9.2.0"` por `"pytest==9.1.0"`, **sin** ejecutar `uv lock`. Reconstruye:

```bash
docker compose run --build --rm app
```

El build se detiene en `RUN uv sync --locked`. Copia en `NOTAS.md` la línea del error que menciona el lockfile. Explica por qué es mejor que el build falle a que instale otra versión sin avisar. Deja `pyproject.toml` como estaba y comprueba que vuelve a dar `4 passed`.

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
| `useradd: command not found` | Escribiste `RUN useradd` antes de la línea `FROM python:...`; debe ir después |
| La descarga de imágenes se corta | Repite el comando; Docker retoma lo ya descargado |

## Entrega

`docker compose run --build --rm app` con 4 de 4 en verde, el `Dockerfile` con `USER app`, y `NOTAS.md` con las respuestas de los pasos 1, 5 y 7.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Hola, entorno](../ejercicio-01-hola-entorno/README.md) | **Ejercicio 02 · Python en Docker** | [Ejercicio 03 · Tipos y conversiones](../ejercicio-03-tipos-y-conversiones/README.md) |
