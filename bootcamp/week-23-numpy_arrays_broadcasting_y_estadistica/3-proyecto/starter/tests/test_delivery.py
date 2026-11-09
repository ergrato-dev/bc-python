"""Tests de la semana 21: cómo se comprueba y se entrega el Observatorio.

No ejecutan el Observatorio: leen los archivos que lo comprueban y lo empaquetan
(.pre-commit-config.yaml, el workflow de la CI, Dependabot, el Dockerfile y compose.yaml)
y comprueban sus reglas: versiones fijadas a un SHA o a un digest, permisos mínimos,
un usuario sin privilegios... Si alguien relaja una regla sin darse cuenta, falla aquí,
en tu máquina, antes que en producción.
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parent.parent
PRE_COMMIT = ROOT / ".pre-commit-config.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"

# Un SHA de commit completo (40 caracteres hexadecimales) y un digest de imagen.
SHA = re.compile(r"[0-9a-f]{40}")
DIGEST = re.compile(r"[^@\s]+:[^@\s]+@sha256:[0-9a-f]{64}")


def read_yaml(path: Path) -> dict[Any, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path.name} no es un diccionario YAML"
    return data


# --- pre-commit -----------------------------------------------------------------------


def repos() -> list[dict[str, Any]]:
    found = read_yaml(PRE_COMMIT)["repos"]
    assert isinstance(found, list)
    return found


def hooks_of(repo: str) -> dict[str, dict[str, Any]]:
    return {
        hook["id"]: hook for entry in repos() if entry["repo"] == repo for hook in entry["hooks"]
    }


def test_pre_commit_config_is_valid() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pre_commit", "validate-config", str(PRE_COMMIT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_remote_hooks_are_pinned_to_a_commit_sha() -> None:
    remote = [entry for entry in repos() if entry["repo"] not in ("local", "meta")]
    assert remote
    for entry in remote:
        assert SHA.fullmatch(entry["rev"]), f"{entry['repo']}: rev {entry['rev']!r}"


def test_each_pinned_rev_says_its_version() -> None:
    # El SHA no se lee: el comentario `# frozen: vX` dice a qué versión corresponde.
    text = PRE_COMMIT.read_text(encoding="utf-8")
    for entry in repos():
        if entry["repo"] != "local":
            assert re.search(rf"rev: {entry['rev']}\s+# frozen: v?\d+\.\d+\.\d+", text)


def test_generic_hooks() -> None:
    hooks = hooks_of("https://github.com/pre-commit/pre-commit-hooks")
    assert set(hooks) == {
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-yaml",
        "check-toml",
        "check-added-large-files",
        "detect-private-key",
    }


def test_local_hooks_are_the_project_tools() -> None:
    assert list(hooks_of("local")) == ["ruff-check", "ruff-format", "mypy", "uv-lock"]


def test_local_hooks_use_the_locked_versions() -> None:
    # `uv run --locked`: la versión de uv.lock, la misma que en tu terminal y en la CI.
    entries = {hook_id: hook["entry"] for hook_id, hook in hooks_of("local").items()}
    assert entries == {
        "ruff-check": "uv run --locked ruff check --fix",
        "ruff-format": "uv run --locked ruff format",
        "mypy": "uv run --locked mypy",
        "uv-lock": "uv lock --check",
    }


def test_local_hooks_use_the_current_language_name() -> None:
    # Desde pre-commit 4.4, `unsupported` es el nombre nuevo de `system`.
    assert {hook["language"] for hook in hooks_of("local").values()} == {"unsupported"}


def test_python_hooks_only_see_python_files() -> None:
    hooks = hooks_of("local")
    for hook_id in ("ruff-check", "ruff-format", "mypy"):
        assert hooks[hook_id]["types"] == ["python"]


def test_mypy_checks_the_whole_project() -> None:
    # Sin nombres de archivo, mypy revisa las carpetas de [tool.mypy] files.
    assert hooks_of("local")["mypy"]["pass_filenames"] is False


def test_uv_lock_hook_runs_only_when_the_dependencies_change() -> None:
    hook = hooks_of("local")["uv-lock"]
    pattern = re.compile(hook["files"])
    assert pattern.search("pyproject.toml")
    assert pattern.search("uv.lock")
    assert not pattern.search("src/observatorio/cli.py")
    assert not pattern.search("docs/pyproject.toml.md")
    assert hook["pass_filenames"] is False


# --- GitHub Actions -------------------------------------------------------------------


def workflow() -> dict[Any, Any]:
    return read_yaml(WORKFLOW)


def triggers() -> dict[str, Any]:
    # En YAML 1.1, `on` sin comillas es el booleano True: PyYAML lo lee así.
    data = workflow()
    found = data.get("on", data.get(True))
    assert isinstance(found, dict)
    return found


def jobs() -> dict[str, dict[str, Any]]:
    found = workflow()["jobs"]
    assert isinstance(found, dict)
    return found


def steps() -> list[dict[str, Any]]:
    return [step for job in jobs().values() for step in job["steps"]]


def runs_of(job: str) -> list[str]:
    return [" ".join(step["run"].split()) for step in jobs()[job]["steps"] if "run" in step]


def test_ci_runs_on_push_to_main_and_on_pull_requests() -> None:
    assert set(triggers()) == {"push", "pull_request"}
    assert triggers()["push"] == {"branches": ["main"]}


def test_ci_never_uses_pull_request_target() -> None:
    # pull_request_target ejecuta código del pull request con los secretos del repositorio.
    assert "pull_request_target" not in WORKFLOW.read_text(encoding="utf-8")


def test_token_can_only_read_the_repository() -> None:
    assert workflow()["permissions"] == {"contents": "read"}
    for name, job in jobs().items():
        assert "permissions" not in job, f"{name} amplía los permisos"


def test_a_new_push_cancels_the_previous_run() -> None:
    concurrency = workflow()["concurrency"]
    assert "github.ref" in concurrency["group"]
    assert concurrency["cancel-in-progress"] is True


def test_uv_never_changes_the_lock_in_ci() -> None:
    assert workflow()["env"] == {"UV_LOCKED": "1"}


def test_three_jobs() -> None:
    assert list(jobs()) == ["quality", "tests", "image"]


def test_every_job_has_a_timeout_and_a_fixed_runner() -> None:
    for name, job in jobs().items():
        assert 0 < job["timeout-minutes"] <= 30, name
        assert job["runs-on"] == "ubuntu-24.04", name


def test_every_action_is_pinned_to_a_commit_sha() -> None:
    uses = [step["uses"] for step in steps() if "uses" in step]
    assert uses
    for action in uses:
        name, _, ref = action.partition("@")
        assert "/" in name and SHA.fullmatch(ref), action


def test_each_pinned_action_says_its_version() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    for step in steps():
        if "uses" in step:
            assert re.search(rf"{re.escape(step['uses'])} # v\d+\.\d+\.\d+", text)


def test_checkout_does_not_keep_the_token() -> None:
    checkouts = [step for step in steps() if step.get("uses", "").startswith("actions/checkout@")]
    assert len(checkouts) == len(jobs())
    for step in checkouts:
        assert step["with"]["persist-credentials"] is False


def test_ci_uses_the_uv_of_the_dockerfile() -> None:
    uv_tag = stage("uv").base.split("@")[0].split(":")[1]
    setups = [step for step in steps() if step.get("uses", "").startswith("astral-sh/setup-uv@")]
    assert len(setups) == 2
    for step in setups:
        assert step["with"]["version"] == uv_tag


def test_quality_runs_pre_commit_and_audits_the_dependencies() -> None:
    assert runs_of("quality") == [
        "uv sync",
        "uv run pre-commit run --all-files --show-diff-on-failure",
        "uv audit --preview-features audit-command",
    ]


def test_tests_run_against_the_postgresql_of_compose() -> None:
    service = jobs()["tests"]["services"]["db"]
    assert service["image"] == compose()["services"]["db"]["image"]
    assert service["env"] == compose()["services"]["db"]["environment"]
    assert service["ports"] == ["5432:5432"]
    assert "--health-cmd" in service["options"]


def test_tests_run_without_terminal_colors() -> None:
    assert jobs()["tests"]["env"]["TERM"] == "dumb"


def test_tests_measure_coverage_and_check_the_migrations() -> None:
    assert runs_of("tests") == [
        "uv sync",
        "uv run coverage run -m pytest",
        "uv run coverage report",
        "uv run alembic upgrade head",
        "uv run alembic check",
    ]


def test_image_job_builds_runtime_and_scans_it() -> None:
    build, smoke, scan = runs_of("image")
    assert build == "docker build --target runtime --tag observatorio:ci ."
    assert smoke == "docker run --rm observatorio:ci observatorio --version"
    assert "trivy" in scan
    assert "--exit-code 1" in scan
    assert "--severity HIGH,CRITICAL" in scan
    assert scan.endswith(" observatorio:ci")


def test_ci_images_are_pinned_by_digest() -> None:
    images = [jobs()["tests"]["services"]["db"]["image"]]
    images += re.findall(r"aquasec/trivy\S*", " ".join(runs_of("image")))
    assert len(images) == 2
    for image in images:
        assert DIGEST.fullmatch(image), image


# --- Dependabot -----------------------------------------------------------------------


def test_dependabot_watches_the_three_ecosystems() -> None:
    updates = read_yaml(DEPENDABOT)["updates"]
    assert [update["package-ecosystem"] for update in updates] == [
        "uv",
        "github-actions",
        "docker",
    ]
    for update in updates:
        assert update["directory"] == "/"
        assert update["schedule"] == {"interval": "weekly"}


def test_dependabot_waits_a_week_after_each_release() -> None:
    for update in read_yaml(DEPENDABOT)["updates"]:
        assert update["cooldown"]["default-days"] >= 7


def test_dependabot_only_proposes_python_patches() -> None:
    docker = read_yaml(DEPENDABOT)["updates"][2]
    assert docker["ignore"] == [
        {
            "dependency-name": "python",
            "update-types": ["version-update:semver-major", "version-update:semver-minor"],
        }
    ]


# --- Dockerfile -----------------------------------------------------------------------


@dataclass
class Stage:
    name: str
    base: str
    instructions: list[str] = field(default_factory=list)

    def lines(self, keyword: str) -> list[str]:
        prefix = keyword + " "
        return [line.removeprefix(prefix) for line in self.instructions if line.startswith(prefix)]


def stages() -> list[Stage]:
    # Une las líneas que acaban en `\`, deja un solo espacio entre palabras y se salta
    # comentarios y líneas vacías.
    text = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    logical = text.replace("\\\n", " ")
    found: list[Stage] = []
    for line in logical.splitlines():
        line = " ".join(line.split())
        if not line or line.startswith("#"):
            continue
        if line.startswith("FROM "):
            base, _, name = line.removeprefix("FROM ").partition(" AS ")
            found.append(Stage(name, base))
        else:
            found[-1].instructions.append(line)
    return found


def stage(name: str) -> Stage:
    return next(found for found in stages() if found.name == name)


def test_dockerfile_stages() -> None:
    # runtime, la última: es la que construye `docker build .` sin --target.
    assert [found.name for found in stages()] == ["uv", "builder", "test", "runtime"]


def test_external_base_images_are_pinned_by_digest() -> None:
    names = {found.name for found in stages()}
    for found in stages():
        if found.base not in names:
            assert DIGEST.fullmatch(found.base), found.base
            assert ":latest" not in found.base


def test_builder_and_runtime_use_the_same_python() -> None:
    assert stage("builder").base == stage("runtime").base
    assert stage("test").base == "builder"


def test_builder_installs_without_development_dependencies() -> None:
    syncs = [line for line in stage("builder").lines("RUN") if "uv sync" in line]
    assert syncs == [
        "uv sync --locked --no-dev --no-install-project",
        "uv sync --locked --no-dev --no-editable",
    ]


def test_runtime_copies_only_the_environment() -> None:
    assert stage("runtime").lines("COPY") == ["--from=builder /opt/venv /opt/venv"]


def test_runtime_has_no_uv() -> None:
    for line in stage("runtime").instructions:
        assert "--from=uv" not in line
        assert not re.search(r"\buvx?\b", line), line


def test_runtime_applies_security_updates_and_removes_pip() -> None:
    (run,) = stage("runtime").lines("RUN")
    assert "apt-get update && apt-get upgrade --yes" in run
    assert "rm -rf /var/lib/apt/lists/*" in run
    assert "/usr/local/bin/pip*" in run
    assert "/usr/local/lib/python3.14/site-packages/pip " in run


def unprivileged(user: str) -> bool:
    uid, _, gid = user.partition(":")
    return uid.isdigit() and int(uid) >= 1000 and gid.isdigit() and int(gid) >= 1000


def test_runtime_runs_as_an_unprivileged_numeric_user() -> None:
    users = stage("runtime").lines("USER")
    assert len(users) == 1
    assert unprivileged(users[0]), users[0]


def test_tests_run_as_an_unprivileged_user() -> None:
    assert [unprivileged(user) for user in stage("test").lines("USER")] == [True]


def test_runtime_serves_by_default() -> None:
    (command,) = stage("runtime").lines("CMD")
    assert json.loads(command) == ["observatorio", "servir", "--host", "0.0.0.0"]
    assert stage("runtime").lines("EXPOSE") == ["8000"]


def test_test_stage_runs_pytest() -> None:
    (command,) = stage("test").lines("CMD")
    assert json.loads(command) == ["pytest"]


def test_secrets_and_git_stay_out_of_the_image() -> None:
    ignored = (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
    assert ".env" in ignored
    assert ".git/" in ignored


# --- compose.yaml ---------------------------------------------------------------------


def compose() -> dict[Any, Any]:
    return read_yaml(ROOT / "compose.yaml")


def test_app_builds_the_test_stage() -> None:
    app = compose()["services"]["app"]
    assert app["build"] == {"context": ".", "target": "test"}
    assert app["image"] == "local/observatorio:week-23-test"


def test_api_builds_the_runtime_stage() -> None:
    api = compose()["services"]["api"]
    assert api["build"] == {"context": ".", "target": "runtime"}
    assert api["image"] == "local/observatorio:week-23"
    assert "command" not in api


def test_api_cannot_write_its_own_image() -> None:
    api = compose()["services"]["api"]
    assert api["read_only"] is True
    assert api["tmpfs"] == ["/tmp"]


def test_api_has_no_privileges() -> None:
    api = compose()["services"]["api"]
    assert api["cap_drop"] == ["ALL"]
    assert api["security_opt"] == ["no-new-privileges:true"]
    assert "privileged" not in api


def test_ports_only_open_to_this_machine() -> None:
    for name, service in compose()["services"].items():
        for port in service.get("ports", []):
            assert port.startswith("127.0.0.1:"), f"{name}: {port}"


def test_postgresql_image_is_pinned_by_digest() -> None:
    assert DIGEST.fullmatch(compose()["services"]["db"]["image"])
