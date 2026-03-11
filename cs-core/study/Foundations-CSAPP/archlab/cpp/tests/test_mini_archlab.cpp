#include "../include/mini_archlab.hpp"

#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

namespace {

int failures = 0;

void expect_true(const char *label, bool condition)
{
    if (!condition) {
        std::cerr << "FAIL: " << label << '\n';
        ++failures;
    }
}

void expect_equal_ll(const char *label, long long actual, long long expected)
{
    if (actual != expected) {
        std::cerr << "FAIL: " << label << " (actual=" << actual << " expected=" << expected << ")\n";
        ++failures;
    }
}

}  // 테스트 helper 이름공간 끝

int main()
{
    const archlab::Node n3{0xc00, nullptr};
    const archlab::Node n2{0x0b0, &n3};
    const archlab::Node n1{0x00a, &n2};
    const std::vector<std::int64_t> src_copy = {0x00a, 0x0b0, 0xc00};
    std::vector<std::int64_t> dst_copy(3, 0);
    const std::vector<std::int64_t> src_ncopy = {3, -2, 9, 0, 7, -5, 11, 4};
    std::vector<std::int64_t> dst_baseline(8, 0);
    std::vector<std::int64_t> dst_optimized(8, 0);
    const auto normal = archlab::seq_iaddq(0x100, 3, 7, -3);
    const auto zeroed = archlab::seq_iaddq(0x210, 9, 5, -5);
    const auto overflow = archlab::seq_iaddq(0x300, 1, std::numeric_limits<std::int64_t>::max(), 1);
    const auto baseline = archlab::ncopy_baseline(src_ncopy, dst_baseline, 8);
    const auto optimized = archlab::ncopy_optimized(src_ncopy, dst_optimized, 8);

    expect_equal_ll("iterative sum matches sample", archlab::sum_list(&n1), 0xcba);
    expect_equal_ll("recursive sum matches sample", archlab::rsum_list(&n1), 0xcba);
    expect_equal_ll("empty recursive sum", archlab::rsum_list(nullptr), 0);
    expect_equal_ll("copy_block xor", archlab::copy_block(src_copy, dst_copy, 3), 0xcba);
    for (std::size_t index = 0; index < src_copy.size(); ++index) {
        expect_equal_ll("copy_block destination", dst_copy[index], src_copy[index]);
    }

    expect_equal_ll("iaddq next pc", normal.next_pc, 0x10a);
    expect_equal_ll("iaddq result", normal.valE, 4);
    expect_true("iaddq clears flags for normal add", !normal.zf && !normal.sf && !normal.of);
    expect_true("iaddq sets zero flag", zeroed.zf && !zeroed.sf && !zeroed.of);
    expect_true("iaddq sets signed overflow", overflow.of && overflow.sf);

    expect_equal_ll("baseline positive count", baseline.count, 5);
    expect_equal_ll("optimized positive count", optimized.count, 5);
    for (std::size_t index = 0; index < src_ncopy.size(); ++index) {
        expect_equal_ll("baseline ncopy destination", dst_baseline[index], src_ncopy[index]);
        expect_equal_ll("optimized ncopy destination", dst_optimized[index], src_ncopy[index]);
    }
    expect_true("optimized cpe beats baseline", optimized.cpe < baseline.cpe);

    if (failures != 0) {
        return 1;
    }

    std::cout << "C++ mini-archlab tests passed\n";
    return 0;
}
