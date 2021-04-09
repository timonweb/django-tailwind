.PHONY: docs

docs:
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html
