PYTHON ?= python3

.PHONY: install run lint test smoke

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e ".[dev]"

run:
	PYTHONPATH=. uvicorn app.main:app --reload --port 8000

lint:
	$(PYTHON) -m ruff check app tests

test:
	PYTHONPATH=. $(PYTHON) -m pytest

smoke:
	PYTHONPATH=. $(PYTHON) -m tests.smoke
