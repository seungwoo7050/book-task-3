PYTHON := python3
PYTHONPATH := ../python/src
TRACE := data/belady.trace
FRAMES := 3

.PHONY: test run-demo clean

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest ../python/tests -q

run-demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m os_virtual_memory --trace $(TRACE) --frames $(FRAMES) --policy all --replay

clean:
	find .. -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find .. -name '*.pyc' -delete 2>/dev/null || true
