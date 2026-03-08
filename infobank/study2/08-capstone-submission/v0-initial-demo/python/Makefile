UV_PYTHON ?= python3.12
PYTHONPATH_ENV := PYTHONPATH=backend/src
UV_RUN := UV_PYTHON=$(UV_PYTHON) $(PYTHONPATH_ENV) uv run

.PHONY: backend-install init-db seed-demo run-backend test-backend lint-backend mypy-backend \
	frontend-install run-frontend test-frontend \
	chat replay evaluate-golden report compare preflight demo-proof-llm demo-proof-heuristic \
	gate-mp1 gate-mp2 gate-mp3 gate-mp4 gate-mp5 gate-all

backend-install:
	UV_PYTHON=$(UV_PYTHON) uv sync --extra dev

init-db:
	$(UV_RUN) python -m cli.main init-db

seed-demo:
	$(UV_RUN) python -m cli.main seed-demo

run-backend:
	$(UV_RUN) uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

test-backend:
	$(UV_RUN) pytest -q

lint-backend:
	$(UV_RUN) ruff check backend/src tests

mypy-backend:
	$(UV_RUN) mypy backend/src

frontend-install:
	cd ../react && pnpm install

run-frontend:
	cd ../react && pnpm dev

test-frontend:
	cd ../react && pnpm test --run

chat:
	$(UV_RUN) python -m cli.main chat "$(MSG)"

replay:
	$(UV_RUN) python -m cli.main replay --fixture backend/data/fixtures/replay_sessions.yaml

evaluate-golden:
	$(UV_RUN) python -m cli.main evaluate --golden-set

report:
	$(UV_RUN) python -m cli.main report --format table

compare:
	$(UV_RUN) python -m cli.main compare --baseline v1.0 --candidate v1.1

preflight:
	$(UV_RUN) python -m cli.main preflight

demo-proof-llm:
	$(UV_RUN) python -m cli.main demo-proof --mode llm

demo-proof-heuristic:
	$(UV_RUN) python -m cli.main demo-proof --mode heuristic

gate-mp1:
	./scripts/verify_mp_integrity.sh mp1

gate-mp2:
	./scripts/verify_mp_integrity.sh mp2

gate-mp3:
	./scripts/verify_mp_integrity.sh mp3

gate-mp4:
	./scripts/verify_mp_integrity.sh mp4

gate-mp5:
	./scripts/verify_mp_integrity.sh mp5

gate-all:
	./scripts/verify_mp_integrity.sh all
