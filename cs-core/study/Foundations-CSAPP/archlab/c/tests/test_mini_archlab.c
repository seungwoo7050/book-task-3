#include "../include/mini_archlab.h"

#include <limits.h>
#include <stdio.h>

static int failures = 0;

static void expect_true(const char *label, int condition)
{
    if (!condition) {
        fprintf(stderr, "FAIL: %s\n", label);
        failures += 1;
    }
}

static void expect_equal_ll(const char *label, long long actual, long long expected)
{
    if (actual != expected) {
        fprintf(stderr, "FAIL: %s (actual=%lld expected=%lld)\n", label, actual, expected);
        failures += 1;
    }
}

int main(void)
{
    ArchNode n3 = {0xc00, NULL};
    ArchNode n2 = {0x0b0, &n3};
    ArchNode n1 = {0x00a, &n2};
    int64_t src_copy[] = {0x00a, 0x0b0, 0xc00};
    int64_t dst_copy[] = {0, 0, 0};
    int64_t src_ncopy[] = {3, -2, 9, 0, 7, -5, 11, 4};
    int64_t dst_baseline[8] = {0};
    int64_t dst_optimized[8] = {0};
    SeqIaddqTrace normal = arch_seq_iaddq(0x100, 3, 7, -3);
    SeqIaddqTrace zeroed = arch_seq_iaddq(0x210, 9, 5, -5);
    SeqIaddqTrace overflow = arch_seq_iaddq(0x300, 1, INT64_MAX, 1);
    NcopyReport baseline = arch_ncopy_baseline(src_ncopy, dst_baseline, 8);
    NcopyReport optimized = arch_ncopy_optimized(src_ncopy, dst_optimized, 8);
    int index;

    expect_equal_ll("iterative sum matches sample", arch_sum_list(&n1), 0xcba);
    expect_equal_ll("recursive sum matches sample", arch_rsum_list(&n1), 0xcba);
    expect_equal_ll("empty recursive sum", arch_rsum_list(NULL), 0);
    expect_equal_ll("copy_block xor", arch_copy_block(src_copy, dst_copy, 3), 0xcba);
    for (index = 0; index < 3; ++index) {
        expect_equal_ll("copy_block destination", dst_copy[index], src_copy[index]);
    }

    expect_equal_ll("iaddq next pc", (long long)normal.next_pc, 0x10a);
    expect_equal_ll("iaddq result", normal.valE, 4);
    expect_true("iaddq clears flags for normal add", !normal.zf && !normal.sf && !normal.of);
    expect_true("iaddq sets zero flag", zeroed.zf && !zeroed.sf && !zeroed.of);
    expect_true("iaddq sets signed overflow", overflow.of && overflow.sf);

    expect_equal_ll("baseline positive count", baseline.count, 5);
    expect_equal_ll("optimized positive count", optimized.count, 5);
    for (index = 0; index < 8; ++index) {
        expect_equal_ll("baseline ncopy destination", dst_baseline[index], src_ncopy[index]);
        expect_equal_ll("optimized ncopy destination", dst_optimized[index], src_ncopy[index]);
    }
    expect_true("optimized cpe beats baseline", optimized.cpe < baseline.cpe);

    if (failures != 0) {
        return 1;
    }

    puts("C mini-archlab tests passed");
    return 0;
}
