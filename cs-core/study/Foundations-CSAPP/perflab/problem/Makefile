# Performance Lab starter Makefile

CC = gcc
CFLAGS = -O0 -Wall -Werror -m64 -g
LDFLAGS = -m64

.PHONY: all status compile compile-csim compile-trans clean

all: status

status:
	@if [ -f code/csim.c ]; then echo "starter present: code/csim.c"; else echo "missing: code/csim.c"; fi
	@if [ -f code/trans.c ]; then echo "starter present: code/trans.c"; else echo "missing: code/trans.c"; fi
	@if [ -f data/traces/study.trace ]; then echo "trace present: data/traces/study.trace"; else echo "missing: data/traces/study.trace"; fi

compile: compile-csim compile-trans

compile-csim:
	$(CC) $(CFLAGS) -o csim-starter code/csim.c code/cachelab.c $(LDFLAGS)
	@echo "starter csim compile check: PASS"
	@rm -f csim-starter

compile-trans:
	$(CC) $(CFLAGS) -c -o trans-starter.o code/trans.c
	@echo "starter transpose compile check: PASS"
	@rm -f trans-starter.o

clean:
	rm -f csim-starter trans-starter.o
