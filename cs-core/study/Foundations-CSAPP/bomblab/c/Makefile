CC = gcc
CFLAGS = -std=c11 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_bomb
TEST_BIN = $(BUILD_DIR)/test_mini_bomb

.PHONY: all test run clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.c src/mini_bomb.c include/mini_bomb.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(BIN) src/main.c src/mini_bomb.c

$(TEST_BIN): tests/test_mini_bomb.c src/mini_bomb.c include/mini_bomb.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(TEST_BIN) tests/test_mini_bomb.c src/mini_bomb.c

test: $(BIN) $(TEST_BIN)
	./$(TEST_BIN)

run: $(BIN)
	@if [ -f data/solutions.txt ]; then \
		./$(BIN) data/solutions.txt; \
	else \
		echo "create c/data/solutions.txt first or run the binary with a custom file."; \
		exit 1; \
	fi

clean:
	rm -rf $(BUILD_DIR)
