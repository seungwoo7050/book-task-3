/*
 * cachelab.h - Helper declarations for Performance Lab.
 */

#ifndef CACHELAB_H
#define CACHELAB_H

void printSummary(int hits, int misses, int evictions);
typedef void (*trans_func_t)(int M, int N, int A[N][M], int B[M][N]);
void registerTransFunction(trans_func_t func, const char *desc);

#endif
