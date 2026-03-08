CC = gcc
CFLAGS = -std=c11 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_archlab
TEST_BIN = $(BUILD_DIR)/test_mini_archlab

.PHONY: all test sample clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.c src/mini_archlab.c include/mini_archlab.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(BIN) src/main.c src/mini_archlab.c

$(TEST_BIN): tests/test_mini_archlab.c src/mini_archlab.c include/mini_archlab.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(TEST_BIN) tests/test_mini_archlab.c src/mini_archlab.c

test: $(BIN) sample $(TEST_BIN)
	./$(TEST_BIN)

sample: $(BIN)
	./$(BIN)

clean:
	rm -rf $(BUILD_DIR)
