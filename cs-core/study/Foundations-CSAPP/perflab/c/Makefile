CC = gcc
CFLAGS = -std=c11 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_perflab
TEST_BIN = $(BUILD_DIR)/test_perflab

.PHONY: all test sample clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.c src/perflab.c include/perflab.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(BIN) src/main.c src/perflab.c

$(TEST_BIN): tests/test_perflab.c src/perflab.c include/perflab.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(TEST_BIN) tests/test_perflab.c src/perflab.c

test: $(BIN) sample $(TEST_BIN)
	./$(TEST_BIN)

sample: $(BIN)
	./$(BIN)

clean:
	rm -rf $(BUILD_DIR)
