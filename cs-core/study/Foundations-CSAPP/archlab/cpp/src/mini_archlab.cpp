#include "mini_archlab.hpp"

#include <algorithm>

namespace archlab {
namespace {

bool add_overflow(std::int64_t a, std::int64_t b, std::int64_t result)
{
    return ((a ^ result) & (b ^ result)) < 0;
}

std::uint64_t baseline_cycles(std::int64_t len)
{
    if (len <= 0) {
        return 6;
    }
    return 8 + static_cast<std::uint64_t>(len) * 9;
}

std::uint64_t optimized_cycles(std::int64_t len)
{
    if (len <= 0) {
        return 7;
    }
    const auto chunks4 = static_cast<std::uint64_t>(len / 4);
    const auto remainder = static_cast<std::uint64_t>(len % 4);
    return 10 + chunks4 * 22 + remainder * 8;
}

}  // 내부 helper 이름공간 끝

std::int64_t sum_list(const Node *head)
{
    std::int64_t total = 0;

    while (head != nullptr) {
        total += head->value;
        head = head->next;
    }
    return total;
}

std::int64_t rsum_list(const Node *head)
{
    if (head == nullptr) {
        return 0;
    }
    return head->value + rsum_list(head->next);
}

std::int64_t copy_block(const std::vector<std::int64_t> &src, std::vector<std::int64_t> &dst, std::int64_t len)
{
    std::int64_t checksum = 0;

    for (std::int64_t index = 0; index < len; ++index) {
        dst[static_cast<std::size_t>(index)] = src[static_cast<std::size_t>(index)];
        checksum ^= src[static_cast<std::size_t>(index)];
    }
    return checksum;
}

SeqIaddqTrace seq_iaddq(std::uint64_t pc, std::uint8_t dst_reg, std::int64_t valB, std::int64_t valC)
{
    const auto raw = static_cast<std::uint64_t>(valB) + static_cast<std::uint64_t>(valC);
    const auto valE = static_cast<std::int64_t>(raw);

    return SeqIaddqTrace{
        pc,
        pc + 10,
        dst_reg,
        valB,
        valC,
        valE,
        valE == 0,
        valE < 0,
        add_overflow(valB, valC, valE),
    };
}

NcopyReport ncopy_baseline(const std::vector<std::int64_t> &src, std::vector<std::int64_t> &dst, std::int64_t len)
{
    std::int64_t count = 0;

    for (std::int64_t index = 0; index < len; ++index) {
        dst[static_cast<std::size_t>(index)] = src[static_cast<std::size_t>(index)];
        if (src[static_cast<std::size_t>(index)] > 0) {
            count += 1;
        }
    }

    const auto cycles = baseline_cycles(len);
    return NcopyReport{count, cycles, len > 0 ? static_cast<double>(cycles) / static_cast<double>(len) : 0.0};
}

NcopyReport ncopy_optimized(const std::vector<std::int64_t> &src, std::vector<std::int64_t> &dst, std::int64_t len)
{
    std::int64_t count = 0;
    std::int64_t index = 0;

    while (index + 3 < len) {
        const auto v0 = src[static_cast<std::size_t>(index)];
        const auto v1 = src[static_cast<std::size_t>(index + 1)];
        const auto v2 = src[static_cast<std::size_t>(index + 2)];
        const auto v3 = src[static_cast<std::size_t>(index + 3)];

        dst[static_cast<std::size_t>(index)] = v0;
        dst[static_cast<std::size_t>(index + 1)] = v1;
        dst[static_cast<std::size_t>(index + 2)] = v2;
        dst[static_cast<std::size_t>(index + 3)] = v3;

        count += v0 > 0;
        count += v1 > 0;
        count += v2 > 0;
        count += v3 > 0;
        index += 4;
    }

    while (index < len) {
        dst[static_cast<std::size_t>(index)] = src[static_cast<std::size_t>(index)];
        if (src[static_cast<std::size_t>(index)] > 0) {
            count += 1;
        }
        index += 1;
    }

    const auto cycles = optimized_cycles(len);
    return NcopyReport{count, cycles, len > 0 ? static_cast<double>(cycles) / static_cast<double>(len) : 0.0};
}

}  // archlab 이름공간 끝
