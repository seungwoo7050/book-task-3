#include "mini_archlab.h"

#include <stdio.h>

int main(void)
{
    ArchNode n3 = {0xc00, NULL};
    ArchNode n2 = {0x0b0, &n3};
    ArchNode n1 = {0x00a, &n2};
    int64_t src[] = {3, -2, 9, 0, 7, -5, 11, 4};
    int64_t dst_baseline[8] = {0};
    int64_t dst_optimized[8] = {0};
    int64_t copy_dst[3] = {0};
    SeqIaddqTrace trace = arch_seq_iaddq(0x100, 0x3, 7, -3);
    NcopyReport baseline = arch_ncopy_baseline(src, dst_baseline, 8);
    NcopyReport optimized = arch_ncopy_optimized(src, dst_optimized, 8);

    printf("Part A iterative sum: %lld\n", (long long)arch_sum_list(&n1));
    printf("Part A recursive sum: %lld\n", (long long)arch_rsum_list(&n1));
    printf("Part A copy xor: %lld\n", (long long)arch_copy_block((const int64_t[]){0x00a, 0x0b0, 0xc00}, copy_dst, 3));
    printf("Part B iaddq sample: pc=0x%llx next=0x%llx valE=%lld ZF=%d SF=%d OF=%d\n",
           (unsigned long long)trace.pc,
           (unsigned long long)trace.next_pc,
           (long long)trace.valE,
           trace.zf,
           trace.sf,
           trace.of);
    printf("Part C baseline: count=%lld cycles=%llu cpe=%.2f\n",
           (long long)baseline.count,
           (unsigned long long)baseline.cycles,
           baseline.cpe);
    printf("Part C optimized: count=%lld cycles=%llu cpe=%.2f\n",
           (long long)optimized.count,
           (unsigned long long)optimized.cycles,
           optimized.cpe);
    return 0;
}
