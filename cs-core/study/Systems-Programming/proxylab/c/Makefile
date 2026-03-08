CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c99 -O2 -g -D_POSIX_C_SOURCE=200809L -Iinclude -I../problem/code
LDFLAGS = -lpthread

TARGET = build/proxy
OBJS = build/proxy.o build/csapp.o

.PHONY: all clean test

all: $(TARGET)

build:
	mkdir -p build

$(TARGET): build $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

build/proxy.o: src/proxy.c ../problem/code/csapp.h | build
	$(CC) $(CFLAGS) -c -o $@ $<

build/csapp.o: ../problem/code/csapp.c ../problem/code/csapp.h | build
	$(CC) $(CFLAGS) -c -o $@ $<

test: $(TARGET)
	bash ../tests/run_proxy_tests.sh ./build/proxy

clean:
	rm -rf build
