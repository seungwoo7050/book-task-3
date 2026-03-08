#include "perflab.hpp"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <sstream>

namespace perflab {
namespace {

struct CacheLine {
    bool valid;
    std::uint64_t tag;
    std::uint64_t lru;
};

struct CacheSet {
    std::vector<CacheLine> lines;
};

struct CacheSim {
    int s;
    int E;
    int b;
    int S;
    std::uint64_t clock;
    PerfStats stats;
    std::vector<CacheSet> sets;
};

void cache_sim_init(CacheSim &cache, int s, int E, int b)
{
    cache.s = s;
    cache.E = E;
    cache.b = b;
    cache.S = 1 << s;
    cache.clock = 1;
    cache.stats = {0, 0, 0};
    cache.sets.assign(static_cast<std::size_t>(cache.S), CacheSet{});
    for (auto &set : cache.sets) {
        set.lines.assign(static_cast<std::size_t>(E), CacheLine{false, 0, 0});
    }
}

void cache_access(CacheSim &cache, std::uint64_t address)
{
    const auto set_mask = (1ULL << cache.s) - 1ULL;
    const auto set_index = (address >> cache.b) & set_mask;
    const auto tag = address >> (cache.s + cache.b);
    auto &set = cache.sets[static_cast<std::size_t>(set_index)];
    int empty_index = -1;
    int victim_index = 0;
    std::uint64_t oldest = UINT64_MAX;

    for (int index = 0; index < cache.E; ++index) {
        auto &line = set.lines[static_cast<std::size_t>(index)];
        if (line.valid && line.tag == tag) {
            cache.stats.hits += 1;
            line.lru = cache.clock++;
            return;
        }
        if (!line.valid && empty_index < 0) {
            empty_index = index;
        }
        if (line.valid && line.lru < oldest) {
            oldest = line.lru;
            victim_index = index;
        }
    }

    cache.stats.misses += 1;
    if (empty_index >= 0) {
        auto &line = set.lines[static_cast<std::size_t>(empty_index)];
        line.valid = true;
        line.tag = tag;
        line.lru = cache.clock++;
        return;
    }

    auto &line = set.lines[static_cast<std::size_t>(victim_index)];
    cache.stats.evictions += 1;
    line.tag = tag;
    line.lru = cache.clock++;
}

void transpose_cache_init(TransposeCache &cache)
{
    cache.stats = {0, 0, 0};
    cache.clock = 1;
    for (auto &line : cache.lines) {
        line.valid = false;
        line.tag = 0;
        line.lru = 0;
    }
}

void transpose_access(TransposeCache &cache, std::uint64_t address)
{
    const auto set_index = (address >> 5) & 31ULL;
    const auto tag = address >> 10;
    auto &line = cache.lines[set_index];

    if (line.valid && line.tag == tag) {
        cache.stats.hits += 1;
    } else {
        cache.stats.misses += 1;
        if (line.valid) {
            cache.stats.evictions += 1;
        }
        line.valid = true;
        line.tag = tag;
    }
    line.lru = cache.clock++;
}

std::uint64_t a_addr(int M, int i, int j)
{
    return static_cast<std::uint64_t>((i * M + j) * 4ULL);
}

std::uint64_t b_addr(int N, int i, int j)
{
    return (1ULL << 20) + static_cast<std::uint64_t>((i * N + j) * 4ULL);
}

int load_a(int M, const std::vector<int> &A, int i, int j, TransposeCache &cache)
{
    transpose_access(cache, a_addr(M, i, j));
    return A[static_cast<std::size_t>(i * M + j)];
}

int load_b(int N, const std::vector<int> &B, int i, int j, TransposeCache &cache)
{
    transpose_access(cache, b_addr(N, i, j));
    return B[static_cast<std::size_t>(i * N + j)];
}

void store_b(int N, std::vector<int> &B, int i, int j, int value, TransposeCache &cache)
{
    transpose_access(cache, b_addr(N, i, j));
    B[static_cast<std::size_t>(i * N + j)] = value;
}

void transpose_32(const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache)
{
    for (int ii = 0; ii < 32; ii += 8) {
        for (int jj = 0; jj < 32; jj += 8) {
            for (int i = ii; i < ii + 8; ++i) {
                int diag_value = 0;
                int diag_index = -1;
                for (int j = jj; j < jj + 8; ++j) {
                    const int value = load_a(32, A, i, j, cache);
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

void transpose_64(const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache)
{
    for (int ii = 0; ii < 64; ii += 8) {
        for (int jj = 0; jj < 64; jj += 8) {
            for (int i = ii; i < ii + 4; ++i) {
                const int a0 = load_a(64, A, i, jj + 0, cache);
                const int a1 = load_a(64, A, i, jj + 1, cache);
                const int a2 = load_a(64, A, i, jj + 2, cache);
                const int a3 = load_a(64, A, i, jj + 3, cache);
                const int a4 = load_a(64, A, i, jj + 4, cache);
                const int a5 = load_a(64, A, i, jj + 5, cache);
                const int a6 = load_a(64, A, i, jj + 6, cache);
                const int a7 = load_a(64, A, i, jj + 7, cache);

                store_b(64, B, jj + 0, i, a0, cache);
                store_b(64, B, jj + 1, i, a1, cache);
                store_b(64, B, jj + 2, i, a2, cache);
                store_b(64, B, jj + 3, i, a3, cache);
                store_b(64, B, jj + 0, i + 4, a4, cache);
                store_b(64, B, jj + 1, i + 4, a5, cache);
                store_b(64, B, jj + 2, i + 4, a6, cache);
                store_b(64, B, jj + 3, i + 4, a7, cache);
            }

            for (int offset = 0; offset < 4; ++offset) {
                const int a0 = load_a(64, A, ii + 4, jj + offset, cache);
                const int a1 = load_a(64, A, ii + 5, jj + offset, cache);
                const int a2 = load_a(64, A, ii + 6, jj + offset, cache);
                const int a3 = load_a(64, A, ii + 7, jj + offset, cache);
                const int b0 = load_b(64, B, jj + offset, ii + 4, cache);
                const int b1 = load_b(64, B, jj + offset, ii + 5, cache);
                const int b2 = load_b(64, B, jj + offset, ii + 6, cache);
                const int b3 = load_b(64, B, jj + offset, ii + 7, cache);

                store_b(64, B, jj + offset, ii + 4, a0, cache);
                store_b(64, B, jj + offset, ii + 5, a1, cache);
                store_b(64, B, jj + offset, ii + 6, a2, cache);
                store_b(64, B, jj + offset, ii + 7, a3, cache);

                store_b(64, B, jj + offset + 4, ii + 0, b0, cache);
                store_b(64, B, jj + offset + 4, ii + 1, b1, cache);
                store_b(64, B, jj + offset + 4, ii + 2, b2, cache);
                store_b(64, B, jj + offset + 4, ii + 3, b3, cache);
            }

            for (int i = ii + 4; i < ii + 8; ++i) {
                const int a4 = load_a(64, A, i, jj + 4, cache);
                const int a5 = load_a(64, A, i, jj + 5, cache);
                const int a6 = load_a(64, A, i, jj + 6, cache);
                const int a7 = load_a(64, A, i, jj + 7, cache);

                store_b(64, B, jj + 4, i, a4, cache);
                store_b(64, B, jj + 5, i, a5, cache);
                store_b(64, B, jj + 6, i, a6, cache);
                store_b(64, B, jj + 7, i, a7, cache);
            }
        }
    }
}

void transpose_generic(int M, int N, const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache)
{
    constexpr int block = 16;

    for (int ii = 0; ii < N; ii += block) {
        for (int jj = 0; jj < M; jj += block) {
            for (int i = ii; i < N && i < ii + block; ++i) {
                for (int j = jj; j < M && j < jj + block; ++j) {
                    const int value = load_a(M, A, i, j, cache);
                    store_b(N, B, j, i, value, cache);
                }
            }
        }
    }
}

}  // namespace

PerfStats run_trace_file(const std::string &tracefile, int s, int E, int b, bool verbose)
{
    std::ifstream file(tracefile);
    CacheSim cache;
    char op = '\0';
    unsigned long long address = 0;
    int size = 0;

    if (!file) {
        std::fprintf(stderr, "could not open trace file: %s\n", tracefile.c_str());
        std::exit(1);
    }

    cache_sim_init(cache, s, E, b);

    while (file >> op >> std::hex >> address >> std::dec) {
        if (file.get() != ',') {
            break;
        }
        file >> size;
        if (op == 'I') {
            continue;
        }
        cache_access(cache, static_cast<std::uint64_t>(address));
        if (op == 'M') {
            cache_access(cache, static_cast<std::uint64_t>(address));
        }
        if (verbose) {
            (void)size;
        }
    }

    return cache.stats;
}

void transpose_naive(int M, int N, const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache)
{
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            const int value = load_a(M, A, i, j, cache);
            store_b(N, B, j, i, value, cache);
        }
    }
}

void transpose_submit(int M, int N, const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache)
{
    if (M == 32 && N == 32) {
        transpose_32(A, B, cache);
    } else if (M == 64 && N == 64) {
        transpose_64(A, B, cache);
    } else {
        transpose_generic(M, N, A, B, cache);
    }
}

bool is_transpose(int M, int N, const std::vector<int> &A, const std::vector<int> &B)
{
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            if (A[static_cast<std::size_t>(i * M + j)] != B[static_cast<std::size_t>(j * N + i)]) {
                return false;
            }
        }
    }
    return true;
}

TransposeResult measure_transpose(int M, int N, TransposeKernel kernel)
{
    std::vector<int> A(static_cast<std::size_t>(M * N));
    std::vector<int> B(static_cast<std::size_t>(M * N), 0);
    TransposeCache cache{};

    for (int i = 0; i < M * N; ++i) {
        A[static_cast<std::size_t>(i)] = i * 3 + 1;
    }

    transpose_cache_init(cache);
    kernel(M, N, A, B, cache);

    return TransposeResult{
        is_transpose(M, N, A, B),
        cache.stats.misses,
        cache.stats.evictions,
    };
}

}  // namespace perflab
