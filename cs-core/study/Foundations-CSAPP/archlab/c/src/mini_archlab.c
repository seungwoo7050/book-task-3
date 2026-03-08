#include "mini_archlab.h"

#include <stddef.h>

int64_t arch_sum_list(const ArchNode *head)
{
    int64_t total = 0;

    while (head != NULL) {
        total += head->value;
        head = head->next;
    }
    return total;
}

int64_t arch_rsum_list(const ArchNode *head)
{
    if (head == NULL) {
        return 0;
    }
    return head->value + arch_rsum_list(head->next);
}

int64_t arch_copy_block(const int64_t *src, int64_t *dst, int64_t len)
{
    int64_t checksum = 0;
    int64_t index;

    for (index = 0; index < len; ++index) {
        dst[index] = src[index];
        checksum ^= src[index];
    }
    return checksum;
}

static int add_overflow(int64_t a, int64_t b, int64_t result)
{
    return ((a ^ result) & (b ^ result)) < 0;
}

SeqIaddqTrace arch_seq_iaddq(uint64_t pc, uint8_t dst_reg, int64_t valB, int64_t valC)
{
    SeqIaddqTrace trace;
    uint64_t raw = (uint64_t)valB + (uint64_t)valC;

    trace.pc = pc;
    trace.next_pc = pc + 10;
    trace.dst_reg = dst_reg;
    trace.valB = valB;
    trace.valC = valC;
    trace.valE = (int64_t)raw;
    trace.zf = trace.valE == 0;
    trace.sf = trace.valE < 0;
    trace.of = add_overflow(valB, valC, trace.valE);
    return trace;
}

static uint64_t baseline_cycles(int64_t len)
{
    if (len <= 0) {
        return 6;
    }
    return 8 + (uint64_t)len * 9;
}

static uint64_t optimized_cycles(int64_t len)
{
    uint64_t chunks4;
    uint64_t remainder;

    if (len <= 0) {
        return 7;
    }
    chunks4 = (uint64_t)len / 4;
    remainder = (uint64_t)len % 4;
    return 10 + chunks4 * 22 + remainder * 8;
}

NcopyReport arch_ncopy_baseline(const int64_t *src, int64_t *dst, int64_t len)
{
    NcopyReport report;
    int64_t count = 0;
    int64_t index;

    for (index = 0; index < len; ++index) {
        dst[index] = src[index];
        if (src[index] > 0) {
            count += 1;
        }
    }

    report.count = count;
    report.cycles = baseline_cycles(len);
    report.cpe = len > 0 ? (double)report.cycles / (double)len : 0.0;
    return report;
}

NcopyReport arch_ncopy_optimized(const int64_t *src, int64_t *dst, int64_t len)
{
    NcopyReport report;
    int64_t count = 0;
    int64_t index = 0;

    while (index + 3 < len) {
        int64_t v0 = src[index];
        int64_t v1 = src[index + 1];
        int64_t v2 = src[index + 2];
        int64_t v3 = src[index + 3];

        dst[index] = v0;
        dst[index + 1] = v1;
        dst[index + 2] = v2;
        dst[index + 3] = v3;

        count += v0 > 0;
        count += v1 > 0;
        count += v2 > 0;
        count += v3 > 0;

        index += 4;
    }

    while (index < len) {
        dst[index] = src[index];
        if (src[index] > 0) {
            count += 1;
        }
        index += 1;
    }

    report.count = count;
    report.cycles = optimized_cycles(len);
    report.cpe = len > 0 ? (double)report.cycles / (double)len : 0.0;
    return report;
}
