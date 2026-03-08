/*
 * cachelab.c - Helper definitions for Performance Lab.
 */

#include <stdio.h>

#include "cachelab.h"

void printSummary(int hits, int misses, int evictions)
{
    printf("hits:%d misses:%d evictions:%d\n", hits, misses, evictions);
}

static trans_func_t funcs[100];
static const char *descs[100];
static int num_funcs = 0;

void registerTransFunction(trans_func_t func, const char *desc)
{
    funcs[num_funcs] = func;
    descs[num_funcs] = desc;
    num_funcs += 1;
}
