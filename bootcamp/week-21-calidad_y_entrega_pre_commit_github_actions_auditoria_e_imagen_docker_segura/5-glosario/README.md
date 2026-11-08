# Glosario — Semana 21

| Término | Definición |
|---|---|
| **Acción (*action*)** | Un paso reutilizable de GitHub Actions, publicado en un repositorio: `actions/checkout`, `astral-sh/setup-uv`. Se usa con `uses:` y debe ir fijada a un SHA |
| **actionlint** | Un revisor de workflows de GitHub Actions: claves mal escritas, expresiones incorrectas y errores de *shell* antes del *push* |
| **Aviso (*advisory*)** | La publicación de una vulnerabilidad: qué paquete, qué versiones afecta, cuál la arregla y cuán grave es. Tiene uno o varios identificadores (CVE, GHSA, PYSEC) |
| **Cadena de suministro** | Todo el código de otros del que depende el tuyo: dependencias directas y transitivas, Python, la imagen base y las acciones de la CI |
| **Capa (Docker)** | Lo que añade una instrucción del `Dockerfile` a la imagen. Lo que una capa borra sigue ocupando en la anterior: por eso se instala y se limpia en el mismo `RUN` |
| **Capacidades de Linux** | Los permisos especiales de root, partidos en piezas: cambiar dueños, abrir puertos bajos, saltarse permisos... `cap_drop: [ALL]` las quita todas |
| **CI (integración continua)** | Comprobar automáticamente cada cambio en una máquina limpia, antes de fusionarlo. En tu proyecto, GitHub Actions |
| **`concurrency`** | La clave de un workflow que agrupa ejecuciones: con `cancel-in-progress`, un *push* nuevo cancela la ejecución anterior de la misma rama |
| **`cooldown`** | La opción de Dependabot que espera unos días antes de proponer una versión recién publicada |
| **CVE** | *Common Vulnerabilities and Exposures*: el catálogo general de vulnerabilidades, con identificadores como `CVE-2024-56201` |
| **Defensa en profundidad** | Varias protecciones independientes, para que si falla una sigan las otras: `USER`, `cap_drop` y `no-new-privileges` a la vez |
| **Dependabot** | El servicio de GitHub que vigila tus dependencias, acciones e imágenes y abre un *pull request* por cada actualización |
| **Dependencia transitiva** | Una dependencia que no pides tú, sino algo que pediste. Está en `uv.lock` y no en `pyproject.toml` |
| **Digest** | El hash `sha256:` del contenido de una imagen. A diferencia de la etiqueta, no puede cambiar |
| ***Distroless*** | Imágenes base sin *shell* ni gestor de paquetes, solo lo necesario para ejecutar un lenguaje |
| **Etapa (*stage*)** | Cada `FROM` de un `Dockerfile` *multi-stage*. Una etapa solo recibe de otra lo que copia con `COPY --from` |
| **Fail-fast** | En una matriz, cancelar los demás jobs en cuanto uno falla. Es lo que hace GitHub Actions por defecto |
| **Gancho de Git (*hook*)** | Un programa que Git ejecuta en un momento concreto, como antes de cada commit (`.git/hooks/pre-commit`). Si termina con error, el commit no se hace |
| **Gancho local** | En pre-commit, un gancho con `repo: local`: ejecuta una orden de tu proyecto, como `uv run --locked mypy`, con tus versiones |
| **Gancho remoto** | En pre-commit, un gancho que vive en otro repositorio y se instala en un entorno aislado, fijado por `rev` |
| **GHSA** | *GitHub Security Advisory*: el identificador de un aviso en la base de datos de GitHub, como `GHSA-cpwx-vrp4-4pq7` |
| **GitHub Actions** | La CI de GitHub: ejecuta los workflows de `.github/workflows/` en máquinas suyas, en respuesta a eventos |
| **Imagen base** | La imagen de la que parte la tuya con `FROM`, como `python:3.14.10-slim-trixie` |
| **Job** | Un conjunto de pasos de un workflow que corre en un runner. Los jobs de un workflow corren en paralelo salvo que uno dependa de otro |
| **Matriz** | `strategy.matrix`: el mismo job con varios valores, como dos versiones de Python |
| ***Multi-stage*** | Un `Dockerfile` con varias etapas, para construir en una y ejecutar en otra con solo lo necesario |
| **`no-new-privileges`** | Una opción de seguridad del contenedor: ningún proceso puede ganar privilegios, ni con un programa *setuid* |
| **OSV** | *Open Source Vulnerabilities*: la base de datos que junta los avisos de muchas fuentes. La consulta `uv audit` |
| **`permissions`** | La clave de un workflow que limita lo que puede hacer su token. `contents: read` solo deja leer el repositorio |
| **pre-commit** | La herramienta que instala y ejecuta ganchos de Git descritos en `.pre-commit-config.yaml` |
| **`pull_request_target`** | Un evento que ejecuta el workflow de `main` con permisos de escritura sobre un *pull request* ajeno. Peligroso: no lo uses |
| **PYSEC** | El identificador de un aviso en la base de datos de avisos de Python de la PyPA |
| ***Read-only*** | Un contenedor con el sistema de archivos en solo lectura: `read_only: true` en compose |
| **Runner** | La máquina que ejecuta un job, como `ubuntu-24.04` de GitHub |
| **Ruleset** | Reglas de GitHub sobre una rama, como exigir un *pull request* y la CI en verde para fusionar en `main` |
| **Servicio (*service container*)** | Un contenedor que GitHub Actions arranca junto a un job, como PostgreSQL para los tests |
| **SHA** | El identificador de 40 caracteres de un commit. Fijar una acción a un SHA impide que alguien la cambie moviendo una etiqueta |
| **Step** | Un paso de un job: una orden (`run`) o una acción (`uses`) |
| **Superficie de ataque** | Todo lo que alguien podría usar si consigue ejecutar código en tu sistema. Se reduce quitando lo que no hace falta |
| **`tmpfs`** | Un sistema de archivos en memoria. En compose, `tmpfs: [/tmp]` deja escribir en `/tmp` aunque el contenedor sea de solo lectura |
| **Token (`GITHUB_TOKEN`)** | La credencial que GitHub da a cada job para hablar con el repositorio. Sus permisos los fija `permissions` |
| **Trivy** | Un escáner de vulnerabilidades para imágenes, sistemas de archivos y configuración |
| **`uv audit`** | La orden de uv, experimental, que busca en OSV avisos para los paquetes de `uv.lock` |
| **`UV_LOCKED`** | La variable que hace que cada orden de uv falle si `uv.lock` no coincide con `pyproject.toml`, como `--locked` |
| **Vulnerabilidad** | Un fallo de un programa que alguien puede aprovechar: leer lo que no debe, colgarlo o ejecutar su código |
| **Workflow** | Un archivo YAML de `.github/workflows/` que dice cuándo (`on`) y qué (`jobs`) ejecuta GitHub Actions |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
