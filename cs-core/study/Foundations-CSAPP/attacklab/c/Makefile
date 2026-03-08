CC = gcc
CFLAGS = -std=c11 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_attacklab
TEST_BIN = $(BUILD_DIR)/test_mini_attacklab

.PHONY: all test samples clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.c src/mini_attacklab.c include/mini_attacklab.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(BIN) src/main.c src/mini_attacklab.c

$(TEST_BIN): tests/test_mini_attacklab.c src/mini_attacklab.c include/mini_attacklab.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $(TEST_BIN) tests/test_mini_attacklab.c src/mini_attacklab.c

test: $(BIN) $(TEST_BIN) samples
	./$(TEST_BIN)

samples: $(BIN)
	@for phase in 1 2 3 4 5; do ./$(BIN) $$phase data/phase$$phase.txt; done

clean:
	rm -rf $(BUILD_DIR)
