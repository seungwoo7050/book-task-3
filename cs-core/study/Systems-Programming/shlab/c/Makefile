CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c99 -D_POSIX_C_SOURCE=200809L -g -Iinclude

TARGET = build/tsh
SRCS = src/tsh.c
OBJS = $(SRCS:src/%.c=build/%.o)

.PHONY: all clean test

all: $(TARGET)

build:
	mkdir -p build

$(TARGET): build $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

build/%.o: src/%.c include/tsh_helper.h | build
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -rf build

test: $(TARGET)
	bash tests/run_tests.sh ./build/tsh
