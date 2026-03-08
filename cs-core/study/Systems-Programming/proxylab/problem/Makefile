CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c99 -O2 -g -D_POSIX_C_SOURCE=200809L
LDFLAGS = -lpthread

TARGET = proxy
OBJS = code/proxy.o code/csapp.o

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

code/proxy.o: code/proxy.c code/csapp.h
	$(CC) $(CFLAGS) -c -o $@ $<

code/csapp.o: code/csapp.c code/csapp.h
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(TARGET) $(OBJS) *~
