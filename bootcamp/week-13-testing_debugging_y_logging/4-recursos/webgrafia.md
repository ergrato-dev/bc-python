# 🌐 Webgrafía - Semana 13

## Documentación Oficial

### pytest

- **Documentación Oficial**: [docs.pytest.org](https://docs.pytest.org/)
- **API Reference**: [docs.pytest.org/en/stable/reference/reference.html](https://docs.pytest.org/en/stable/reference/reference.html)
- **Fixtures Reference**: [docs.pytest.org/en/stable/reference/fixtures.html](https://docs.pytest.org/en/stable/reference/fixtures.html)
- **Plugins Index**: [docs.pytest.org/en/stable/reference/plugin_list.html](https://docs.pytest.org/en/stable/reference/plugin_list.html)

### unittest.mock

- **Documentación Oficial**: [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)
- **Mock Examples**: [docs.python.org/3/library/unittest.mock-examples.html](https://docs.python.org/3/library/unittest.mock-examples.html)

### pdb

- **Documentación Oficial**: [docs.python.org/3/library/pdb.html](https://docs.python.org/3/library/pdb.html)
- **Debugger Commands**: [docs.python.org/3/library/pdb.html#debugger-commands](https://docs.python.org/3/library/pdb.html#debugger-commands)

### logging

- **Documentación Oficial**: [docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)
- **Logging Cookbook**: [docs.python.org/3/howto/logging-cookbook.html](https://docs.python.org/3/howto/logging-cookbook.html)
- **Configuration**: [docs.python.org/3/library/logging.config.html](https://docs.python.org/3/library/logging.config.html)

---

## Tutoriales y Artículos

### Real Python (Testing)

- [Getting Started with Testing in Python](https://realpython.com/python-testing/)
- [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [Understanding Mock in Python](https://realpython.com/python-mock-library/)
- [Python's unittest: Writing Unit Tests](https://realpython.com/python-unittest/)

### Real Python (Debugging/Logging)

- [Python Debugging with pdb](https://realpython.com/python-debugging-pdb/)
- [Logging in Python](https://realpython.com/python-logging/)
- [Python Logging: A Stroll Through the Source Code](https://realpython.com/python-logging-source-code/)

### pytest-cov

- **Documentación**: [pytest-cov.readthedocs.io](https://pytest-cov.readthedocs.io/)
- **Coverage.py**: [coverage.readthedocs.io](https://coverage.readthedocs.io/)

---

## Herramientas Online

### Coverage

- **Codecov**: [codecov.io](https://codecov.io/) - Análisis de cobertura en CI/CD
- **Coveralls**: [coveralls.io](https://coveralls.io/) - Tracking de cobertura

### Testing Platforms

- **pytest-benchmark**: [pytest-benchmark.readthedocs.io](https://pytest-benchmark.readthedocs.io/) - Benchmarking
- **Hypothesis**: [hypothesis.readthedocs.io](https://hypothesis.readthedocs.io/) - Property-based testing

---

## Cheat Sheets

### pytest Cheat Sheet

```
# Ejecutar tests
pytest                      # Todos los tests
pytest test_file.py         # Un archivo específico
pytest -k "test_name"       # Tests que coincidan con nombre
pytest -v                   # Verbose
pytest -x                   # Parar al primer fallo

# Markers
pytest -m slow              # Solo tests marcados como slow
pytest -m "not slow"        # Excluir tests lentos

# Coverage
pytest --cov=src            # Medir cobertura
pytest --cov-report=html    # Reporte HTML
```

### pdb Cheat Sheet

```
# Comandos básicos
n (next)      - Siguiente línea
s (step)      - Entrar en función
c (continue)  - Continuar hasta siguiente breakpoint
q (quit)      - Salir del debugger

# Inspección
p <expr>      - Imprimir expresión
pp <expr>     - Pretty print
l (list)      - Mostrar código alrededor
w (where)     - Stack trace

# Breakpoints
b <line>      - Breakpoint en línea
b <func>      - Breakpoint en función
cl            - Limpiar breakpoints
```

### logging Levels

```
DEBUG    - Información detallada para diagnóstico
INFO     - Confirmación de que todo funciona
WARNING  - Algo inesperado pero el programa sigue
ERROR    - Problema serio, alguna función falló
CRITICAL - Error grave, el programa puede terminar
```

---

## Blogs y Recursos Adicionales

- **Martin Fowler - Testing Pyramid**: [martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html)
- **pytest Tips and Tricks**: [pythontesting.net](https://pythontesting.net/)
- **Better Python Debugging**: [realpython.com/python-debugging-pdb/](https://realpython.com/python-debugging-pdb/)

---

> 💡 **Recomendación**: Guarda esta página como referencia rápida durante el desarrollo de tus proyectos.
