#ifndef MM_H
#define MM_H

#include <cstddef>

extern "C" {
int mm_init(void);
void *mm_malloc(std::size_t size);
void mm_free(void *ptr);
void *mm_realloc(void *ptr, std::size_t size);
}

#endif
