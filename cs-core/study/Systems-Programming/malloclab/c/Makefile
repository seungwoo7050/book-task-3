CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c99 -O2 -g -D_POSIX_C_SOURCE=200809L -Iinclude -I../problem/code

TARGET = build/mdriver
OBJS = build/mm.o build/memlib.o build/driver.o

.PHONY: all clean test

all: $(TARGET)

build:
	mkdir -p build

$(TARGET): build $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

build/mm.o: src/mm.c include/mm.h include/memlib.h | build
	$(CC) $(CFLAGS) -c -o $@ $<

build/memlib.o: ../problem/code/memlib.c ../problem/code/memlib.h | build
	$(CC) $(CFLAGS) -c -o $@ $<

build/driver.o: ../problem/script/mdriver.c include/mm.h include/memlib.h | build
	$(CC) $(CFLAGS) -c -o $@ $<

test: $(TARGET)
	./build/mdriver -t ../problem/data/traces -v

clean:
	rm -rf build
