PYTHON   = python3
ifeq ($(origin CXX), default)
CXX := $(shell if command -v g++-14 >/dev/null 2>&1; then echo g++-14; else echo g++; fi)
endif
ifeq ($(origin CXX), undefined)
CXX := $(shell if command -v g++-14 >/dev/null 2>&1; then echo g++-14; else echo g++; fi)
endif
CXXFLAGS ?= -std=c++17 -O2 -Wall
ifeq ($(notdir $(CXX)),g++-14)
	CXXFLAGS += -D_Alignof=alignof
endif

PY_SOLUTION  = ../python/src/solution.py
CPP_SOLUTION = ../cpp/src/solution.cpp
CPP_BINARY   = ../cpp/bin/app

.PHONY: all build run-py run-cpp test clean

all: test

build:
	@mkdir -p ../cpp/bin
	@$(CXX) $(CXXFLAGS) $(CPP_SOLUTION) -o $(CPP_BINARY)

run-py:
	@$(PYTHON) $(PY_SOLUTION) < data/input1.txt

run-cpp: build
	@$(CPP_BINARY) < data/input1.txt

test:
	@cd script && bash test.sh

clean:
	@rm -f $(CPP_BINARY)
