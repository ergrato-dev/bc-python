# Tus tests de la semana 21: sustituye este ejemplo por al menos 6 tests tuyos (paso 15).
# Usa las funciones de test_delivery.py (compose, stage, jobs, runs_of, read_yaml...):
# que la etapa builder compile a .pyc (el reto del paso 14), que `api` espere a `db`, su
# healthcheck, que Trivy no cuente lo que no tiene arreglo, que la CI no tenga secretos
# escritos, que .dockerignore deje fuera .venv/...
from test_delivery import compose


def test_example_the_api_waits_for_a_healthy_postgresql() -> None:
    api = compose()["services"]["api"]
    assert api["depends_on"] == {"db": {"condition": "service_healthy"}}
