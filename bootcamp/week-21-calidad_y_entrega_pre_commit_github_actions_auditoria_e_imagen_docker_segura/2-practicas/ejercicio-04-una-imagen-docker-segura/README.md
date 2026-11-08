# Ejercicio 04 — Una imagen Docker segura

⏱️ 1 h 30 min · Teoría previa: [05](../../1-teoria/05-una-imagen-docker-segura.md)

## Objetivo

Construir cuatro versiones de la misma imagen, de la ingenua a la segura, y **medir** qué cambia en cada una:

- separar **construir** de **ejecutar** con un Dockerfile *multi-stage*, sin uv ni dependencias de desarrollo en la imagen final;
- ejecutar con un **usuario sin privilegios**;
- fijar la imagen base por su **digest**, aplicarle los parches de Debian y quitarle **pip**;
- ejecutar con el sistema de archivos en **solo lectura**, sin **capacidades** y sin poder ganar privilegios;
- **escanear** las imágenes con Trivy y comparar.

`main.py` es una **sonda**: escribe quién es dentro del contenedor, qué herramientas encuentra, qué paquetes hay, dónde puede escribir y qué privilegios tiene. Ejercicio **guiado**: descomentas cada paso del `Dockerfile` y de `compose.yaml`, construyes y comparas. No se entrega.

## Antes de empezar

Docker funcionando (`docker version`) y unos 3 GB libres: la imagen ingenua es grande. En tu máquina, la sonda:

```bash
cd bootcamp/week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/2-practicas/ejercicio-04-una-imagen-docker-segura/starter
uv run python main.py
```

```
Ejercicio 04 · Una imagen Docker segura
usuario              <tú> (uid 1000)
python               3.14.10
uv                   sí
pip                  ...
...
```

## Pasos

### 1. La imagen ingenua

La etapa `ingenua` ya está escrita: la imagen completa de Python, uv dentro, todo el proyecto copiado y `uv sync` con todo. Funciona. Constrúyela y ejecútala:

```bash
docker build --target ingenua -t local/practica-21:ingenua .
docker run --rm local/practica-21:ingenua
```

```
Ejercicio 04 · Una imagen Docker segura
usuario              root (uid 0)
python               3.14.10
uv                   sí
pip                  sí
gcc                  sí
git                  sí
rich instalado       sí
pytest instalado     sí
escribir en /app     sí
escribir en /tmp     sí
capacidades          00000000a80425fb
NoNewPrivs           0
```

Si alguien consigue ejecutar código dentro de este contenedor (por un fallo en tu programa o en una dependencia), es **root**, tiene un compilador (`gcc`), `git`, `pip` y `uv` para bajarse lo que quiera, y puede **reescribir tu programa** en `/app`. `capacidades` son los privilegios de Linux que Docker da por defecto a root (cambiar el dueño de archivos, abrir puertos bajos...), en hexadecimal. Y lleva pytest, que en producción nadie usa.

### 2. Dos etapas: construir y ejecutar

Descomenta el **PASO 2** del `Dockerfile`, y:

```bash
docker build --target slim -t local/practica-21:slim .
docker run --rm local/practica-21:slim
```

```
usuario              root (uid 0)
python               3.14.10
uv                   no
pip                  sí
gcc                  no
git                  no
rich instalado       sí
pytest instalado     no
escribir en /app     sí
...
```

`builder` instala con uv y `--no-dev`; `slim` copia **solo** `/opt/venv` y `main.py`. Lo que hay en `builder` (uv, la caché, `pyproject.toml`) no llega a la imagen final: cada `FROM` empieza de cero, y `COPY --from=builder` elige qué se trae. La base es `slim`, sin compilador ni `git`. pytest ya no está: era de desarrollo. Mira los tamaños:

```bash
docker images local/practica-21
```

```
IMAGE                        ID             DISK USAGE   CONTENT SIZE   EXTRA
local/practica-21:ingenua    3756be12ae4a       1.69GB          437MB
local/practica-21:slim       ...                 197MB         47.5MB
```

`DISK USAGE` es lo que ocupa en tu disco; `CONTENT SIZE`, lo que se descarga, comprimido.

### 3. Sin root

Descomenta el **PASO 3**, y:

```bash
docker build --target sin-root -t local/practica-21:sin-root .
docker run --rm local/practica-21:sin-root
```

```
usuario              app (uid 10001)
...
escribir en /app     no (Permission denied)
escribir en /tmp     sí
capacidades          0000000000000000
NoNewPrivs           0
```

`FROM slim AS sin-root` parte de la etapa anterior y añade dos líneas. Ahora el proceso es el uid 10001: no puede tocar `/app`, que es de root, y un usuario normal no tiene capacidades. `USER 10001:10001` va **por número**: quien ejecute la imagen (Docker, Kubernetes) puede comprobar que no es 0 sin leer `/etc/passwd`. Sigue habiendo `pip`.

### 4. Fijada, parcheada y sin pip

Descomenta el **PASO 4**, y:

```bash
docker build --target segura -t local/practica-21:segura .
docker run --rm local/practica-21:segura
```

```
usuario              app (uid 10001)
python               3.14.10
uv                   no
pip                  no
gcc                  no
git                  no
rich instalado       sí
pytest instalado     no
escribir en /app     no (Permission denied)
escribir en /tmp     sí
capacidades          0000000000000000
NoNewPrivs           0
```

Tres cambios:

