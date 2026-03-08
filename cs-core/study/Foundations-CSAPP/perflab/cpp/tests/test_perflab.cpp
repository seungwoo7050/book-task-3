#include "../include/perflab.hpp"

#include <iostream>

namespace {

int failures = 0;

void expect_equal_int(const char *label, int actual, int expected)
{
    if (actual != expected) {
        std::cerr << "FAIL: " << label << " (actual=" << actual << " expected=" << expected << ")\n";
        ++failures;
    }
}

void expect_true(const char *label, bool condition)
{
    if (!condition) {
        std::cerr << "FAIL: " << label << '\n';
        ++failures;
    }
}

}  // namespace

int main()
{
    const auto stats1 = perflab::run_trace_file("../problem/data/traces/study.trace", 1, 1, 1, false);
    const auto stats2 = perflab::run_trace_file("../problem/data/traces/study.trace", 2, 1, 2, false);
    const auto stats3 = perflab::run_trace_file("../problem/data/traces/study.trace", 5, 1, 5, false);

    expect_equal_int("study trace config 1 hits", stats1.hits, 5);
    expect_equal_int("study trace config 1 misses", stats1.misses, 10);
    expect_equal_int("study trace config 1 evictions", stats1.evictions, 8);

    expect_equal_int("study trace config 2 hits", stats2.hits, 6);
    expect_equal_int("study trace config 2 misses", stats2.misses, 9);
    expect_equal_int("study trace config 2 evictions", stats2.evictions, 7);

    expect_equal_int("study trace config 3 hits", stats3.hits, 10);
    expect_equal_int("study trace config 3 misses", stats3.misses, 5);
    expect_equal_int("study trace config 3 evictions", stats3.evictions, 0);

    const auto naive32 = perflab::measure_transpose(32, 32, perflab::transpose_naive);
    const auto tuned32 = perflab::measure_transpose(32, 32, perflab::transpose_submit);
    const auto naive64 = perflab::measure_transpose(64, 64, perflab::transpose_naive);
    const auto tuned64 = perflab::measure_transpose(64, 64, perflab::transpose_submit);
    const auto naive61 = perflab::measure_transpose(61, 67, perflab::transpose_naive);
    const auto tuned61 = perflab::measure_transpose(61, 67, perflab::transpose_submit);

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

    std::cout << "C++ perflab tests passed\n";
    return 0;
}
