#ifndef MINI_ARCHLAB_H
#define MINI_ARCHLAB_H

#include <stdint.h>

typedef struct ArchNode {
    int64_t value;
    struct ArchNode *next;
} ArchNode;

typedef struct {
    uint64_t pc;
    uint64_t next_pc;
    uint8_t dst_reg;
    int64_t valB;
    int64_t valC;
    int64_t valE;
    int zf;
    int sf;
    int of;
} SeqIaddqTrace;

typedef struct {
    int64_t count;
    uint64_t cycles;
    double cpe;
} NcopyReport;

int64_t arch_sum_list(const ArchNode *head);
int64_t arch_rsum_list(const ArchNode *head);
int64_t arch_copy_block(const int64_t *src, int64_t *dst, int64_t len);
SeqIaddqTrace arch_seq_iaddq(uint64_t pc, uint8_t dst_reg, int64_t valB, int64_t valC);
NcopyReport arch_ncopy_baseline(const int64_t *src, int64_t *dst, int64_t len);
NcopyReport arch_ncopy_optimized(const int64_t *src, int64_t *dst, int64_t len);

#endif
