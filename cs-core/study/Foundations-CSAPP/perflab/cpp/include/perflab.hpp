#ifndef PERFLAB_HPP
#define PERFLAB_HPP

#include <cstdint>
#include <string>
#include <vector>

namespace perflab {

struct PerfStats {
    int hits;
    int misses;
    int evictions;
};

struct TransposeResult {
    bool correct;
    int misses;
    int evictions;
};

struct DirectMappedLine {
    bool valid;
    std::uint64_t tag;
    std::uint64_t lru;
};

struct TransposeCache {
    PerfStats stats;
    std::uint64_t clock;
    DirectMappedLine lines[32];
};

using TransposeKernel = void (*)(int M, int N, const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache);

PerfStats run_trace_file(const std::string &tracefile, int s, int E, int b, bool verbose);
void transpose_naive(int M, int N, const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache);
void transpose_submit(int M, int N, const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache);
bool is_transpose(int M, int N, const std::vector<int> &A, const std::vector<int> &B);
TransposeResult measure_transpose(int M, int N, TransposeKernel kernel);

}  // perflab 이름공간 끝

#endif
