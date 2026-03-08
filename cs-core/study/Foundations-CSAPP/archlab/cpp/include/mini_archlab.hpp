#ifndef MINI_ARCHLAB_HPP
#define MINI_ARCHLAB_HPP

#include <cstdint>
#include <vector>

namespace archlab {

struct Node {
    std::int64_t value;
    const Node *next;
};

struct SeqIaddqTrace {
    std::uint64_t pc;
    std::uint64_t next_pc;
    std::uint8_t dst_reg;
    std::int64_t valB;
    std::int64_t valC;
    std::int64_t valE;
    bool zf;
    bool sf;
    bool of;
};

struct NcopyReport {
    std::int64_t count;
    std::uint64_t cycles;
    double cpe;
};

std::int64_t sum_list(const Node *head);
std::int64_t rsum_list(const Node *head);
std::int64_t copy_block(const std::vector<std::int64_t> &src, std::vector<std::int64_t> &dst, std::int64_t len);
SeqIaddqTrace seq_iaddq(std::uint64_t pc, std::uint8_t dst_reg, std::int64_t valB, std::int64_t valC);
NcopyReport ncopy_baseline(const std::vector<std::int64_t> &src, std::vector<std::int64_t> &dst, std::int64_t len);
NcopyReport ncopy_optimized(const std::vector<std::int64_t> &src, std::vector<std::int64_t> &dst, std::int64_t len);

}  // namespace archlab

#endif
