#include "perflab.h"

#include <stdio.h>

static void print_trace_result(int s, int E, int b)
{
    PerfStats stats;

    perflab_run_trace_file("../problem/data/traces/study.trace", s, E, b, 0, &stats);
    printf("csim study.trace (s=%d E=%d b=%d): hits=%d misses=%d evictions=%d\n",
           s,
           E,
           b,
           stats.hits,
           stats.misses,
           stats.evictions);
}

static void print_transpose_result(int M, int N)
{
    TransposeResult naive = perflab_measure_transpose(M, N, perflab_transpose_naive);
    TransposeResult tuned = perflab_measure_transpose(M, N, perflab_transpose_submit);

    printf("transpose %dx%d naive misses=%d tuned misses=%d correct=%d\n",
           M,
           N,
           naive.misses,
           tuned.misses,
           tuned.correct);
}

int main(void)
{
    print_trace_result(1, 1, 1);
    print_trace_result(2, 1, 2);
    print_trace_result(5, 1, 5);

    print_transpose_result(32, 32);
    print_transpose_result(64, 64);
    print_transpose_result(61, 67);
    return 0;
}
