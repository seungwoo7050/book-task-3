CXX = g++
CXXFLAGS = -std=c++20 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_bomb
TEST_BIN = $(BUILD_DIR)/test_mini_bomb

.PHONY: all test run clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.cpp src/mini_bomb.cpp include/mini_bomb.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(BIN) src/main.cpp src/mini_bomb.cpp

$(TEST_BIN): tests/test_mini_bomb.cpp src/mini_bomb.cpp include/mini_bomb.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(TEST_BIN) tests/test_mini_bomb.cpp src/mini_bomb.cpp

test: $(BIN) $(TEST_BIN)
	./$(TEST_BIN)

run: $(BIN)
	@if [ -f data/solutions.txt ]; then \
		./$(BIN) data/solutions.txt; \
	else \
		echo "create cpp/data/solutions.txt first or run the binary with a custom file."; \
		exit 1; \
	fi

clean:
	rm -rf $(BUILD_DIR)