- **`@sha256:...`**: la etiqueta `3.14.10-slim-trixie` se puede volver a publicar con otro contenido; el digest es el contenido. Mañana construyes exactamente la misma base;
- **`apt-get upgrade`**: el digest congela la base con sus fallos; esta línea aplica los parches de seguridad que Debian publicó después;
- **fuera pip**: en producción nadie instala nada, y pip lleva dentro sus propias dependencias (`urllib3`, `msgpack`...), con sus avisos. Lo verás en el paso 6.

### 5. Un contenedor que no puede cambiar nada

Descomenta el **PASO 5** de `compose.yaml`, y:

```bash
docker compose run --rm segura
```

```
...
escribir en /app     no (Read-only file system)
escribir en /tmp     sí
capacidades          0000000000000000
NoNewPrivs           1
```

`read_only: true` monta la imagen en **solo lectura**: el error ya no es de permisos, es que no se puede escribir en ningún sitio, ni siendo root. `/tmp` es un `tmpfs`: vive en memoria y se pierde al parar. `NoNewPrivs 1`: ningún programa puede ganar privilegios, aunque sea *setuid*. ¿Y `cap_drop: [ALL]`, si `app` ya no tenía capacidades? Prueba a ejecutar como root, como haría alguien que cambia la configuración:

```bash
docker compose run --rm --user 0 segura
docker run --rm --user 0 local/practica-21:segura
```

```
usuario              root (uid 0)
...
capacidades          0000000000000000
NoNewPrivs           1
...
usuario              root (uid 0)
...
capacidades          00000000a80425fb
NoNewPrivs           0
```

Con compose, root tampoco tiene capacidades: cada capa protege aunque falle otra. Eso es **defensa en profundidad**.

### 6. Escanear con Trivy

Trivy busca, en los paquetes de Debian y de Python de una imagen, vulnerabilidades conocidas. Ejecútalo con Docker, sin instalarlo; el volumen `trivycache` guarda su base de datos entre ejecuciones:

```bash
TRIVY=aquasec/trivy:0.76.1@sha256:790fd66d1697395d8693d1acaa1ea702406a20f109b6fc7bac8db623eca6c06c
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivycache:/root/.cache $TRIVY \
  image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed local/practica-21:ingenua
echo $?
```

```
local/practica-21:ingenua (debian 13.7)
=======================================
Total: 4 (HIGH: 4, CRITICAL: 0)
...
│ zlib1g     │ CVE-2026-76844 │ HIGH     │ fixed  │ 1:1.3.dfsg+really1.3.1-1+b1 │ ...
...
Python (python-pkg)
===================
Total: 5 (HIGH: 5, CRITICAL: 0)
...
│ msgpack    │ CVE-2026-114613     │ HIGH     │ fixed  │ 1.1.2             │ 1.2.3         │ ...
│ setuptools │ CVE-2025-47273      │          │        │ 70.3.0            │ 78.1.1        │ ...
│ urllib3    │ CVE-2026-97687      │          │        │ 2.7.0             │ 2.8.0         │ ...
...
1
```

La primera vez descarga su base de datos (unos segundos). Las opciones:

- `--severity HIGH,CRITICAL`: solo lo grave;
- `--ignore-unfixed`: solo lo que **tiene arreglo**. Lo que no lo tiene no lo puedes arreglar tú hoy;
- `--exit-code 1`: termina con error si encuentra algo. Así lo usarás en la CI.

Los paquetes de Python con avisos (`msgpack`, `setuptools`, `urllib3`) **no son tuyos**: son los que pip lleva dentro. Ahora la segura:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivycache:/root/.cache $TRIVY \
  image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed local/practica-21:segura
echo $?
```

```
...
│ local/practica-21:segura (debian 13.7)  │   debian   │        0        │    -    │
...
0
```

Sin filtros, Trivy cuenta **todo**, también lo leve y lo que no tiene arreglo. En esta máquina:

| Imagen | Tamaño | Vulnerabilidades | HIGH o CRITICAL con arreglo |
|---|---|---|---|
| `ingenua` | 1,69 GB | 2367 | 9 |
| `segura` | 198 MB | 186 | 0 |

Tus números serán otros (salen avisos y parches cada semana), pero la proporción se mantiene: menos cosas dentro, menos cosas que pueden fallar.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `failed to solve: target stage "slim" could not be found` | No descomentaste el paso de esa etapa, o el nombre tras `AS` no coincide |
| `process "/bin/sh -c uv sync --locked --no-dev" did not complete successfully` | Lee las líneas de antes: casi siempre, `uv.lock` no corresponde a `pyproject.toml` (`uv lock` en tu máquina) |
| `no configuration file provided: not found` | Ejecuta `docker compose` en la carpeta `starter/`, donde está `compose.yaml` |
| `services must be a mapping` | El paso 5 sigue comentado, o la sangría no coincide |
| Trivy: `permission denied while trying to connect to the Docker daemon socket` | Tu usuario no puede usar Docker sin `sudo`: el mismo problema que con `docker run` |
| Trivy tarda mucho la primera vez | Descarga su base de datos; las siguientes la reutiliza desde el volumen `trivycache` |
| La sonda dice `escribir en /tmp: no` | Con `read_only: true` hace falta el `tmpfs` de `/tmp` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Auditar dependencias](../ejercicio-03-auditar-dependencias/README.md) | **Ejercicio 04 · Una imagen Docker segura** | [Proyecto · Calidad y entrega del Observatorio](../../3-proyecto/README.md) |
