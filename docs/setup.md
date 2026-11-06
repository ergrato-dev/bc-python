# Preparar tu máquina

Para la semana 1 necesitas cuatro cosas. Todo lo demás (Python, bibliotecas, PostgreSQL, Jupyter) lo instalan `uv` o Docker cuando hace falta. Versiones exactas en [stack-versions.md](stack-versions.md).

| Qué | Versión | Cómo comprobarlo |
|---|---|---|
| Docker Engine + plugin Compose | Engine 29 o superior, Compose v5 | `docker --version` y `docker compose version` |
| uv | 0.13.7 | `uv --version` |
| Git | cualquiera reciente | `git --version` |
| VS Code | estable reciente | abre la carpeta del bootcamp sin errores |

**No instales Python desde python.org ni con el gestor de paquetes del sistema.** `uv` descarga la versión exacta que pide cada proyecto (`.python-version` y `requires-python`) y la aísla del Python del sistema. Así nunca rompes herramientas del sistema operativo ni mezclas versiones.

**Tampoco necesitas Anaconda ni conda**, ni siquiera en las fases de data science e IA. NumPy, pandas, scikit-learn, PyTorch, Transformers y JupyterLab se instalan con `uv add` desde PyPI, y lo que no es Python (bibliotecas del sistema) lo pone la imagen Docker. No necesitas GPU: PyTorch se instala en su versión para CPU y los ejercicios están dimensionados para entrenar en minutos en un portátil. Si ya tienes conda instalado, desactiva su entorno base para que no se cuele en el `PATH`: `conda config --set auto_activate_base false`.

## Google Colab (alternativa oficial desde la semana 23)

[Google Colab](https://colab.research.google.com) ejecuta notebooks en la nube, con GPU gratuita (limitada por tiempo). En el bootcamp es una **alternativa oficial** para los notebooks de las fases 4 y 5, y la forma de usar GPU en las semanas de PyTorch y Transformers (34-36) si tu equipo no tiene.

| Uso | Dónde |
|---|---|
| Explorar datos, probar ideas, entrenar con GPU | Colab o JupyterLab local, a tu elección |
| Entregar (tests, `uv.lock`, Docker, pull request) | Siempre tu repositorio local |

Cada notebook trae un botón "Abrir en Colab" y una primera celda que instala las versiones fijadas del curso con uv. Sube a Colab solo datos sintéticos o anonimizados: lo que subes queda en tu Google Drive y en servidores de Google.

## Windows: usa WSL2

Todo el bootcamp se trabaja dentro de Linux. En Windows:

1. Abre PowerShell como administrador y ejecuta `wsl --install -d Ubuntu-24.04`. Reinicia cuando te lo pida.
2. Instala Docker Desktop y activa **Settings → Resources → WSL integration** para Ubuntu.
3. A partir de aquí, cada comando de esta guía se escribe en la terminal de Ubuntu, no en PowerShell.
4. Guarda tus proyectos dentro de Linux (`~/proyectos`), no en `/mnt/c/...`: el acceso a archivos de Windows desde WSL es mucho más lento.

## Docker

- **Linux**: sigue <https://docs.docker.com/engine/install/> para tu distribución y después `sudo usermod -aG docker $USER` (cierra sesión y vuelve a entrar para que surta efecto).
- **macOS y Windows**: Docker Desktop desde <https://docs.docker.com/desktop/>.

Comprueba:

```bash
docker run --rm hello-world
```

Debe terminar con `Hello from Docker!`. Si dice `permission denied ... docker.sock`, en Linux te falta el grupo `docker` (paso anterior).

## uv

```bash
curl -LsSf https://astral.sh/uv/0.13.7/install.sh | sh
```

Cierra y abre la terminal, y comprueba:

```bash
uv --version          # uv 0.13.7
uv python install 3.14.10
uv python list --only-installed
```

Si ya tenías otra versión de uv, `uv self update 0.13.7` la deja en la del bootcamp.

## VS Code

Instala estas extensiones:

| Extensión | Para qué |
|---|---|
| Python (`ms-python.python`) | ejecutar y depurar |
| Ruff (`charliermarsh.ruff`) | lint y formato al guardar |
| Mypy Type Checker (`ms-python.mypy-type-checker`) | errores de tipos en el editor |
| Jupyter (`ms-toolsai.jupyter`) | notebooks, desde la semana 27 |
| Container Tools (`ms-azuretools.vscode-containers`) | ver imágenes y contenedores |
| WSL (`ms-vscode-remote.remote-wsl`) | solo en Windows |

En Windows, abre VS Code desde la terminal de Ubuntu con `code .` para que trabaje dentro de WSL.

## Primera comprobación

Cuando exista la semana 1:

```bash
cd bootcamp/week-01-entorno_docker_uv_y_tipos/2-practicas/ejercicio-01-hola-entorno/starter
uv run python --version     # Python 3.14.10
uv run pytest               # los tests arrancan en rojo: es lo esperado
```

La primera vez, `uv` descarga Python y crea `.venv/` dentro del starter. No subas `.venv/` al repositorio: ya está en `.gitignore`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Inicio del bootcamp](../README.md) | **Preparar tu máquina** | [Dominios](dominios.md) |

← [Volver al inicio del bootcamp](../README.md)
