# Ejercicio 03 — Auditar dependencias

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-cadena-de-suministro-auditar-y-actualizar-dependencias.md)

## Objetivo

Encontrar las vulnerabilidades conocidas de tus dependencias y quitarlas, sin romper nada:

- ver qué tienes instalado y **quién pide qué**, también lo que no pediste tú;
- **auditar** el proyecto con `uv audit` y leer un aviso: su identificador, qué versión lo arregla y dónde leer más;
- **actualizar** una dependencia directa, y una **transitiva** que no aparece en tu `pyproject.toml`;
- **ignorar** un aviso, sabiendo lo que haces, y preparar la auditoría para la CI.

El proyecto pide a propósito `jinja2==3.1.4` y `requests==2.32.3`, versiones de 2024, y sujeta `urllib3` en `2.2.3`. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

`uv audit` consulta una base de datos de avisos en Internet (OSV). Copia el `starter/`, para no cambiar el del bootcamp:

```bash
cp -r bootcamp/week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/2-practicas/ejercicio-03-auditar-dependencias/starter ~/practicas/semana-21/ej03
cd ~/practicas/semana-21/ej03
uv run python main.py
```

```
...
Ejercicio 03 · Auditar dependencias
```

## Pasos

### 1. Lo que hay instalado

Descomenta el **PASO 1** de `main.py` y ejecuta:

```
--- Paso 1: lo instalado ---
certifi              2026.10.23
charset-normalizer   3.5.2
idna                 3.20
Jinja2               3.1.4
MarkupSafe           3.0.4
requests             2.32.3
urllib3              2.2.3
```

Pediste dos paquetes y tienes siete. Compáralo con el árbol de uv:

```bash
uv tree
```

```
auditar-dependencias v0.1.0
├── jinja2 v3.1.4
│   └── markupsafe v3.0.4
└── requests v2.32.3
    ├── certifi v2026.10.23
    ├── charset-normalizer v3.5.2
    ├── idna v3.20
    └── urllib3 v2.2.3
```

Los cinco que no pediste son **dependencias transitivas**: las pide algo que pediste tú. Tu programa ejecuta su código igual que el de las directas, y sus fallos son tuyos.

### 2. Quién pide qué

Descomenta el **PASO 2** y ejecuta:

```
--- Paso 2: quién pide qué ---
jinja2 pide: MarkupSafe>=2.0
requests pide: charset-normalizer <4,>=2, idna <4,>=2.5, urllib3 <3,>=1.21.1, certifi >=2017.4.17
```

Cada paquete declara **rangos**, no versiones: `requests` acepta cualquier `urllib3` desde 1.21.1 y antes de 3. Es `uv lock` quien elige una versión concreta dentro de los rangos y la apunta en `uv.lock`. Al revés, para un paquete concreto:

```bash
uv tree --invert --package urllib3
```

```
urllib3 v2.2.3
└── requests v2.32.3
    └── auditar-dependencias v0.1.0
```

### 3. La auditoría

```bash
uv audit
echo $?
```

```
warning: `uv audit` is experimental and may change without warning. Pass `--preview-features audit-command` to disable this warning.
...
Found 13 known vulnerabilities and no adverse project statuses in 7 packages

Vulnerabilities:

jinja2 3.1.4 has 3 known vulnerabilities:

- PYSEC-2026-1472: Jinja has a sandbox breakout through malicious filenames

  Fixed in: 3.1.5

  Advisory information: https://nvd.nist.gov/vuln/detail/CVE-2024-56201
...
requests 2.32.3 has 2 known vulnerabilities:
...
urllib3 2.2.3 has 8 known vulnerabilities:
...
1
```

Tu número puede ser **mayor**: la base de datos crece cada semana, y lo que hoy está limpio mañana puede no estarlo. Por eso la auditoría va en la CI, y no se hace una vez. Lee un aviso entero:

- **`PYSEC-2026-1472`**: el identificador del aviso en la base de datos de Python. El mismo fallo tiene un **CVE** (`CVE-2024-56201`, el catálogo general) y un **GHSA** (el de GitHub);
- **`Fixed in: 3.1.5`**: la primera versión sin el fallo;
- **el enlace**: qué pasa, a quién afecta y en qué condiciones. "Sandbox breakout" solo te afecta si ejecutas plantillas de Jinja escritas por otros; tu decisión depende de eso, no solo del título.

`echo $?` dice `1`: con avisos, `uv audit` termina con error, y en la CI el job falla. `no adverse project statuses`: ninguno de tus paquetes está marcado como archivado o abandonado por su autor.

El mismo informe, para un programa:

```bash
uv audit --preview-features audit-command --output-format json | python -m json.tool | head -20
```

```
{
    "schema": {
        "version": "preview"
    },
    "summary": {
        "audited_packages": 7,
        "vulnerabilities": 13,
        "adverse_statuses": 0
    },
    "vulnerabilities": [
        {
            "dependency": {
                "name": "jinja2",
                "version": "3.1.4"
            },
            "id": "GHSA-cpwx-vrp4-4pq7",
            "display_id": "PYSEC-2026-1471",
            "aliases": [
                "CVE-2025-27516",
                "PYSEC-2026-1471"
...
```

`--preview-features audit-command` quita el aviso de "experimental". Lo usarás así en tu CI.

