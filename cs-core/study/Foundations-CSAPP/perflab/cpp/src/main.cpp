#include "perflab.hpp"

#include <iostream>

static void print_trace_result(int s, int E, int b)
{
    const auto stats = perflab::run_trace_file("../problem/data/traces/study.trace", s, E, b, false);
    std::cout << "csim study.trace (s=" << s << " E=" << E << " b=" << b << "): hits=" << stats.hits
              << " misses=" << stats.misses << " evictions=" << stats.evictions << '\n';
}

static void print_transpose_result(int M, int N)
{
    const auto naive = perflab::measure_transpose(M, N, perflab::transpose_naive);
    const auto tuned = perflab::measure_transpose(M, N, perflab::transpose_submit);
    std::cout << "transpose " << M << "x" << N << " naive misses=" << naive.misses
              << " tuned misses=" << tuned.misses << " correct=" << tuned.correct << '\n';
}

int main()
{
    print_trace_result(1, 1, 1);
    print_trace_result(2, 1, 2);
    print_trace_result(5, 1, 5);

    print_transpose_result(32, 32);
    print_transpose_result(64, 64);
    print_transpose_result(61, 67);
    return 0;
}
