PYTHON_BOOTSTRAP := $(shell command -v python3.13 2>/dev/null || command -v python3 2>/dev/null)
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
VENV_STAMP := $(VENV)/.deps-installed

TRACK_ROOT := study/Foundations-Security
CAPSTONE_TRACK_ROOT := study/Capstone
CRYPTO_ROOT := $(TRACK_ROOT)/crypto-primitives-in-practice
AUTH_ROOT := $(TRACK_ROOT)/auth-threat-modeling
OWASP_ROOT := $(TRACK_ROOT)/owasp-backend-mitigations
DEPENDENCY_ROOT := $(TRACK_ROOT)/dependency-vulnerability-workflow
CAPSTONE_ROOT := $(CAPSTONE_TRACK_ROOT)/collab-saas-security-review

PROJECT_DIRS := \
	$(CRYPTO_ROOT) \
	$(AUTH_ROOT) \
	$(OWASP_ROOT) \
	$(DEPENDENCY_ROOT)

.PHONY: venv doctor test-unit test-capstone demo-crypto demo-auth demo-owasp demo-dependency demo-capstone clean

$(VENV)/bin/python:
	@test -n "$(PYTHON_BOOTSTRAP)" || (echo "python3.13 or python3 not found" && exit 1)
	@if [ ! -x $(VENV)/bin/python ]; then $(PYTHON_BOOTSTRAP) -m venv $(VENV); fi

$(VENV_STAMP): pyproject.toml | $(VENV)/bin/python
	@$(PIP) install --upgrade pip >/dev/null
	@$(PIP) install -e ".[dev]" >/dev/null
	@touch $(VENV_STAMP)

venv: $(VENV_STAMP)

doctor: venv
	@$(PYTHON) -c "import sys; assert sys.version_info >= (3, 13), sys.version"
	@echo "doctor ok"

test-unit: venv
	@set -e; \
	for dir in $(PROJECT_DIRS); do \
		echo "==> $$dir"; \
		PYTHONPATH=$$dir/python/src $(PYTHON) -m pytest $$dir/python/tests; \
	done

test-capstone: venv
	PYTHONPATH=$(CAPSTONE_ROOT)/python/src $(PYTHON) -m pytest $(CAPSTONE_ROOT)/python/tests

demo-crypto: venv
	PYTHONPATH=$(CRYPTO_ROOT)/python/src $(PYTHON) -m crypto_primitives_in_practice.cli demo $(CRYPTO_ROOT)/problem/data/demo_profile.json

demo-auth: venv
	PYTHONPATH=$(AUTH_ROOT)/python/src $(PYTHON) -m auth_threat_modeling.cli demo $(AUTH_ROOT)/problem/data/demo_profile.json

demo-owasp: venv
	PYTHONPATH=$(OWASP_ROOT)/python/src $(PYTHON) -m owasp_backend_mitigations.cli demo $(OWASP_ROOT)/problem/data/demo_profile.json

demo-dependency: venv
	PYTHONPATH=$(DEPENDENCY_ROOT)/python/src $(PYTHON) -m dependency_vulnerability_workflow.cli demo $(DEPENDENCY_ROOT)/problem/data/demo_profile.json

demo-capstone: venv
	rm -rf .artifacts/capstone/demo
	mkdir -p .artifacts/capstone/demo
	PYTHONPATH=$(CAPSTONE_ROOT)/python/src $(PYTHON) -m collab_saas_security_review.cli demo $(CAPSTONE_ROOT)/problem/data/demo_bundle.json

clean:
	rm -rf $(VENV) .artifacts
