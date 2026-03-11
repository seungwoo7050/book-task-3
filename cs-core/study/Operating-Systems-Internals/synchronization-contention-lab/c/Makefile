CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -O2 -Iinclude
LDFLAGS ?= -pthread
BIN_DIR := bin
TARGET := $(BIN_DIR)/contention_lab
SRCS := src/main.c src/contention_lab.c

.PHONY: all test bench clean

all: $(TARGET)

$(TARGET): $(SRCS) include/contention_lab.h | $(BIN_DIR)
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET) $(LDFLAGS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

test: $(TARGET)
	bash tests/test_cases.sh

bench: $(TARGET)
	@echo "[counter]"
	@./$(TARGET) --scenario counter --threads 8 --iterations 20000
	@echo
	@echo "[gate]"
	@./$(TARGET) --scenario gate --threads 8 --iterations 10000
	@echo
	@echo "[buffer]"
	@./$(TARGET) --scenario buffer --threads 8 --iterations 5000

clean:
	rm -rf $(BIN_DIR)
