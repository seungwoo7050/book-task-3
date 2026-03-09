PYTHON ?= python3

.PHONY: install run lint test smoke

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e ".[dev]"

run:
	uvicorn app.main:app --reload

lint:
	ruff check app tests

test:
	pytest

smoke:
	$(PYTHON) -m tests.smoke
