/*
 * mm.h - allocator API shared by the starter, C track, and C++ track.
 */

#ifndef MM_H
#define MM_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int mm_init(void);
void *mm_malloc(size_t size);
void mm_free(void *ptr);
void *mm_realloc(void *ptr, size_t size);

#ifdef __cplusplus
}
#endif

#endif
