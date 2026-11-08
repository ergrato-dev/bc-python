# Webgrafía — Semana 21

| Recurso | Para qué |
|---|---|
| [pre-commit](https://pre-commit.com/) (en inglés) | La documentación oficial: el archivo de configuración, las opciones de cada gancho, `SKIP`, `autoupdate` y los lenguajes. La teoría 02 |
| [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) (en inglés) | Los ganchos genéricos, uno por uno, con sus argumentos. Y la [lista de ganchos](https://pre-commit.com/hooks.html) de otros proyectos |
| [Puntos de enganche en Git](https://git-scm.com/book/es/v2/Personalizaci%C3%B3n-de-Git-Puntos-de-enganche-en-Git) (en español) | Los ganchos de Git sin pre-commit: cuáles hay y cuándo se ejecutan. El ejercicio 01, paso 1 |
| [uv y pre-commit](https://docs.astral.sh/uv/guides/integration/pre-commit/) (en inglés) | Los ganchos oficiales de uv, como `uv-lock`, si prefieres el remoto al local |
| [uv en GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/) (en inglés) | `setup-uv`, la caché, versiones de Python y PostgreSQL como servicio. La teoría 03 |
| [uv en Docker](https://docs.astral.sh/uv/guides/integration/docker/) (en inglés) | Las recetas de Astral: *multi-stage*, `--no-editable`, `UV_COMPILE_BYTECODE` y la caché. La teoría 05 |
| [Sintaxis de los workflows](https://docs.github.com/es/actions/using-workflows/workflow-syntax-for-github-actions) (en español) | Cada clave de un workflow: `on`, `permissions`, `concurrency`, `jobs`, `services`, `strategy`... Para consultar |
| [Usar Actions de forma segura](https://docs.github.com/en/actions/reference/security/secure-use) (en inglés) | La guía de seguridad de GitHub: acciones por SHA, permisos del token, secretos y `pull_request_target` |
| [Opciones de Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) (en inglés) | `package-ecosystem`, `schedule`, `cooldown`, `ignore`, `groups`... El `dependabot.yml` de tu proyecto |
| [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) (en inglés) | Cómo exigir *pull requests* y comprobaciones en verde para fusionar en `main`. La teoría 01, sección 8 |
| [actionlint](https://github.com/rhysd/actionlint) (en inglés) | Qué revisa, y cómo usarlo como gancho de pre-commit |
| [`gh run view`](https://cli.github.com/manual/gh_run_view) (en inglés) | El manual de `gh` para leer ejecuciones y registros desde la terminal |
| [OSV](https://osv.dev/) (en inglés) | La base de datos de vulnerabilidades que consulta `uv audit`. Busca un paquete tuyo y mira su historial |
| [GitHub Advisory Database](https://github.com/advisories) y [CVE](https://www.cve.org/) (en inglés) | Los avisos GHSA y el catálogo CVE. Busca `jinja2` o `urllib3` para ver los del ejercicio 03 |
| [El ataque a Trivy](https://www.aquasec.com/blog/trivy-supply-chain-attack-what-you-need-to-know) (en inglés) | El relato de Aqua Security sobre las etiquetas movidas de `trivy-action` en marzo de 2026. La teoría 03, sección 6 |
| [Trivy](https://trivy.dev/) (en inglés) | El escáner: imágenes, sistemas de archivos, configuración y secretos |
| [Construcciones *multi-stage*](https://docs.docker.com/build/building/multi-stage/) y [buenas prácticas](https://docs.docker.com/build/building/best-practices/) (en inglés) | La documentación de Docker sobre etapas, imágenes base pequeñas, `USER` y capas |
| [Seguridad del motor de Docker](https://docs.docker.com/engine/security/) (en inglés) | Qué aísla Docker y qué no: capacidades, *namespaces*, `no-new-privileges` |
| [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html) (en inglés) | Una lista de reglas para contenedores, con el porqué de cada una. Compárala con tu `compose.yaml` |
| [SLSA](https://slsa.dev/) (en inglés) | Un marco para la seguridad de la cadena de suministro: qué garantías puede dar un proceso de entrega. Para cuando quieras ir más allá |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
