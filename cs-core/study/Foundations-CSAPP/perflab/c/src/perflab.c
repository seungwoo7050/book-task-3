#include "perflab.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int valid;
    uint64_t tag;
    uint64_t lru;
} CacheLine;

typedef struct {
    CacheLine *lines;
} CacheSet;

typedef struct {
    int s;
    int E;
    int b;
    int S;
    uint64_t clock;
    PerfStats stats;
    CacheSet *sets;
} CacheSim;

static void cache_sim_init(CacheSim *cache, int s, int E, int b)
{
    int set_index;

    cache->s = s;
    cache->E = E;
    cache->b = b;
    cache->S = 1 << s;
    cache->clock = 1;
    cache->stats.hits = 0;
    cache->stats.misses = 0;
    cache->stats.evictions = 0;
    cache->sets = (CacheSet *)calloc((size_t)cache->S, sizeof(CacheSet));
    for (set_index = 0; set_index < cache->S; ++set_index) {
        cache->sets[set_index].lines = (CacheLine *)calloc((size_t)E, sizeof(CacheLine));
    }
}

static void cache_sim_destroy(CacheSim *cache)
{
    int set_index;

    for (set_index = 0; set_index < cache->S; ++set_index) {
        free(cache->sets[set_index].lines);
    }
    free(cache->sets);
}

static void cache_access(CacheSim *cache, uint64_t address)
{
    uint64_t set_mask = (1ULL << cache->s) - 1ULL;
    uint64_t set_index = (address >> cache->b) & set_mask;
    uint64_t tag = address >> (cache->s + cache->b);
    CacheSet *set = &cache->sets[set_index];
    int line_index;
    int empty_index = -1;
    int victim_index = 0;
    uint64_t oldest_lru = UINT64_MAX;

    for (line_index = 0; line_index < cache->E; ++line_index) {
        CacheLine *line = &set->lines[line_index];
        if (line->valid && line->tag == tag) {
            cache->stats.hits += 1;
            line->lru = cache->clock++;
            return;
        }
        if (!line->valid && empty_index < 0) {
            empty_index = line_index;
        }
        if (line->valid && line->lru < oldest_lru) {
            oldest_lru = line->lru;
            victim_index = line_index;
        }
    }

    cache->stats.misses += 1;
    if (empty_index >= 0) {
        set->lines[empty_index].valid = 1;
        set->lines[empty_index].tag = tag;
        set->lines[empty_index].lru = cache->clock++;
        return;
    }

    cache->stats.evictions += 1;
    set->lines[victim_index].tag = tag;
    set->lines[victim_index].lru = cache->clock++;
}

void perflab_run_trace_file(const char *tracefile, int s, int E, int b, int verbose, PerfStats *out)
{
    FILE *file = fopen(tracefile, "r");
    CacheSim cache;
    char op;
    unsigned long long address;
    int size;

    if (file == NULL) {
        fprintf(stderr, "could not open trace file: %s\n", tracefile);
        exit(1);
    }

    cache_sim_init(&cache, s, E, b);

    while (fscanf(file, " %c %llx,%d", &op, &address, &size) == 3) {
        if (op == 'I') {
            continue;
        }
        cache_access(&cache, (uint64_t)address);
        if (op == 'M') {
            cache_access(&cache, (uint64_t)address);
        }
        if (verbose) {
            (void)size;
        }
    }

    fclose(file);
    *out = cache.stats;
    cache_sim_destroy(&cache);
}

static void transpose_cache_init(TransposeCache *cache)
{
    memset(cache, 0, sizeof(*cache));
    cache->clock = 1;
}

static void transpose_access(TransposeCache *cache, uint64_t address)
{
    uint64_t set_index = (address >> 5) & 31ULL;
    uint64_t tag = address >> 10;
    DirectMappedLine *line = &cache->lines[set_index];

    if (line->valid && line->tag == tag) {
        cache->stats.hits += 1;
    } else {
        cache->stats.misses += 1;
        if (line->valid) {
            cache->stats.evictions += 1;
        }
        line->valid = 1;
        line->tag = tag;
    }
    line->lru = cache->clock++;
}

static uint64_t a_addr(int M, int i, int j)
{
    return (uint64_t)((i * M + j) * 4ULL);
}

static uint64_t b_addr(int N, int i, int j)
{
    return (1ULL << 20) + (uint64_t)((i * N + j) * 4ULL);
}

static int load_a(int M, const int *A, int i, int j, TransposeCache *cache)
{
    transpose_access(cache, a_addr(M, i, j));
    return A[i * M + j];
}

static int load_b(int N, const int *B, int i, int j, TransposeCache *cache)
{
    transpose_access(cache, b_addr(N, i, j));
    return B[i * N + j];
}

static void store_b(int N, int *B, int i, int j, int value, TransposeCache *cache)
{
    transpose_access(cache, b_addr(N, i, j));
    B[i * N + j] = value;
}

void perflab_transpose_naive(int M, int N, const int *A, int *B, TransposeCache *cache)
{
    int i;
    int j;

    for (i = 0; i < N; ++i) {
        for (j = 0; j < M; ++j) {
            int value = load_a(M, A, i, j, cache);
            store_b(N, B, j, i, value, cache);
        }
    }
}

