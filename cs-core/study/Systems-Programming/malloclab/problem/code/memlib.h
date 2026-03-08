/*
 * memlib.h - heap emulator interface.
 */

#ifndef MEMLIB_H
#define MEMLIB_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

void mem_init(void);
void mem_deinit(void);
void mem_reset_brk(void);
void *mem_sbrk(int incr);
void *mem_heap_lo(void);
void *mem_heap_hi(void);
size_t mem_heapsize(void);

#ifdef __cplusplus
}
#endif

#endif
