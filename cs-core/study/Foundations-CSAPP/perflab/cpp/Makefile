CXX = g++
CXXFLAGS = -std=c++20 -O1 -Wall -Wextra -Werror -Iinclude
BUILD_DIR = build
BIN = $(BUILD_DIR)/mini_perflab
TEST_BIN = $(BUILD_DIR)/test_perflab

.PHONY: all test sample clean

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): src/main.cpp src/perflab.cpp include/perflab.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(BIN) src/main.cpp src/perflab.cpp

$(TEST_BIN): tests/test_perflab.cpp src/perflab.cpp include/perflab.hpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $(TEST_BIN) tests/test_perflab.cpp src/perflab.cpp

test: $(BIN) sample $(TEST_BIN)
	./$(TEST_BIN)

sample: $(BIN)
	./$(BIN)

clean:
	rm -rf $(BUILD_DIR)
