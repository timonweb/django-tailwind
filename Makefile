.PHONY: docs

docs:
	uv run --group docs sphinx-build -b html -d docs/_build/doctrees docs docs/_build/html
