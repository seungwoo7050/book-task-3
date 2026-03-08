#include "mini_archlab.hpp"

#include <iostream>
#include <vector>

int main()
{
    const archlab::Node n3{0xc00, nullptr};
    const archlab::Node n2{0x0b0, &n3};
    const archlab::Node n1{0x00a, &n2};
    const std::vector<std::int64_t> src = {3, -2, 9, 0, 7, -5, 11, 4};
    std::vector<std::int64_t> dst_baseline(8, 0);
    std::vector<std::int64_t> dst_optimized(8, 0);
    std::vector<std::int64_t> copy_dst(3, 0);
    const auto trace = archlab::seq_iaddq(0x100, 0x3, 7, -3);
    const auto baseline = archlab::ncopy_baseline(src, dst_baseline, 8);
    const auto optimized = archlab::ncopy_optimized(src, dst_optimized, 8);

    std::cout << "Part A iterative sum: " << archlab::sum_list(&n1) << '\n';
    std::cout << "Part A recursive sum: " << archlab::rsum_list(&n1) << '\n';
    std::cout << "Part A copy xor: " << archlab::copy_block({0x00a, 0x0b0, 0xc00}, copy_dst, 3) << '\n';
    std::cout << "Part B iaddq sample: pc=0x" << std::hex << trace.pc
              << " next=0x" << trace.next_pc << std::dec
              << " valE=" << trace.valE
              << " ZF=" << trace.zf
              << " SF=" << trace.sf
              << " OF=" << trace.of << '\n';
    std::cout << "Part C baseline: count=" << baseline.count
              << " cycles=" << baseline.cycles
              << " cpe=" << baseline.cpe << '\n';
    std::cout << "Part C optimized: count=" << optimized.count
              << " cycles=" << optimized.cycles
              << " cpe=" << optimized.cpe << '\n';
    return 0;
}
