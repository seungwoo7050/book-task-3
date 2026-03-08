#include "../include/perflab.h"

#include <stdio.h>

static int failures = 0;

static void expect_equal_int(const char *label, int actual, int expected)
{
    if (actual != expected) {
        fprintf(stderr, "FAIL: %s (actual=%d expected=%d)\n", label, actual, expected);
        failures += 1;
    }
}

static void expect_true(const char *label, int condition)
{
    if (!condition) {
        fprintf(stderr, "FAIL: %s\n", label);
        failures += 1;
    }
}

int main(void)
{
    PerfStats stats;
    TransposeResult naive32;
    TransposeResult tuned32;
    TransposeResult naive64;
    TransposeResult tuned64;
    TransposeResult naive61;
    TransposeResult tuned61;

    perflab_run_trace_file("../problem/data/traces/study.trace", 1, 1, 1, 0, &stats);
    expect_equal_int("study trace config 1 hits", stats.hits, 5);
    expect_equal_int("study trace config 1 misses", stats.misses, 10);
    expect_equal_int("study trace config 1 evictions", stats.evictions, 8);

    perflab_run_trace_file("../problem/data/traces/study.trace", 2, 1, 2, 0, &stats);
    expect_equal_int("study trace config 2 hits", stats.hits, 6);
    expect_equal_int("study trace config 2 misses", stats.misses, 9);
    expect_equal_int("study trace config 2 evictions", stats.evictions, 7);

    perflab_run_trace_file("../problem/data/traces/study.trace", 5, 1, 5, 0, &stats);
    expect_equal_int("study trace config 3 hits", stats.hits, 10);
    expect_equal_int("study trace config 3 misses", stats.misses, 5);
    expect_equal_int("study trace config 3 evictions", stats.evictions, 0);

    naive32 = perflab_measure_transpose(32, 32, perflab_transpose_naive);
    tuned32 = perflab_measure_transpose(32, 32, perflab_transpose_submit);
    naive64 = perflab_measure_transpose(64, 64, perflab_transpose_naive);
    tuned64 = perflab_measure_transpose(64, 64, perflab_transpose_submit);
    naive61 = perflab_measure_transpose(61, 67, perflab_transpose_naive);
    tuned61 = perflab_measure_transpose(61, 67, perflab_transpose_submit);

    expect_true("32x32 tuned transpose correct", tuned32.correct);
    expect_true("64x64 tuned transpose correct", tuned64.correct);
    expect_true("61x67 tuned transpose correct", tuned61.correct);

    expect_true("32x32 tuned beats naive", tuned32.misses < naive32.misses);
    expect_true("64x64 tuned beats naive", tuned64.misses < naive64.misses);
    expect_true("61x67 tuned beats naive", tuned61.misses < naive61.misses);

    expect_true("32x32 threshold", tuned32.misses < 300);
    expect_true("64x64 threshold", tuned64.misses < 1300);
    expect_true("61x67 threshold", tuned61.misses < 2000);

    if (failures != 0) {
        return 1;
    }

    puts("C perflab tests passed");
    return 0;
}
