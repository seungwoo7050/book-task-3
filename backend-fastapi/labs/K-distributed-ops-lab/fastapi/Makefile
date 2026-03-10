PYTHON ?= python3

.PHONY: install run lint test smoke

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install fastapi httpx "PyJWT[crypto]" pydantic-settings redis sqlalchemy uvicorn email-validator argon2-cffi pytest ruff websockets

run:
	docker compose up --build

lint:
	$(PYTHON) -m ruff check gateway/app gateway/tests services/identity-service/app services/identity-service/tests services/workspace-service/app services/workspace-service/tests services/notification-service/app services/notification-service/tests tests

test:
	$(MAKE) -C gateway test
	$(MAKE) -C services/identity-service test
	$(MAKE) -C services/workspace-service test
	$(MAKE) -C services/notification-service test
	$(PYTHON) -m pytest tests

smoke:
	$(PYTHON) -m tests.smoke
