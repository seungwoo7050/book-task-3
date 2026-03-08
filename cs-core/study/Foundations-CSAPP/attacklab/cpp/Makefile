CXX = g++
CXXFLAGS = -std=c++20 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_attacklab
TEST_BIN = $(BUILD_DIR)/test_mini_attacklab

.PHONY: all test samples clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.cpp src/mini_attacklab.cpp include/mini_attacklab.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(BIN) src/main.cpp src/mini_attacklab.cpp

$(TEST_BIN): tests/test_mini_attacklab.cpp src/mini_attacklab.cpp include/mini_attacklab.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(TEST_BIN) tests/test_mini_attacklab.cpp src/mini_attacklab.cpp

test: $(BIN) $(TEST_BIN) samples
	./$(TEST_BIN)

samples: $(BIN)
	@for phase in 1 2 3 4 5; do ./$(BIN) $$phase data/phase$$phase.txt; done

clean:
	rm -rf $(BUILD_DIR)
