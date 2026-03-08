CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c99 -O2 -g -D_POSIX_C_SOURCE=200809L

TARGET = mdriver
OBJS = code/mm.o code/memlib.o script/mdriver.o

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

code/mm.o: code/mm.c code/mm.h code/memlib.h
	$(CC) $(CFLAGS) -c -o $@ $<

code/memlib.o: code/memlib.c code/memlib.h
	$(CC) $(CFLAGS) -c -o $@ $<

script/mdriver.o: script/mdriver.c code/mm.h code/memlib.h
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(TARGET) $(OBJS) *~
