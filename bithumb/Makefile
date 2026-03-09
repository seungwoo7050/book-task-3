VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
VENV_STAMP := $(VENV)/.deps-installed

UNIT_DIRS := \
	00-aws-security-foundations/01-aws-security-primitives/python \
	00-aws-security-foundations/03-cloudtrail-log-basics/python \
	01-cloud-security-core/04-iam-policy-analyzer/python \
	01-cloud-security-core/05-cspm-rule-engine/python \
	01-cloud-security-core/06-remediation-pack-runner/python \
	01-cloud-security-core/07-security-lake-mini/python \
	01-cloud-security-core/08-container-guardrails/python \
	01-cloud-security-core/09-exception-and-evidence-manager/python

INTEGRATION_DIRS := \
	00-aws-security-foundations/02-terraform-aws-lab/python

CAPSTONE_DIR := 02-capstone/10-cloud-security-control-plane/python
CAPSTONE_DB_URL ?= postgresql+psycopg://study2:study2@127.0.0.1:54340/study2_control_plane
CAPSTONE_LAKE_DIR ?= .artifacts/capstone/lake

.PHONY: venv doctor test-unit test-integration test-capstone test-all capstone-up capstone-down demo-capstone clean

$(VENV)/bin/python:
	@test -d $(VENV) || python3 -m venv $(VENV)

$(VENV_STAMP): pyproject.toml | $(VENV)/bin/python
	@find $(VENV)/lib -maxdepth 3 -name '~tudy2*' -exec rm -rf {} + >/dev/null 2>&1 || true
	@$(PIP) install --upgrade pip >/dev/null
	@$(PIP) install -e ".[dev]" >/dev/null
	@touch $(VENV_STAMP)

venv: $(VENV_STAMP)

doctor: venv
	@$(PYTHON) -c "import sys; assert sys.version_info >= (3, 13), sys.version"
	@docker --version >/dev/null
	@terraform version >/dev/null
	@echo "doctor ok"

test-unit: venv
	@set -e; \
	for dir in $(UNIT_DIRS); do \
		echo "==> $$dir"; \
		PYTHONPATH=$$dir/src $(PYTHON) -m pytest $$dir/tests; \
	done

test-integration: venv
	@set -e; \
	for dir in $(INTEGRATION_DIRS); do \
		echo "==> $$dir"; \
		PYTHONPATH=$$dir/src $(PYTHON) -m pytest $$dir/tests; \
	done

test-capstone: venv
	@mkdir -p .artifacts/capstone
	PYTHONPATH=$(CAPSTONE_DIR)/src $(PYTHON) -m pytest $(CAPSTONE_DIR)/tests

test-all: doctor test-unit test-integration test-capstone

capstone-up:
	docker compose up -d postgres
	@for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do \
		state=$$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' study2-control-plane-postgres 2>/dev/null || true); \
		if [ "$$state" = "healthy" ]; then \
			echo "postgres healthy"; \
			exit 0; \
		fi; \
		sleep 2; \
	done; \
	echo "postgres did not become healthy in time"; \
	exit 1

capstone-down:
	docker compose down

demo-capstone: venv
	@mkdir -p .artifacts/capstone
	@if [ -n "$$DATABASE_URL" ]; then \
		PYTHONPATH=$(CAPSTONE_DIR)/src DATABASE_URL="$$DATABASE_URL" CONTROL_PLANE_LAKE_DIR="$(CAPSTONE_LAKE_DIR)" $(PYTHON) $(CAPSTONE_DIR)/src/cloud_security_control_plane/demo_capture.py; \
	elif docker info >/dev/null 2>&1; then \
		$(MAKE) capstone-up; \
		PYTHONPATH=$(CAPSTONE_DIR)/src DATABASE_URL="$(CAPSTONE_DB_URL)" CONTROL_PLANE_LAKE_DIR="$(CAPSTONE_LAKE_DIR)" $(PYTHON) $(CAPSTONE_DIR)/src/cloud_security_control_plane/demo_capture.py; \
	else \
		echo "docker daemon unavailable, falling back to sqlite demo database"; \
		PYTHONPATH=$(CAPSTONE_DIR)/src DATABASE_URL="sqlite+pysqlite:///$$(pwd)/.artifacts/capstone/demo.sqlite3" CONTROL_PLANE_LAKE_DIR="$(CAPSTONE_LAKE_DIR)" $(PYTHON) $(CAPSTONE_DIR)/src/cloud_security_control_plane/demo_capture.py; \
	fi

clean:
	rm -rf $(VENV) .artifacts