static void transpose_32(int M, int N, const int *A, int *B, TransposeCache *cache)
{
    int ii;
    int jj;
    int i;

    (void)M;
    (void)N;

    for (ii = 0; ii < 32; ii += 8) {
        for (jj = 0; jj < 32; jj += 8) {
            for (i = ii; i < ii + 8; ++i) {
                int diag_value = 0;
                int diag_index = -1;
                int j;
                for (j = jj; j < jj + 8; ++j) {
                    int value = load_a(32, A, i, j, cache);
                    if (ii == jj && i == j) {
                        diag_value = value;
                        diag_index = i;
                    } else {
                        store_b(32, B, j, i, value, cache);
                    }
                }
                if (diag_index >= 0) {
                    store_b(32, B, diag_index, diag_index, diag_value, cache);
                }
            }
        }
    }
}

static void transpose_64(const int *A, int *B, TransposeCache *cache)
{
    int ii;
    int jj;

    for (ii = 0; ii < 64; ii += 8) {
        for (jj = 0; jj < 64; jj += 8) {
            int i;
            for (i = ii; i < ii + 4; ++i) {
                int a0 = load_a(64, A, i, jj + 0, cache);
                int a1 = load_a(64, A, i, jj + 1, cache);
                int a2 = load_a(64, A, i, jj + 2, cache);
                int a3 = load_a(64, A, i, jj + 3, cache);
                int a4 = load_a(64, A, i, jj + 4, cache);
                int a5 = load_a(64, A, i, jj + 5, cache);
                int a6 = load_a(64, A, i, jj + 6, cache);
                int a7 = load_a(64, A, i, jj + 7, cache);

                store_b(64, B, jj + 0, i, a0, cache);
                store_b(64, B, jj + 1, i, a1, cache);
                store_b(64, B, jj + 2, i, a2, cache);
                store_b(64, B, jj + 3, i, a3, cache);
                store_b(64, B, jj + 0, i + 4, a4, cache);
                store_b(64, B, jj + 1, i + 4, a5, cache);
                store_b(64, B, jj + 2, i + 4, a6, cache);
                store_b(64, B, jj + 3, i + 4, a7, cache);
            }

            for (i = 0; i < 4; ++i) {
                int a0 = load_a(64, A, ii + 4, jj + i, cache);
                int a1 = load_a(64, A, ii + 5, jj + i, cache);
                int a2 = load_a(64, A, ii + 6, jj + i, cache);
                int a3 = load_a(64, A, ii + 7, jj + i, cache);
                int b0 = load_b(64, B, jj + i, ii + 4, cache);
                int b1 = load_b(64, B, jj + i, ii + 5, cache);
                int b2 = load_b(64, B, jj + i, ii + 6, cache);
                int b3 = load_b(64, B, jj + i, ii + 7, cache);

                store_b(64, B, jj + i, ii + 4, a0, cache);
                store_b(64, B, jj + i, ii + 5, a1, cache);
                store_b(64, B, jj + i, ii + 6, a2, cache);
                store_b(64, B, jj + i, ii + 7, a3, cache);

                store_b(64, B, jj + i + 4, ii + 0, b0, cache);
                store_b(64, B, jj + i + 4, ii + 1, b1, cache);
                store_b(64, B, jj + i + 4, ii + 2, b2, cache);
                store_b(64, B, jj + i + 4, ii + 3, b3, cache);
            }

            for (i = ii + 4; i < ii + 8; ++i) {
                int a4 = load_a(64, A, i, jj + 4, cache);
                int a5 = load_a(64, A, i, jj + 5, cache);
                int a6 = load_a(64, A, i, jj + 6, cache);
                int a7 = load_a(64, A, i, jj + 7, cache);

                store_b(64, B, jj + 4, i, a4, cache);
                store_b(64, B, jj + 5, i, a5, cache);
                store_b(64, B, jj + 6, i, a6, cache);
                store_b(64, B, jj + 7, i, a7, cache);
            }
        }
    }
}

static void transpose_generic(int M, int N, const int *A, int *B, TransposeCache *cache)
{
    int block = 16;
    int ii;
    int jj;
    int i;
    int j;

    for (ii = 0; ii < N; ii += block) {
        for (jj = 0; jj < M; jj += block) {
            for (i = ii; i < N && i < ii + block; ++i) {
                for (j = jj; j < M && j < jj + block; ++j) {
                    int value = load_a(M, A, i, j, cache);
                    store_b(N, B, j, i, value, cache);
                }
            }
        }
    }
}

void perflab_transpose_submit(int M, int N, const int *A, int *B, TransposeCache *cache)
{
    if (M == 32 && N == 32) {
        transpose_32(M, N, A, B, cache);
    } else if (M == 64 && N == 64) {
        transpose_64(A, B, cache);
    } else {
        transpose_generic(M, N, A, B, cache);
    }
}

int perflab_is_transpose(int M, int N, const int *A, const int *B)
{
    int i;
    int j;

    for (i = 0; i < N; ++i) {
        for (j = 0; j < M; ++j) {
            if (A[i * M + j] != B[j * N + i]) {
                return 0;
            }
        }
    }
    return 1;
}

TransposeResult perflab_measure_transpose(int M, int N, transpose_kernel_t kernel)
{
    int *A = (int *)malloc((size_t)M * (size_t)N * sizeof(int));
    int *B = (int *)calloc((size_t)M * (size_t)N, sizeof(int));
    int i;
    TransposeCache cache;
    TransposeResult result;

    if (A == NULL || B == NULL) {
        fprintf(stderr, "matrix allocation failed\n");
        exit(1);
    }

    for (i = 0; i < M * N; ++i) {
        A[i] = i * 3 + 1;
    }

    transpose_cache_init(&cache);
    kernel(M, N, A, B, &cache);

    result.correct = perflab_is_transpose(M, N, A, B);
    result.misses = cache.stats.misses;
    result.evictions = cache.stats.evictions;

    free(A);
    free(B);
    return result;
}
