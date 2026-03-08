PYTHON      = python3
PY_SOLUTION = ../python/src/solution.py

.PHONY: all run-py test clean

all: test

run-py:
	@$(PYTHON) $(PY_SOLUTION) < data/input1.txt

test:
	@cd script && bash test.sh

clean:
	@true
