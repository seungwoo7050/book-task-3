PYTHON := python3
PYTHONPATH := ../python/src

.PHONY: test run-demo clean

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest ../python/tests -q

run-demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) script/run_demo.py

clean:
	find .. -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find .. -name '*.pyc' -delete 2>/dev/null || true
