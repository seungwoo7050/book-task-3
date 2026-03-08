CXX = g++
CXXFLAGS = -Wall -Wextra -Werror -std=c++20 -D_POSIX_C_SOURCE=200809L -g -Iinclude

TARGET = build/tsh
SRCS = src/tsh.cpp
OBJS = $(SRCS:src/%.cpp=build/%.o)

.PHONY: all clean test

all: $(TARGET)

build:
	mkdir -p build

$(TARGET): build $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS)

build/%.o: src/%.cpp include/tsh_helper.hpp | build
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -rf build

test: $(TARGET)
	bash tests/run_tests.sh ./build/tsh