### 4. Actualizar las directas

Primero, qué hay más nuevo:

```bash
uv tree --outdated
```

```
auditar-dependencias v0.1.0
├── jinja2 v3.1.4 (latest: v3.1.6)
│   └── markupsafe v3.0.4
└── requests v2.32.3 (latest: v2.34.2)
    ├── certifi v2026.10.23
    ├── charset-normalizer v3.5.2
    ├── idna v3.20
    └── urllib3 v2.2.3 (latest: v2.8.0)
```

Antes de fijar una versión, haz lo de siempre (`docs/stack-versions.md`): ¿cuándo salió?, ¿tiene avisos? `jinja2 3.1.6` es de marzo de 2025 y `requests 2.34.2` de mayo de 2026. Actualiza las dos:

```bash
uv add jinja2==3.1.6 requests==2.34.2
uv audit --preview-features audit-command
```

```
Resolved 8 packages in 314ms
 - jinja2==3.1.4
 + jinja2==3.1.6
 - requests==2.32.3
 + requests==2.34.2
...
Found 8 known vulnerabilities and no adverse project statuses in 7 packages
...
urllib3 2.2.3 has 8 known vulnerabilities:
```

`uv add` cambia la versión en `pyproject.toml` y en `uv.lock`, e instala. Quedan los 8 de `urllib3`, que no está en tu `pyproject.toml`.

### 5. Actualizar una transitiva

Una transitiva se actualiza en `uv.lock`, sin añadirla a `pyproject.toml`:

```bash
uv lock --upgrade-package urllib3
uv tree --invert --package urllib3
```

```
Resolved 8 packages in 325ms
urllib3 v2.2.3
└── requests v2.34.2
    └── auditar-dependencias v0.1.0
```

Sigue en `2.2.3`: `constraint-dependencies` en `[tool.uv]` lo sujeta. Una restricción (*constraint*) no instala nada, pero limita la versión de un paquete si alguien lo pide; a veces la necesitas, por ejemplo para esquivar una versión rota, y si se te olvida quitarla, te deja con los fallos viejos. Borra de `pyproject.toml` el comentario y la línea `constraint-dependencies = ["urllib3==2.2.3"]`, y:

```bash
uv lock
uv tree --invert --package urllib3
```

Sigue en `2.2.3`. `uv lock` **no actualiza** lo que ya está en `uv.lock` si sigue siendo válido: así, añadir una dependencia no te cambia las demás por sorpresa. Para actualizar, hay que pedirlo:

```bash
uv lock --upgrade-package urllib3
uv audit --preview-features audit-command
echo $?
```

```
Resolved 8 packages in 60ms
Updated urllib3 v2.2.3 -> v2.8.0
...
Found no known vulnerabilities and no adverse project statuses in 7 packages
0
```

`uv lock --upgrade` actualiza **todo** dentro de los rangos. Es cómodo, pero un cambio a la vez es más fácil de revisar, y de deshacer si algo se rompe. Ejecuta `uv run python main.py` y compara el paso 1 con el del principio.

### 6. Ignorar un aviso, sabiendo lo que haces

Vuelve a la versión vieja de `requests` para ver cómo se ignora un aviso concreto:

```bash
uv add requests==2.32.3
uv audit --preview-features audit-command --ignore PYSEC-2026-2275
```

```
...
Found 1 known vulnerability and no adverse project statuses in 7 packages
...
requests 2.32.3 has 1 known vulnerability:

- PYSEC-2026-1872: Requests vulnerable to .netrc credentials leak via malicious URLs
...
```

`PYSEC-2026-2275` es el fichero temporal de `extract_zipped_paths()`; si nunca usas esa función, puede que no te afecte. Ignorarlo es una **decisión**: escríbela donde la vea quien venga detrás (en el *pull request* o junto a la orden en la CI), con el motivo y una fecha para revisarla. `--ignore-until-fixed` es más prudente: ignora el aviso **solo mientras no haya arreglo**. Este ya lo tiene (`2.33.0`), así que no lo ignora:

```bash
uv audit --preview-features audit-command --ignore-until-fixed PYSEC-2026-2275
```

```
...
Found 2 known vulnerabilities and no adverse project statuses in 7 packages
...
```

Deja `requests` en `2.34.2` (`uv add requests==2.34.2`) y comprueba que `uv audit` vuelve a dar 0.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `uv audit` tarda o falla con un error de red | Consulta `https://api.osv.dev`: necesita Internet |
| `error: unrecognized subcommand 'audit'` | Tu uv es anterior a la del bootcamp: `uv self update` o la versión de `docs/stack-versions.md` |
| Salen más avisos que en el README | Normal: la base de datos crece. Lo que importa es que tras los pasos 4 y 5 no quede ninguno |
| `uv add` dice `No solution found when resolving dependencies` | Una versión no existe o choca con otra: revisa el número en PyPI |
| `urllib3` no sube del 2.2.3 | Queda la línea `constraint-dependencies`, o usaste `uv lock` sin `--upgrade-package urllib3` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Integración continua con GitHub Actions](../ejercicio-02-integracion-continua-con-github-actions/README.md) | **Ejercicio 03 · Auditar dependencias** | [Ejercicio 04 · Una imagen Docker segura](../ejercicio-04-una-imagen-docker-segura/README.md) |
