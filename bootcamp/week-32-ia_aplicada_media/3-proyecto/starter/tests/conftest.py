import os

# client = OpenAI() at module level requiere una key — en tests, cualquier string es válido
# porque dry_run=True nunca hace llamadas reales a la API.
os.environ.setdefault("OPENAI_API_KEY", "sk-test-dry-run-no-real-calls")
