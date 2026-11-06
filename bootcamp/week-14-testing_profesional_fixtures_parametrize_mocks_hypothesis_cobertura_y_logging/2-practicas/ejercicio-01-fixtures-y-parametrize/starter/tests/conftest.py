# conftest.py: pytest lo carga antes que los tests de esta carpeta. Sus fixtures
# valen en todos los archivos test_*.py sin importarlas.
from pathlib import Path

import pytest


# ============================================
# PASO 4: Una fixture compartida en conftest.py
# ============================================
# Descomenta las siguientes líneas:
# @pytest.fixture
# def sample_file(tmp_path: Path) -> Path:
#     path = tmp_path / "norte.txt"
#     path.write_text("Norte\n12,5\nNA\n8\n", encoding="utf-8")
#     return path
