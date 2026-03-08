#ifndef PERFLAB_H
#define PERFLAB_H

#include <stdint.h>

typedef struct {
    int hits;
    int misses;
    int evictions;
} PerfStats;

typedef struct {
    int correct;
    int misses;
    int evictions;
} TransposeResult;

typedef struct {
    int valid;
    uint64_t tag;
    uint64_t lru;
} DirectMappedLine;

typedef struct {
    PerfStats stats;
    uint64_t clock;
    DirectMappedLine lines[32];
} TransposeCache;

typedef void (*transpose_kernel_t)(int M, int N, const int *A, int *B, TransposeCache *cache);

void perflab_run_trace_file(const char *tracefile, int s, int E, int b, int verbose, PerfStats *out);
void perflab_transpose_naive(int M, int N, const int *A, int *B, TransposeCache *cache);
void perflab_transpose_submit(int M, int N, const int *A, int *B, TransposeCache *cache);
int perflab_is_transpose(int M, int N, const int *A, const int *B);
TransposeResult perflab_measure_transpose(int M, int N, transpose_kernel_t kernel);

#endif
