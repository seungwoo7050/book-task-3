#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#include "memlib.h"

#define MAX_HEAP (1 << 28)

static char *heap_start = NULL;
static char *heap_brk = NULL;
static char *heap_limit = NULL;

void mem_init(void)
{
    heap_start = (char *)malloc(MAX_HEAP);
    if (heap_start == NULL) {
        fprintf(stderr, "mem_init: malloc failed\n");
        exit(1);
    }
    heap_brk = heap_start;
    heap_limit = heap_start + MAX_HEAP;
}

void mem_deinit(void)
{
    if (heap_start != NULL) {
        free(heap_start);
    }
    heap_start = NULL;
    heap_brk = NULL;
    heap_limit = NULL;
}

void mem_reset_brk(void)
{
    heap_brk = heap_start;
}

void *mem_sbrk(int incr)
{
    char *old_brk = heap_brk;

    if (incr < 0 || heap_brk + incr > heap_limit) {
        errno = ENOMEM;
        fprintf(stderr, "ERROR: mem_sbrk failed. Ran out of memory...\n");
        return (void *)-1;
    }

    heap_brk += incr;
    return (void *)old_brk;
}

void *mem_heap_lo(void)
{
    return (void *)heap_start;
}

void *mem_heap_hi(void)
{
    return (void *)(heap_brk - 1);
}

size_t mem_heapsize(void)
{
    return (size_t)(heap_brk - heap_start);
}
