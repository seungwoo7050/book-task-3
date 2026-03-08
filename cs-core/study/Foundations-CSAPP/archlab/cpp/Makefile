CXX = g++
CXXFLAGS = -std=c++20 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_archlab
TEST_BIN = $(BUILD_DIR)/test_mini_archlab

.PHONY: all test sample clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.cpp src/mini_archlab.cpp include/mini_archlab.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(BIN) src/main.cpp src/mini_archlab.cpp

$(TEST_BIN): tests/test_mini_archlab.cpp src/mini_archlab.cpp include/mini_archlab.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(TEST_BIN) tests/test_mini_archlab.cpp src/mini_archlab.cpp

test: $(BIN) sample $(TEST_BIN)
	./$(TEST_BIN)

sample: $(BIN)
	./$(BIN)

clean:
	rm -rf $(BUILD_DIR)
